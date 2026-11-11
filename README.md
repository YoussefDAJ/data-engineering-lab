# Energy Data Engineering Lab

**Du script Python séquentiel à un pipeline modulaire, testé et observable — analyse de données énergétiques publiques (2000–2025).**

> **Portfolio Data Engineering — projet évolutif.** Le dépôt conserve les versions successives du même pipeline afin de montrer l'amélioration progressive de son architecture, de ses contrôles et de sa traçabilité.

## 1. Objectif et question métier

Ce projet personnel utilise les données énergétiques publiques d'**Our World in Data (OWID)** pour construire un pipeline reproductible avec Python. Il documente trois étapes d'apprentissage :

- **V1 :** réaliser un traitement de données avec un script séquentiel ;
- **V2 :** organiser le code en fonctions indépendantes et écrire des tests unitaires ;
- **V3 :** ajouter la journalisation (`logging`), la mesure du temps d'exécution et la remontée des erreurs.

**Question métier :** comment la part des énergies renouvelables dans la **production d'électricité** a-t-elle évolué en France et en Allemagne entre 2000 et 2025 ?

## 2. Résultats de l'analyse

### Évolution de la part des renouvelables

![Évolution de la part renouvelable dans la production électrique en France et en Allemagne](reports/figures/evolution_renouvelables.png)

_Indicateur : part des énergies renouvelables dans la production totale d'électricité (%). Source : Our World in Data, Energy Dataset, version du 10 septembre 2026._

| Indicateur                                  |  France | Allemagne |
| ------------------------------------------- | ------: | --------: |
| Part renouvelable en 2000                   | 12,74 % |    6,22 % |
| Part renouvelable en 2025                   | 26,06 % |   59,09 % |
| Évolution 2000–2025 (points de pourcentage) |  +13,33 |    +52,87 |

### Trois enseignements

1. **Progression dans les deux pays :** la part des renouvelables augmente entre 2000 et 2025.
2. **Progression plus marquée en Allemagne :** +52,87 points, contre +13,33 points pour la France.
3. **Inversion de l'écart :** en 2000, la France dépasse l'Allemagne de **6,51 points** ; en 2025, l'Allemagne dépasse la France de **33,03 points**.

Les écarts sont calculés à partir des valeurs non arrondies, puis arrondis à deux décimales.

**Limites de l'analyse :** l'indicateur décrit la structure de la **production électrique**, et non l'énergie totale, la consommation d'électricité ou l'intensité carbone. La part du nucléaire, notamment, empêche d'assimiler part renouvelable et décarbonation. Cette analyse descriptive n'identifie pas les causes des évolutions observées.

**Livrables :** [données transformées](data/processed/renewables_fr_de.csv) · [tableau des KPI](reports/kpi_summary.csv) · [graphique](reports/figures/evolution_renouvelables.png)

## 3. Traitement et qualité des données

Le pipeline suit la chaîne suivante :

```text
OWID (CSV brut)
       |
       v
Ingestion pandas
       |
       v
Filtrage : France et Allemagne, 2000–2025
       |
       v
Contrôles qualité et traitement des valeurs manquantes
       |
       v
Export CSV (52 observations)
       |
       v
KPI et visualisation Matplotlib
```

Les contrôles portent sur la présence des deux pays, les doublons `(country, year)`, les valeurs manquantes de `renewables_electricity_share_pct` et les pourcentages hors de l'intervalle `[0, 100]`. Le nettoyage supprime les observations dont cette variable est manquante. Sur le jeu et la période retenus, le fichier transformé contient **52 observations** (26 années × 2 pays).

Ces contrôles portent sur le **périmètre métier analysé** et ne constituent pas un audit exhaustif de toute la base OWID.

## 4. Évolution du code : trois versions d'un même pipeline

