from pathlib import Path
import pandas as pd

# Chemins du projet
BASE = Path(__file__).resolve().parent.parent

SOURCE = BASE / "data/raw/owid_energy.csv"
SORTIE = BASE / "data/processed/renewables_fr_de.csv"

# Charger les colonnes utiles
colonnes = ["country", "year", "renewables_electricity_share_pct"]

df = pd.read_csv(SOURCE, usecols=colonnes)

# Filtrer les pays et les années
resultat = df.loc[
    df["country"].isin(["France", "Germany"]) & (df["year"] >= 2000)
].copy()

# Supprimer les valeurs manquantes de l'indicateur
resultat = resultat.dropna(subset=["renewables_electricity_share_pct"])

# Trier les observations
resultat = resultat.sort_values(["country", "year"])

# Contrôles de qualité
if resultat.duplicated(["country", "year"]).any():
    raise ValueError("Doublons pays-année détectés")

if not resultat["renewables_electricity_share_pct"].between(0, 100).all():
    raise ValueError("Pourcentage hors limites")

# Exporter les données transformées
SORTIE.parent.mkdir(parents=True, exist_ok=True)
resultat.to_csv(SORTIE, index=False)

print(resultat.tail(10))
print("Export terminé :", SORTIE)
