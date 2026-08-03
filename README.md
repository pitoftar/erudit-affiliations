### Préambule

Depuis peu, les affiliations institutionnelles des auteur·ice·s des articles publiés sur la plateforme [Érudit](https://www.erudit.org) sont associés à un identifiant pérenne [ROR](https://ror.org/).
Puisque les revues n'encodent pas elles-mêmes ces affiliations, la tâche de le faire revient à l'équipe d'Érudit.

À l'été 2025, un [script Python](https://github.com/pitoftar/erudit-affiliation-2025/blob/master/detection_affiliation.ipynb) a été développé par le stagiaire de l'EBSI et bibliothécaire Samuel Desnoyers pour effectuer une association entre les affiliations en plein texte extraites d'Érudit et un dictionnaire, constitué d'une version locale du ROR.
Ces associations fonctionnent sur une logique de _string-matching_ et récupèrent, si possible, un identifiant ROR à partir de l'affiliation en plein texte.
En raison de nombreux problèmes de désambiguisation, chacune de ces affiliations doit être validée manuellement.

Sur les ~9700 instance-auteur·ice[^1] extraites depuis la plateforme pour 2025, on dénombre près de 2000 cas où aucun identifiant pérenne ROR n'a été récupéré, entre autres parce qu'aucun string pour identifier l'affiliation n'a été produit lors de l'extraction.
Cela ne signifie pas pour autant que ces auteur·ice·s n'ont pas d'affiliation : il se pourrait que
1) celles-ci se trouvent dans le PDF et n'aient pas été balisées;
2) celles-ci ont été extraites, mais le script n'a repéré aucun match dans le dictionnaire des institutions ROR;
3) celles-ci se trouvent dans une affiliation en plein texte à même le document XML, potentiellement située dans une notice bibliographique balisée `notebio`.

Ce dépôt se veut un bac à sable afin de raffiner ce processus d'attribution des affiliations et de le rendre à la fois plus exhaustif et plus performant.

[^1]: On entend par une « instance-auteur·ice » que la plus petite unité répertoriée et non-dupliquée est l'affiliation. On examine d'abord les articles, puis les auteur·ice, et enfin, les affiliations. Un·e auteur·ice peut avoir plus d'une affiliation, et apparaîtra donc plusieurs fois. Si l'auteur·ice n'a aucune affiliation indiquée sur l'article, une ligne vide lui sera tout de même consacrée dans le document. Cela signifie que chaque article peut apparaître plusieurs fois, et que chaque auteur·ice peut apparaître plusieurs fois (pour plusieurs affiliations pour un même article ou pour plusieurs articles). Chaque affiliation, telle qu'elle a été inscrite par l'auteur·ice sur un article donné, n'apparaît qu'une fois. Chacune est représentée par un identifiant unique, structuré comme suit : `no_article.no_auteur.nom_auteur.index_affiliation`.

## Pragmatique

