from pathlib import Path
import pandas as pd

CHEMIN = Path(__file__).resolve().parent.parent / "data" / "ventes.csv"


def ventes_par_region(chemin: Path) -> pd.DataFrame:
    ventes = pd.read_csv(chemin)

    ventes["chiffre_affaires"] = ventes["quantite"] * ventes["prix_unitaire"]

    resultat = ventes.groupby("region", as_index=False)["chiffre_affaires"].sum()

    return resultat


if __name__ == "__main__":
    print(ventes_par_region(CHEMIN))
