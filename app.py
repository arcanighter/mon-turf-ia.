import streamlit as st
import requests

def scan_camouflage():
    url = "https://online.pmu.fr/stats/edito/pmu-infocentre/programme/30012026/R3/C6/partants"
    
    # On simule un navigateur Chrome sur MacOS de manière très précise
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
        'Referer': 'https://www.pmu.fr/turf/',
        'Origin': 'https://www.pmu.fr'
    }
    
    session = requests.Session() # Utiliser une session garde les cookies
    try:
        response = session.get(url, headers=headers, timeout=10)
        return response
    except Exception as e:
        return str(e)

# Teste ce code dans ton app.py
