import pandas as pd
import json
import urllib.parse

# Configuration - Update these paths to match your files
csv_path = "amazon_scrape_20250703_190143/amazon_products_20250703_190143.csv"
json_path = "amazon_scrape_20250703_190143/amazon_products_20250703_190143.json"
output_csv = "Output/amazon_products.csv"
output_json = "Output/amazon_products.json"

# 1. Update CSV File
# ==================

# Load your existing CSV data
df = pd.read_csv(csv_path)

# Load the JSON data which contains the URLs
with open(json_path, 'r', encoding='utf-8') as f:
    json_data = json.load(f)

# Create mapping from product name to URLs
url_mapping = {}
for product in json_data:
    key = (product['product_name'], product['brand'])
    
    # Extract actual Amazon URL from affiliate link
    amazon_url = ""
    if product.get('affiliate_link'):
        # Try to decode the URL from affiliate link
        affiliate_url = product['affiliate_link']
        if '?url=' in affiliate_url:
            amazon_url = affiliate_url.split('?url=')[1].split('&')[0]
            amazon_url = urllib.parse.unquote(amazon_url)
    
    url_mapping[key] = {
        'product_url': amazon_url,
        'image_url': product.get('image_url', '')
    }

# Add new columns to DataFrame
df['product_url'] = df.apply(lambda row: url_mapping.get(
    (row['product_name'], row['brand']), 
    {'product_url': '', 'image_url': ''}
)['product_url'], axis=1)

df['image_url'] = df.apply(lambda row: url_mapping.get(
    (row['product_name'], row['brand']), 
    {'product_url': '', 'image_url': ''}
)['image_url'], axis=1)

# Reorder columns to match your desired format
column_order = [
    "product_name", "brand", "category", "gender", "price", 
    "discounted_price", "affiliate_link", "product_url",  # Added product_url here
    "image_clean", "image_original", "image_url", "source_platform"
]
df = df[column_order]

# Save updated CSV
df.to_csv(output_csv, index=False)
print(f"Updated CSV saved to: {output_csv}")

# 2. Update JSON File
# ===================

# Update JSON data with the new fields
updated_json_data = []
for product in json_data:
    # Extract actual Amazon URL from affiliate link
    amazon_url = ""
    if product.get('affiliate_link'):
        affiliate_url = product['affiliate_link']
        if '?url=' in affiliate_url:
            amazon_url = affiliate_url.split('?url=')[1].split('&')[0]
            amazon_url = urllib.parse.unquote(amazon_url)
    
    # Create updated product entry
    updated_product = {
        **product,
        "product_url": amazon_url,
        "image_url": product.get("image_url", "")
    }
    updated_json_data.append(updated_product)

# Save updated JSON
with open(output_json, 'w', encoding='utf-8') as f:
    json.dump(updated_json_data, f, indent=2, ensure_ascii=False)

print(f"Updated JSON saved to: {output_json}")
print("Processing complete!")