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
from rich.live import Live
from rich.layout import Layout
from rich.align import Align
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
        
        # Enhanced category mapping with better search terms
        self.categories = {
            "Shoes": {
                "Women": [
                    "women+high+heels+shoes",
                    "women+sneakers+running+shoes", 
                    "women+flat+shoes+casual",
                    "women+sandals+summer",
                    "women+boots+ankle",
                    "women+loafers+formal"
                ],
                "Men": [
                    "men+sneakers+sports+shoes",
                    "men+formal+dress+shoes",
                    "men+boots+leather",
                    "men+loafers+slip+on",
                    "men+casual+shoes",
                    "men+running+shoes"
                ]
            },
            "Bags": {
                "Women": [
                    "women+tote+bags+leather",
                    "women+clutch+bags+evening",
                    "women+handbags+shoulder",
                    "women+backpack+travel",
                    "women+crossbody+bags",
                    "women+satchel+bags"
                ],
                "Men": [
                    "men+backpack+laptop",
                    "men+messenger+bags",
                    "men+briefcase+office",
                    "men+duffle+bags+travel",
                    "men+sling+bags",
                    "men+gym+bags"
                ],
                "Unisex": [
                    "travel+bags+luggage",
                    "gym+bags+sports",
                    "laptop+bags+backpack"
                ]
            },
            "Accessories": {
                "Women": [
                    "women+sunglasses+fashion",
                    "women+belts+leather",
                    "women+scarves+silk",
                    "women+jewelry+necklace",
                    "women+watches+fashion",
                    "women+wallets+purse"
                ],
                "Men": [
                    "men+sunglasses+aviator",
                    "men+belts+leather",
                    "men+watches+analog",
                    "men+wallets+leather",
                    "men+ties+formal",
                    "men+cufflinks+accessories"
                ],
                "Unisex": [
                    "sunglasses+uv+protection",
                    "phone+accessories+cases",
                    "fitness+trackers+watches"
                ]
            },
            "Clothing": {
                "Women": [
                    "women+dresses+casual",
                    "women+jackets+winter",
                    "women+tops+blouses",
                    "women+jeans+denim",
                    "women+skirts+fashion",
                    "women+sweaters+knitwear"
                ],
                "Men": [
                    "men+shirts+formal",
                    "men+jackets+casual",
                    "men+jeans+denim",
                    "men+t+shirts+cotton",
                    "men+suits+formal",
                    "men+sweaters+winter"
                ]
            }
        }

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
            return True
            
        except Exception as e:
            self.console.print(f"[red]✗[/red] Error initializing driver: {e}")
            return False

    def close_driver(self):
        """Close the Chrome driver"""
        if self.driver:
            self.driver.quit()
            self.console.print("[yellow]Driver closed[/yellow]")

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
        
        # Different affiliate networks (replace with actual affiliate IDs)
        affiliate_networks = [
            f"https://affiliate-network1.com/redirect?url={urllib.parse.quote(amazon_url)}&product={urllib.parse.quote(product_name)}",
            f"https://affiliate-network2.com/track?amazon_url={urllib.parse.quote(amazon_url)}",
            f"https://commission-junction.com/amazon?link={urllib.parse.quote(amazon_url)}"
        ]
        
        return random.choice(affiliate_networks)

    def generate_image_names(self, product_name, brand, category):
        """Generate SEO-friendly image file names"""
        # Clean and format for SEO
        clean_name = re.sub(r'[^a-zA-Z0-9\s]', '', product_name.lower())
        clean_name = re.sub(r'\s+', '-', clean_name)[:50]  # Limit length
        
        clean_brand = re.sub(r'[^a-zA-Z0-9\s]', '', brand.lower()) if brand else "generic"
        clean_brand = re.sub(r'\s+', '-', clean_brand)[:20]
        
        clean_category = category.lower().replace(' ', '-')
        
        # Generate SEO-friendly names
        base_name = f"{clean_category}-{clean_name}-{clean_brand}"
        
        image_clean = f"{base_name}-nobg.jpg"
        image_original = f"{base_name}-original.jpg"
        
        return image_clean, image_original

    def get_amazon_search_url(self, search_term, sort_by="relevance"):
        """Generate Amazon search URL with better parameters"""
        base_url = "https://www.amazon.com/s"
        
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
        """Extract detailed product information"""
        try:
            product_data = {
                "product_name": "",
                "brand": "",
                "category": category,
                "gender": gender,
                "price": None,
                "discounted_price": None,
                "affiliate_link": "",
                "image_clean": "",
                "image_original": "",
                "source_platform": "Amazon"
            }

            # Enhanced product name extraction
            name_selectors = [
                ".//h2//a//span",
                ".//h2//span",
                ".//span[@class='a-size-base-plus']",
                ".//span[@class='a-size-base']",
                ".//h3//a//span",
                ".//a[@class='a-link-normal']//span"
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
                ".//span[@class='a-size-base-plus']"
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
                    product_data["discounted_price"] = unique_prices[0]
                    product_data["price"] = unique_prices[1]
                else:
                    product_data["price"] = unique_prices[0]
                    product_data["discounted_price"] = unique_prices[0]

            # Extract product URL for affiliate link
            try:
                link_element = product_element.find_element(By.XPATH, ".//h2//a")
                product_url = link_element.get_attribute("href")
                if product_url:
                    if product_url.startswith('/'):
                        product_url = "https://www.amazon.com" + product_url
                    product_data["affiliate_link"] = self.generate_affiliate_link(
                        product_url, product_data["product_name"]
                    )
            except:
                pass

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
            return None

    def scrape_search_results(self, search_term, category, gender, max_products=30):
        """Scrape products from search results with progress tracking"""
        products = []
        
        try:
            # Get search URL
            search_url = self.get_amazon_search_url(search_term)
            
            with self.console.status(f"[bold green]Loading search results for: {search_term}"):
                self.driver.get(search_url)
                self.random_delay(2, 4)
            
            # Handle potential blocking
            if any(keyword in self.driver.current_url.lower() for keyword in ['captcha', 'robot', 'verify']):
                self.console.print("[red]⚠️  Detected captcha/verification page[/red]")
                self.console.print("[yellow]Please solve manually and press Enter to continue...[/yellow]")
                input()
            
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
                        continue
            
            self.console.print(f"[green]Extracted {len(products)} products from {search_term}[/green]")
            
        except Exception as e:
            self.console.print(f"[red]Error scraping search results for {search_term}: {e}[/red]")
        
        return products

    def create_stats_panel(self):
        """Create a statistics panel for live display"""
        stats_text = f"""
[bold]Session Statistics[/bold]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[green]Total Products Scraped:[/green] {self.session_stats['total_products']}
[green]Successful Extractions:[/green] {self.session_stats['successful_extractions']}
[red]Failed Extractions:[/red] {self.session_stats['failed_extractions']}
[blue]Categories Processed:[/blue] {self.session_stats['categories_processed']}

[yellow]Success Rate:[/yellow] {(self.session_stats['successful_extractions'] / max(1, self.session_stats['successful_extractions'] + self.session_stats['failed_extractions']) * 100):.1f}%
"""
        
        return Panel(stats_text, title="📊 Scraping Progress", border_style="blue")

    def scrape_all_categories(self, max_products_per_search=25):
        """Scrape all categories with enhanced progress tracking"""
        
        # Initialize session
        self.session_stats['start_time'] = datetime.now()
        
        # Display welcome message
        welcome_panel = Panel(
            Text("🚀 Amazon Product Scraper Started", style="bold green", justify="center"),
            border_style="green"
        )
        self.console.print(welcome_panel)
        
        # Create timestamped filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"amazon_products_{timestamp}.csv"
        
        all_products = []
        
        # Main scraping loop
        with open(filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([
                "product_name", "brand", "category", "gender", "price", 
                "discounted_price", "affiliate_link", "image_clean", 
                "image_original", "source_platform"
            ])
            
            # Process each category
            for category, genders in self.categories.items():
                
                category_panel = Panel(
                    f"[bold blue]Processing Category: {category}[/bold blue]",
                    border_style="blue"
                )
                self.console.print(category_panel)
                
                for gender, search_terms in genders.items():
                    
                    self.console.print(f"\n[bold yellow]--- {gender} {category} ---[/bold yellow]")
                    
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
                                product["image_clean"],
                                product["image_original"],
                                product["source_platform"]
                            ])
                        
                        all_products.extend(products)
                        self.session_stats['total_products'] += len(products)
                        
                        # Random delay between searches
                        self.random_delay(3, 6)
                
                self.session_stats['categories_processed'] += 1
                
                # Show progress after each category
                self.console.print(self.create_stats_panel())
        
        # Final summary
        self.show_final_summary(all_products, filename)
        
        return all_products

    def show_final_summary(self, products, filename):
        """Display final scraping summary"""
        
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
        
        # Add rows to table
        table.add_row("Total Products", str(len(products)))
        table.add_row("Success Rate", f"{(self.session_stats['successful_extractions'] / max(1, self.session_stats['successful_extractions'] + self.session_stats['failed_extractions']) * 100):.1f}%")
        table.add_row("Total Time", str(total_time).split('.')[0])
        table.add_row("Products/Minute", f"{len(products) / max(1, total_time.total_seconds() / 60):.1f}")
        table.add_row("Output File", filename)
        
        self.console.print(table)
        
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
    
    # Display banner
    banner = """
    [bold blue]
     ___      _                         ___                  _         
    /   \__ _| | ___ __   ___ _ __     / __\___  _   _ _ __ | | ___  ___
    / /\ / _` | |/ / '_ \ / _ \ '__|   / /  / _ \| | | | '_ \| |/ _ \/ __|
    / /_// (_| |   <| | | |  __/ |     / /__| (_) | |_| | |_) | |  __/\__ \\
    /___,' \__,_|_|\_\_| |_|\___|_|     \____/\___/ \__,_| .__/|_|\___||___/
                                                      |_|                  
    [/bold blue]
    """
    console.print(banner)
    console.print("🚀 Starting Amazon Product Scraper", style="bold green")
    
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
    finally:
        # Ensure driver is closed
        scraper.close_driver()
        console.print("[green]Scraping completed![/green]")

# Entry point
if __name__ == "__main__":
    main()