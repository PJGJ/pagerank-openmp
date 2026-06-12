# PageRank con OpenMP

## Descripción del proyecto

Este proyecto implementa el algoritmo PageRank en C++ y lo paraleliza usando OpenMP. El objetivo es evaluar la mejora en rendimiento al calcular PageRank sobre grafos web dirigidos de gran tamaño usando múltiples hilos en un sistema de memoria compartida.

Aunque los experimentos pueden ejecutarse en un cluster, la implementación con OpenMP se limita a un solo nodo de memoria compartida.

## Datasets

El proyecto usa datasets públicos de grafos web de SNAP Stanford:

| Dataset | Nodos | Aristas |
|---|---:|---:|
| web-Stanford | 281,903 | 2,312,497 |
| web-Google | 875,713 | 5,105,039 |
| web-BerkStan | 685,230 | 7,600,595 |

Los datasets deben colocarse en la carpeta `data/`. Ver `data/README.md`.

## Requisitos

- Compilador de C++ con soporte para OpenMP
- Python 3
- Linux, WSL o un nodo de cluster con memoria compartida

## Compilación

~~~bash
g++ -O3 -fopenmp src/pagerank.cpp -o src/pagerank
~~~

## Ejecutar un experimento

~~~bash
./src/pagerank data/web-Stanford.txt 100 0.85 4
~~~

Argumentos:

~~~text
1. archivo del grafo
2. número de iteraciones
3. factor de amortiguamiento
4. número de hilos
~~~

## Ejecutar todos los experimentos

~~~bash
./scripts/run_formal_tests.sh
python3 scripts/summarize_results.py
~~~

Los tiempos crudos se guardan en:

~~~text
results/raw_times.csv
~~~

Los resultados resumidos se guardan en:

~~~text
results/summary.csv
~~~

## Resultados

El experimento formal usó 100 iteraciones, factor de amortiguamiento 0.85 y 5 repeticiones por cada combinación de dataset y número de hilos.

| Dataset | Hilos | Tiempo promedio | Speedup | Eficiencia |
|---|---:|---:|---:|---:|
| web-Stanford | 1 | 0.554529 | 1.0000 | 1.0000 |
| web-Stanford | 2 | 0.373993 | 1.4827 | 0.7414 |
| web-Stanford | 4 | 0.330006 | 1.6804 | 0.4201 |
| web-Stanford | 8 | 0.254229 | 2.1812 | 0.2727 |
| web-Google | 1 | 2.476523 | 1.0000 | 1.0000 |
| web-Google | 2 | 1.962963 | 1.2616 | 0.6308 |
| web-Google | 4 | 1.514570 | 1.6351 | 0.4088 |
| web-Google | 8 | 1.149150 | 2.1551 | 0.2694 |
| web-BerkStan | 1 | 1.210549 | 1.0000 | 1.0000 |
| web-BerkStan | 2 | 0.722177 | 1.6763 | 0.8381 |
| web-BerkStan | 4 | 0.521053 | 2.3233 | 0.5808 |
| web-BerkStan | 8 | 0.477911 | 2.5330 | 0.3166 |

## Video demo

Enlace al video demo:

~~~text
https://drive.google.com/file/d/1QJ_ryyYxlpfjlCDeDJU4yJwVA0to4-zV/view?usp=sharing
~~~

## Estructura del repositorio

~~~text
pagerank-openmp/
├── README.md
├── data/
│   └── README.md
├── report/
├── results/
│   ├── raw_times.csv
│   ├── summary.csv
│   └── times.csv
├── scripts/
│   ├── run_tests.sh
│   ├── run_formal_tests.sh
│   └── summarize_results.py
└── src/
    ├── graph_info.cpp
    └── pagerank.cpp
~~~
