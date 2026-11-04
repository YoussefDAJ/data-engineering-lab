# Energy Data Engineering Lab

## Objectif

Construire progressivement une plateforme de traitement
et d'analyse de données énergétiques publiques.

## Premier cas métier

Étudier l'évolution de la part des énergies renouvelables
dans la production d'électricité en France et en Allemagne.

## Source

Our World in Data - Energy Dataset
Version : 2026-09-10

https://catalog.ourworldindata.org/energy/owid_energy/

Les données sont compilées à partir de plusieurs producteurs,
notamment Ember et Energy Institute. Consulter les conditions
de réutilisation et les références sur le site source.

## Technologies

- Python
- pandas
- Git et GitHub
- pytest (prochain module)

## Installation

python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt

## Données

Télécharger le CSV officiel dans data/raw/owid_energy.csv
depuis l'URL de la version 2026-09-10 indiquée ci-dessus.

## Exécution

python src/energy_pipeline.py

## Résultat

data/processed/renewables_fr_de.csv

## Prochaines étapes

- Tests automatisés
- Analyse SQL
- Data Warehouse
- dbt
- Airflow
- Visualisation
