import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Turf-IA Cloud", layout="wide")
st.title("🏇 Le Cœur du Réacteur - Cloud Edition")

with st.sidebar:
    st.header("Configuration")
    date_pmu = st.text_input("Date (JJMMAAAA)", "30012026")
    reunion = st.number_input("Réunion (R)", 1, 10, 3)
    course = st.number_input("Course (C)", 1, 20, 6)
    btn_scan = st.button("🚀 FORCER LE SCAN")

if btn_scan:
    # On tente plusieurs URLs pour contourner le blocage DNS du serveur
    urls = [
        f"https://online.pmu.fr/stats/edito/pmu-infocentre/programme/{date_pmu}/R{reunion}/C{course}/partants",
        f"https://turf-pmu.com/api/partants/R{reunion}C{course}" # URL de secours
    ]
    
    success = False
    for url in urls:
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
            response = requests.get(url, headers=headers, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                partants = []
                # Traitement des données
                for p in data.get('partants', []):
                    musique = p.get('musique', '')
                    forme = musique.count('1') + musique.count('2') + musique.count('3')
                    partants.append({
                        'N°': p.get('numPmu'),
                        'Nom': p.get('nom'),
                        'Cote': p.get('coteProbable', 0),
                        'Indice Forme': forme,
                        'Jockey': p.get('jockey'),
                        'Musique': musique
                    })
                
                st.success(f"✅ Données récupérées via : {url.split('/')[2]}")
                st.table(pd.DataFrame(partants))
                success = True
                break
        except:
            continue
            
    if not success:
        st.error("🚨 Le serveur Streamlit ne parvient pas à joindre le PMU. Solution : Essaye d'ouvrir cette même URL sur ton téléphone en 4G, si elle s'affiche, c'est que le site PMU est momentanément saturé.")
