from pathlib import Path
import pandas as pd

# Configuration commune
BASE = Path(__file__).resolve().parent.parent

SOURCE = BASE / "data/raw/owid_energy.csv"
SORTIE = BASE / "data/processed/renewables_fr_de.csv"

COLONNES = ["country", "year", "renewables_electricity_share_pct"]

PAYS = ("France", "Germany")


# Fonction 1 : ingestion
def charger_donnees(chemin: Path) -> pd.DataFrame:
    """Charge les colonnes utiles du fichier OWID."""
    return pd.read_csv(chemin, usecols=COLONNES)


# Fonction 2 : transformation et contrôle qualité
def nettoyer_donnees(df: pd.DataFrame) -> pd.DataFrame:
    """Filtre les données et vérifie leur cohérence."""

    manquantes = set(COLONNES) - set(df.columns)

    if manquantes:
        raise ValueError(f"Colonnes absentes : {sorted(manquantes)}")

    resultat = (
        df.loc[df["country"].isin(PAYS) & df["year"].between(2000, 2025), COLONNES]
        .dropna(subset=["renewables_electricity_share_pct"])
        .copy()
    )

    if resultat.empty:
        raise ValueError("Aucune observation exploitable.")

    if set(resultat["country"]) != set(PAYS):
        raise ValueError("France ou Allemagne absente des résultats.")

    if resultat.duplicated(["country", "year"]).any():
        raise ValueError("Doublons pays-année détectés.")

    if not resultat["renewables_electricity_share_pct"].between(0, 100).all():
        raise ValueError("Part renouvelable hors de [0, 100].")

    return resultat.sort_values(["country", "year"]).reset_index(drop=True)


# Fonction 3 : export
def exporter_donnees(df: pd.DataFrame, chemin: Path) -> None:
    """Enregistre les données préparées dans un CSV."""

    chemin.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(chemin, index=False)


# Fonction principale : orchestration
def main() -> None:
    """Exécute les différentes étapes du pipeline."""

    donnees = charger_donnees(SOURCE)

    resultat = nettoyer_donnees(donnees)

    exporter_donnees(resultat, SORTIE)

    print(f"{len(resultat)} observations exportées " f"vers {SORTIE}")


if __name__ == "__main__":
    main()
