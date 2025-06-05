import polars as pl

df = pl.read_csv("product_details.csv")

options = df.filter(
    pl.col("sizes").str.contains_any(["34-Extra Long", "34-35"])
).filter(pl.col("in_stock"))

options = options.group_by(["title", "url", "price"]).agg(pl.col("colour"))

for i, option in enumerate(options.iter_rows(named=True), 1):
    print(f"{i}: {option['title']} ({option['price']})")
    print(f"Colours: {', '.join(option['colour'])}")
    print(option["url"])
    print()
