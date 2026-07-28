# préambule
from pathlib import Path
import pandas as pd
import xml.etree.ElementTree as ET
import csv

# stocker les id des articles dans une liste
# /!\ remplacer 'sample.csv' par la liste complète
df = pd.read_csv('sample.csv', names=['idar'])
articles = df['idar'].tolist()

# ne considérer que les dossiers dont le nom se trouve dans la liste
racine = Path("./erudit_data")

# dictionnaire pour résoudre le namespace XML
ns = {'erudit': 'http://www.erudit.org/xsd/article'}

def recuperer_xml_notebio(racine, articles):
    """Retourne une liste comprenant les chemins vers les documents XML
    qui contienent au moins une balise <notebio>.
    
    La variable "racine" passée à la fonction correspond au chemin de
    l'emplacement des dossiers à trier.
    La variable "articles" correspond à la liste d'ID uniques des articles
    sans affiliation candidats à l'extraction du contenu des balises notebio."""

    chemins_xml_sans_affiliation = [
        fichier for fichier in racine.rglob('*')
        if fichier.is_file() and fichier.parent.name in articles
    ]

    # parser les documents XML pour récupérer ceux qui ont une balise notebio
    ar_nb = []

    for chemin in chemins_xml_sans_affiliation:
        article = ET.parse(chemin).getroot()
        if article.findall(".//erudit:notebio", ns) and chemin not in ar_nb:
            ar_nb.append(chemin)
    return ar_nb

xml_avec_notebio = recuperer_xml_notebio(racine, articles)
print(f"{len(xml_avec_notebio)} articles avec notices récupérés.")

def texte_notebio(notice):
    """Concatène tous les paragraphes de la notice biobibliographique
    pour les regrouper dans un seul paragraphe suivi.
    
    La variable "notice" passée à la fonction correspond à l'élément XML
    contenant potentiellement plusieurs balises "alinea"."""

    alinea = notice.findall(".//erudit:alinea", ns)

    texte = []

    for a in alinea:
        texte.append(a.text)
    return ' '.join(texte)

def metadonnees_au(xml, idau):
    """Retourne les métadonnées des auteur·ices d'un article
    en fonction de leur index dans l'article (e.g. au1, au2, etc.).
    
    La variable "xml" passée à la fonction correspond à l'arborescence
    d'un document XML à examiner.
    La variable "idau" correspond à l'identifiant unique, extrait de la
    balise "idrefs" ou du contenu de l'attribut "id" de la balise "auteur"."""

    prenom = xml.find(".//*[@id='%s']//erudit:prenom" % idau, ns).text

    aut_nom = xml.find('.//erudit:autreprenom', ns)
    if aut_nom:
        aut_nom = aut_nom.text

    nomfam = xml.find(".//*[@id='%s']//erudit:nomfamille" % idau, ns).text

    return {
        "idau": idau,
        "prenom": prenom,
        "autreprenom": aut_nom if aut_nom is not None else None,
        "nomfamille": nomfam,
        "nomcomplet": f"{prenom} {nomfam}".strip(),
    }



# trouver textes notebio et metadonnées auteur
for chemin in xml_avec_notebio:
    xml = ET.parse(chemin).getroot()

    for nb in xml.findall(".//erudit:notebio", ns):
        nb_id = nb.get('idrefs')
        notebio = texte_notebio(nb)
        print(notebio)

        autaires = xml.findall('.//erudit:auteur', ns)

        for autaire in autaires:
            au_id = autaire.get('id')
            if nb_id == au_id:
                metadonnees = metadonnees_au(xml, au_id)
                print(metadonnees)

# # récupérer les informations depuis le document XML
# metadonnees_nb = {}

# with open('resultats.csv', 'w', newline='') as r:
#     colonnes = ['idar', 'idref', 'notebio', 'idau', 'prenom', 'autreprenom', 'nomfamille', 'nom_full', 'idu_nb']
#     scribe = csv.DictWriter(r, fieldnames=colonnes)
#     scribe.writeheader()          
#     for f in xml_avec_notebio:
#         xml = ET.parse(f).getroot()
#         for notebio in xml.findall(".//erudit:notebio", ns):
#             # IDU article
#             idar = xml.get('idproprio')
#             metadonnees_nb["idar"] = idar
#             # ID auteur·ice
#             nb_id = notebio.get('idrefs')
#             metadonnees_nb["idref"] = nb_id
#             # texte de notebio
#             # gestion des cas de notebio avec plusieurs paragraphes
#             alinea = notebio.findall('.//erudit:alinea', ns)
#             texte = []
#             for a in alinea:
#                 texte.append(a.text)
#             txtnotebio = ' '.join(texte)
#             metadonnees_nb["notebio"] = txtnotebio
#             # associer idref avec idauteur·ices
#             autaires = xml.findall('.//erudit:auteur', ns)
#             for autaire in autaires:
#                 au_id = autaire.get('id')
#                 if nb_id == au_id:
#                     prenom = xml.find(".//*[@id='%s']//erudit:prenom" % au_id, ns).text
#                     aut_nom = xml.find('.//erudit:autreprenom', ns)
#                     if aut_nom:
#                         aut_nom = aut_nom.text
#                     nomfam = xml.find(".//*[@id='%s']//erudit:nomfamille" % au_id, ns).text
#                     metadonnees_nb.update({"idau": au_id, "prenom": prenom, "autreprenom": aut_nom, "nomfamille": nomfam})
#             nomcomplet = prenom + ' ' + nomfam
#             metadonnees_nb["nom_full"] = nomcomplet
#             idu_nb = '.'.join([idar, nb_id, nomcomplet]) + '.1'
#             metadonnees_nb["idu_nb"] = idu_nb
#             scribe.writerow(metadonnees_nb)
#             print(f'Notice {idar}.{nb_id} complétée')