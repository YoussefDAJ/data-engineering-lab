from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

BASE = Path(__file__).resolve().parent.parent

SOURCE = BASE / "data/processed/renewables_fr_de.csv"
REPORTS = BASE / "reports"
FIGURES = REPORTS / "figures"

FIGURES.mkdir(parents=True, exist_ok=True)

# 1. Charger les données transformées
df = pd.read_csv(SOURCE)

# 2. Contrôler les données
if df.empty:
    raise ValueError("Le fichier ne contient aucune donnée.")

if df.duplicated(["country", "year"]).any():
    raise ValueError("Doublons pays-année détectés.")

# 3. Calculer les KPI par pays
resultats = []

for pays, groupe in df.groupby("country"):
    groupe = groupe.sort_values("year")

    debut = groupe.iloc[0]
    fin = groupe.iloc[-1]

    part_debut = debut["renewables_electricity_share_pct"]
    part_fin = fin["renewables_electricity_share_pct"]

    resultats.append(
        {
            "Pays": pays,
            "Annee_debut": int(debut["year"]),
            "Annee_fin": int(fin["year"]),
            "Part_debut_pct": round(part_debut, 2),
            "Part_fin_pct": round(part_fin, 2),
            "Evolution_points": round(part_fin - part_debut, 2),
        }
    )

kpi = pd.DataFrame(resultats)

# 4. Exporter le tableau de synthèse
kpi.to_csv(REPORTS / "kpi_summary.csv", index=False)

print("\nSYNTHÈSE DES INDICATEURS")
print(kpi.to_string(index=False))

# 5. Produire le graphique
fig, ax = plt.subplots(figsize=(11, 6))

for pays, groupe in df.groupby("country"):
    groupe = groupe.sort_values("year")

    ax.plot(
        groupe["year"],
        groupe["renewables_electricity_share_pct"],
        marker="o",
        markersize=3,
        linewidth=2,
        label=pays,
    )

ax.set_title("Part des renouvelables dans la production électrique")
ax.set_xlabel("Année")
ax.set_ylabel("Part de la production électrique (%)")
ax.grid(alpha=0.3)
ax.legend()

fig.tight_layout()

fig.savefig(FIGURES / "evolution_renouvelables.png", dpi=200, bbox_inches="tight")

plt.close(fig)

print("\nGraphique enregistré dans reports/figures/")
