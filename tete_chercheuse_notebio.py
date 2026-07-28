# préambule
from pathlib import Path
import pandas as pd
import xml.etree.ElementTree as ET
import csv
from datetime import datetime

# stocker les id des articles dans une liste
# /!\ remplacer 'sample.csv' par la liste complète
df = pd.read_csv('articles_affiliations_vides.csv', names=['idar'])
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
    sans affiliation candidats à l'extraction du contenu des balises notebio.
    """

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
    contenant potentiellement plusieurs balises "alinea".
    """

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
    balise "idrefs" ou du contenu de l'attribut "id" de la balise "auteur".
    """

    prenom = xml.find(".//*[@id='%s']/nompers/erudit:prenom" % idau, ns)
    if prenom is not None:
        prenom = prenom.text

    aut_nom = xml.find('./nompers/erudit:autreprenom', ns)
    if aut_nom is not None:
        aut_nom = aut_nom.text

    nomfam = xml.find(".//*[@id='%s']/nompers/erudit:nomfamille" % idau, ns)
    if nomfam is not None:
        nomfam = nomfam.text

    return {
        "idau": idau,
        "prenom": prenom if prenom is not None else None,
        "autreprenom": aut_nom if aut_nom is not None else None,
        "nomfamille": nomfam if nomfam is not None else None,
        "nomcomplet": f"{prenom} {nomfam}".strip(),
    }

def metadonnees_completes(xml, notice, idar):
    """Retourne un dictionnaire avec les métadonnées complètes
    pour chaque balise "notebio".
    
    La variable "xml" passée à la fonction correspond à l'arborescence
    complète d'un document XML à examiner.
    La variable "notice" correspond à une balise "notebio" trouvée dans
    l'arborescence XML.
    La variable "idar" correspond à l'identifiant unique de l'article tel
    qu'identifié par la valeur de l'attribut "idproprio" de la balise
    englobante "article".
    """

    nb_id = notice.get('idrefs')
    notebio = texte_notebio(notice)
    autaire = metadonnees_au(xml, nb_id)
    nomcomplet = autaire.get("nomcomplet")

    return {
        "idar": idar,
        "idref": nb_id,
        "notebio": notebio,
        "idu_nb": f"{idar}.{nb_id}.{nomcomplet}.1",
        **autaire,
    }

colonnes = ['idar', 'idref', 'notebio', 'idau', 'prenom', 'autreprenom', 'nomfamille', 'nomcomplet', 'idu_nb']

maintenant = datetime.now().strftime("%Y%m%d-%H%M%S")

with open(f'out/{maintenant}_resultats.csv', 'w', newline='') as r:
    scribe = csv.DictWriter(r, fieldnames=colonnes)
    scribe.writeheader()

    for chemin in xml_avec_notebio:
        xml = ET.parse(chemin).getroot()
        idar = xml.get('idproprio')

        for notebio in xml.findall('.//erudit:notebio', ns):
            print(f'En train de travailler sur {idar}.')
            metadonnees = metadonnees_completes(xml, notebio, idar)
            scribe.writerow(metadonnees)
            print(f'Notice {idar}.{metadonnees['idref']} complétée')