| Critère             | V1 — Séquentielle                              | V2 — Modulaire                                                 | V3 — Observable                                                      |
| ------------------- | ---------------------------------------------- | -------------------------------------------------------------- | -------------------------------------------------------------------- |
| Fichier             | [`energy_pipeline.py`](src/energy_pipeline.py) | [`energy_pipeline_modular.py`](src/energy_pipeline_modular.py) | [`energy_pipeline_observable.py`](src/energy_pipeline_observable.py) |
| Organisation        | Un script avec plusieurs étapes                | Fonctions réutilisables et `main()`                            | Réutilise les fonctions V2 et orchestre leur exécution               |
| Qualité des données | Contrôles dans le script                       | Validation dans une fonction testable                          | Même validation + suivi des valeurs manquantes                       |
| Gestion des erreurs | Exceptions bloquantes                          | Exceptions dans les fonctions                                  | Exceptions journalisées, puis propagées                              |
| Traçabilité         | Messages `print()`                             | Message final `print()`                                        | Logs `INFO`, `WARNING`, `ERROR` et durée d'exécution                 |
| Tests               | Pas de tests dédiés                            | 6 scénarios de test                                            | 4 scénarios supplémentaires                                          |
| Résultat métier     | CSV transformé                                 | Même CSV                                                       | Même CSV                                                             |

### V1 — Pipeline séquentiel

Le premier script charge le CSV, filtre les pays et la période, nettoie les données, applique des contrôles et exporte le résultat. C'est une bonne première approche, mais ses étapes sont moins faciles à tester indépendamment.

### V2 — Pipeline modulaire

La deuxième version sépare les responsabilités :

- `charger_donnees(chemin)` : ingestion du CSV ;
- `nettoyer_donnees(df)` : transformation et validation ;
- `exporter_donnees(df, chemin)` : écriture du CSV ;
- `main()` : orchestration des fonctions.

Cette structure facilite la réutilisation, les tests et la maintenance. Les annotations de type (`Path`, `pd.DataFrame`, `None`) précisent les contrats des fonctions.

### V3 — Pipeline observable : logging et gestion des erreurs

La troisième version **importe et réutilise les fonctions de V2**, sans recopier leur logique métier. Elle ajoute une couche de suivi de l'exécution dans `executer_pipeline(source, sortie)` :

- **`INFO` :** démarrage, nombre de lignes chargées, contrôles validés, export et durée d'exécution ;
- **`WARNING` :** détection de valeurs manquantes pour `renewables_electricity_share_pct` **sur le périmètre France/Allemagne, 2000–2025**, avant nettoyage ;
- **`ERROR` :** journalisation d'un échec et de sa trace avec `LOGGER.exception()`, puis propagation de l'exception avec `raise` ;
- **Journal local :** événements affichés dans le Terminal et enregistrés dans `logs/energy_pipeline.log`.

Une valeur manquante entraîne un avertissement, **pas nécessairement l'arrêt du pipeline** : l'observation concernée est ensuite exclue selon la règle de nettoyage. Une anomalie bloquante (fichier absent, pourcentage invalide, pays manquant, etc.) provoque une exception.

Le dossier `logs/` est exclu de Git : les journaux locaux ne sont pas publiés sur GitHub.

**Enseignement principal :** la V3 n'améliore pas nécessairement la vitesse de calcul. Elle facilite surtout le **diagnostic des échecs**, la **traçabilité** et le **suivi de la qualité des données**.

## 5. Tests automatisés

Les tests utilisent de petits jeux de données fictifs, distincts du CSV OWID, pour isoler les comportements du code.

| Suite                                                | Scénarios couverts                                                                                           | Nombre |
| ---------------------------------------------------- | ------------------------------------------------------------------------------------------------------------ | -----: |
| [Tests V2](tests/test_energy_pipeline_modular.py)    | Filtrage et valeurs manquantes, doublons, pourcentage invalide, export CSV, pays absent, colonne absente     |      6 |
| [Tests V3](tests/test_energy_pipeline_observable.py) | Exécution et logs `INFO`, source absente, pourcentage invalide, avertissement `WARNING` sur valeur manquante |      4 |
| **Total prévu**                                      | **Exécution avec `pytest`**                                                                                  | **10** |

Les tests V3 utilisent `caplog` pour vérifier les événements journalisés et `tmp_path` pour éviter de modifier les vrais fichiers du projet.

**Validation à reproduire localement :**

```bash
python -m pytest -v
```

L'objectif est **10 tests réussis** après ajout des fichiers V3. Le résultat effectif doit être vérifié sur l'environnement d'exécution ; la présence de dix scénarios ne constitue pas, à elle seule, une preuve d'exécution réussie.

## 6. Reproduire le projet

