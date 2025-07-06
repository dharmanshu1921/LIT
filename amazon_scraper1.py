# import os
# import shutil
# import logging
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import TimeoutException, NoSuchElementException
# from selenium.webdriver.common.action_chains import ActionChains
# import time
# import csv
# import re
# import urllib.parse
# import random
# from datetime import datetime
# from rich.console import Console
# from rich.table import Table
# from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
# from rich.panel import Panel
# from rich.text import Text
# import requests
# import json

# class AmazonScraper:
#     def __init__(self):
#         self.console = Console()
#         self.setup_driver_options()
#         self.driver = None
#         self.session_stats = {
#             'total_products': 0,
#             'successful_extractions': 0,
#             'failed_extractions': 0,
#             'categories_processed': 0,
#             'start_time': None
#         }
#         self.output_dir = ""
#         self.images_dir = ""
#         self.logger = self.setup_logger()
        
#         # Vastly expanded category mapping with detailed search terms
#         self.categories = {
#             "Shoes": {
#                 "Women": [
#                     "women+high+heels+designer", "women+sneakers+athletic", "women+boots+ankle", 
#                     "women+sandals+summer", "women+loafers+formal", "women+wedges+casual",
#                     "women+flats+ballet", "women+platform+shoes", "women+espadrilles",
#                     "women+athletic+running", "women+hiking+boots", "women+rain+boots",
#                     "women+dress+shoes", "women+work+shoes", "women+dance+shoes",
#                     "women+wide+width+shoes", "women+orthopedic+shoes", "women+skate+shoes"
#                 ],
#                 "Men": [
#                     "men+sneakers+casual", "men+dress+shoes+formal", "men+boots+work", 
#                     "men+sandals+slide", "men+loafers+driving", "men+oxfords",
#                     "men+derby+shoes", "men+trainers+gym", "men+hiking+shoes",
#                     "men+running+shoes", "men+boat+shoes", "men+chukka+boots",
#                     "men+chelsea+boots", "men+work+boots", "men+climbing+shoes",
#                     "men+wide+width+shoes", "men+orthopedic+shoes", "men+skate+shoes"
#                 ],
#                 "Unisex": [
#                     "unisex+sneakers", "unisex+slip+on", "unisex+canvas+shoes",
#                     "unisex+water+shoes", "unisex+skateboarding", "unisex+minimalist+shoes",
#                     "unisex+barefoot+shoes"
#                 ]
#             },
#             "Bags": {
#                 "Women": [
#                     "women+designer+handbags", "women+tote+bags+leather", "women+clutch+evening",
#                     "women+shoulder+bags", "women+backpack+travel", "women+crossbody+sling",
#                     "women+satchel+work", "women+belt+bags", "women+beach+bags",
#                     "women+laptop+backpacks", "women+minaudiere", "women+top+handle",
#                     "women+drawstring+bags", "women+evening+clutches", "women+quilted+bags"
#                 ],
#                 "Men": [
#                     "men+leather+messenger", "men+backpack+laptop", "men+briefcase+professional",
#                     "men+duffle+travel", "men+sling+bag", "men+gym+duffel",
#                     "men+shoulder+bag", "men+waist+pack", "men+tote+bag",
#                     "men+garment+bag", "men+tech+backpack", "men+travel+backpack",
#                     "men+camera+bag", "men+cycling+backpack", "men+fishing+vest"
#                 ],
#                 "Unisex": [
#                     "luggage+sets", "carry+on+luggage", "checked+luggage",
#                     "travel+backpacks", "duffel+bags+large", "laptop+backpacks+waterproof",
#                     "gym+duffels", "cooler+bags", "picnic+baskets",
#                     "compression+sacks", "dry+bags", "camera+backpacks",
#                     "hydration+packs", "tactical+backpacks", "rolling+backpacks"
#                 ]
#             },
#             "Accessories": {
#                 "Women": [
#                     "women+designer+sunglasses", "women+belts+leather", "women+scarves+silk",
#                     "women+statement+necklace", "women+designer+watches", "women+designer+wallets",
#                     "women+hair+accessories", "women+jewelry+sets", "women+brooches",
#                     "women+gloves", "women+hats+fashion", "women+stockings",
#                     "women+ties+scarves", "women+keychains", "women+tech+accessories"
#                 ],
#                 "Men": [
#                     "men+aviator+sunglasses", "men+leather+belts", "men+automatic+watches",
#                     "men+bifold+wallets", "men+designer+ties", "men+cufflinks+set",
#                     "men+pocket+squares", "men+hats+caps", "men+gloves+leather",
#                     "men+socks+dress", "men+tech+accessories", "men+keychains",
#                     "men+bracelets", "men+suspenders", "men+arm+sleeves"
#                 ],
#                 "Unisex": [
#                     "luxury+sunglasses", "designer+eyeglasses", "fitness+trackers",
#                     "smart+watches", "phone+cases+premium", "laptop+sleeves",
#                     "umbrellas+windproof", "travel+pillows", "blankets+throws",
#                     "gadget+accessories", "cables+organizers", "chargers+premium",
#                     "power+banks+fast", "headphones+wireless", "earbuds+premium"
#                 ]
#             },
#             "Clothing": {
#                 "Women": [
#                     "women+designer+dresses", "women+jackets+designer", "women+blouses+silk",
#                     "women+designer+jeans", "women+skirts+pleated", "women+sweaters+cashmere",
#                     "women+suits+pantsuits", "women+activewear+sets", "women+swimwear+designer",
#                     "women+lingerie+luxury", "women+coats+wool", "women+cardigans",
#                     "women+pajamas+silk", "women+shapewear", "women+maternity+dresses"
#                 ],
#                 "Men": [
#                     "men+designer+shirts", "men+jackets+bomber", "men+jeans+designer",
#                     "men+designer+t-shirts", "men+suits+designer", "men+sweaters+merino",
#                     "men+activewear+sets", "men+swim+trunks", "men+underwear+premium",
#                     "men+coats+overcoats", "men+vests+sleeveless", "men+pajamas",
#                     "men+robes", "men+base+layers", "men+formal+waistcoats"
#                 ],
#                 "Unisex": [
#                     "luxury+hoodies", "premium+sweatshirts", "designer+track+pants",
#                     "cashmere+robes", "silk+pajamas", "thermal+underwear",
#                     "rain+jackets", "down+jackets", "fleece+jackets",
#                     "performance+tees", "yoga+pants", "compression+wear",
#                     "sun+protective+clothing", "sports+bras", "cycling+shorts"
#                 ]
#             },
#             "Jewelry": {
#                 "Women": [
#                     "women+diamond+necklaces", "women+gold+earrings", "women+pearl+bracelets",
#                     "women+gemstone+rings", "women+designer+brooches", "women+charm+bracelets",
#                     "women+body+jewelry", "women+anklets", "women+cuff+bracelets",
#                     "women+statement+earrings", "women+bridal+sets", "women+designer+pendants"
#                 ],
#                 "Men": [
#                     "men+designer+watches", "men+gold+chains", "men+signet+rings",
#                     "men+cufflinks+designer", "men+bracelets+leather", "men+pendants",
#                     "men+earrings", "men+tie+clips", "men+money+clips",
#                     "men+designer+rings", "men+anklets", "men+body+jewelry"
#                 ],
#                 "Unisex": [
#                     "luxury+watches", "designer+bracelets", "couple+rings",
#                     "designer+engagement+rings", "wedding+bands", "eternity+rings",
#                     "designer+cufflinks", "money+clips", "pocket+watches",
#                     "designer+body+jewelry", "anklets+unisex", "charm+bracelets"
#                 ]
#             },
#             "Watches": {
#                 "Women": [
#                     "women+designer+watches", "women+luxury+watches", "women+diamond+watches",
#                     "women+gold+watches", "women+sport+watches", "women+smart+watches",
#                     "women+dress+watches", "women+analog+watches", "women+digital+watches"
#                 ],
#                 "Men": [
#                     "men+designer+watches", "men+luxury+watches", "men+automatic+watches",
#                     "men+chronograph+watches", "men+dive+watches", "men+pilot+watches",
#                     "men+sport+watches", "men+smart+watches", "men+quartz+watches"
#                 ],
#                 "Unisex": [
#                     "unisex+designer+watches", "unisex+smart+watches", "unisex+sport+watches",
#                     "unisex+digital+watches", "unisex+analog+watches", "couple+watch+sets"
#                 ]
#             },
#             "Beauty": {
#                 "Women": [
#                     "women+designer+perfume", "women+skincare+sets", "women+makeup+kits",
#                     "women+hair+treatment", "women+cosmetic+bags", "women+brushes+set",
#                     "women+luxury+makeup", "women+organic+skincare", "women+suncare+luxury"
#                 ],
#                 "Men": [
#                     "men+cologne+designer", "men+grooming+kits", "men+skincare+premium",
#                     "men+beard+care", "men+shaving+kits", "men+hair+styling",
#                     "men+deodorant+luxury", "men+fragrance+sets", "men+suncare"
#                 ],
#                 "Unisex": [
#                     "luxury+perfume+sets", "designer+fragrances", "organic+skincare",
#                     "premium+hair+care", "designer+cosmetic+bags", "makeup+organizers",
#                     "travel+beauty+kits", "spa+accessories", "aromatherapy+diffusers"
#                 ]
#             },
#             "Home": {
#                 "Unisex": [
#                     "luxury+bedding+sets", "designer+throw+pillows", "premium+towels",
#                     "designer+curtains", "luxury+rugs", "premium+cookware",
#                     "designer+dinnerware", "luxury+glassware", "premium+small+appliances",
#                     "designer+home+decor", "luxury+candles", "premium+wall+art",
#                     "designer+vases", "luxury+throw+blankets", "premium+storage"
#                 ]
#             },
#             "Electronics": {
#                 "Unisex": [
#                     "designer+headphones", "premium+earbuds", "luxury+speakers",
#                     "designer+smart+watches", "premium+laptops", "luxury+tablets",
#                     "designer+phone+cases", "premium+camera+bags", "luxury+gaming+accessories",
#                     "designer+chargers", "premium+webcams", "luxury+monitors"
#                 ]
#             }
#         }

