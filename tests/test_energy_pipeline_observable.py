"""Tests automatisés du pipeline énergétique V3."""

import logging

import pandas as pd
import pytest

from src.energy_pipeline_observable import executer_pipeline


# Test 1 : exécution réussie et journalisation
def test_succes_et_logs(tmp_path, caplog):
    source = tmp_path / "entree.csv"
    sortie = tmp_path / "processed" / "sortie.csv"

    df = pd.DataFrame(
        {
            "country": ["France", "Germany", "Spain"],
            "year": [2000, 2025, 2025],
            "renewables_electricity_share_pct": [12.74, 59.09, 50.0],
        }
    )

    df.to_csv(source, index=False)

    with caplog.at_level(
        logging.INFO,
        logger="src.energy_pipeline_observable",
    ):
        n = executer_pipeline(source, sortie)

    assert n == 2
    assert sortie.exists()

    assert "Ingestion terminée" in caplog.text
    assert "Contrôles validés" in caplog.text
    assert "Export terminé" in caplog.text

    resultat = pd.read_csv(sortie)

    assert len(resultat) == 2
    assert set(resultat["country"]) == {"France", "Germany"}


# Test 2 : fichier source inexistant
def test_source_absente(tmp_path, caplog):
    source = tmp_path / "absent.csv"
    sortie = tmp_path / "processed" / "sortie.csv"

    with caplog.at_level(
        logging.ERROR,
        logger="src.energy_pipeline_observable",
    ):
        with pytest.raises(FileNotFoundError):
            executer_pipeline(source, sortie)

    assert "Échec du pipeline" in caplog.text
    assert not sortie.exists()


# Test 3 : pourcentage invalide
def test_part_invalide(tmp_path, caplog):
    source = tmp_path / "invalid.csv"
    sortie = tmp_path / "processed" / "sortie.csv"

    df = pd.DataFrame(
        {
            "country": ["France", "Germany"],
            "year": [2000, 2025],
            "renewables_electricity_share_pct": [12.74, 120.0],
        }
    )

    df.to_csv(source, index=False)

    with caplog.at_level(
        logging.ERROR,
        logger="src.energy_pipeline_observable",
    ):
        with pytest.raises(ValueError, match="hors de"):
            executer_pipeline(source, sortie)

    assert "Échec du pipeline" in caplog.text
    assert not sortie.exists()


# Test 4 : détection des valeurs manquantes
def test_warning_valeurs_manquantes(tmp_path, caplog):
    source = tmp_path / "donnees.csv"
    sortie = tmp_path / "processed" / "resultat.csv"

    df = pd.DataFrame(
        {
            "country": ["France", "Germany", "France"],
            "year": [2000, 2025, 2001],
            "renewables_electricity_share_pct": [12.74, 59.09, None],
        }
    )

    df.to_csv(source, index=False)

    with caplog.at_level(
        logging.WARNING,
        logger="src.energy_pipeline_observable",
    ):
        n = executer_pipeline(source, sortie)

    # Vérifier la présence du WARNING
    assert "Valeurs manquantes détectées" in caplog.text
    assert "1 lignes" in caplog.text

    # Le pipeline continue normalement
    assert n == 2
    assert sortie.exists()

    # Vérifier que la ligne manquante a été exclue
    resultat = pd.read_csv(sortie)

    assert len(resultat) == 2
    assert resultat["renewables_electricity_share_pct"].notna().all()
