import asyncio
import time

import polars as pl
from playwright.async_api import async_playwright
from tqdm import tqdm


async def scroll_and_extract_product_links(page):
    product_links = set()
    previous_height = 0

    while True:
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        await page.wait_for_timeout(2000)
        current_height = await page.evaluate("document.body.scrollHeight")
        if current_height == previous_height:
            break
        previous_height = current_height

    elements = await page.query_selector_all('a[href*="/p/P"]')
    for elem in elements:
        href = await elem.get_attribute("href")
        if href and "https://www.marksandspencer.com/en-at" in href:
            product_links.add(href.split("#")[0])

    return sorted(product_links)


async def extract_product_details(context, url):
    try:
        page = await context.new_page()
        await page.goto(url)
        await page.wait_for_selector("h1", timeout=5000)

        # Title
        title = await page.locator("h1.product-name").text_content()

        # Colours
        initial_color = await page.locator("span.colo-label + b").text_content()
        color_links = await page.locator(".swatch-link").all()

        options = []
        for swatch in color_links:
            swatch_class = await swatch.locator("div.selected-color").get_attribute(
                "class"
            )
            if "color-selected" in (swatch_class or ""):
                current_color = initial_color
            else:
                await swatch.click()
                timeout = 10  # seconds
                start = time.time()
                while True:
                    current_color = await page.locator(
                        "span.colo-label + b"
                    ).text_content()
                    if current_color and current_color.strip() != initial_color:
                        break
                    if time.time() - start > timeout:
                        print("Timed out waiting for color to update")
                        break
                    await asyncio.sleep(0.2)
                initial_color = current_color

            # Price
            price = await page.locator("span.value").first.text_content()

            # Sizes
            size_elements = await page.locator(
                'select.select-size option:not([value="undefined"])'
            ).element_handles()
            sizes = []
            for el in size_elements:
                label = await el.text_content()
                if "Select Size" in label:
                    continue
                in_stock = await el.get_attribute("data-isoos") == "false"
                sizes.append({"label": label.strip(), "in_stock": in_stock})

            options.append(
                pl.DataFrame(
                    {
                        "url": url,
                        "title": title.strip() if title else "N/A",
                        "price": price.strip() if price else "N/A",
                        "colour": current_color,
                        "sizes": [
                            size["label"]
                            .replace("Out of Stock", "")
                            .replace("Low in Stock", "")
                            .strip()
                            for size in sizes
                        ],
                        "in_stock": [size["in_stock"] for size in sizes],
                    }
                )
            )
            await asyncio.sleep(1)

        await page.close()
        return options

    except Exception as e:
        print(f"Error extracting {url}: {e}")
        return None


async def main():
    url = "https://www.marksandspencer.com/en-at/l/men/trousers/"
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto(url)
        await page.wait_for_selector('a[href*="/p/P"]')

        print("🔄 Scrolling and collecting product links...")
        product_links = await scroll_and_extract_product_links(page)
        print(f"✅ Found {len(product_links)} products.")

        print("🔍 Extracting product details...")
        product_details = []
        for link in tqdm(product_links):
            options = await extract_product_details(context, link)
            if options is not None:
                product_details += options
            await asyncio.sleep(5)

        await page.close()
        await browser.close()

        product_details: pl.DataFrame = pl.concat(product_details)
        product_details.write_csv("product_details.csv")
        print("✅ Product details saved to product_details.csv")


# Run the async function
asyncio.run(main())