#     def setup_logger(self):
#         """Set up logging configuration"""
#         logger = logging.getLogger('amazon_scraper')
#         logger.setLevel(logging.INFO)
        
#         # Create logs directory if not exists
#         logs_dir = os.path.join(os.getcwd(), 'logs')
#         os.makedirs(logs_dir, exist_ok=True)
        
#         # Create file handler
#         log_file = os.path.join(logs_dir, f'amazon_scraper_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')
#         file_handler = logging.FileHandler(log_file)
#         file_handler.setLevel(logging.INFO)
        
#         # Create console handler
#         console_handler = logging.StreamHandler()
#         console_handler.setLevel(logging.INFO)
        
#         # Create formatter
#         formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#         file_handler.setFormatter(formatter)
#         console_handler.setFormatter(formatter)
        
#         # Add handlers to logger
#         logger.addHandler(file_handler)
#         logger.addHandler(console_handler)
        
#         return logger

#     def setup_driver_options(self):
#         """Setup Chrome options with enhanced anti-detection measures"""
#         self.options = Options()
        
#         # Basic options
#         self.options.add_argument("--start-maximized")
#         self.options.add_argument("--disable-blink-features=AutomationControlled")
#         self.options.add_experimental_option("excludeSwitches", ["enable-automation"])
#         self.options.add_experimental_option('useAutomationExtension', False)
        
#         # Enhanced anti-detection
#         self.options.add_argument("--disable-extensions")
#         self.options.add_argument("--disable-plugins-discovery")
#         self.options.add_argument("--disable-web-security")
#         self.options.add_argument("--disable-features=VizDisplayCompositor")
#         self.options.add_argument("--no-first-run")
#         self.options.add_argument("--no-service-autorun")
#         self.options.add_argument("--password-store=basic")
        
#         # Random user agents
#         user_agents = [
#             "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
#             "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
#             "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
#             "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0"
#         ]
        
#         self.options.add_argument(f"--user-agent={random.choice(user_agents)}")
        
#         # Uncomment for headless mode
#         # self.options.add_argument("--headless")

#     def start_driver(self):
#         """Initialize Chrome driver with enhanced settings"""
#         try:
#             self.driver = webdriver.Chrome(options=self.options)
            
#             # Execute script to hide automation indicators
#             self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
#             self.driver.execute_script("Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]})")
#             self.driver.execute_script("Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']})")
            
#             self.console.print("[green]✓[/green] Chrome driver initialized successfully")
#             self.logger.info("Chrome driver initialized successfully")
#             return True
            
#         except Exception as e:
#             self.console.print(f"[red]✗[/red] Error initializing driver: {e}")
#             self.logger.error(f"Error initializing driver: {e}")
#             return False

#     def close_driver(self):
#         """Close the Chrome driver"""
#         if self.driver:
#             self.driver.quit()
#             self.console.print("[yellow]Driver closed[/yellow]")
#             self.logger.info("Driver closed")

#     def random_delay(self, min_delay=1, max_delay=3):
#         """Add random delay to avoid detection"""
#         delay = random.uniform(min_delay, max_delay)
#         time.sleep(delay)

#     def human_like_scroll(self):
#         """Simulate human-like scrolling behavior"""
#         try:
#             # Random scroll actions
#             for _ in range(random.randint(1, 3)):
#                 scroll_amount = random.randint(300, 800)
#                 self.driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
#                 time.sleep(random.uniform(0.5, 1.5))
                
#             # Scroll back up sometimes
#             if random.random() < 0.3:
#                 self.driver.execute_script("window.scrollBy(0, -200);")
#                 time.sleep(random.uniform(0.5, 1.0))
                
#         except Exception as e:
#             self.console.print(f"[yellow]Warning: Scroll simulation failed: {e}[/yellow]")
#             self.logger.warning(f"Scroll simulation failed: {e}")

#     def extract_price(self, price_text):
#         """Extract numeric price from text"""
#         if not price_text:
#             return None
        
#         # Clean price text and extract numbers
#         cleaned = re.sub(r'[^\d.,]', '', price_text)
#         price_match = re.search(r'(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)', cleaned)
        
#         if price_match:
#             price_str = price_match.group(1).replace(',', '')
#             try:
#                 return float(price_str)
#             except ValueError:
#                 return None
#         return None

#     def clean_text(self, text):
#         """Clean and normalize text"""
#         if not text:
#             return ""
#         # Remove extra whitespace and special characters
#         cleaned = re.sub(r'\s+', ' ', text.strip())
#         return cleaned.replace('\n', ' ').replace('\r', ' ')

#     def generate_affiliate_link(self, amazon_url, product_name):
#         """Generate affiliate link using different affiliate networks"""
        
#         # Different affiliate networks for India
#         affiliate_networks = [
#             f"https://affiliate-network1.in/redirect?url={urllib.parse.quote(amazon_url)}&product={urllib.parse.quote(product_name)}",
#             f"https://affiliate-network2.in/track?amazon_url={urllib.parse.quote(amazon_url)}",
#             f"https://commission-junction.in/amazon?link={urllib.parse.quote(amazon_url)}"
#         ]
        
#         return random.choice(affiliate_networks)

#     def generate_image_names(self, product_name, brand, category):
#         """Generate SEO-friendly image file names matching the specified format"""
#         # Clean and format for SEO
#         clean_name = re.sub(r'[^a-zA-Z0-9\s]', '', product_name.lower())
#         clean_name = re.sub(r'\s+', '-', clean_name)[:50]  # Limit length
        
#         clean_brand = re.sub(r'[^a-zA-Z0-9\s]', '', brand.lower()) if brand else "nobrand"
#         clean_brand = re.sub(r'\s+', '-', clean_brand)[:20]
        
#         # Generate SEO-friendly names in the specified format
#         image_clean = f"{clean_name}-{clean_brand}-nobg.jpg"
#         image_original = f"{clean_name}-original.jpg"
        
#         return image_clean, image_original

#     def download_image(self, image_url, image_name):
#         """Download and save product image"""
#         try:
#             if not image_url or not image_name:
#                 return False
                
#             # Create images directory if not exists
#             os.makedirs(self.images_dir, exist_ok=True)
            
#             # Get image path
#             image_path = os.path.join(self.images_dir, image_name)
            
#             # Skip if already exists
#             if os.path.exists(image_path):
#                 return True
                
