# Application de Matching Automatique de Factures

Ce projet vise à automatiser l’association des factures aux transactions bancaires à l’aide de l’OCR et du matching intelligent.

## Fonctionnalités
**Importation** : Relevés bancaires (CSV) & factures (JPG)
**Matching Intelligent** :Algorithme de correspondance basé sur des critères comme le montant, la date et le nom du marchand
**Interface** : Développement avec Streamlit
**Exportation** : Génération d’un fichier recapitulatif des associations trouvées

### Aspects Techniques
**lecture et Parsing des fichiers** : Lecture du relevé bancaire (CSV) avec pandas et Extraction de texte depuis les factures (JPG) avec Tesseract OCR
**Prétraitement des données** : Nettoyage des données extraites (normalisation des formats de date, montants, suppression des bruits textuels)
**Matching Algorithmique** : Utilisation d'un algorithme de fuzzy matching pour associer des valeurs similaires malgré des variations de format et 
la Comparaison des montants et des dates pour une correspondance optimale.
**Déploiement et Interface** : Développement de l'interface en Streamlit avec un hébergement sur Streamlit Cloud pour un accès facile.

## Instructions d'Utilisation
**Installer les dépendances** :'''bash 
pip install -r requirements.txt

## Technologies Utilisées  
- **Python** : Langage principal du projet 
- **Pandas** : Manipulation et analyse des données CSV
- **Pytesseract ** : Extraction du texte depuis les images de factures
- **Streamlit** : Création d’une interface utilisateur simple et efficace
- **Fuzzy Matching ** : Algorithme de correspondance des transactions

## Exemple d'utilisation  
Après avoir installé les dépendances, lancez l'application avec : '''bash
streamlit run app.py



## Conclusion 
Ce projet de matching automatique des factures avec un relevé bancaire vise à faciliter la gestion financière
en automatisant le rapprochement entre des transactions et leurs justificatifs.
Grâce à des technologies comme Streamlit pour l’interface utilisateur,
Pandas pour le traitement des données, et Pytesseract pour l’extraction de texte OCR,
l’application simplifie une tâche habituellement repetitif.