À prime abord, les deux premiers cas documentés dans le [préambule](https://github.com/pitoftar/erudit-affiliation-2025/tree/master#pr%C3%A9ambule) ne présentent pas de solution évidente.

Dans la première situation, il n'y a d'autre choix que de vérifier un par un des PDFs des articles concernés.
Un certain prétraitement pourrait être envisagé au niveau de la revue éventuellement, mais la validation manuelle semble, pour l'instant, incontournable.

Dans la deuxième situation, un travail pourrait être envisagé pour que le script incorpore des cas limites ou fonctionne avec un intervalle de confiance.
On pourrait, par exemple, imaginer un premier tri où certaines affiliations seraient indiquées comme étant à valider, et d'autres seraient indiquées comme étant relativement fiables.
Par exemple, un string présentant une correspondance exacte avec une institution non-ambiguë n'aurait pas besoin d'être validé, mais un cas comme « Ministère de la santé » ou « Hôpital Hôtel-Dieu » serait marqué comme devant être revu.
Cependant, dans ce cas aussi, la validation manuelle semble difficilement évitable.

En revanche, dans le troisième cas, il est relativement évident d'identifier la présence ou l'absence d'une balise `notebio` dans le XML.
La balise peut ensuite être extraite en plein texte.
En raison de leur structure hétérogène et de l'absence de standardisation autour de la rédaction des notice biobibliographiques, il n'est pas possible d'associer des identifiants pérennes à celles-ci de manière automatique.
Une fois la balise identifiée, une validation demeure nécessaire afin d'identifier l'affiliation actuelle de l'auteur·ice[^2].

[^2]: Des grands modèles de langage seraient potentiellement en mesure de prendre en charge cette classification et pourraient donc être envisagés pour cette tâche.

### Nous avons

- Un dump du contenu, balisé en XML, de tous les articles parus sur Érudit entre 2023 et 2025 (récupérable à partir de [https://redevance.erudit.org](https://redevance.erudit.org))
- Une liste de toutes les [instances-auteur·ice](https://docs.google.com/spreadsheets/d/1zezZNg5HjF7R-d47UakkZSSYIgwduwd4/edit?gid=2144806381#gid=2144806381)[^3] des articles parus en 2025
- Une liste (dans un fichier csv) des ID articles uniques pour lesquels le champ `author_affiliation_content` est vide (n = 883)

[^3]: Lien externe vers un Google Sheets privé.

### Nous voulons

- Une sortie minimalement structurée avec, sur chaque ligne/pour chaque objet
	- l'IDU de l'article (e.g. `1100000ar`)
	- le nom de l'auteur·ice concerné·e (e.g. `Simon van Bellen`)
	- un concat de l'ID de l'auteur·ice concerné·e (`au1`) et de l'ID de l'article (e.g. `1100000ar.au1`)
	- le texte complet de la notice bibliographique associée
	- une tentative de regénération de l'IDU des instances-auteur·ice dans `affiliations_standardisées_2025`[^1]

### Nous devons

1) Ne considérer que les documents XML dont l'attribut `idproprio` de la balise `<article>` est un match exact avec l'ID de l'un des articles pour lequel le champ `author_affiliation_content` est vide
2) Parmi ces documents XML, ne retenir que ceux qui contiennent une balise `<notebio>`
3) Récupérer le contenu des balises `<prenom>` et `<nomfamille>` dont l'attribut `id` de la balise parent `auteur` correspond à l'attribut `idrefs` de chaque balise `<notebio>`
4) Récupérer le contenu textuel de la balise `<notebio>`
5) Inscrire les informations dans un fichier csv ligne par ligne

## Pratique

### Pile logicielle

