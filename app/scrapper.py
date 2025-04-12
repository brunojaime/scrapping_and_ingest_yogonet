from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def scrape_yogonet(chromedriver_path="/usr/local/bin/chromedriver"):
    # Configuramos el servicio y las opciones de Chrome
    service = Service(chromedriver_path)
    options = webdriver.ChromeOptions()
    #options.add_argument('--headless')  # Modo sin interfaz
    #options.add_argument('--disable-gpu')
    #options.add_argument('--window-size=1920x1080')

    driver = webdriver.Chrome(service=service, options=options)
    driver.get("https://www.yogonet.com/international/")
   
    elements = []

    try:
       
        title = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.slot.slot_1.noticia.cargada div.volanta"))
        ).text.strip()
        elements.append({"Title":title})
        print("Title:",title)  


        kicker = WebDriverWait(driver, 5).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "div.slot.slot_1.noticia.cargada h2.titulo.fuente_roboto_slab > a"))
    ).text.strip()
        
        elements.append({"Kicker":kicker})
        print("Kicker:",kicker)

        image_url = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.slot.slot_1.noticia.cargada div.imagen img"))
    ).get_attribute("src")
        
        elements.append({"Image URL":image_url})
        print("Image URL:",image_url)

    finally:
        driver.quit()

    return elements

