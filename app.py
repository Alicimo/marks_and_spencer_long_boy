import polars as pl
import streamlit as st

st.title("M&S Product Explorer")

# Load data
df = pl.read_csv("product_details.csv")

# Filter only in-stock items
in_stock = df.filter(pl.col("in_stock"))

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