- Python 3
- Module `xml.etree.ElementTree`
    - 📄 [Documentation](https://docs.python.org/3/library/xml.etree.elementtree.html)
    - ℹ️ [Information sur les différents parsers](https://realpython.com/python-xml-parser/#learn-about-xml-parsers-in-pythons-standard-library)
- Librairie `pathlib`
- Librairie `csv`
- Librairie `pandas`

### Étapes

#### Identifier les XML d'articles sans affiliations

Fonction `recuperer_xml_notebio()`

- Stocker les IDU dans une liste
- Vérifier si chaque titre de dossier correspond exactement à un élément qui se trouve dans la liste
- Créer une liste des fichiers à examiner
- Parser les fichiers
- Créer une liste de fichiers qui comportent la balise `notebio`
- Ajouter le chemin vers ce fichier dans une liste

### Récupérer le texte des notices

Fonction `texte_notebio()`

- Parcourir chacune des notices
- Extraire le texte en tenant compte du fait
	- qu'une même notice peut avoir plusieurs paragraphes
	- que tout le texte n'est pas nécessairement l'enfant direct de la balise `alinea`, puisqu'elle contient parfois d'autres balises (p. ex. `marquage`) qui peuvent elles-mêmes contenir du texte

#### Extraire le nom des auteur·ice à partir de leur index dans l'article

Fonction `metadonnees_au()`

Pour chaque `notebio`

- Identifier la valeur de la variable `idrefs` dans la balise `notebio`
- Passer la valeur de la variable `idrefs` à la fonction
- Trouver la valeur de la variable `id` dans la balise `auteur` qui constitue un **match exact** avec `idrefs`
- Extraire le texte balisé par `prenom`, `autreprenom` et `nomfamille`
	- 📝 N.B.: Même si le contenu de la balise `autreprenom` n'est généralement pas identifiée dans le document d'attribution, j'ai choisi de l'inclure puisqu'il peut faciliter la recherche d'individus dont il faut valider manuellement l'affiliation
- Stocker le texte dans un dictionnaire si ces variables sont présentes

#### Extraire les métadonnées complètes pour chaque document XML

Fonction `metadonnees_completes()`

- Extraire l'identifiant unique de chaque article à partir de l'attribut `idproprio`
- Pour chaque notebio, extraire le contenu de la balise `idrefs`
- Pour chaque notebio, extraire le contenu textuel
- Pour chaque notebio, extraire les métadonnées de l'auteur·ice
- Stocker les informations dans un dictionnaire

#### Inscrire les informations dans un fichier csv

Pour chaque `notebio`

- Inscrire les informations dans un fichier csv, ligne par ligne
	- IDU de l'article
	- IDU + Référence auteurice (notebio)
	- Contenu notebio
	- IDU + Référence auteurice (auteur)
	- Prénom auteurice
	- Nom famille auteurice
	- Nom complet
	- IDU + Référence auteurice (notebio) + nom complet + `.1`

## Quelques problèmes connus

- Certains articles ne retournent ni valeur pour la balise `idrefs` ni prénom, ni nom de famille. Ces deux dernières informations sont pourtant présentes dans les fichiers XML. C'est par exemple le cas de l'article [1118513ar](https://www.erudit.org/fr/revues/archivaria/2025-n99-archivaria010099/1118513ar.xml), seulement pour la cinquième autrice (Karen Suurtamm) ou de l'article [1117727ar](https://www.erudit.org/fr/revues/possibles/2025-v49-n1-possibles010004/1117727ar.xml). Le problème semble être lié à l'absence d'une balise `idrefs` dans `notebio` : ces dernières sont alors seulement identifiées par une balise `id`. Il faudrait trouver un moyen de contourner le problème en extrayant aussi les prénoms et noms de famille même si la balise `idrefs` est absente. Le vol. 49 n°1 (printemps 2025) de la revue _Possibles_ semble particulièrement concerné, ainsi que le n°12 de la revue _MuseMedusa_.
- Certains articles formulent des notices communes pour tous·tes leurs auteur·ices. C'est par exemple le cas de [1121908ar](https://www.erudit.org/fr/revues/jssac/2024-v49-n2-jssac010441/1121908ar.xml). Dans ce cas, l'identifiant unique reconstitué (p. ex. `1121908ar.au1 au2 au3 au4 au5.None None.1`) ne correspond pas à celui extrait dans le document d'attribution (p. ex. `1121908ar.au1.Michael Windover.1`). Cette différence s'explique puisque le présent script se base d'abord sur l'`idref` de la notice pour construire l'identifiant unique, alors que le premier script se base (je suppose) sur la valeur de l'attribut `id` de la balise `auteur`.
- À [au moins une occasion](https://www.erudit.org/fr/revues/memoires/2025-v16-n2-memoires010471/1122239ar.xml), deux co-auteur·ices ont vu leurs notices biobibliographiques être inversées dans l'extraction. Cela s'explique puisque les balises `notebio` faisaient référence au mauvais index comparativement à la balise `auteur`. Les coquilles de ce genre devront probablement être signalées à et corrigées par l'équipe de prod.