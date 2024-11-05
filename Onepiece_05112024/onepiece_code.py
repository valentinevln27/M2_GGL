# -*- coding: utf-8 -*-
"""
Created on Tue Nov  5 15:44:07 2024

@author: vanleene
"""  

import requests

#%%
# Définir le nombre de chapitres et de pages par chapitre à télécharger
start_chapter = 1
end_chapter = 5   # Définissez le dernier chapitre que vous voulez télécharger
max_pages = 100    # Nombre maximum de pages par chapitre

# Boucle sur les chapitres
for chapter in range(start_chapter, end_chapter + 1):
    # Boucle sur les pages dans chaque chapitre
    for j in range(1, max_pages + 1):
        # Formattage de j2 avec un zéro devant si nécessaire
        j2 = f'{j:02}'  # Formatage pour ajouter un zéro devant si nécessaire (par exemple, "01", "02", etc.)

        # URL corrigée avec les variables chapter et j2
        pic_url = f'https://www.scan-vf.net/uploads/manga/one_piece/chapters/chapitre-{chapter}/{j2}.webp'
        headers = {'user-agent': 'my-agent/1.0.1'}

        # Envoi de la requête pour télécharger l'image
        try:
            response = requests.get(pic_url, stream=True, headers=headers)
            if response.ok:
                # Sauvegarder l'image si la réponse est réussie
                with open(f'chapitre_{chapter}_page_{j2}.webp', 'wb') as f:
                    f.write(response.content)
                print(f"Image chapitre {chapter}, page {j2} téléchargée avec succès.")
            else:
                # Si la page n'existe pas, sortir de la boucle des pages pour ce chapitre
                print(f"Page {j2} du chapitre {chapter} non disponible, arrêt du téléchargement pour ce chapitre.")
                break
        except requests.exceptions.RequestException as e:
            print(f"Erreur de connexion pour le chapitre {chapter}, page {j2} : {e}")
            break

#%%
# Définir les chapitres et les pages par chapitre à générer dans le fichier HTML
start_chapter = 1
end_chapter = 5   # Dernier chapitre à inclure
max_pages = 100   # Nombre maximum de pages par chapitre

# Récupérer les pages disponibles pour chaque chapitre
chapters_data = {}  # Dictionnaire pour stocker les pages disponibles pour chaque chapitre
headers = {'user-agent': 'my-agent/1.0.1'}

for chapter in range(start_chapter, end_chapter + 1):
    chapters_data[chapter] = []
    for j in range(1, max_pages + 1):
        j2 = f'{j:02}'
        pic_url = f'https://www.scan-vf.net/uploads/manga/one_piece/chapters/chapitre-{chapter}/{j2}.webp'

        try:
            response = requests.head(pic_url, headers=headers)
            if response.status_code == 200:
                chapters_data[chapter].append(j2)
            else:
                break
        except requests.exceptions.RequestException as e:
            print(f"Erreur de connexion pour le chapitre {chapter}, page {j2} : {e}")
            break

# Générer la page HTML
with open("one_piece_navigation.html", "w", encoding="utf-8") as html_file:
    html_file.write("""
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Navigation One Piece</title>
    <style>
        .navigation {
            text-align: center;
            margin-top: 20px;
        }
        img {
            max-width: 100%;
            height: auto;
        }
    </style>
</head>
<body>
    <h1>One Piece - Navigation par Chapitre et Page</h1>
    <div class="navigation">
        <button id="prev-page" onclick="navigatePage(-1)">⬅️ Page Précédente</button>
        <button id="next-page" onclick="navigatePage(1)">Page Suivante ➡️</button>
    </div>
    <div class="navigation">
        <label for="chapter-select">Choisir un chapitre :</label>
        <select id="chapter-select" onchange="changeChapter()">
""")

    # Ajouter les options de chapitre dans le menu déroulant
    for chapter in range(start_chapter, end_chapter + 1):
        html_file.write(f'<option value="{chapter}">Chapitre {chapter}</option>\n')

    # Suite du code HTML pour l'image et les scripts JavaScript
    html_file.write("""
        </select>
    </div>
    <div class="navigation">
        <p id="page-info">Chapitre 1 - Page 01</p>
        <img id="manga-page" src="" alt="Page actuelle de One Piece">
    </div>
    <script>
        // Stocker les données des chapitres et des pages
        const chaptersData = """ + str(chapters_data) + """;

        let currentChapter = 1;
        let currentPageIndex = 0;

        // Charger la page d'image
        function loadPage() {
            const page = chaptersData[currentChapter][currentPageIndex];
            const imgUrl = `https://www.scan-vf.net/uploads/manga/one_piece/chapters/chapitre-${currentChapter}/${page}.webp`;
            document.getElementById("manga-page").src = imgUrl;

            // Mettre à jour le texte du numéro de chapitre et de page
            document.getElementById("page-info").textContent = `Chapitre ${currentChapter} - Page ${page}`;

            // Gérer l'état des boutons
            document.getElementById("prev-page").disabled = (currentPageIndex === 0);
            document.getElementById("next-page").disabled = (currentPageIndex === chaptersData[currentChapter].length - 1);
        }

        // Changer de page
        function navigatePage(direction) {
            currentPageIndex += direction;
            loadPage();
        }

        // Changer de chapitre
        function changeChapter() {
            currentChapter = parseInt(document.getElementById("chapter-select").value);
            currentPageIndex = 0;
            loadPage();
        }

        // Initialisation de la page
        document.getElementById("chapter-select").value = currentChapter;
        loadPage();
    </script>
</body>
</html>
""")

print("Le fichier HTML de navigation a été créé : one_piece_navigation.html")
