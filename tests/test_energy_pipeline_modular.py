import pandas as pd
import pytest

from src.energy_pipeline_modular import nettoyer_donnees, exporter_donnees


# Jeu de données fictif pour les tests
def jeu_exemple() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "country": ["France", "Germany", "Spain", "France"],
            "year": [2000, 2025, 2020, 2001],
            "renewables_electricity_share_pct": [12.74, 59.09, 40.0, None],
        }
    )


# Test 1 : filtrage et valeurs manquantes
def test_filtrage_et_valeurs_manquantes() -> None:
    resultat = nettoyer_donnees(jeu_exemple())

    assert len(resultat) == 2
    assert set(resultat["country"]) == {"France", "Germany"}
    assert resultat["renewables_electricity_share_pct"].notna().all()


# Test 2 : refus des doublons
def test_rejet_des_doublons() -> None:
    df = jeu_exemple()

    df = pd.concat([df, df.iloc[[0]]], ignore_index=True)

    with pytest.raises(ValueError, match="Doublons"):
        nettoyer_donnees(df)


# Test 3 : pourcentages invalides
def test_rejet_pourcentage_invalide() -> None:
    df = jeu_exemple()

    df.loc[df["country"] == "Germany", "renewables_electricity_share_pct"] = 120

    with pytest.raises(ValueError, match="hors"):
        nettoyer_donnees(df)


# Test 4 : export CSV
def test_export_csv(tmp_path) -> None:
    chemin = tmp_path / "processed" / "resultat.csv"

    exporter_donnees(nettoyer_donnees(jeu_exemple()), chemin)

    assert chemin.exists()

    resultat = pd.read_csv(chemin)
    assert len(resultat) == 2


# Test 5 : vérifier le rejet d'un pays absent
def test_pays_absent() -> None:
    df = jeu_exemple()

    # Supprimer l'Allemagne uniquement pour ce test
    df = df[df["country"] != "Germany"].copy()

    # Vérifier que le pipeline détecte le pays manquant
    with pytest.raises(ValueError, match="France ou Allemagne absente"):
        nettoyer_donnees(df)


# Test 6 : vérifier le rejet d'une colonne absente
def test_colonne_absente() -> None:
    df = jeu_exemple()

    # Supprimer la colonne 'year' pour ce test
    df = df.drop(columns=["year"])

    # Vérifier que le pipeline détecte la colonne manquante
    with pytest.raises(ValueError, match="Colonnes absentes"):
        nettoyer_donnees(df)
