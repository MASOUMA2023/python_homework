from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import json
import os

URL= "https://durhamcounty.bibliocommons.com/v2/search?query=learning%20spanish&searchType=smart"

options = webdriver.ChromeOptions()
options.add_argument('--headless') 
options.add_argument('--disable-gpu')  
options.add_argument('--window-size=1920x1080') 

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
driver.get(URL)

WebDriverWait(driver, 15).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "li.cp-search-result-item"))
)

li_elements = driver.find_elements(By.CSS_SELECTOR, "li.cp-search-result-item")
print("Number of <li> elements found:", len(li_elements), "books")

results=[]

for li in li_elements:
    try:
        title_element= li.find_element(By.CSS_SELECTOR, 'span.title-content')
        title= title_element.text.strip()
    except:
        continue

    authors=[]
    try:
        author_elements=li.find_elements(By.CSS_SELECTOR, 'a.author-link')
        authors = [a.text.strip() for a in author_elements if a.text.strip()]
        author_string = "; ".join(authors) if authors else "Unknown"
    except:
        author_string = "Unknown"

    try:
        format_elem= li.find_element(By.CSS_SELECTOR, 'a.manifestation-item-link')
        format_year= format_elem.text.strip()
    except:
        format_year='Unknown'
    
    results.append({"Title":title,
                    'Author': author_string,
                    'Format_year':format_year})

df= pd.DataFrame(results)
print(df)

csv_path='get_books.csv'

df.to_csv(csv_path, index=False)
print(f"csv file saved to {csv_path}")


json_path= 'get_books.json'
with open(json_path, 'w', encoding='utf-8') as f:
     json.dump(results, f,ensure_ascii=False, indent=2)
     print(f'json file saved to {json_path}')


driver.quit()