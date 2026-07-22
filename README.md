### Préambule

Depuis peu, les affiliations institutionnelles des auteur·ice·s des articles publiés sur la plateforme [Érudit](https://www.erudit.org) sont associés à un identifiant pérenne [ROR](https://ror.org/).
Puisque les revues n'encodent pas elles-mêmes ces affiliations, la tâche de le faire revient à l'équipe d'Érudit.

À l'été 2025, un (script Python)[https://github.com/pitoftar/erudit-affiliation-2025/blob/master/detection_affiliation.ipynb] a été développé par le stagiaire de l'EBSI et bibliothécaire Samuel Desnoyers pour effectuer une association entre les affiliations en plein texte extraites d'Érudit et un dictionnaire, constitué d'une version locale du ROR.
Ces associations fonctionnent sur une logique de _string-matching_ et récupèrent, si possible, un identifiant ROR à partir de l'affiliation en plein texte.
En raison de nombreux problèmes de désambiguisation, chacune de ces affiliations doit être validée manuellement.

Sur les ~9700 instance-auteur·ice[^1] extraites depuis la plateforme pour 2025, on dénombre près de 2000 cas où aucun identifiant pérenne ROR n'a été récupéré, entre autres parce qu'aucun string pour identifier l'affiliation n'a été produit lors de l'extraction.
Cela ne signifie pas pour autant que ces auteur·ice·s n'ont pas d'affiliation : il se pourrait que
1) celles-ci se trouvent dans le PDF et n'aient pas été balisées;
2) celles-ci ont été extraites, mais le script n'a repéré aucun match dans le dictionnaire des institutions ROR;
3) celles-ci se trouvent dans une affiliation en plein texte à même le document XML, potentiellement située dans une notice bibliographique balisée `notebio`.

Ce dépôt se veut un bac à sable afin de raffiner ce processus d'attribution des affiliations et de le rendre à la fois plus exhaustif et plus performant.

[^1]: On entend par une « instance-auteur·ice » que la plus petite unité répertoriée et non-dupliquée est l'affiliation. On examine d'abord les articles, puis les auteur·ice, et enfin, les affiliations. Un·e auteur·ice peut avoir plus d'une affiliation, et apparaîtra donc plusieurs fois. Si l'auteur·ice n'a aucune affiliation indiquée sur l'article, une ligne vide lui sera tout de même consacrée dans le document.

## Pragmatique

Les deux premiers cas documentés dans le [[#Préambule|préambule]] ne présentent pas de solution évidente.

Dans la première situation, il n'y a d'autre choix que de vérifier un par un des PDFs des articles concernés.
Un certain prétraitement pourrait être envisagé au niveau de la revue éventuellement, mais la validation manuelle semble, pour l'instant, incontournable.

Dans la deuxième situation, un travail pourrait être envisagé pour que le script incorpore des cas limites ou fonctionne avec un intervale de confiance.
Cependant, dans ce cas aussi, la validation manuelle semble difficilement évitable.

En revanche, dans le troisième cas, il est relativement évident d'identifier la présence ou l'absence d'une balise `notebio` dans le XML.
En raison de leur structure hétérogène et de l'absence de standardisation autour de la rédaction des notice biobibliographiques, il n'est pas possible d'associer des identifiants pérennes à celles-ci.
Une fois la balise identifiée, une validation demeure nécessaire afin d'identifier l'affiliation actuelle de l'auteur·ice[^2].

[^2]: Des grands modèles de langage pourraient être en mesure de prendre en charge cette classification et pourraient donc être envisagés pour cette tâche. 