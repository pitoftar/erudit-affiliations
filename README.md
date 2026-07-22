### Préambule
Depuis peu, les affiliations institutionnelles des auteur·ice·s des articles publiés sur la plateforme [Érudit](https://www.erudit.org) sont associés à un identifiant pérenne [ROR](https://ror.org/).
Puisque les revues n'encodent pas elles-mêmes ces affiliations, la tâche de le faire revient à l'équipe d'Érudit.
À l'été 2025, un script Python a été développé par le stagiaire de l'EBSI et bibliothécaire Samuel Desnoyers pour effectuer une association entre les affiliations en plein texte extraites d'Érudit et un dictionnaire, constitué d'une version locale du ROR.
Ces associations fonctionnent sur une logique de _string-matching_ et récupèrent, si possible, un identifiant ROR à partir de l'affiliation en plein texte.
En raison de nombreux problèmes de désambiguisation, chacune de ces affiliations doit être validée manuellement.

Sur les ~9700 instance-auteur·ice[^1] extraites depuis la plateforme pour 2025, on dénombre près de 2000 cas où aucun identifiant pérenne ROR n'a été récupéré, entre autres parce qu'aucun string pour identifier l'affiliation n'a été produit lors de l'extraction.
Cela ne signifie pas pour autant que ces auteur·ice·s n'ont pas d'affiliation : il se pourrait que
1) celles-ci se trouvent dans le PDF et n'aient pas été balisées;
2) celles-ci se trouvent dans une affiliation en plein texte à même le document XML, potentiellement située dans une notice bibliographique balisée `notebio`;
3) celles-ci ont été extraites, mais le script n'a repéré aucun match dans le dictionnaire des institutions ROR.

Ce dépôt se veut un bac à sable afin de raffiner ce processus d'attribution des affiliations et de le rendre à la fois plus exhaustif et plus performant.

[^1]: On entend par une « instance-auteur·ice » que la plus petite unité est l'affiliation. On examine d'abord les articles, puis les auteur·ice, et enfin, les affiliations. Un·e auteur·ice peut avoir plus d'une affiliation, et apparaîtra donc plusieurs fois. Si l'auteur·ice n'a aucune affiliation indiquée sur l'article, une ligne vide lui sera tout de même consacrée dans le document.