#             # Download image
#             headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
#             response = requests.get(image_url, headers=headers, stream=True, timeout=10)
            
#             if response.status_code == 200:
#                 with open(image_path, 'wb') as f:
#                     response.raw.decode_content = True
#                     shutil.copyfileobj(response.raw, f)
#                 self.logger.info(f"Downloaded image: {image_name}")
#                 return True
#             return False
#         except Exception as e:
#             self.logger.error(f"Error downloading image {image_name}: {e}")
#             return False

#     def get_amazon_search_url(self, search_term, sort_by="relevance"):
#         """Generate Amazon India search URL with better parameters"""
#         base_url = "https://www.amazon.in/s"
        
#         # URL parameters for better results
#         params = {
#             'k': search_term,
#             'ref': 'sr_pg_1',
#             'qid': str(int(time.time())),
#         }
        
#         # Add sorting if specified
#         if sort_by == "price_low":
#             params['s'] = "price-asc-rank"
#         elif sort_by == "price_high":
#             params['s'] = "price-desc-rank"
#         elif sort_by == "rating":
#             params['s'] = "review-rank"
#         elif sort_by == "newest":
#             params['s'] = "date-desc-rank"
        
#         # Build URL
#         url = f"{base_url}?" + urllib.parse.urlencode(params)
#         return url

#     def scrape_product_details(self, product_element, category, gender):
#         """Extract detailed product information including image URL"""
#         try:
#             product_data = {
#                 "product_name": "",
#                 "brand": "",
#                 "category": category,
#                 "gender": gender,
#                 "price": None,
#                 "discounted_price": None,
#                 "affiliate_link": "",
#                 "image_clean": "",
#                 "image_original": "",
#                 "source_platform": "Amazon India",
#                 "image_url": ""
#             }

#             # Enhanced product name extraction
#             name_selectors = [
#                 ".//h2//a//span",
#                 ".//h2//span",
#                 ".//span[@class='a-size-base-plus']",
#                 ".//span[@class='a-size-base']",
#                 ".//h3//a//span",
#                 ".//a[@class='a-link-normal']//span"
#             ]
            
#             for selector in name_selectors:
#                 try:
#                     elements = product_element.find_elements(By.XPATH, selector)
#                     for element in elements:
#                         text = self.clean_text(element.text)
#                         if text and len(text) > 10:  # Ensure meaningful product name
#                             product_data["product_name"] = text
#                             break
#                     if product_data["product_name"]:
#                         break
#                 except:
#                     continue

#             # Enhanced brand extraction
#             brand_selectors = [
#                 ".//span[contains(@class, 'a-size-base-plus') and contains(text(), 'Brand:')]/../span[2]",
#                 ".//span[contains(@class, 'a-size-base') and preceding-sibling::span[contains(text(), 'Brand')]]",
#                 ".//div[@class='a-row a-size-base a-color-secondary']//span[1]",
#                 ".//span[@class='a-size-base-plus']"
#             ]
            
#             for selector in brand_selectors:
#                 try:
#                     element = product_element.find_element(By.XPATH, selector)
#                     brand_text = self.clean_text(element.text)
#                     if brand_text and not any(word in brand_text.lower() for word in ['visit', 'store', 'brand', 'by']):
#                         product_data["brand"] = brand_text
#                         break
#                 except:
#                     continue
            
#             # Extract brand from product name if not found
#             if not product_data["brand"] and product_data["product_name"]:
#                 words = product_data["product_name"].split()
#                 if words:
#                     product_data["brand"] = words[0]

#             # Enhanced price extraction
#             price_selectors = [
#                 ".//span[@class='a-price-whole']",
#                 ".//span[@class='a-price-fraction']",
#                 ".//span[contains(@class, 'a-price')]//span[@class='a-offscreen']",
#                 ".//span[@class='a-price-range']",
#                 ".//span[contains(@class, 'a-price-symbol')]/../span[2]"
#             ]
            
#             found_prices = []
#             for selector in price_selectors:
#                 try:
#                     elements = product_element.find_elements(By.XPATH, selector)
#                     for element in elements:
#                         price_text = element.text or element.get_attribute('textContent')
#                         if price_text:
#                             price_value = self.extract_price(price_text)
#                             if price_value and price_value > 0:
#                                 found_prices.append(price_value)
#                 except:
#                     continue
            
#             # Process found prices
#             if found_prices:
#                 unique_prices = sorted(list(set(found_prices)))
#                 if len(unique_prices) >= 2:
#                     product_data["discounted_price"] = unique_prices[0]
#                     product_data["price"] = unique_prices[1]
#                 else:
#                     product_data["price"] = unique_prices[0]
#                     product_data["discounted_price"] = unique_prices[0]

#             # Extract product URL for affiliate link
#             try:
#                 link_element = product_element.find_element(By.XPATH, ".//h2//a")
#                 product_url = link_element.get_attribute("href")
#                 if product_url:
#                     if product_url.startswith('/'):
#                         product_url = "https://www.amazon.in" + product_url
#                     product_data["affiliate_link"] = self.generate_affiliate_link(
#                         product_url, product_data["product_name"]
#                     )
#             except:
#                 pass

#             # Extract image URL
#             try:
#                 image_element = product_element.find_element(By.XPATH, ".//img[@data-image-latency='s-product-image']")
#                 image_url = image_element.get_attribute('src')
#                 if not image_url or 'data:image' in image_url:
#                     image_url = image_element.get_attribute('data-src')
#                 if not image_url:
#                     srcset = image_element.get_attribute('srcset')
#                     if srcset:
#                         # Take the first URL from srcset
#                         urls = [u.strip().split(' ')[0] for u in srcset.split(',')]
#                         if urls:
#                             image_url = urls[0]
#                 product_data["image_url"] = image_url
#             except:
#                 pass

#             # Generate image names
#             if product_data["product_name"]:
#                 image_clean, image_original = self.generate_image_names(
#                     product_data["product_name"], 
#                     product_data["brand"], 
#                     category
#                 )
#                 product_data["image_clean"] = image_clean
#                 product_data["image_original"] = image_original

#             return product_data if product_data["product_name"] else None

#         except Exception as e:
#             self.console.print(f"[red]Error extracting product: {e}[/red]")
#             self.logger.error(f"Error extracting product: {e}")
#             return None

#     def scrape_search_results(self, search_term, category, gender, max_products=100):
#         """Scrape products from search results with progress tracking"""
#         products = []
        
#         try:
#             # Get search URL
#             search_url = self.get_amazon_search_url(search_term)
#             self.logger.info(f"Scraping search: {search_term}")
            
#             with self.console.status(f"[bold green]Loading search results for: {search_term}"):
#                 self.driver.get(search_url)
#                 self.random_delay(2, 4)
            
#             # Handle potential blocking
#             if any(keyword in self.driver.current_url.lower() for keyword in ['captcha', 'robot', 'verify']):
#                 self.console.print("[red]⚠️  Detected captcha/verification page[/red]")
#                 self.console.print("[yellow]Please solve manually and press Enter to continue...[/yellow]")
#                 self.logger.warning("Captcha detected, waiting for manual intervention")
#                 input()
#                 self.logger.info("Manual captcha solving completed")
            
#             # Simulate human behavior
#             self.human_like_scroll()
            
#             # Find product containers with multiple selectors
#             product_selectors = [
#                 "//div[@data-component-type='s-search-result']",
#                 "//div[contains(@class, 's-result-item')]",
#                 "//div[@data-index]",
#                 "//div[contains(@class, 'product-item')]"
#             ]
            
#             product_elements = []
#             for selector in product_selectors:
#                 try:
#                     elements = self.driver.find_elements(By.XPATH, selector)
#                     if elements:
#                         product_elements = elements
#                         break
#                 except:
#                     continue
            
#             if not product_elements:
#                 self.console.print(f"[yellow]No products found for: {search_term}[/yellow]")
#                 self.logger.warning(f"No products found for search: {search_term}")
#                 return products
            
#             # Process products with progress bar
#             with Progress(
#                 SpinnerColumn(),
#                 TextColumn("[progress.description]{task.description}"),
#                 BarColumn(),
#                 TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
#                 TimeElapsedColumn(),
#                 console=self.console
#             ) as progress:
                
