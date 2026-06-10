import csv
from collections import defaultdict

raw_file = "results/raw_times.csv"
out_file = "results/summary.csv"

data = defaultdict(list)
info = {}

with open(raw_file, newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        dataset = row["dataset"]
        threads = int(row["threads"])
        time = float(row["time"])

        data[(dataset, threads)].append(time)
        info[dataset] = (row["nodes"], row["edges"])

datasets = ["web-Stanford", "web-Google", "web-BerkStan"]
thread_counts = [1, 2, 4, 8]

with open(out_file, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["dataset", "nodes", "edges", "threads", "avg_time", "speedup", "efficiency"])

    for dataset in datasets:
        base = sum(data[(dataset, 1)]) / len(data[(dataset, 1)])
        nodes, edges = info[dataset]

        for threads in thread_counts:
            avg_time = sum(data[(dataset, threads)]) / len(data[(dataset, threads)])
            speedup = base / avg_time
            efficiency = speedup / threads

            writer.writerow([
                dataset,
                nodes,
                edges,
                threads,
                f"{avg_time:.6f}",
                f"{speedup:.4f}",
                f"{efficiency:.4f}"
            ])

print(open(out_file).read())
