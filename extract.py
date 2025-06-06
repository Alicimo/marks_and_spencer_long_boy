import polars as pl
import streamlit as st

st.title("M&S Product Explorer")

# Load data
df = pl.read_csv("product_details.csv")

# Parse list columns from string to actual lists
df = df.with_columns(
    pl.col("sizes").str.json_decode(),
    pl.col("in_stock").str.json_decode(),
)

# Explode the lists so each row has one size and its in_stock status
exploded = df.explode(["sizes", "in_stock"])

# Filter only in-stock items
in_stock = exploded.filter(pl.col("in_stock"))

# Get unique sizes and colours for filters
all_sizes = in_stock["sizes"].unique().sort().to_list()
all_colours = in_stock["colour"].unique().sort().to_list()

# Create filters
selected_sizes = st.multiselect("Filter by sizes", all_sizes)
selected_colours = st.multiselect("Filter by colours", all_colours)

# Apply filters
filtered = in_stock
if selected_sizes:
    filtered = filtered.filter(pl.col("sizes").is_in(selected_sizes))
if selected_colours:
    filtered = filtered.filter(pl.col("colour").is_in(selected_colours))

# Group by product and aggregate colours
grouped = filtered.group_by(["title", "url", "price"]).agg(
    pl.col("colour").unique().sort().alias("colours")
)

# Display results
st.subheader(f"Found {len(grouped)} products")
for i, row in enumerate(grouped.iter_rows(named=True), 1):
    st.markdown(f"**{i}: {row['title']} ({row['price']})**")
    st.markdown(f"Colours: {', '.join(row['colours'])}")
    st.markdown(f"[Product Link]({row['url']})")
    st.divider()
