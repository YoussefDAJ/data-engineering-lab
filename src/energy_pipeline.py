from pathlib import Path
import pandas as pd

# 1. Définir les chemins
BASE = Path(__file__).resolve().parent.parent

SOURCE = BASE / "data/raw/owid_energy.csv"
SORTIE = BASE / "data/processed/renewables_fr_de.csv"

# 2. Charger les données
colonnes = ["country", "year", "renewables_electricity_share_pct"]

df = pd.read_csv(SOURCE, usecols=colonnes)

# 3. Filtrer les observations
df = df.loc[
    df["country"].isin(["France", "Germany"]) & df["year"].between(2000, 2025)
].copy()

# 4. Contrôler les données manquantes
print("Valeurs manquantes :")
print(df.isna().sum())

df = df.dropna(subset=["renewables_electricity_share_pct"])

# 5. Vérifier la qualité des données
if df.duplicated(["country", "year"]).any():
    raise ValueError("Doublons pays/année")

if not df["renewables_electricity_share_pct"].between(0, 100).all():
    raise ValueError("Pourcentage invalide")

if set(df["country"]) != {"France", "Germany"}:
    raise ValueError("Un pays est absent des résultats")

# 6. Trier les observations
df = df.sort_values(["country", "year"])

# 7. Exporter les données propres
SORTIE.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(SORTIE, index=False)

# 8. Afficher les résultats
print("\nDimensions :", df.shape)
print("\nDernières observations par pays :")

dernieres = df.sort_values("year").groupby("country").tail(1)

print(dernieres.to_string(index=False))
print("\nFichier créé :", SORTIE)