#                 task = progress.add_task(
#                     f"Extracting products from {search_term}...", 
#                     total=min(len(product_elements), max_products)
#                 )
                
#                 for i, product_element in enumerate(product_elements[:max_products]):
#                     try:
#                         product_data = self.scrape_product_details(product_element, category, gender)
                        
#                         if product_data and product_data['product_name']:
#                             # Download and save image
#                             if product_data.get('image_url'):
#                                 self.download_image(product_data['image_url'], product_data['image_original'])
                            
#                             products.append(product_data)
#                             self.session_stats['successful_extractions'] += 1
                            
#                             # Show extracted product
#                             progress.console.print(
#                                 f"[green]✓[/green] {product_data['product_name'][:50]}..."
#                             )
#                         else:
#                             self.session_stats['failed_extractions'] += 1
                        
#                         progress.update(task, advance=1)
                        
#                         # Random delay between extractions
#                         self.random_delay(0.5, 1.5)
                        
#                     except Exception as e:
#                         self.session_stats['failed_extractions'] += 1
#                         progress.console.print(f"[red]✗[/red] Error processing product {i+1}: {e}")
#                         self.logger.error(f"Error processing product {i+1}: {e}")
#                         continue
            
#             self.console.print(f"[green]Extracted {len(products)} products from {search_term}[/green]")
#             self.logger.info(f"Extracted {len(products)} products from {search_term}")
            
#         except Exception as e:
#             self.console.print(f"[red]Error scraping search results for {search_term}: {e}[/red]")
#             self.logger.error(f"Error scraping search results for {search_term}: {e}")
        
#         return products

#     def create_stats_panel(self):
#         """Create a statistics panel for live display"""
#         stats_text = f"""
# [bold]Session Statistics[/bold]
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# [green]Total Products Scraped:[/green] {self.session_stats['total_products']}
# [green]Successful Extractions:[/green] {self.session_stats['successful_extractions']}
# [red]Failed Extractions:[/red] {self.session_stats['failed_extractions']}
# [blue]Categories Processed:[/blue] {self.session_stats['categories_processed']}

# [yellow]Success Rate:[/yellow] {(self.session_stats['successful_extractions'] / max(1, self.session_stats['successful_extractions'] + self.session_stats['failed_extractions']) * 100):.1f}%
# """
        
#         return Panel(stats_text, title="📊 Scraping Progress", border_style="blue")

#     def scrape_all_categories(self, max_products_per_search=100):
#         """Scrape all categories with enhanced progress tracking"""
        
#         # Initialize session
#         self.session_stats['start_time'] = datetime.now()
#         timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
#         self.output_dir = os.path.join(os.getcwd(), f"amazon_scrape_{timestamp}")
#         self.images_dir = os.path.join(self.output_dir, "images")
        
#         # Create output directory
#         os.makedirs(self.output_dir, exist_ok=True)
#         os.makedirs(self.images_dir, exist_ok=True)
        
#         # Display welcome message
#         welcome_panel = Panel(
#             Text("🚀 Amazon India Product Scraper Started", style="bold green", justify="center"),
#             border_style="green"
#         )
#         self.console.print(welcome_panel)
#         self.logger.info("Amazon India Product Scraper Started")
        
#         # Create files
#         csv_filename = os.path.join(self.output_dir, f"amazon_products_{timestamp}.csv")
#         json_filename = os.path.join(self.output_dir, f"amazon_products_{timestamp}.json")
        
#         all_products = []
        
#         # Main scraping loop
#         with open(csv_filename, mode="w", newline="", encoding="utf-8") as file:
#             writer = csv.writer(file)
#             writer.writerow([
#                 "product_name", "brand", "category", "gender", "price", 
#                 "discounted_price", "affiliate_link", "image_clean", 
#                 "image_original", "source_platform"
#             ])
            
#             # Process each category
#             for category, genders in self.categories.items():
                
#                 category_panel = Panel(
#                     f"[bold blue]Processing Category: {category}[/bold blue]",
#                     border_style="blue"
#                 )
#                 self.console.print(category_panel)
#                 self.logger.info(f"Processing category: {category}")
                
#                 for gender, search_terms in genders.items():
                    
#                     self.console.print(f"\n[bold yellow]--- {gender} {category} ---[/bold yellow]")
#                     self.logger.info(f"Processing gender: {gender} in {category}")
                    
#                     for search_term in search_terms:
#                         # Scrape products
#                         products = self.scrape_search_results(
#                             search_term, category, gender, max_products_per_search
#                         )
                        
#                         # Write to CSV
#                         for product in products:
#                             writer.writerow([
#                                 product["product_name"],
#                                 product["brand"],
#                                 product["category"],
#                                 product["gender"],
#                                 product["price"],
#                                 product["discounted_price"],
#                                 product["affiliate_link"],
#                                 product["image_clean"],
#                                 product["image_original"],
#                                 product["source_platform"]
#                             ])
                        
#                         all_products.extend(products)
#                         self.session_stats['total_products'] += len(products)
                        
#                         # Random delay between searches
#                         self.random_delay(3, 6)
                
#                 self.session_stats['categories_processed'] += 1
                
#                 # Show progress after each category
#                 self.console.print(self.create_stats_panel())
        
#         # Save JSON file
#         with open(json_filename, 'w', encoding='utf-8') as json_file:
#             json.dump(all_products, json_file, indent=2)
#             self.logger.info(f"Saved JSON file: {json_filename}")
        
#         # Final summary
#         self.show_final_summary(all_products, csv_filename)
        
#         return all_products

#     def show_final_summary(self, products, filename):
#         """Display final scraping summary"""
        
#         # Create summary table
#         table = Table(title="📈 Final Scraping Summary", border_style="green")
#         table.add_column("Metric", style="cyan", no_wrap=True)
#         table.add_column("Value", style="magenta")
        
#         # Calculate statistics
#         total_time = datetime.now() - self.session_stats['start_time']
#         category_counts = {}
#         brand_counts = {}
        
#         for product in products:
#             category = product['category']
#             brand = product['brand']
#             category_counts[category] = category_counts.get(category, 0) + 1
#             if brand:
#                 brand_counts[brand] = brand_counts.get(brand, 0) + 1
        
#         # Add rows to table
#         table.add_row("Total Products", str(len(products)))
#         table.add_row("Success Rate", f"{(self.session_stats['successful_extractions'] / max(1, self.session_stats['successful_extractions'] + self.session_stats['failed_extractions']) * 100):.1f}%")
#         table.add_row("Total Time", str(total_time).split('.')[0])
#         table.add_row("Products/Minute", f"{len(products) / max(1, total_time.total_seconds() / 60):.1f}")
#         table.add_row("Output File", filename)
#         table.add_row("Images Downloaded", str(len(os.listdir(self.images_dir)) if os.path.exists(self.images_dir) else "0"))
        
#         self.console.print(table)
#         self.logger.info(f"Scraping completed. Total products: {len(products)}")
        
#         # Category breakdown
#         if category_counts:
#             cat_table = Table(title="📊 Products by Category", border_style="blue")
#             cat_table.add_column("Category", style="cyan")
#             cat_table.add_column("Count", style="magenta")
            
#             for category, count in sorted(category_counts.items()):
#                 cat_table.add_row(category, str(count))
            
#             self.console.print(cat_table)
        
#         # Top brands
#         if brand_counts:
#             top_brands = sorted(brand_counts.items(), key=lambda x: x[1], reverse=True)[:10]
#             brand_table = Table(title="🏆 Top Brands", border_style="yellow")
#             brand_table.add_column("Brand", style="cyan")
#             brand_table.add_column("Products", style="magenta")
            
#             for brand, count in top_brands:
#                 brand_table.add_row(brand, str(count))
            
#             self.console.print(brand_table)

# def main():
#     """Main function with enhanced error handling and user interaction"""
#     console = Console()
    
#     # Display banner (fixed escape sequence)
#     banner = r"""
#      ___      _                         ___                  _         
#     /   \__ _| | ___ __   ___ _ __     / __\___  _   _ _ __ | | ___  ___
#     / /\ / _` | |/ / '_ \ / _ \ '__|   / /  / _ \| | | | '_ \| |/ _ \/ __|
#     / /_// (_| |   <| | | |  __/ |     / /__| (_) | |_| | |_) | |  __/\__ \
#     /___,' \__,_|_|\_\_| |_|\___|_|     \____/\___/ \__,_| .__/|_|\___||___/
#                                                       |_|                  
#     """
#     console.print(banner, style="bold blue")
#     console.print("🚀 Starting Amazon India Product Scraper", style="bold green")
    
