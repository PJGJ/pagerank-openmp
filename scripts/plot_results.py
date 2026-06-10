import csv
import matplotlib.pyplot as plt
from collections import defaultdict

data = defaultdict(list)

with open("results/summary.csv", newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        dataset = row["dataset"]
        data[dataset].append({
            "threads": int(row["threads"]),
            "avg_time": float(row["avg_time"]),
            "speedup": float(row["speedup"]),
            "efficiency": float(row["efficiency"])
        })

plt.figure()
for dataset, rows in data.items():
    rows.sort(key=lambda x: x["threads"])
    plt.plot([r["threads"] for r in rows], [r["avg_time"] for r in rows], marker="o", label=dataset)
plt.xlabel("Número de hilos")
plt.ylabel("Tiempo promedio (segundos)")
plt.title("Tiempo promedio de PageRank con OpenMP")
plt.legend()
plt.grid(True)
plt.savefig("results/tiempo_promedio.png", dpi=300, bbox_inches="tight")

plt.figure()
for dataset, rows in data.items():
    rows.sort(key=lambda x: x["threads"])
    plt.plot([r["threads"] for r in rows], [r["speedup"] for r in rows], marker="o", label=dataset)
plt.xlabel("Número de hilos")
plt.ylabel("Speedup")
plt.title("Speedup de PageRank con OpenMP")
plt.legend()
plt.grid(True)
plt.savefig("results/speedup.png", dpi=300, bbox_inches="tight")

plt.figure()
for dataset, rows in data.items():
    rows.sort(key=lambda x: x["threads"])
    plt.plot([r["threads"] for r in rows], [r["efficiency"] for r in rows], marker="o", label=dataset)
plt.xlabel("Número de hilos")
plt.ylabel("Eficiencia")
plt.title("Eficiencia de PageRank con OpenMP")
plt.legend()
plt.grid(True)
plt.savefig("results/eficiencia.png", dpi=300, bbox_inches="tight")

print("Gráficas creadas en results/")
