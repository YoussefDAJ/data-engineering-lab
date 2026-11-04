# Energy Data Engineering Lab

## Objectif

Construire progressivement une plateforme de traitement
et d'analyse de données énergétiques publiques.

## Premier cas métier

Comment a évolué la part des renouvelables
dans la production d'électricité en France
et en Allemagne entre 2000 et 2025 ?

## Source

Our World in Data - Energy Dataset
Version : 2026-09-10

https://catalog.ourworldindata.org/energy/owid_energy/

Les données sont compilées à partir de plusieurs producteurs,
notamment Ember et Energy Institute. Consulter les conditions
de réutilisation et les références sur le site source.

Licence des données électriques Ember :
Creative Commons Attribution 4.0 (CC BY 4.0).

### Méthodologie

1. Extraction des données énergétiques OWID.
2. Sélection de la France et de l'Allemagne.
3. Filtrage de la période 2000-2025.
4. Traitement des valeurs manquantes.
5. Vérification des doublons et pourcentages.
6. Calcul de l'évolution en points de pourcentage.
7. Export CSV et visualisation.

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

## Résultats de l'analyse

### Visualisation

![Évolution des renouvelables en France et Allemagne](reports/figures/evolution_renouvelables.png)

### Données et indicateurs

- [Données transformées](data/processed/renewables_fr_de.csv)
- [Tableau des KPI](reports/kpi_summary.csv)

### Principaux résultats (2000–2025)

L'analyse porte sur la part des énergies renouvelables
dans la production totale d'électricité en France et
en Allemagne.

| Indicateur                |  France | Allemagne |
| ------------------------- | ------: | --------: |
| Part renouvelable en 2000 | 12,74 % |    6,22 % |
| Part renouvelable en 2025 | 26,06 % |   59,09 % |
| Évolution (points de %)   |  +13,33 |    +52,87 |

### Interprétation

**1. Une progression dans les deux pays**

Entre 2000 et 2025, la part de l'électricité produite
à partir de sources renouvelables augmente en France
et en Allemagne.

**2. Une progression plus marquée en Allemagne**

L'Allemagne passe de 6,22 % à 59,09 %, soit
une augmentation de 52,87 points de pourcentage.

La France passe de 12,74 % à 26,06 %, soit
une augmentation de 13,33 points.

**3. Un écart qui s'inverse**

En 2000, la France présente une part renouvelable
supérieure de 6,51 points à celle de l'Allemagne.

En 2025, la part allemande dépasse celle de
la France de 33,02 points.

### Limites de l'analyse

- L'indicateur mesure une part de production électrique,
  et non la part des renouvelables dans l'énergie totale.
- Les variations annuelles peuvent notamment dépendre
  des conditions météorologiques et de la production
  hydroélectrique, éolienne ou solaire.
- La part renouvelable ne suffit pas à mesurer
  l'intensité carbone de l'électricité.
- Cette analyse descriptive ne permet pas d'établir
  les causes des différences entre les deux pays.
