import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import streamlit as st

def download_images_from_url(url, download_folder):
    # Überprüfen, ob der Ordner existiert, andernfalls erstellen
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    # Anforderung an die Webseite senden
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        st.error(f'Fehler beim Abrufen der Webseite {url}: {e}')
        return

    # BeautifulSoup verwenden, um den HTML-Inhalt zu analysieren
    soup = BeautifulSoup(response.text, 'html.parser')

    # Alle Bilder mit dem Tag 'img' finden
    img_tags = soup.find_all('img')

    # Alle Bild-URLs sammeln und nur die gewünschten herunterladen
    for img_tag in img_tags:
        img_url = img_tag.get('src')

        # Manchmal sind die URLs relativ, also müssen wir sie absolut machen
        img_url = urljoin(url, img_url)

        # Den Dateinamen aus der URL extrahieren
        img_name = os.path.basename(img_url)

        # Prüfen, ob der Dateiname mit 'il_794xN' beginnt und die Datei eine .jpg-Datei ist
        if img_name.startswith('il_794xN') and img_name.lower().endswith('.jpg'):
            # Den vollständigen Pfad für den Download erstellen
            download_path = os.path.join(download_folder, img_name)

            # Das Bild herunterladen und speichern
            try:
                img_data = requests.get(img_url).content
                with open(download_path, 'wb') as img_file:
                    img_file.write(img_data)

                st.success(f'{img_name} wurde heruntergeladen.')
            except requests.exceptions.RequestException as e:
                st.error(f'Fehler beim Herunterladen von {img_name}: {e}')

# Streamlit App
st.title('Web Scraper für Bilder')

# Benutzer nach einer Liste von URLs fragen
urls_to_scrape = st.text_area('Bitte geben Sie eine Liste von URLs ein (jede URL in einer neuen Zeile):', height=200)

# Benutzer nach dem Download-Ordner fragen oder einen Standard verwenden
download_folder = st.text_input('Bitte geben Sie den Pfad zum Download-Ordner ein (oder leer lassen für "downloaded_images"):')
if not download_folder:
    download_folder = 'downloaded_images'

# Button zum Starten des Downloads
if st.button('Bilder herunterladen'):
    st.info(f'Der Download wird gestartet. Bitte warten...')

    # Die eingegebenen URLs in eine Liste aufteilen
    urls_list = urls_to_scrape.split('\n')

    # Für jede URL den Download durchführen
    for url in urls_list:
        download_images_from_url(url.strip(), download_folder)

    st.success('Der Download wurde abgeschlossen.')

# Schaltfläche zum Löschen der eingegebenen URLs
if st.button('Eingegebene URLs löschen'):
    st.text_area('Bitte geben Sie eine Liste von URLs ein (jede URL in einer neuen Zeile):', value='')

# Optional: Anzeige der heruntergeladenen Bilder im Download-Ordner
if st.checkbox('Anzeigen der heruntergeladenen Bilder im Download-Ordner'):
    downloaded_images = os.listdir(download_folder)
    st.write(downloaded_images)
