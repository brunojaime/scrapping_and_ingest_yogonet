from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

import time
import tempfile

def scrape_yogonet(url):
    
    elements = []
    options = webdriver.ChromeOptions()
   #options.add_argument('--headless') 
    options.add_argument('--disable-gpu')
    #options.add_argument("--no-sandbox")  
    options.add_argument("--disable-dev-shm-usage")  
    options.add_argument("--disable-gpu") 
    options.add_argument('--window-size=1920x1080')
    temp_user_data_dir = tempfile.mkdtemp()
    options.add_argument(f'--user-data-dir={temp_user_data_dir}')
    driver = webdriver.Chrome(options=options)

    driver.get(url)
    
    
    
    links = WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.item_menu a"))
    )
    urls = [link.get_attribute("href") for link in links if link.get_attribute("href") and not link.get_attribute("href").startswith("javascript") ]
    print("URLs encontradas:")
    urls_validas =  [final_url for final_url in urls if es_categoria_valida(url,final_url)]
    print("URls validas")
    for url in urls_validas:
        print("-", url)
        elements.extend(get_element(driver, url))
       

    return elements
    
def get_element(driver,url) :
        this_elements = []
        driver.get(url)
        try:
            noticias = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.item_listado_noticias"))
            )
            for noticia in noticias:
            
                title = noticia.find_element(By.CSS_SELECTOR, ".volanta_item_listado_noticias a").get_attribute("title")
                image_url = noticia.find_element(By.CSS_SELECTOR, ".imagen_item_listado_noticias img").get_attribute("src")
                texto_completo = noticia.find_element(By.CSS_SELECTOR, ".volanta_item_listado_noticias a").text.strip()
                kicker = texto_completo.split(" ", 1)[-1].strip()  
                this_elements.append({"title":title,"kicker":kicker,"image_url":image_url,"link":url})
        except (TimeoutException, NoSuchElementException) as e:
             print(f"Error al procesar {url}: {e}")
        return this_elements

def es_categoria_valida(base,link):
    
    if not link.startswith(base):
        return False
    resto = link[len(base):]
    return resto.count("/") == 2