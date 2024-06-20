import requests
from bs4 import BeautifulSoup
import pandas as pd
import sys

def scrapovat_vysledky_voleb(base_url, vystupni_soubor):
    print(f"ZÍSKÁVÁM DATA Z URL: {base_url}")
    
    # Počáteční požadavek na získání hlavní stránky
    response = requests.get(base_url)
    if response.status_code != 200:
        print(f"Chyba: Nelze přistoupit na {base_url}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    odkazy_obce = [a['href'] for a in soup.find_all('a', href=True) if 'ps311' in a['href']]
    
    data = []
    for odkaz_obec in odkazy_obce:
        obec_url = f"https://volby.cz/pls/ps2017nss/{odkaz_obec}"
        print(f"ZÍSKÁVÁM DATA Z URL: {obec_url}")
        
        response_obec = requests.get(obec_url)
        if response_obec.status_code != 200:
            print(f"Chyba: Nelze přistoupit na {obec_url}")
            continue

        soup_obec = BeautifulSoup(response_obec.text, 'html.parser')
        
        try:
            kod = soup_obec.find("td", {"headers": "sa2"}).text.strip()
            nazev = soup_obec.find("td", {"headers": "sa1"}).text.strip()
            volici = int(soup_obec.find("td", {"headers": "sa3"}).text.strip().replace('\xa0', '').replace(' ', ''))
            obalky = int(soup_obec.find("td", {"headers": "sa4"}).text.strip().replace('\xa0', '').replace(' ', '').replace(',', ''))
            platne_hlasy = int(soup_obec.find("td", {"headers": "sa5"}).text.strip().replace('\xa0', '').replace(' ', '').replace(',', ''))
            
            strany_data = soup_obec.find_all("td", {"class": "overflow_name"})
            hlasy_data = soup_obec.find_all("td", {"class": "cislo"})
            
            strany = {strana.text.strip(): int(hlasy.text.strip().replace('\xa0', '').replace(' ', '').replace(',', '')) 
                      for strana, hlasy in zip(strany_data, hlasy_data[1::2])}  # každé druhé číslo je hlas pro stranu

            data.append({
                'kod': kod,
                'nazev': nazev,
                'volici': volici,
                'obalky': obalky,
                'platne_hlasy': platne_hlasy,
                **strany
            })
        except Exception as e:
            print(f"Chyba při zpracování dat z URL: {obec_url} - {e}")
            continue

    df = pd.DataFrame(data)
    print(f"UKLÁDÁM DATA DO SOUBORU: {vystupni_soubor}")
    df.to_csv(vystupni_soubor, index=False)
    print(f"DOKONČUJI: {sys.argv[0]}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Použití: python volby17.py <URL> <vystupni_soubor.csv>")
        sys.exit(1)

    base_url = sys.argv[1]
    vystupni_soubor = sys.argv[2]
    
    scrapovat_vysledky_voleb(base_url, vystupni_soubor)
