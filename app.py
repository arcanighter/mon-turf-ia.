import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Turf-IA Cloud", layout="wide")
st.title("🏇 Le Cœur du Réacteur - Cloud Edition")

# --- INTERFACE ---
with st.sidebar:
    st.header("Configuration")
    date_pmu = st.text_input("Date (JJMMAAAA)", "30012026")
    reunion = st.number_input("Réunion (R)", 1, 10, 3)
    course = st.number_input("Course (C)", 1, 20, 6)
    btn_scan = st.button("🚀 LANCER L'ANALYSE")

# --- MOTEUR DE RECHERCHE DE DONNÉES ---
if btn_scan:
    # Liste de sources alternatives pour contourner les blocages DNS
    sources = [
        f"https://online.pmu.fr/stats/edito/pmu-infocentre/programme/{date_pmu}/R{reunion}/C{course}/partants",
        f"https://pt-api.pronostic-turfiste.fr/api/partants/R{reunion}C{course}"
    ]
    
    data_found = False
    
    for url in sources:
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            response = requests.get(url, headers=headers, timeout=8)
            
            if response.status_code == 200:
                raw_data = response.json()
                
                # Adaptation selon la source (PMU ou alternative)
                partants_raw = raw_data.get('partants', [])
                processed_data = []
                
                for p in partants_raw:
                    musique = p.get('musique', '')
                    # Calcul de l'Indice Forme (Podiums 1-2-3)
                    forme = musique.count('1') + musique.count('2') + musique.count('3')
                    
                    processed_data.append({
                        'N°': p.get('numPmu') or p.get('num'),
                        'Nom': p.get('nom'),
                        'Cote': p.get('coteProbable', 0),
                        'Forme': forme,
                        'Jockey': p.get('jockey'),
                        'Musique': musique
                    })
                
                if processed_data:
                    df = pd.DataFrame(processed_data)
                    st.success(f"✅ Données récupérées avec succès !")
                    
                    # Mise en évidence de l'Edge (Cote > 10 et Forme > 2)
                    st.dataframe(df.sort_values('N°').style.highlight_max(subset=['Forme'], color='#2ecc71'))
                    data_found = True
                    break
        except Exception as e:
            continue

    if not data_found:
        st.error("🚨 Blocage persistant. Le serveur PMU est inaccessible depuis cette zone.")
        st.info("💡 Solution de secours : Copie-colle la liste des partants ici, et je l'analyserai pour toi instantanément.")
