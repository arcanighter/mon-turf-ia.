import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Turf-IA Connect", layout="wide")

st.title("🏇 Le Cœur du Réacteur - Analyse Automatique")

# Barre latérale pour choisir la course
with st.sidebar:
    st.header("Paramètres")
    date_pmu = st.text_input("Date (JJMMAAAA)", "30012026")
    reunion = st.number_input("Réunion (R)", min_value=1, max_value=10, value=3)
    course = st.number_input("Course (C)", min_value=1, max_value=20, value=6)
    btn_scan = st.button("🚀 LANCER LE SCAN")

if btn_scan:
    url = f"https://online.pmu.fr/stats/edito/pmu-infocentre/programme/{date_pmu}/R{reunion}/C{course}/partants"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    with st.spinner("Récupération des données PMU..."):
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                partants = []
                for p in data.get('partants', []):
                    musique = p.get('musique', '')
                    # Notre fameux Indice de Forme IA
                    forme = musique.count('1') + musique.count('2') + musique.count('3')
                    
                    partants.append({
                        'N°': p.get('numPmu'),
                        'Nom': p.get('nom'),
                        'Cote': p.get('coteProbable', 0),
                        'Indice Forme': forme,
                        'Jockey': p.get('jockey'),
                        'Musique': musique
                    })
                
                df = pd.DataFrame(partants)
                
                # --- AFFICHAGE DES SIGNAUX ---
                st.subheader(f"Analyse de la R{reunion}C{course}")
                
                # Mise en évidence de l'Edge
                def highlight_edge(row):
                    if row['Indice Forme'] >= 3 and row['Cote'] >= 10:
                        return ['background-color: #2ecc71'] * len(row)
                    return [''] * len(row)

                st.table(df.style.apply(highlight_edge, axis=1))
                
            else:
                st.error(f"Le serveur PMU a répondu avec une erreur {response.status_code}")
        except Exception as e:
            st.error(f"Erreur de connexion : {e}")