Instructions prévues pour **macOS / Linux**, avec Python 3 compatible avec les versions spécifiées dans `requirements.txt`.

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

Le fichier CSV original n'est pas versionné dans ce dépôt. La version datée permet de travailler sur une source stable, sous réserve de sa disponibilité dans le catalogue.

### 3. Exécuter et comparer V1, V2 et V3

```bash
# V1
python src/energy_pipeline.py
cp data/processed/renewables_fr_de.csv /tmp/renewables_v1.csv

# V2
python src/energy_pipeline_modular.py
diff -u /tmp/renewables_v1.csv data/processed/renewables_fr_de.csv
cp data/processed/renewables_fr_de.csv /tmp/renewables_v2.csv

# V3 (exécution en module, depuis la racine du dépôt)
python -m src.energy_pipeline_observable
diff -u /tmp/renewables_v2.csv data/processed/renewables_fr_de.csv
```

Quand `diff` n'affiche aucune différence, les sorties comparées sont identiques. **Les trois programmes écrivent dans le même fichier** `data/processed/renewables_fr_de.csv` : chaque nouvelle exécution remplace la sortie précédente.

### 4. Vérifier les logs

```bash
cat logs/energy_pipeline.log
```

Les dates, durées, chemins et avertissements présents dans le journal dépendent des données et de l'exécution. Le `WARNING` ne s'affiche que si des valeurs manquantes sont détectées dans le périmètre analysé.

### 5. Exécuter les tests et régénérer le rapport

```bash
python -m pytest -v
python src/create_report.py
```

**Sorties attendues :**

- `data/processed/renewables_fr_de.csv` — données nettoyées ;
- `reports/kpi_summary.csv` — indicateurs France/Allemagne ;
- `reports/figures/evolution_renouvelables.png` — graphique ;
- `logs/energy_pipeline.log` — journal local de V3, non versionné.

## 7. Technologies et organisation du dépôt

**Python · pandas · Matplotlib · pytest · logging · Git/GitHub**

```text
data-engineering-lab/
├── data/
│   ├── raw/                            # CSV OWID original, non versionné
│   └── processed/                      # CSV nettoyé publié
├── src/
│   ├── __init__.py
│   ├── energy_pipeline.py              # V1
│   ├── energy_pipeline_modular.py      # V2
│   ├── energy_pipeline_observable.py   # V3
│   └── create_report.py               # KPI et graphique
├── tests/
│   ├── test_energy_pipeline_modular.py
│   └── test_energy_pipeline_observable.py
├── reports/
│   ├── figures/
│   │   └── evolution_renouvelables.png
│   └── kpi_summary.csv
├── logs/                                # Généré localement, ignoré par Git
├── .gitignore
├── requirements.txt
└── README.md
```

## 8. Sources, attribution et licences

- **Our World in Data (OWID)** — [Energy Dataset et documentation](https://catalog.ourworldindata.org/energy/owid_energy/), version utilisée : **2026-09-10**. Ce jeu de données regroupe et harmonise plusieurs sources.
- **Ember** — [Yearly Electricity Data](https://ember-energy.org/data/yearly-electricity-data/). Ses données électriques sont proposées sous licence [Creative Commons Attribution 4.0 (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/).
- **Energy Institute** — [Statistical Review of World Energy](https://www.energyinst.org/statistical-review/), autre producteur cité dans le jeu énergétique OWID.

**Attribution :** analyse, transformation et visualisation personnelles à partir du jeu énergétique d'Our World in Data et de ses producteurs d'origine. Les licences des données tierces peuvent différer : consulter les références et conditions indiquées dans le catalogue OWID. La licence CC BY 4.0 mentionnée ici concerne les données électriques d'Ember et ne doit pas être étendue automatiquement à tout le jeu OWID.

## 9. Prochaines étapes

- Automatiser l'ingestion des données à partir d'une URL ou d'une API HTTP (Jour 5).
- Renforcer les validations et automatiser l'exécution des tests avec GitHub Actions.
- Approfondir SQL, la modélisation analytique, dbt et l'orchestration de pipelines avec Airflow.

**Ce projet est un laboratoire de progression : les versions V1, V2 et V3 sont conservées pour rendre visibles les évolutions du code et des pratiques d'ingénierie.**
