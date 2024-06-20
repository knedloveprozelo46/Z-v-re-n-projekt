# Scraping výsledků voleb 2017

## Popis projektu
Projekt scrapuje výsledky voleb 2017 pro daný územní celek z webu volby.cz a ukládá je do souboru CSV.

## Instalace
1. Vytvoř si virtuální prostředí:

    python -m venv venv
    source venv/bin/activate  # Pro Windows použijte `venv\Scripts\activate`


2. Nainstaluj potřebné knihovny:

    pip install -r requirements.txt


## Použití
Spusť skript s argumenty:

python volby17.py "<URL>" "<vystupni_soubor.csv>"
