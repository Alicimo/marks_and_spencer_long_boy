import polars as pl
import streamlit as st

st.title("M&S Product Explorer")

# Load data
df = pl.read_csv("product_details.csv")

# Filter only in-stock items
in_stock = df.filter(pl.col("in_stock"))

# Add text search
search_text = st.text_input("Search by product title")
text_filtered = in_stock
if search_text:
    text_filtered = text_filtered.filter(
        pl.col("title").str.to_lowercase().str.contains(search_text.lower())
    )

# Get unique sizes and colours for filters from the text-filtered set
all_sizes = text_filtered["sizes"].unique().sort().to_list()
all_colours = text_filtered["colour"].unique().sort().to_list()

# Create filters
selected_sizes = st.multiselect("Filter by sizes", all_sizes)
selected_colours = st.multiselect("Filter by colours", all_colours)

# Apply filters
filtered = text_filtered
if selected_sizes:
    filtered = filtered.filter(pl.col("sizes").is_in(selected_sizes))
if selected_colours:
    filtered = filtered.filter(pl.col("colour").is_in(selected_colours))

# Group by product and aggregate colours
grouped = filtered.group_by(["title", "url", "price"]).agg(
    pl.col("colour").unique().sort().alias("colours")
)

# Prepare display DataFrame
display_df = grouped.select([
    pl.col("title").alias("Product"),
    pl.col("price").alias("Price"),
    pl.col("colours").list.join(", ").alias("Colours"),
    pl.col("url").alias("Link")
])

# Display results
st.subheader(f"Found {len(grouped)} products")
st.dataframe(
    display_df,
    column_config={
        "Link": st.column_config.LinkColumn("Product Link", display_text="link")
    },
    hide_index=True,
)