#     scraper = AmazonScraper()
    
#     try:
#         # Initialize driver
#         if not scraper.start_driver():
#             console.print("[red]Failed to start driver. Exiting.[/red]")
#             return
        
#         # Start scraping
#         scraper.scrape_all_categories()
        
#     except Exception as e:
#         console.print(f"[red]Unexpected error: {e}[/red]")
#         scraper.logger.exception("Unexpected error occurred")
#     finally:
#         # Ensure driver is closed
#         scraper.close_driver()
#         console.print("[green]Scraping completed![/green]")

# # Entry point
# if __name__ == "__main__":
#     main()

import os
import shutil
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
import time
import csv
import re
import urllib.parse
import random
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
from rich.panel import Panel
from rich.text import Text
import requests
import json

class AmazonScraper:
    def __init__(self):
        self.console = Console()
        self.setup_driver_options()
        self.driver = None
        self.session_stats = {
            'total_products': 0,
            'successful_extractions': 0,
            'failed_extractions': 0,
            'categories_processed': 0,
            'start_time': None
        }
        self.output_dir = ""
        self.images_dir = ""
        self.logger = self.setup_logger()
        
        # Vastly expanded category mapping with detailed search terms
        self.categories = {
            "Shoes": {
                "Women": [
                    "women+high+heels+designer", "women+sneakers+athletic", "women+boots+ankle", 
                    "women+sandals+summer", "women+loafers+formal", "women+wedges+casual",
                    "women+flats+ballet", "women+platform+shoes", "women+espadrilles",
                    "women+athletic+running", "women+hiking+boots", "women+rain+boots",
                    "women+dress+shoes", "women+work+shoes", "women+dance+shoes",
                    "women+wide+width+shoes", "women+orthopedic+shoes", "women+skate+shoes"
                ],
                "Men": [
                    "men+sneakers+casual", "men+dress+shoes+formal", "men+boots+work", 
                    "men+sandals+slide", "men+loafers+driving", "men+oxfords",
                    "men+derby+shoes", "men+trainers+gym", "men+hiking+shoes",
                    "men+running+shoes", "men+boat+shoes", "men+chukka+boots",
                    "men+chelsea+boots", "men+work+boots", "men+climbing+shoes",
                    "men+wide+width+shoes", "men+orthopedic+shoes", "men+skate+shoes"
                ],
                "Unisex": [
                    "unisex+sneakers", "unisex+slip+on", "unisex+canvas+shoes",
                    "unisex+water+shoes", "unisex+skateboarding", "unisex+minimalist+shoes",
                    "unisex+barefoot+shoes"
                ]
            },
            "Bags": {
                "Women": [
                    "women+designer+handbags", "women+tote+bags+leather", "women+clutch+evening",
                    "women+shoulder+bags", "women+backpack+travel", "women+crossbody+sling",
                    "women+satchel+work", "women+belt+bags", "women+beach+bags",
                    "women+laptop+backpacks", "women+minaudiere", "women+top+handle",
                    "women+drawstring+bags", "women+evening+clutches", "women+quilted+bags"
                ],
                "Men": [
                    "men+leather+messenger", "men+backpack+laptop", "men+briefcase+professional",
                    "men+duffle+travel", "men+sling+bag", "men+gym+duffel",
                    "men+shoulder+bag", "men+waist+pack", "men+tote+bag",
                    "men+garment+bag", "men+tech+backpack", "men+travel+backpack",
                    "men+camera+bag", "men+cycling+backpack", "men+fishing+vest"
                ],
                "Unisex": [
                    "luggage+sets", "carry+on+luggage", "checked+luggage",
                    "travel+backpacks", "duffel+bags+large", "laptop+backpacks+waterproof",
                    "gym+duffels", "cooler+bags", "picnic+baskets",
                    "compression+sacks", "dry+bags", "camera+backpacks",
                    "hydration+packs", "tactical+backpacks", "rolling+backpacks"
                ]
            },
            "Accessories": {
                "Women": [
                    "women+designer+sunglasses", "women+belts+leather", "women+scarves+silk",
                    "women+statement+necklace", "women+designer+watches", "women+designer+wallets",
                    "women+hair+accessories", "women+jewelry+sets", "women+brooches",
                    "women+gloves", "women+hats+fashion", "women+stockings",
                    "women+ties+scarves", "women+keychains", "women+tech+accessories"
                ],
                "Men": [
                    "men+aviator+sunglasses", "men+leather+belts", "men+automatic+watches",
                    "men+bifold+wallets", "men+designer+ties", "men+cufflinks+set",
                    "men+pocket+squares", "men+hats+caps", "men+gloves+leather",
                    "men+socks+dress", "men+tech+accessories", "men+keychains",
                    "men+bracelets", "men+suspenders", "men+arm+sleeves"
                ],
                "Unisex": [
                    "luxury+sunglasses", "designer+eyeglasses", "fitness+trackers",
                    "smart+watches", "phone+cases+premium", "laptop+sleeves",
                    "umbrellas+windproof", "travel+pillows", "blankets+throws",
                    "gadget+accessories", "cables+organizers", "chargers+premium",
                    "power+banks+fast", "headphones+wireless", "earbuds+premium"
                ]
            },
            "Clothing": {
                "Women": [
                    "women+designer+dresses", "women+jackets+designer", "women+blouses+silk",
                    "women+designer+jeans", "women+skirts+pleated", "women+sweaters+cashmere",
                    "women+suits+pantsuits", "women+activewear+sets", "women+swimwear+designer",
                    "women+lingerie+luxury", "women+coats+wool", "women+cardigans",
                    "women+pajamas+silk", "women+shapewear", "women+maternity+dresses"
                ],
                "Men": [
                    "men+designer+shirts", "men+jackets+bomber", "men+jeans+designer",
                    "men+designer+t-shirts", "men+suits+designer", "men+sweaters+merino",
                    "men+activewear+sets", "men+swim+trunks", "men+underwear+premium",
                    "men+coats+overcoats", "men+vests+sleeveless", "men+pajamas",
                    "men+robes", "men+base+layers", "men+formal+waistcoats"
                ],
                "Unisex": [
                    "luxury+hoodies", "premium+sweatshirts", "designer+track+pants",
                    "cashmere+robes", "silk+pajamas", "thermal+underwear",
                    "rain+jackets", "down+jackets", "fleece+jackets",
                    "performance+tees", "yoga+pants", "compression+wear",
                    "sun+protective+clothing", "sports+bras", "cycling+shorts"
                ]
            },
            "Jewelry": {
                "Women": [
                    "women+diamond+necklaces", "women+gold+earrings", "women+pearl+bracelets",
                    "women+gemstone+rings", "women+designer+brooches", "women+charm+bracelets",
                    "women+body+jewelry", "women+anklets", "women+cuff+bracelets",
                    "women+statement+earrings", "women+bridal+sets", "women+designer+pendants"
                ],
                "Men": [
                    "men+designer+watches", "men+gold+chains", "men+signet+rings",
                    "men+cufflinks+designer", "men+bracelets+leather", "men+pendants",
                    "men+earrings", "men+tie+clips", "men+money+clips",
                    "men+designer+rings", "men+anklets", "men+body+jewelry"
                ],
                "Unisex": [
                    "luxury+watches", "designer+bracelets", "couple+rings",
                    "designer+engagement+rings", "wedding+bands", "eternity+rings",
                    "designer+cufflinks", "money+clips", "pocket+watches",
                    "designer+body+jewelry", "anklets+unisex", "charm+bracelets"
                ]
            },
            "Watches": {
                "Women": [
                    "women+designer+watches", "women+luxury+watches", "women+diamond+watches",
                    "women+gold+watches", "women+sport+watches", "women+smart+watches",
                    "women+dress+watches", "women+analog+watches", "women+digital+watches"
                ],
                "Men": [
                    "men+designer+watches", "men+luxury+watches", "men+automatic+watches",
                    "men+chronograph+watches", "men+dive+watches", "men+pilot+watches",
                    "men+sport+watches", "men+smart+watches", "men+quartz+watches"
                ],
                "Unisex": [
                    "unisex+designer+watches", "unisex+smart+watches", "unisex+sport+watches",
                    "unisex+digital+watches", "unisex+analog+watches", "couple+watch+sets"
                ]
            },
            "Beauty": {
                "Women": [
                    "women+designer+perfume", "women+skincare+sets", "women+makeup+kits",
                    "women+hair+treatment", "women+cosmetic+bags", "women+brushes+set",
                    "women+luxury+makeup", "women+organic+skincare", "women+suncare+luxury"
                ],
                "Men": [
                    "men+cologne+designer", "men+grooming+kits", "men+skincare+premium",
                    "men+beard+care", "men+shaving+kits", "men+hair+styling",
                    "men+deodorant+luxury", "men+fragrance+sets", "men+suncare"
                ],
                "Unisex": [
                    "luxury+perfume+sets", "designer+fragrances", "organic+skincare",
                    "premium+hair+care", "designer+cosmetic+bags", "makeup+organizers",
                    "travel+beauty+kits", "spa+accessories", "aromatherapy+diffusers"
                ]
            },
            "Home": {
                "Unisex": [
                    "luxury+bedding+sets", "designer+throw+pillows", "premium+towels",
                    "designer+curtains", "luxury+rugs", "premium+cookware",
                    "designer+dinnerware", "luxury+glassware", "premium+small+appliances",
                    "designer+home+decor", "luxury+candles", "premium+wall+art",
                    "designer+vases", "luxury+throw+blankets", "premium+storage"
                ]
            },
            "Electronics": {
                "Unisex": [
                    "designer+headphones", "premium+earbuds", "luxury+speakers",
                    "designer+smart+watches", "premium+laptops", "luxury+tablets",
                    "designer+phone+cases", "premium+camera+bags", "luxury+gaming+accessories",
                    "designer+chargers", "premium+webcams", "luxury+monitors"
                ]
            }
        }

    def setup_logger(self):
        """Set up logging configuration"""
        logger = logging.getLogger('amazon_scraper')
        logger.setLevel(logging.INFO)
        
        # Create logs directory if not exists
        logs_dir = os.path.join(os.getcwd(), 'logs')
        os.makedirs(logs_dir, exist_ok=True)
        
        # Create file handler
        log_file = os.path.join(logs_dir, f'amazon_scraper_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.INFO)
        
        # Create console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Create formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Add handlers to logger
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
        return logger

    def setup_driver_options(self):
        """Setup Chrome options with enhanced anti-detection measures"""
        self.options = Options()
        
        # Basic options
        self.options.add_argument("--start-maximized")
        self.options.add_argument("--disable-blink-features=AutomationControlled")
        self.options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.options.add_experimental_option('useAutomationExtension', False)
        
        # Enhanced anti-detection
        self.options.add_argument("--disable-extensions")
        self.options.add_argument("--disable-plugins-discovery")
        self.options.add_argument("--disable-web-security")
        self.options.add_argument("--disable-features=VizDisplayCompositor")
        self.options.add_argument("--no-first-run")
        self.options.add_argument("--no-service-autorun")
        self.options.add_argument("--password-store=basic")
        
        # Random user agents
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0"
        ]
        
        self.options.add_argument(f"--user-agent={random.choice(user_agents)}")
        
        # Uncomment for headless mode
        # self.options.add_argument("--headless")

    def start_driver(self):
        """Initialize Chrome driver with enhanced settings"""
        try:
            self.driver = webdriver.Chrome(options=self.options)
            
            # Execute script to hide automation indicators
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            self.driver.execute_script("Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]})")
            self.driver.execute_script("Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']})")
            
            self.console.print("[green]✓[/green] Chrome driver initialized successfully")
            self.logger.info("Chrome driver initialized successfully")
            return True
            
        except Exception as e:
            self.console.print(f"[red]✗[/red] Error initializing driver: {e}")
            self.logger.error(f"Error initializing driver: {e}")
            return False

    def close_driver(self):
        """Close the Chrome driver"""
        if self.driver:
            self.driver.quit()
            self.console.print("[yellow]Driver closed[/yellow]")
            self.logger.info("Driver closed")

    def random_delay(self, min_delay=1, max_delay=3):
        """Add random delay to avoid detection"""
        delay = random.uniform(min_delay, max_delay)
        time.sleep(delay)

    def human_like_scroll(self):
        """Simulate human-like scrolling behavior"""
        try:
            # Random scroll actions
            for _ in range(random.randint(1, 3)):
                scroll_amount = random.randint(300, 800)
                self.driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
                time.sleep(random.uniform(0.5, 1.5))
                
            # Scroll back up sometimes
            if random.random() < 0.3:
                self.driver.execute_script("window.scrollBy(0, -200);")
                time.sleep(random.uniform(0.5, 1.0))
                
        except Exception as e:
            self.console.print(f"[yellow]Warning: Scroll simulation failed: {e}[/yellow]")
            self.logger.warning(f"Scroll simulation failed: {e}")

    def extract_price(self, price_text):
        """Extract numeric price from text"""
        if not price_text:
            return None
        
        # Clean price text and extract numbers
        cleaned = re.sub(r'[^\d.,]', '', price_text)
        price_match = re.search(r'(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)', cleaned)
        
        if price_match:
            price_str = price_match.group(1).replace(',', '')
            try:
                return float(price_str)
            except ValueError:
                return None
        return None

    def clean_text(self, text):
        """Clean and normalize text"""
        if not text:
            return ""
        # Remove extra whitespace and special characters
        cleaned = re.sub(r'\s+', ' ', text.strip())
        return cleaned.replace('\n', ' ').replace('\r', ' ')

    def generate_affiliate_link(self, amazon_url, product_name):
        """Generate affiliate link using different affiliate networks"""
        
        # Different affiliate networks for India
        affiliate_networks = [
            f"https://affiliate-network1.in/redirect?url={urllib.parse.quote(amazon_url)}&product={urllib.parse.quote(product_name)}",
            f"https://affiliate-network2.in/track?amazon_url={urllib.parse.quote(amazon_url)}",
            f"https://commission-junction.in/amazon?link={urllib.parse.quote(amazon_url)}"
        ]
        
        return random.choice(affiliate_networks)

    def generate_image_names(self, product_name, brand, category):
        """Generate SEO-friendly image file names matching the specified format"""
        # Clean and format for SEO
        clean_name = re.sub(r'[^a-zA-Z0-9\s]', '', product_name.lower())
        clean_name = re.sub(r'\s+', '-', clean_name)[:50]  # Limit length
        
        clean_brand = re.sub(r'[^a-zA-Z0-9\s]', '', brand.lower()) if brand else "nobrand"
        clean_brand = re.sub(r'\s+', '-', clean_brand)[:20]
        
        # Generate SEO-friendly names in the specified format
        image_clean = f"{clean_name}-{clean_brand}-nobg.jpg"
        image_original = f"{clean_name}-original.jpg"
        
        return image_clean, image_original

    def download_image(self, image_url, image_name):
        """Download and save product image"""
        try:
            if not image_url or not image_name or 'http' not in image_url:
                self.logger.warning(f"Invalid image URL or name: {image_url}")
                return False
                
            # Create images directory if not exists
            os.makedirs(self.images_dir, exist_ok=True)
            
            # Get image path
            image_path = os.path.join(self.images_dir, image_name)
            
            # Skip if already exists
            if os.path.exists(image_path):
                return True
                
            # Download image
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
                'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.9',
            }
            
            # Handle Amazon image URLs - get higher resolution version
            if 'images-amazon.com' in image_url:
                image_url = re.sub(r'\._.+_\.', '._AC_SL1000_.', image_url)
                image_url = re.sub(r'\._.+\.jpg', '._AC_SL1000_.jpg', image_url)
            
            response = requests.get(image_url, headers=headers, stream=True, timeout=15)
            
            if response.status_code == 200:
                with open(image_path, 'wb') as f:
                    response.raw.decode_content = True
                    shutil.copyfileobj(response.raw, f)
                self.logger.info(f"Downloaded image: {image_name}")
                return True
            else:
                self.logger.warning(f"Failed to download image {image_name}. Status: {response.status_code}")
                return False
        except Exception as e:
            self.logger.error(f"Error downloading image {image_name}: {e}")
            return False

    def get_amazon_search_url(self, search_term, sort_by="relevance"):
        """Generate Amazon India search URL with better parameters"""
        base_url = "https://www.amazon.in/s"
        
        # URL parameters for better results
        params = {
            'k': search_term,
            'ref': 'sr_pg_1',
            'qid': str(int(time.time())),
        }
        
        # Add sorting if specified
        if sort_by == "price_low":
            params['s'] = "price-asc-rank"
        elif sort_by == "price_high":
            params['s'] = "price-desc-rank"
        elif sort_by == "rating":
            params['s'] = "review-rank"
        elif sort_by == "newest":
            params['s'] = "date-desc-rank"
        
        # Build URL
        url = f"{base_url}?" + urllib.parse.urlencode(params)
        return url

    def scrape_product_details(self, product_element, category, gender):
        """Extract detailed product information including image URL"""
        try:
            product_data = {
                "product_name": "",
                "brand": "",
                "category": category,
                "gender": gender,
                "price": None,
                "discounted_price": None,
                "affiliate_link": "",
                "product_url": "",  # Actual Amazon URL
                "image_clean": "",
                "image_original": "",
                "source_platform": "Amazon India",
                "image_url": ""     # Original image URL
            }

            # Enhanced product name extraction
            name_selectors = [
                ".//h2//a//span",
                ".//h2//span",
                ".//span[@class='a-size-base-plus a-color-base']",
                ".//span[@class='a-size-base a-color-base']",
                ".//h3//a//span",
                ".//a[@class='a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal']//span"
            ]
            
            for selector in name_selectors:
                try:
                    elements = product_element.find_elements(By.XPATH, selector)
                    for element in elements:
                        text = self.clean_text(element.text)
                        if text and len(text) > 10:  # Ensure meaningful product name
                            product_data["product_name"] = text
                            break
                    if product_data["product_name"]:
                        break
                except:
                    continue

            # Enhanced brand extraction
            brand_selectors = [
                ".//span[contains(@class, 'a-size-base-plus') and contains(text(), 'Brand:')]/../span[2]",
                ".//span[contains(@class, 'a-size-base') and preceding-sibling::span[contains(text(), 'Brand')]]",
                ".//div[@class='a-row a-size-base a-color-secondary']//span[1]",
                ".//span[@class='a-size-base-plus']",
                ".//div[contains(@class, 'a-row')]/span[contains(text(), 'Brand')]/following-sibling::span"
            ]
            
            for selector in brand_selectors:
                try:
                    element = product_element.find_element(By.XPATH, selector)
                    brand_text = self.clean_text(element.text)
                    if brand_text and not any(word in brand_text.lower() for word in ['visit', 'store', 'brand', 'by']):
                        product_data["brand"] = brand_text
                        break
                except:
                    continue
            
            # Extract brand from product name if not found
            if not product_data["brand"] and product_data["product_name"]:
                words = product_data["product_name"].split()
                if words:
                    product_data["brand"] = words[0]

            # Enhanced price extraction
            price_selectors = [
                ".//span[@class='a-price-whole']",
                ".//span[@class='a-price-fraction']",
                ".//span[contains(@class, 'a-price')]//span[@class='a-offscreen']",
                ".//span[@class='a-price-range']",
                ".//span[contains(@class, 'a-price-symbol')]/../span[2]"
            ]
            
            found_prices = []
            for selector in price_selectors:
                try:
                    elements = product_element.find_elements(By.XPATH, selector)
                    for element in elements:
                        price_text = element.text or element.get_attribute('textContent')
                        if price_text:
                            price_value = self.extract_price(price_text)
                            if price_value and price_value > 0:
                                found_prices.append(price_value)
                except:
                    continue
            
            # Process found prices
            if found_prices:
                unique_prices = sorted(list(set(found_prices)))
                if len(unique_prices) >= 2:
                    product_data["discounted_price"] = min(unique_prices)
                    product_data["price"] = max(unique_prices)
                else:
                    product_data["price"] = unique_prices[0]
                    product_data["discounted_price"] = unique_prices[0]

            # Extract product URL
            try:
                link_element = product_element.find_element(By.XPATH, ".//h2//a")
                product_url = link_element.get_attribute("href")
                if product_url:
                    if product_url.startswith('/'):
                        product_url = "https://www.amazon.in" + product_url
                    # Store actual product URL
                    product_data["product_url"] = product_url
                    # Generate affiliate link
                    product_data["affiliate_link"] = self.generate_affiliate_link(
                        product_url, product_data["product_name"]
                    )
            except:
                pass

            # Extract image URL
            try:
                img_selectors = [
                    ".//img[@data-image-latency='s-product-image']",
                    ".//img[@class='s-image']",
                    ".//img[contains(@src, 'images-amazon.com')]"
                ]
                
                for selector in img_selectors:
                    try:
                        image_element = product_element.find_element(By.XPATH, selector)
                        image_url = image_element.get_attribute('src') or image_element.get_attribute('data-src')
                        if image_url and 'http' in image_url:
                            # Get higher resolution image
                            image_url = re.sub(r'\._.+_\.', '._AC_SL1000_.', image_url)
                            image_url = re.sub(r'\._.+\.jpg', '._AC_SL1000_.jpg', image_url)
                            product_data["image_url"] = image_url
                            break
                    except:
                        continue
            except Exception as e:
                self.logger.warning(f"Image extraction error: {e}")

            # Generate image names
            if product_data["product_name"]:
                image_clean, image_original = self.generate_image_names(
                    product_data["product_name"], 
                    product_data["brand"], 
                    category
                )
                product_data["image_clean"] = image_clean
                product_data["image_original"] = image_original

            return product_data if product_data["product_name"] else None

        except Exception as e:
            self.console.print(f"[red]Error extracting product: {e}[/red]")
            self.logger.error(f"Error extracting product: {e}")
            return None

    def scrape_search_results(self, search_term, category, gender, max_products=100):
        """Scrape products from search results with progress tracking"""
        products = []
        
        try:
            # Get search URL
            search_url = self.get_amazon_search_url(search_term)
            self.logger.info(f"Scraping search: {search_term}")
            
            with self.console.status(f"[bold green]Loading search results for: {search_term}"):
                self.driver.get(search_url)
                self.random_delay(2, 4)
            
            # Handle potential blocking
            if any(keyword in self.driver.current_url.lower() for keyword in ['captcha', 'robot', 'verify']):
                self.console.print("[red]⚠️  Detected captcha/verification page[/red]")
                self.console.print("[yellow]Please solve manually and press Enter to continue...[/yellow]")
                self.logger.warning("Captcha detected, waiting for manual intervention")
                input()
                self.logger.info("Manual captcha solving completed")
            
            # Simulate human behavior
            self.human_like_scroll()
            
            # Find product containers with multiple selectors
            product_selectors = [
                "//div[@data-component-type='s-search-result']",
                "//div[contains(@class, 's-result-item')]",
                "//div[@data-index]",
                "//div[contains(@class, 'product-item')]"
            ]
            
            product_elements = []
            for selector in product_selectors:
                try:
                    elements = self.driver.find_elements(By.XPATH, selector)
                    if elements:
                        product_elements = elements
                        break
                except:
                    continue
            
            if not product_elements:
                self.console.print(f"[yellow]No products found for: {search_term}[/yellow]")
                self.logger.warning(f"No products found for search: {search_term}")
                return products
            
            # Process products with progress bar
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                TimeElapsedColumn(),
                console=self.console
            ) as progress:
                
                task = progress.add_task(
                    f"Extracting products from {search_term}...", 
                    total=min(len(product_elements), max_products)
                )
                
                for i, product_element in enumerate(product_elements[:max_products]):
                    try:
                        product_data = self.scrape_product_details(product_element, category, gender)
                        
                        if product_data and product_data['product_name']:
                            # Download and save image
                            if product_data.get('image_url'):
                                self.download_image(product_data['image_url'], product_data['image_original'])
                            
                            products.append(product_data)
                            self.session_stats['successful_extractions'] += 1
                            
                            # Show extracted product
                            progress.console.print(
                                f"[green]✓[/green] {product_data['product_name'][:50]}..."
                            )
                        else:
                            self.session_stats['failed_extractions'] += 1
                        
                        progress.update(task, advance=1)
                        
                        # Random delay between extractions
                        self.random_delay(0.5, 1.5)
                        
                    except Exception as e:
                        self.session_stats['failed_extractions'] += 1
                        progress.console.print(f"[red]✗[/red] Error processing product {i+1}: {e}")
                        self.logger.error(f"Error processing product {i+1}: {e}")
                        continue
            
            self.console.print(f"[green]Extracted {len(products)} products from {search_term}[/green]")
            self.logger.info(f"Extracted {len(products)} products from {search_term}")
            
        except Exception as e:
            self.console.print(f"[red]Error scraping search results for {search_term}: {e}[/red]")
            self.logger.error(f"Error scraping search results for {search_term}: {e}")
        
        return products

    def create_stats_panel(self):
        """Create a statistics panel for live display"""
        success_rate = 0
        total_extractions = self.session_stats['successful_extractions'] + self.session_stats['failed_extractions']
        if total_extractions > 0:
            success_rate = (self.session_stats['successful_extractions'] / total_extractions) * 100
            
        stats_text = f"""
[bold]Session Statistics[/bold]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[green]Total Products Scraped:[/green] {self.session_stats['total_products']}
[green]Successful Extractions:[/green] {self.session_stats['successful_extractions']}
[red]Failed Extractions:[/red] {self.session_stats['failed_extractions']}
[blue]Categories Processed:[/blue] {self.session_stats['categories_processed']}

[yellow]Success Rate:[/yellow] {success_rate:.1f}%
"""
        
        return Panel(stats_text, title="📊 Scraping Progress", border_style="blue")

    def scrape_all_categories(self, max_products_per_search=100):
        """Scrape all categories with enhanced progress tracking"""
        
        # Initialize session
        self.session_stats['start_time'] = datetime.now()
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.output_dir = os.path.join(os.getcwd(), f"amazon_scrape_{timestamp}")
        self.images_dir = os.path.join(self.output_dir, "images")
        
        # Create output directory
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(self.images_dir, exist_ok=True)
        
        # Display welcome message
        welcome_panel = Panel(
            Text("🚀 Amazon India Product Scraper Started", style="bold green", justify="center"),
            border_style="green"
        )
        self.console.print(welcome_panel)
        self.logger.info("Amazon India Product Scraper Started")
        
        # Create files
        csv_filename = os.path.join(self.output_dir, f"amazon_products_{timestamp}.csv")
        json_filename = os.path.join(self.output_dir, f"amazon_products_{timestamp}.json")
        
        all_products = []
        
        # Main scraping loop
        with open(csv_filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            # UPDATED HEADER WITH NEW COLUMNS
            writer.writerow([
                "product_name", "brand", "category", "gender", "price", 
                "discounted_price", "affiliate_link", "product_url", 
                "image_clean", "image_original", "image_url", "source_platform"
            ])
            
            # Process each category
            for category, genders in self.categories.items():
                
                category_panel = Panel(
                    f"[bold blue]Processing Category: {category}[/bold blue]",
                    border_style="blue"
                )
                self.console.print(category_panel)
                self.logger.info(f"Processing category: {category}")
                
                for gender, search_terms in genders.items():
                    
                    self.console.print(f"\n[bold yellow]--- {gender} {category} ---[/bold yellow]")
                    self.logger.info(f"Processing gender: {gender} in {category}")
                    
                    for search_term in search_terms:
                        # Scrape products
                        products = self.scrape_search_results(
                            search_term, category, gender, max_products_per_search
                        )
                        
                        # Write to CSV
                        for product in products:
                            writer.writerow([
                                product["product_name"],
                                product["brand"],
                                product["category"],
                                product["gender"],
                                product["price"],
                                product["discounted_price"],
                                product["affiliate_link"],
                                product["product_url"],
                                product["image_clean"],
                                product["image_original"],
                                product["image_url"],
                                product["source_platform"]
                            ])
                        
                        all_products.extend(products)
                        self.session_stats['total_products'] += len(products)
                        
                        # Random delay between searches
                        self.random_delay(3, 6)
                
                self.session_stats['categories_processed'] += 1
                
                # Show progress after each category
                self.console.print(self.create_stats_panel())
        
        # Save JSON file
        with open(json_filename, 'w', encoding='utf-8') as json_file:
            json.dump(all_products, json_file, indent=2, ensure_ascii=False)
            self.logger.info(f"Saved JSON file: {json_filename}")
        
        # Final summary
        self.show_final_summary(all_products, csv_filename)
        
        return all_products

    def show_final_summary(self, products, filename):
        """Display final scraping summary"""
        # Count downloaded images
        image_count = len([f for f in os.listdir(self.images_dir) 
                          if os.path.isfile(os.path.join(self.images_dir, f))]) \
            if os.path.exists(self.images_dir) else 0
        
        # Create summary table
        table = Table(title="📈 Final Scraping Summary", border_style="green")
        table.add_column("Metric", style="cyan", no_wrap=True)
        table.add_column("Value", style="magenta")
        
        # Calculate statistics
        total_time = datetime.now() - self.session_stats['start_time']
        category_counts = {}
        brand_counts = {}
        
        for product in products:
            category = product['category']
            brand = product['brand']
            category_counts[category] = category_counts.get(category, 0) + 1
            if brand:
                brand_counts[brand] = brand_counts.get(brand, 0) + 1
        
        # Calculate success rate
        success_rate = 0
        total_extractions = self.session_stats['successful_extractions'] + self.session_stats['failed_extractions']
        if total_extractions > 0:
            success_rate = (self.session_stats['successful_extractions'] / total_extractions) * 100
        
        # Add rows to table
        table.add_row("Total Products", str(len(products)))
        table.add_row("Success Rate", f"{success_rate:.1f}%")
        table.add_row("Total Time", str(total_time).split('.')[0])
        table.add_row("Products/Minute", f"{len(products) / max(1, total_time.total_seconds() / 60):.1f}")
        table.add_row("Output File", filename)
        table.add_row("Images Downloaded", str(image_count))
        
        self.console.print(table)
        self.logger.info(f"Scraping completed. Total products: {len(products)}")
        
        # Category breakdown
        if category_counts:
            cat_table = Table(title="📊 Products by Category", border_style="blue")
            cat_table.add_column("Category", style="cyan")
            cat_table.add_column("Count", style="magenta")
            
            for category, count in sorted(category_counts.items()):
                cat_table.add_row(category, str(count))
            
            self.console.print(cat_table)
        
        # Top brands
        if brand_counts:
            top_brands = sorted(brand_counts.items(), key=lambda x: x[1], reverse=True)[:10]
            brand_table = Table(title="🏆 Top Brands", border_style="yellow")
            brand_table.add_column("Brand", style="cyan")
            brand_table.add_column("Products", style="magenta")
            
            for brand, count in top_brands:
                brand_table.add_row(brand, str(count))
            
            self.console.print(brand_table)

def main():
    """Main function with enhanced error handling and user interaction"""
    console = Console()
    
    # Display banner (fixed escape sequence)
    banner = r"""
     ___      _                         ___                  _         
    /   \__ _| | ___ __   ___ _ __     / __\___  _   _ _ __ | | ___  ___
    / /\ / _` | |/ / '_ \ / _ \ '__|   / /  / _ \| | | | '_ \| |/ _ \/ __|
    / /_// (_| |   <| | | |  __/ |     / /__| (_) | |_| | |_) | |  __/\__ \
    /___,' \__,_|_|\_\_| |_|\___|_|     \____/\___/ \__,_| .__/|_|\___||___/
                                                      |_|                  
    """
    console.print(banner, style="bold blue")
    console.print("🚀 Starting Amazon India Product Scraper", style="bold green")
    
    scraper = AmazonScraper()
    
    try:
        # Initialize driver
        if not scraper.start_driver():
            console.print("[red]Failed to start driver. Exiting.[/red]")
            return
        
        # Start scraping
        scraper.scrape_all_categories()
        
    except Exception as e:
        console.print(f"[red]Unexpected error: {e}[/red]")
        scraper.logger.exception("Unexpected error occurred")
    finally:
        # Ensure driver is closed
        scraper.close_driver()
        console.print("[green]Scraping completed![/green]")

# Entry point
if __name__ == "__main__":
    main()