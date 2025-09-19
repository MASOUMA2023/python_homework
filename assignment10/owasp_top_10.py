from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import os


URL= " https://owasp.org/www-project-top-ten/"

options = webdriver.ChromeOptions()
options.add_argument('--headless') 
options.add_argument('--disable-gpu')  
options.add_argument('--window-size=1920x1080') 

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
driver.get(URL)

WebDriverWait(driver, 15).until(
    EC.presence_of_element_located((By.XPATH, '//*[@id="sec-main"]/ul[2]'))
    )

items= driver.find_elements(By.XPATH, '//*[@id="sec-main"]/ul[2]/li')

top10_list=[]
for item in items:
    try:
        title_elem= item.find_element(By.XPATH, './a')
        title= title_elem.text.strip()
        link= title_elem.get_attribute('href')
    except:
        continue
    top10_list.append({'title': title, 'link':link})
print(top10_list)

df= pd.DataFrame(top10_list)
csv_path=os.path.join(os.path.dirname(__file__), "owasp_top_10.csv")
df.to_csv(csv_path, index=False)
print(f"csv file saved to {csv_path}")

driver.quit()


