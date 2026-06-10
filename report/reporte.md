# PageRank con OpenMP

## 1. Introducción

PageRank es un algoritmo usado para asignar importancia a los nodos de un grafo dirigido. En un grafo web, cada nodo representa una página y cada arista representa un enlace de una página hacia otra. La idea principal es que una página es más importante si recibe enlaces desde páginas que también son importantes.

Este proyecto implementa PageRank en C++ y paraleliza el cálculo usando OpenMP. El objetivo es evaluar la mejora en rendimiento al usar múltiples hilos sobre grafos web grandes en un sistema de memoria compartida.

## 2. Objetivo

Implementar y evaluar una versión paralela del algoritmo PageRank usando OpenMP, comparando tiempos de ejecución, speedup y eficiencia con distintos números de hilos.

## 3. Datasets utilizados

Se usaron tres datasets públicos de grafos web de SNAP Stanford.

| Dataset | Nodos | Aristas |
|---|---:|---:|
| web-Stanford | 281,903 | 2,312,497 |
| web-Google | 875,713 | 5,105,039 |
| web-BerkStan | 685,230 | 7,600,595 |

Los archivos contienen pares de nodos en formato:

```text
FromNodeId    ToNodeId
```

Cada línea representa una arista dirigida.

## 4. Metodología

El algoritmo fue implementado en C++ usando OpenMP. Para cada nodo se calcula su nuevo valor de PageRank a partir de los nodos que apuntan hacia él. La paralelización se aplicó sobre el ciclo que actualiza los valores de PageRank para todos los nodos.

Se usaron los siguientes parámetros:

| Parámetro | Valor |
|---|---:|
| Iteraciones | 100 |
| Factor de amortiguamiento | 0.85 |
| Repeticiones por caso | 5 |
| Hilos probados | 1, 2, 4, 8 |

Para cada combinación de dataset e hilos se midió el tiempo de ejecución. Luego se calculó el tiempo promedio, speedup y eficiencia.

El speedup se calculó como:

```text
Speedup = T1 / Tp
```

La eficiencia se calculó como:

```text
Eficiencia = Speedup / p
```

donde `T1` es el tiempo usando 1 hilo, `Tp` es el tiempo usando `p` hilos, y `p` es el número de hilos.

## 5. Resultados

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

## 6. Análisis

Los resultados muestran que el uso de OpenMP reduce el tiempo de ejecución en los tres datasets. El mejor speedup se obtuvo en `web-BerkStan`, donde con 8 hilos se alcanzó un speedup de 2.5330.

La eficiencia disminuye al aumentar el número de hilos. Esto es esperado porque no todo el trabajo del programa es paralelizable y también existe costo por sincronización, acceso a memoria y distribución del trabajo entre hilos.

Aunque el speedup no es lineal, los resultados muestran una mejora clara al pasar de 1 hilo a múltiples hilos. Esto confirma que PageRank puede beneficiarse de paralelismo en memoria compartida.

## 7. Uso de OpenMP y relación con MPI

Este proyecto se enfoca en OpenMP porque los datasets seleccionados caben en memoria de una sola máquina o de un solo nodo de cluster. OpenMP trabaja con memoria compartida, por lo que es adecuado para este caso.

Si se trabajara con grafos mucho más grandes que no caben en la memoria de un solo nodo, entonces sería necesario usar MPI para distribuir el grafo entre varios nodos. En este proyecto, MPI se considera una posible extensión, pero no es necesario para los datasets usados.

## 8. Conclusión

Se implementó PageRank en C++ y se paralelizó usando OpenMP. Los experimentos con tres grafos web muestran que el uso de múltiples hilos reduce el tiempo de ejecución y produce speedup en todos los casos.

El proyecto demuestra el uso de cómputo paralelo en memoria compartida para procesar grafos grandes. Aunque la eficiencia disminuye al aumentar el número de hilos, el rendimiento mejora claramente respecto a la ejecución con un solo hilo.

## 9. Archivos principales del proyecto

| Archivo | Descripción |
|---|---|
| `src/pagerank.cpp` | Implementación principal de PageRank con OpenMP |
| `scripts/run_formal_tests.sh` | Script para correr los experimentos |
| `scripts/summarize_results.py` | Script para calcular promedios, speedup y eficiencia |
| `scripts/plot_results_svg.py` | Script para generar gráficas |
| `results/raw_times.csv` | Tiempos crudos |
| `results/summary.csv` | Resultados resumidos |
| `results/tiempo_promedio.svg` | Gráfica de tiempos |
| `results/speedup.svg` | Gráfica de speedup |
| `results/eficiencia.svg` | Gráfica de eficiencia |
