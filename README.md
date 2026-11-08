# Energy Data Engineering Lab

**Du script Python exploratoire au pipeline modulaire testé — analyse de données énergétiques publiques (2000–2025).**

## Objectif et question métier

Ce projet personnel documente la construction progressive d'un pipeline de traitement de données énergétiques avec Python. Il illustre également le passage d'un script séquentiel à une architecture modulaire, afin d'améliorer la lisibilité, la réutilisation et la testabilité du code.

**Question métier :** comment la part des énergies renouvelables dans la **production d'électricité** a-t-elle évolué en France et en Allemagne entre 2000 et 2025 ?

## Résultats de l'analyse

### Évolution de la part des renouvelables

![Évolution de la part renouvelable dans la production électrique en France et en Allemagne](reports/figures/evolution_renouvelables.png)

_Indicateur : part des énergies renouvelables dans la production totale d'électricité (%). Source : Our World in Data, Energy Dataset, version du 10 septembre 2026._

| Indicateur                                  |  France | Allemagne |
| ------------------------------------------- | ------: | --------: |
| Part renouvelable en 2000                   | 12,74 % |    6,22 % |
| Part renouvelable en 2025                   | 26,06 % |   59,09 % |
| Évolution 2000–2025 (points de pourcentage) |  +13,33 |    +52,87 |

### Trois enseignements

1. **Progression dans les deux pays :** la part renouvelable augmente entre 2000 et 2025.
2. **Progression plus forte en Allemagne :** +52,87 points contre +13,33 points en France.
3. **Inversion de l'écart :** en 2000, la France dépasse l'Allemagne de **6,51 points** ; en 2025, l'Allemagne dépasse la France de **33,03 points**.

Les écarts sont calculés à partir des valeurs non arrondies, puis arrondis à deux décimales.

**Limites :** cet indicateur concerne la production électrique, pas l'énergie totale ni la consommation électrique. Il ne suffit pas pour comparer l'intensité carbone des mix électriques (notamment en raison du nucléaire), et cette analyse descriptive n'identifie pas les causes de ces évolutions.

**Consulter les livrables :** [données transformées](data/processed/renewables_fr_de.csv) · [tableau des KPI](reports/kpi_summary.csv) · [graphique](reports/figures/evolution_renouvelables.png)

## Pipeline et qualité des données

Le traitement suit cinq étapes :

1. Charger le CSV public d'Our World in Data (OWID).
2. Sélectionner **France** et **Germany**, puis les années **2000–2025**.
3. Écarter les observations sans valeur pour `renewables_electricity_share_pct`.
4. Vérifier la présence des pays, l'absence de doublons pays–année et les parts comprises entre 0 et 100 %.
5. Exporter **52 observations** (26 années × 2 pays), calculer les KPI et produire un graphique.

La qualité des données est contrôlée sur les observations retenues, sans prétendre évaluer l'ensemble du jeu OWID.

## Évolution du code : deux versions du même pipeline

| Critère             | V1 — Script séquentiel                         | V2 — Pipeline modulaire                                        |
| ------------------- | ---------------------------------------------- | -------------------------------------------------------------- |
| Fichier             | [`energy_pipeline.py`](src/energy_pipeline.py) | [`energy_pipeline_modular.py`](src/energy_pipeline_modular.py) |
| Organisation        | Étapes exécutées dans un même script           | Fonctions séparées et `main()`                                 |
| Réutilisation       | Logique moins facilement isolable              | Transformations importables                                    |
| Gestion des erreurs | Contrôles dans le flux du script               | Exceptions dans les fonctions de validation                    |
| Typage              | Pas d'annotations explicites                   | Annotations `Path`, `pd.DataFrame`, `None`                     |
| Vérification        | Exécution du pipeline                          | Tests unitaires avec `pytest`                                  |
| Livrable            | CSV transformé                                 | Même CSV transformé                                            |

### Fonctions de la version modulaire

