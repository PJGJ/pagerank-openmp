import csv
from collections import defaultdict

data = defaultdict(list)

with open("results/summary.csv", newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        data[row["dataset"]].append({
            "threads": int(row["threads"]),
            "avg_time": float(row["avg_time"]),
            "speedup": float(row["speedup"]),
            "efficiency": float(row["efficiency"])
        })

def make_chart(filename, metric, title, ylabel):
    width, height = 900, 550
    left, right, top, bottom = 90, 40, 60, 80
    plot_w = width - left - right
    plot_h = height - top - bottom

    all_rows = [r for rows in data.values() for r in rows]
    xs = sorted(set(r["threads"] for r in all_rows))
    ymax = max(r[metric] for r in all_rows) * 1.15

    def sx(x):
        return left + (x - min(xs)) / (max(xs) - min(xs)) * plot_w

    def sy(y):
        return top + plot_h - (y / ymax) * plot_h

    colors = ["#1f77b4", "#ff7f0e", "#2ca02c"]

    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">')
    svg.append('<rect width="100%" height="100%" fill="white"/>')
    svg.append(f'<text x="{width/2}" y="35" text-anchor="middle" font-size="24" font-family="Arial">{title}</text>')

    svg.append(f'<line x1="{left}" y1="{top}" x2="{left}" y2="{top+plot_h}" stroke="black"/>')
    svg.append(f'<line x1="{left}" y1="{top+plot_h}" x2="{left+plot_w}" y2="{top+plot_h}" stroke="black"/>')

    for x in xs:
        px = sx(x)
        svg.append(f'<line x1="{px}" y1="{top+plot_h}" x2="{px}" y2="{top+plot_h+6}" stroke="black"/>')
        svg.append(f'<text x="{px}" y="{top+plot_h+28}" text-anchor="middle" font-size="14" font-family="Arial">{x}</text>')

    for i in range(6):
        yval = ymax * i / 5
        py = sy(yval)
        svg.append(f'<line x1="{left-6}" y1="{py}" x2="{left}" y2="{py}" stroke="black"/>')
        svg.append(f'<line x1="{left}" y1="{py}" x2="{left+plot_w}" y2="{py}" stroke="#dddddd"/>')
        svg.append(f'<text x="{left-12}" y="{py+5}" text-anchor="end" font-size="13" font-family="Arial">{yval:.2f}</text>')

    svg.append(f'<text x="{width/2}" y="{height-25}" text-anchor="middle" font-size="16" font-family="Arial">Número de hilos</text>')
    svg.append(f'<text x="25" y="{height/2}" text-anchor="middle" font-size="16" font-family="Arial" transform="rotate(-90 25 {height/2})">{ylabel}</text>')

    for color, (dataset, rows) in zip(colors, data.items()):
        rows = sorted(rows, key=lambda r: r["threads"])
        points = " ".join(f'{sx(r["threads"])},{sy(r[metric])}' for r in rows)
        svg.append(f'<polyline points="{points}" fill="none" stroke="{color}" stroke-width="3"/>')

        for r in rows:
            svg.append(f'<circle cx="{sx(r["threads"])}" cy="{sy(r[metric])}" r="5" fill="{color}"/>')

    legend_x = left + plot_w - 170
    legend_y = top + 20

    for i, (color, dataset) in enumerate(zip(colors, data.keys())):
        y = legend_y + i * 25
        svg.append(f'<rect x="{legend_x}" y="{y-10}" width="14" height="14" fill="{color}"/>')
        svg.append(f'<text x="{legend_x+22}" y="{y+2}" font-size="14" font-family="Arial">{dataset}</text>')

    svg.append('</svg>')

    with open(filename, "w") as f:
        f.write("\n".join(svg))

make_chart("results/tiempo_promedio.svg", "avg_time", "Tiempo promedio de PageRank con OpenMP", "Tiempo promedio")
make_chart("results/speedup.svg", "speedup", "Speedup de PageRank con OpenMP", "Speedup")
make_chart("results/eficiencia.svg", "efficiency", "Eficiencia de PageRank con OpenMP", "Eficiencia")

print("Gráficas creadas en results/")
