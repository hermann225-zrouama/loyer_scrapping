# Projet Scrapinator

Le projet Scrapinator est un outil de web scraping qui permet d'extraire des données à partir de pages web (facebook). Le projet est organisé en plusieurs dossiers, chacun ayant une fonction spécifique.

# AVANT TOUTE CHOSE VEUILLEZ INSTALLER CORRECTEMENT TENSORFLOW POUR LE BON FONCTIONNEMENT DU PACKAGE *SPACY*

## Fonctionnalités

- Scrapping des infos de location en fonction de deux localités au choix de l'utilisateur
- Extraction des informations et traitements des données scrappées
- Création d'un fichier csv contenant les informations scrappées
- Description des données scrappées

## Arborescence du projet

project/
├── data/
├── docs/
│   ├── utilisation.md
├── notebooks/
│   ├── installer.ipynb
├── scripts/
│   ├── core.py
├── extraction_script.py
├── scrapinator.py
├── readme.md
├── cookies.txt

- Le dossier data contient les données extraites à partir des pages web. Les fichiers dans ce dossier sont générés par le script d'extraction.

- Le dossier docs contient la documentation du projet, en particulier le fichier utilisation.md qui décrit comment utiliser l'outil Scrapinator.

- Le dossier notebooks contient le notebook scrapinator.ipynb, qui est un exemple d'utilisation de l'outil Scrapinator.

- Le dossier scripts contient les scripts principaux du projet, notamment core.py, qui contient la logique de l'outil, et installer.py, qui permet d'installer les dépendances nécessaires.

- Le fichier extraction_script.py est un script qui permet d'extraire des données à partir d'une page web en utilisant l'outil Scrapinator.

- Le fichier scrapinator.py est le fichier principal qui importe et exécute les fonctions définies dans le script core.py.

- Le fichier README.md est le fichier que vous lisez actuellement, il décrit l'arborescence du projet et son contenu.

Ce projet est à des fins pédagogiques uniquement et ne doit pas être utilisé à des fins malveillantes.