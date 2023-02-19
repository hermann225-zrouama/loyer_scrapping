import pandas as pd
from dotenv import load_dotenv, dotenv_values
import spacy
from art import *


load_dotenv()
config = dotenv_values(".env")

class Scrapinator:
    def __init__(self, zone: list,nb_page_google: int, nb_page_fb_group: int):
        tprint("SCRAPINATOR")
        print("\nBienvenue dans Scrapinator, le scraper de groupes Facebook pour la récupération d'infos sur les maisons en location!")
        if len(zone) != 2:
            raise ValueError("L'argument zone doit être une liste de 2 éléments")
        self.zone = zone
        self.nb_page_google = nb_page_google
        self.nb_page_fb_group = nb_page_fb_group
        self.scrapping_results = {
            "loyer": None,
            "nombre_piece": None,
            "annee_publication": None,
            "jour_publication": None,
            "mois_publication": None,
            "type_logement": None,
            "standing": None,
            "commune": None,
            "quartier": None,
            "nb_loyer": None,
            "lien": None,
        }

    def extract_features(self,post_text):
        """Extrait les informations pertinentes d'un texte de publication.

        Args:
            post_text (dict): Un dictionnaire avec les clés "texte", "date" et "lien",
                            qui représentent le texte de la publication, la date de
                            publication et le lien de la publication.
            COMMUNE (str): Le nom de la commune associée à la publication.

        Returns:
            dict: Un dictionnaire avec les informations suivantes :
                - "loyer": le montant du loyer en FCFA, extrait du texte de la publication.
                - "nombre_piece": le nombre de pièces du logement, extrait du texte de la publication.
                - "annee_publication": l'année de publication de la publication.
                - "jour_publication": le jour de publication de la publication.
                - "mois_publication": le mois de publication de la publication.
                - "type_logement": le type de logement (immeuble ou appartement) extrait du texte de la publication.
                - "standing": None (non utilisé).
                - "commune": Le nom de la commune associée à la publication.
                - "quartier": None (non utilisé).
                - "nb_loyer": None (non utilisé).
                - "lien": le lien de la publication.
        """
        self.scrapping_results = {
            "loyer": None,
            "nombre_piece": None,
            "annee_publication": None,
            "jour_publication": None,
            "mois_publication": None,
            "type_logement": None,
            "standing": None,
            "commune": None,
            "quartier": None,
            "nb_loyer": None,
            "lien": None,
        }

        # Conversion post_text en dataframe
        post_df = pd.DataFrame(post_text.apply(pd.Series))

        # Si le post est nan on retourne un dictionnaire vide
        if pd.isna(post_df.iloc[0, 0]):
            return self.scrapping_results

        # EXTRACTION LOYER & NOMBRE DE PIECES
        nlp = spacy.load("fr_core_news_sm")
        post_text = {"texte": post_df.iloc[0, 0], "date": post_df.iloc[1, 0]}
        doc = nlp(post_text["texte"])
        self.scrapping_results["lien"] = post_df.iloc[2, 0]
        # self.scrapping_results["commune"] = self.zone

        try:
            for i, token in enumerate(doc):
                if token.text.endswith("fr") or token.text.endswith("f") or token.text.endswith("0"):
                    self.scrapping_results["loyer"] = token.text
                    break
                elif token.text.lower() == "loyer":
                    next_token = doc[i + 1] if i + 1 < len(doc) else None
                    while next_token and not next_token.like_num:
                        i += 1
                        next_token = doc[i + 1] if i + 1 < len(doc) else None
                    if next_token and next_token.like_num:
                        self.scrapping_results["loyer"] = next_token.text
                        break
        except:
            pass

        try:
            l = [t for t in doc if 'pièces' in t.text.lower() and t.pos_ == "NOUN"]

            if l:
                term = l[0]
                subtree = [t for t in term.subtree]
                pieces = [t for t in subtree if t.text.lower() == "pièces" or t.text.lower() == "fr cfa" or t.text.lower() == "franc cfa" or t.text.lower() == "francs cfa" or t.text.lower() == "francs cfa"]
                if pieces:
                    nb_piece = pieces[0].nbor(-1)
                    if nb_piece.like_num == True:
                        self.scrapping_results["nombre_piece"] = nb_piece.text
        except:
            pass

        # EXTRACTION ANNEE, MOIS, JOUR
        try:
            annee, mois, jour = post_text["date"].split(" ")[0].split("-")
            self.scrapping_results["annee_publication"] = annee
            self.scrapping_results["mois_publication"] = mois
            self.scrapping_results["jour_publication"] = jour
        except:
            pass

        # EXTRACTION TYPE DE LOGEMENT
        try:
            for i, token in enumerate(doc):
                if token.text.lower() == "immeuble" or token.text.lower() == "étage":
                    self.scrapping_results["type_logement"] = "immeuble"
                    break
                elif token.text.lower() == "maison":
                    self.scrapping_results["type_logement"] = "appartement"
                    break
        except:
            pass

        # EXTRACTION ZONE
        try:
            for i, token in enumerate(doc):
                if token.text.lower() in self.zone:
                    # recupere la position de la valeur du tableau self.zone qui correspond au token.text.lower()
                    index = self.zone.index(token.text.lower())
                    self.scrapping_results["commune"] = self.zone[index]

                    break
        except:
            pass

        # EXTRACTION DU STANDING
        try:
            for i, token in enumerate(doc):
                if token.text.lower() == "haut standing":
                    self.scrapping_results["standing"] = token.text
                    break
        except:
            pass    
        return self.scrapping_results

    def transformer(self):
        """
        Cette fonction extrait des fonctionnalités à partir de données de posts Facebook et enregistre les résultats dans un fichier CSV.

        Args:
            None

        Returns:
            None: Enregistre la sortie dans un fichier CSV.
        """
        tprint("transformator")
        print("\nTransformation des données en cours...")
        # Partie 2 : Traitement des données
        data = pd.read_csv("data/output.csv")
        data = data[['post_text', 'time', 'post_url']]
        data.head()

        # Appliquer la fonction extract_features sur chaque ligne du dataframe data et créer un nouveau dataframe avec les résultats
        self.data_features = data.apply(self.extract_features, axis=1)
        self.data_features = pd.DataFrame(self.data_features.apply(pd.Series))
        print("Dimensions du dataframe : ")
        print(self.data_features.shape)
        self.data_features.to_csv("data/resultat.csv", index=False, encoding="utf-8",)
        self.data_features.head(50)
        return self.data_features


