from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from pymongo import MongoClient
from datetime import datetime
import re

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)")
options.add_argument("--disable-blink-features=AutomationControlled")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get('https://www.amazon.es/s?k=ratón+gaming')

try:
    WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.ID, "sp-cc-accept"))
    ).click()
except:
    pass

WebDriverWait(driver, 15).until(
    EC.presence_of_all_elements_located(
        (By.CSS_SELECTOR, "div.s-main-slot div[data-component-type='s-search-result']")
    )
)

soup = BeautifulSoup(driver.page_source, 'html.parser')
driver.quit()

mongo_uri = "mongodb+srv://kialilyas:PLnlhyirHzcdXYJK@cluster0.mdpwawe.mongodb.net/amazon_scraper?retryWrites=true&w=majority"
client = MongoClient(mongo_uri)
db = client['amazon_scraper']
collection = db['productos']

products = soup.select('div.s-main-slot div[data-component-type="s-search-result"]')
print(f"Productos encontrados: {len(products)}")

for p in products:
    title = p.select_one('h2 span')
    price_whole = p.select_one('span.a-price-whole')
    price_fraction = p.select_one('span.a-price-fraction')

    if title and price_whole and price_fraction:
        name = title.text.strip()
        # Extraer solo dígitos de euros y céntimos
        raw_whole = ''.join(re.findall(r'\d+', price_whole.text))
        raw_fraction = ''.join(re.findall(r'\d+', price_fraction.text))
        importe = f"{raw_whole}.{raw_fraction}"
        price_val = float(importe)
        fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        collection.insert_one({
            'name': name,
            'price': price_val,
            'fecha_extraccion': fecha_actual
        })
        print(f"Insertado: {name} - {price_val} € - {fecha_actual}")
