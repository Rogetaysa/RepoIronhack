import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL base d'Ironman (ajusta segons el lloc web)
BASE_URL = "https://www.ironman.com"

def get_race_info(race_url):
    """Funció per obtenir la informació d'una cursa concreta."""
    response = requests.get(race_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Aconsegueix informació específica (ajusta segons la pàgina)
    data = {}
    try:
        data['Swim'] = soup.find('div', text='Swim').find_next('p').text.strip()
        data['Bike'] = soup.find('div', text='Bike').find_next('p').text.strip()
        data['Run'] = soup.find('div', text='Run').find_next('p').text.strip()
        data['Avg. Air Temp'] = soup.find('div', text='Avg. Air Temp').find_next('p').text.strip()
        data['Avg. Water Temp'] = soup.find('div', text='Avg. Water Temp').find_next('p').text.strip()
        data['Bike Altitude'] = soup.find('div', text='Bike Altitude').find_next('p').text.strip()
        data['Run Altitude'] = soup.find('div', text='Run Altitude').find_next('p').text.strip()
    except Exception as e:
        print(f"Error scraping {race_url}: {e}")
    return data

def get_all_races():
    """Funció per obtenir els enllaços de totes les curses."""
    races = []
    response = requests.get(f"{BASE_URL}/races")
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Troba els enllaços de les curses (ajusta el selector segons el lloc web)
    race_links = soup.find_all('a', class_='race-link')  # Ajustar si cal
    for link in race_links:
        race_url = BASE_URL + link['href']
        races.append(race_url)
    return races

def main():
    # Obtenir les curses
    race_urls = get_all_races()
    
    # Extreure informació de cada cursa
    race_data = []
    for url in race_urls:
        print(f"Scraping: {url}")
        info = get_race_info(url)
        if info:
            race_data.append(info)
    
    # Guardar les dades en un CSV
    df = pd.DataFrame(race_data)
    df.to_csv('ironman_races.csv', index=False)
    print("Dades guardades a ironman_races.csv")

if __name__ == "__main__":
    main()

