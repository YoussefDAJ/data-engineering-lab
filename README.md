
# Analyse des ventes avec Python

## 1. Présentation du projet

Ce projet permet d'analyser les performances
commerciales d'une entreprise à partir d'un
fichier CSV.

## 2. Objectif métier

Calculer le chiffre d'affaires par région
pour identifier les régions les plus performantes.

## 3. Technologies utilisées

- Python
- pandas
- pytest (pour les futurs tests)
- Git

## 4. Structure du projet

- data/ : fichiers de données
- src/ : scripts Python
- tests/ : tests automatisés
- notebooks/ : analyses exploratoires
- requirements.txt : dépendances Python

## 5. Installation

Créer un environnement virtuel :

    python3 -m venv .venv

Activer l'environnement :

    source .venv/bin/activate

Installer les bibliothèques :

    python -m pip install -r requirements.txt

## 6. Exécution

Depuis la racine du projet :

    python src/kpi.py

## 7. Résultats attendus

Chiffre d'affaires par région :

- Nord : 390 €
- Sud : 500 €
- Total : 890 €

## 8. Source des données

Jeu de données fictif créé pour
l'apprentissage de Python et pandas.

## 9. Améliorations prévues

- Ajouter des tests automatisés
- Contrôler la qualité des données
- Exporter les indicateurs en CSV
- Automatiser le pipeline de traitement
