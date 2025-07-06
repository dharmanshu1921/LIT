from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import os
import time

# Setup Chrome options for Mac
options = Options()
options.add_argument("--start-maximized")
options.add_argument("--disable-infobars")
options.add_argument("--disable-extensions")
# Uncomment the next line to run in headless mode
# options.add_argument("--headless=new")

# Initialize Chrome driver
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)
wait = WebDriverWait(driver, 20)

# Target URL
url = "https://www.ajio.com/women-westernwear-dresses/c/830316003"
driver.get(url)

# Improved scrolling to load more products
last_height = driver.execute_script("return document.body.scrollHeight")
scroll_attempts = 0
max_attempts = 8

while scroll_attempts < max_attempts:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)  # Allow time for content to load
    
    # Check if we've reached the bottom
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
        
    last_height = new_height
    scroll_attempts += 1

# Wait for products
try:
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "rilrtl-products-list__item")))
except Exception as e:
    print(f"❌ Timed out waiting for products: {e}")
    driver.save_screenshot("ajio_debug.png")
    driver.quit()
    exit()

# Get product items
items = driver.find_elements(By.CLASS_NAME, "rilrtl-products-list__item")
print(f"✅ Found {len(items)} products")

data = []

for item in items:
    try:
        brand = item.find_element(By.CLASS_NAME, "brand").text.strip()
        name = item.find_element(By.CLASS_NAME, "nameCls").text.strip()
        price = item.find_element(By.CLASS_NAME, "price").text.replace("₹", "").replace(",", "").strip()
    except Exception as e:
        print(f"⚠️ Skipping product due to missing data: {e}")
        continue

    # Get original price if available
    try:
        original_price = item.find_element(By.CLASS_NAME, "orginal-price").text.replace("₹", "").replace(",", "").strip()
    except:
        original_price = price

    # Improved image extraction
    img_url = None
    img_selectors = [
        'img.rilrtl-lazy-img.rilrtl-lazy-img-loaded',
        'img.rilrtl-lazy-img',
        '.imgHolder img'
    ]
    
    for selector in img_selectors:
        try:
            img = item.find_element(By.CSS_SELECTOR, selector)
            img_url = img.get_attribute("src") or img.get_attribute("data-src")
            if img_url and img_url.startswith('http'):
                break
        except:
            continue

    if not img_url:
        img_url = "https://via.placeholder.com/150?text=No+Image"

    data.append({
        "brand": brand,
        "product_name": name,
        "price": price,
        "original_price": original_price,
        "image_url": img_url
    })

driver.quit()

# Save to CSV
os.makedirs("data", exist_ok=True)
df = pd.DataFrame(data)
df.to_csv("data/ajio_sample.csv", index=False)
print(f"✅ Saved {len(df)} products to data/ajio_sample.csv")
