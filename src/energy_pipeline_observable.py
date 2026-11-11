"""V3 : pipeline énergétique avec logging et gestion des erreurs."""

import logging
from pathlib import Path
from time import perf_counter

from src.energy_pipeline_modular import (
    SOURCE,
    SORTIE,
    charger_donnees,
    nettoyer_donnees,
    exporter_donnees,
)

# Logger propre à ce module
LOGGER = logging.getLogger(__name__)

BASE = Path(__file__).resolve().parent.parent
FICHIER_LOG = BASE / "logs" / "energy_pipeline.log"


def executer_pipeline(source: Path, sortie: Path) -> int:
    """Exécute le pipeline et retourne le nombre de lignes exportées."""

    debut = perf_counter()

    LOGGER.info("Démarrage du pipeline | source=%s", source)

    try:
        # Étape 1 : ingestion
        donnees = charger_donnees(source)

        LOGGER.info(
            "Ingestion terminée | %d lignes chargées",
            len(donnees),
        )

        # Étape 2 : contrôle des valeurs manquantes
        # Périmètre : France et Allemagne, 2000-2025
        donnees_cibles = donnees.loc[
            donnees["country"].isin(["France", "Germany"])
            & donnees["year"].between(2000, 2025)
        ]

        nombre_manquants = (
            donnees_cibles["renewables_electricity_share_pct"].isna().sum()
        )

        if nombre_manquants > 0:
            LOGGER.warning(
                "Valeurs manquantes détectées | %d lignes | "
                "périmètre=France/Allemagne 2000-2025",
                nombre_manquants,
            )
        else:
            LOGGER.info(
                "Contrôle des valeurs manquantes réussi | " "aucune valeur manquante"
            )

        # Étape 3 : nettoyage et contrôles qualité
        resultat = nettoyer_donnees(donnees)

        LOGGER.info(
            "Contrôles validés | %d lignes conservées",
            len(resultat),
        )

        # Étape 4 : export
        exporter_donnees(resultat, sortie)

        LOGGER.info(
            "Export terminé | %d lignes | destination=%s | durée=%.2f s",
            len(resultat),
            sortie,
            perf_counter() - debut,
        )

        return len(resultat)

    except (OSError, ValueError):
        LOGGER.exception("Échec du pipeline")
        raise


def main() -> None:
    """Configure les logs et lance le pipeline."""

    FICHIER_LOG.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(
                FICHIER_LOG,
                encoding="utf-8",
            ),
        ],
    )

    executer_pipeline(SOURCE, SORTIE)


if __name__ == "__main__":
    main()
