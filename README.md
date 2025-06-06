# M&S Product Explorer

This project consists of two main components:
1. A web scraper (`main.py`) that extracts product data from Marks & Spencer
2. A Streamlit application (`app.py`) that provides an interactive interface to explore the scraped product data

## Scraper Features
- Extracts product details including titles, prices, colors, sizes and availability
- Handles infinite scroll pages
- Processes multiple color variants for each product
- Saves data to CSV format

## Application Features
- Filters products by in-stock status
- Fuzzy search by product title
- Filter by sizes and colors
- Clean tabular display with clickable product links

## Installation
1. Clone the repository:
```bash
git clone https://github.com/yourusername/ms-product-explorer.git
cd ms-product-explorer
```

2. Install dependencies using `uv`:
```bash
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

## Usage
1. Run the scraper to collect product data:
```bash
python main.py
```

2. Launch the Streamlit application:
```bash
streamlit run app.py
```

## File Descriptions
- `main.py`: Scrapes product data from Marks & Spencer
- `app.py`: Provides interactive product exploration interface
- `product_details.csv`: Output of scraper (input for application)
- `requirements.txt`: Python dependencies
