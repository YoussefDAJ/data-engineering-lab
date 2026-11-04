from pathlib import Path
import pandas as pd

CHEMIN = Path(__file__).resolve().parent.parent / "data" / "ventes.csv"


def ventes_par_region(chemin: Path) -> pd.DataFrame:

    ventes = pd.read_csv(chemin)

    # 1. Vérifier les quantités négatives
    if (ventes["quantite"] < 0).any():
        raise ValueError("Quantité négative détectée !")

    # 2. Calculer le chiffre d'affaires
    ventes["chiffre_affaires"] = ventes["quantite"] * ventes["prix_unitaire"]

    # 3. Regrouper les données par région
    resultat = (
        ventes.groupby("region")
        .agg(
            chiffre_affaires=("chiffre_affaires", "sum"),
            nombre_transactions=("produit", "size"),
        )
        .reset_index()
    )

    # 4. Calculer la part du CA total
    total_ca = resultat["chiffre_affaires"].sum()

    resultat["part_ca_pct"] = (
        resultat["chiffre_affaires"] / total_ca * 100 if total_ca != 0 else 0
    ).round(2)

    return resultat


if __name__ == "__main__":
    print(ventes_par_region(CHEMIN))
