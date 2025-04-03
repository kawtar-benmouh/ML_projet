# Matching Automatique de Factures à un Relevé Bancaire

## Description du Projet
Ce projet vise à automatiser le **matching** entre des factures numérisées et les transactions bancaires correspondantes. Grâce à l'utilisation de **PixTral** et d'algorithmes de **matching textuel**, le système identifie et associe les transactions de manière efficace.

## Fonctionnalités Principales
- Extraction des informations de factures (montant, date, fournisseur) via **PixTral**.
- Chargement et analyse des transactions bancaires à partir d'un fichier CSV.
- Algorithme de **matching intelligent** basé sur la similarité des données.
- Interface utilisateur développée avec **Streamlit**.

## Technologies Utilisées
- **Python** : Langage principal du projet
- **Pandas** : Manipulation et analyse des données CSV
- **PixTral** : Extraction du texte depuis les images de factures
- **Streamlit** : Création d’une interface utilisateur simple et efficace
- **Fuzzy Matching (FuzzyWuzzy ou RapidFuzz)** : Algorithme de correspondance des transactions

## Installation et Utilisation
### 1. Cloner le dépôt
```bash
git clone https://github.com/kawtar-benmouh/ML_projet.git
cd ML_projet
```

### 2. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 3. Lancer l'application
```bash
streamlit run app.py
```

## Stratégie de Matching
L’algorithme de matching repose sur plusieurs critères :
- **Montant** : Vérification de l’égalité ou d’une marge d’erreur acceptable.
- **Date** : Correspondance exacte ou rapprochée.
- **Nom du fournisseur** : Matching basé sur la similarité textuelle.
- **Références de facture** : Extraction et comparaison si disponibles.

## Évaluation des Performances
Afin de mesurer l’efficacité du matching entre les factures et les transactions bancaires, 
nous utilisons la **métrique de rappel (Recall)**. Cette métrique permet d’évaluer la capacité du modèle à retrouver toutes les correspondances correctes.

### Formule du Recall
Le Recall est défini comme suit :
```math
Recall = \frac{TP}{TP + FN}
```
- **TP (True Positives)** : Une transaction du relevé bancaire est correctement associée à la bonne facture.
- **FN (False Negatives)** : Une transaction avait une facture correspondante, mais l’algorithme ne l’a pas détectée.
- **FP (False Positive )** : L’algorithme a associé une transaction à une facture erronée.
- **TN (True Negative )** : Aucune facture ne correspond à une transaction, et l’algorithme n’a pas fait d’association incorrecte.

### Analyse
- Un **Recall élevé** signifie que la majorité des factures ont bien été appariées avec leurs transactions correspondantes.
- Un **Recall faible** indique que plusieurs factures valides n’ont pas été retrouvées, ce qui peut nécessiter des ajustements dans l’algorithme de matching .
