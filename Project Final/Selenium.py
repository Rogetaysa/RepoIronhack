from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time

driver = webdriver.Chrome()  # Baixa el chromedriver corresponent al teu navegador

driver.get("https://www.ironman.com/races")
time.sleep(3)  # Espera perquè carregui el JavaScript

# Exemple per extreure dades amb Selenium
race_elements = driver.find_elements(By.CLASS_NAME, 'race-link')  # Ajustar segons la pàgina
race_links = [elem.get_attribute('href') for elem in race_elements]

print(race_links)
driver.quit()