- `charger_donnees(chemin)` : lit les colonnes utiles du CSV.
- `nettoyer_donnees(df)` : applique les filtres et valide les observations.
- `exporter_donnees(df, chemin)` : écrit un fichier CSV.
- `main()` : orchestre les étapes du pipeline.

Les [tests du pipeline modulaire](tests/test_energy_pipeline_modular.py) couvrent six scénarios : filtrage et valeurs manquantes, doublons, pourcentages invalides, export CSV, pays absent et colonne absente.

**Enseignement :** le principal gain n'est pas la vitesse d'exécution, mais la facilité de maintenance, de réutilisation et de test.

## Reproduire le projet

Instructions pour **macOS / Linux**, à partir d'un terminal et d'une installation Python 3 compatible avec les dépendances du projet.

### 1. Cloner le dépôt et installer les dépendances

```bash
git clone https://github.com/YoussefDAJ/data-engineering-lab.git
cd data-engineering-lab
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

### 2. Télécharger la version figée des données OWID

```bash
mkdir -p data/raw
curl -L --fail --retry 3 \
  "https://catalog.ourworldindata.org/garden/energy/2026-09-10/owid_energy/owid_energy.csv" \
  -o data/raw/owid_energy.csv
```

Le CSV original n'est pas stocké dans le dépôt ; le téléchargement ci-dessus récupère la **version du 10 septembre 2026**, afin d'éviter que des mises à jour ultérieures du catalogue modifient les résultats de cette analyse.

### 3. Exécuter les deux versions et comparer leurs sorties

```bash
python src/energy_pipeline.py
cp data/processed/renewables_fr_de.csv /tmp/renewables_v1.csv

python src/energy_pipeline_modular.py
diff -u /tmp/renewables_v1.csv data/processed/renewables_fr_de.csv
```

Si `diff` ne produit aucune ligne, les deux fichiers CSV sont identiques. Les programmes utilisent le même nom de fichier de sortie : les lancer successivement écrase donc le même CSV.

### 4. Exécuter les tests et produire les résultats

```bash
python -m pytest -v
python src/create_report.py
```

Les livrables générés sont `data/processed/renewables_fr_de.csv`, `reports/kpi_summary.csv` et `reports/figures/evolution_renouvelables.png`.

## Technologies et structure

**Python · pandas · Matplotlib · pytest · Git/GitHub**

```text
data-engineering-lab/
├── data/
│   ├── raw/                  # CSV OWID téléchargé, non versionné
│   └── processed/            # CSV nettoyé publié
├── src/
│   ├── energy_pipeline.py
│   ├── energy_pipeline_modular.py
│   └── create_report.py
├── tests/
│   └── test_energy_pipeline_modular.py
├── reports/
│   ├── figures/
│   │   └── evolution_renouvelables.png
│   └── kpi_summary.csv
├── requirements.txt
└── README.md
```

## Sources, attribution et licences

- **Our World in Data (OWID)** — [Energy Dataset et documentation](https://catalog.ourworldindata.org/energy/owid_energy/), version utilisée : **2026-09-10**. Le jeu de données regroupe et harmonise plusieurs sources.
- **Ember** — [Yearly Electricity Data](https://ember-energy.org/data/yearly-electricity-data/). Ses données électriques sont proposées sous licence [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
- **Energy Institute** — [Statistical Review of World Energy](https://www.energyinst.org/statistical-review/), autre producteur cité dans le jeu énergétique OWID.

**Attribution :** analyse, transformation et visualisation personnelles à partir du jeu énergétique d'Our World in Data et de ses producteurs d'origine. Les licences des données tierces peuvent différer : consulter les références et conditions indiquées pour chaque variable dans le catalogue OWID. La mention CC BY 4.0 concerne les données électriques d'Ember ; elle ne doit pas être étendue automatiquement à tout le jeu OWID.

## Prochaines étapes

Ajouter de la journalisation (`logging`), améliorer les tests et l'automatisation, puis approfondir SQL, la modélisation analytique et l'orchestration de pipelines.
