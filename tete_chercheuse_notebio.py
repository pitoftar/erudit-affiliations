# préambule
from pathlib import Path
import pandas as pd
import xml.etree.ElementTree as ET
import csv

# stocker les id des articles dans une liste
# /!\ remplacer 'sample' par la liste complète au moment d'exécuter le vrai script
df = pd.read_csv('sample.csv', names=['idar'])
sample = df['idar'].tolist()

# créer le jeu de données pour stocker les informations
affiliations_notesbio = pd.DataFrame(columns=["IDU de l'article", "IDau notebio", "Contenu notebio", "IDau auteur", "Prénom", "Nom de famille", "Nom complet", "IDU reconstitué"])

# ne considérer que les dossiers dont le nom se trouve dans la liste
racine = Path("/home/adrien/Documents/erudit-affiliation-2025/xml_pour_notebio")
chemins_xml_sans_affiliation = [
    fichier for fichier in racine.rglob('*')
    if fichier.is_file() and fichier.parent.name in sample
]

# parser les documents XML pour récupérer ceux qui ont une balise notebio

xml_avec_notebio = []

for chemin in chemins_xml_sans_affiliation:
    article = ET.parse(chemin).getroot()
    for child in article.iter():
        if child.attrib:
            print(f"Tag: {child.tag} | Attributes: {child.attrib}") # imprime tous les éléments (n=2293)
