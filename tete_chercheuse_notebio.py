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
affiliations_notesbio = pd.DataFrame(columns=[
    "IDU de l'article",
    "IDau notebio",
    "Contenu notebio",
    "IDau auteur",
    "Prénom",
    "Nom de famille",
    "Nom complet",
    "IDU affiliation reconstitué"])

# ne considérer que les dossiers dont le nom se trouve dans la liste
racine = Path("/home/adrien/Documents/erudit-affiliation-2025/erudit_data")
chemins_xml_sans_affiliation = [
    fichier for fichier in racine.rglob('*')
    if fichier.is_file() and fichier.parent.name in sample
]

# parser les documents XML pour récupérer ceux qui ont une balise notebio
xml_avec_notebio = []

ns = {'erudit': 'http://www.erudit.org/xsd/article'} # dictionnaire pour résoudre le namespace XML

for chemin in chemins_xml_sans_affiliation:
    article = ET.parse(chemin).getroot()
    notebios = article.findall(".//erudit:notebio", ns)
    for notebio in notebios:
        if notebio is not None and chemin not in xml_avec_notebio:
            xml_avec_notebio.append(chemin)

print(f"{len(xml_avec_notebio)} articles avec notices récupérés")

# récupérer les informations depuis le document XML
metadonnees_nb = {}

x = 1

for f in xml_avec_notebio:
    xml = ET.parse(f).getroot()
    for notebio in xml.findall(".//erudit:notebio", ns):
        # IDU article
        idar = xml.get('idproprio')
        metadonnees_nb["idar"] = idar
        # ID auteur·ice
        nb_id = notebio.get('idrefs')
        metadonnees_nb["idref"] = nb_id
        # texte de notebio
        # gestion des cas de notebio avec plusieurs paragraphes
        alinea = notebio.findall('.//erudit:alinea', ns)
        texte = []
        for a in alinea:
            texte.append(a.text)
        txtnotebio = ' '.join(texte)
        metadonnees_nb["notebio"] = txtnotebio
        # associer idref avec idauteur·ices
        autaires = xml.findall('.//erudit:auteur', ns)
        for autaire in autaires:
            au_id = autaire.get('id') # fonctionne pour obtenir l'id auteur tel que représenté dans la balise auteur
            if nb_id == au_id:
                prenom = xml.find('.//erudit:prenom', ns).text
                aut_nom = xml.find('.//erudit:autreprenom', ns)
                if aut_nom:
                    aut_nom = aut_nom.text
                nomfam = xml.find('.//erudit:nomfamille', ns).text
                metadonnees_nb.update({"idau": au_id, "prenom": prenom, "autreprenom": aut_nom, "nomfamille": nomfam})
        print(metadonnees_nb)
        print(f'Notice {idar}.{nb_id} complétée')
        # print(metadonnees_nb)