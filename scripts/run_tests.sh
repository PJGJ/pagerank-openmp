#!/bin/bash

EXEC=src/pagerank
OUT=results/times.csv

echo "dataset,nodes,edges,threads,iterations,time,last_diff" > $OUT

for DATASET in web-Stanford web-Google web-BerkStan
do
  for THREADS in 1 2 4 8
  do
    FILE=/mnt/c/PageRankData/${DATASET}.txt
    OUTPUT=$($EXEC $FILE 20 0.85 $THREADS)

    NODES=$(echo "$OUTPUT" | grep "Nodes:" | awk '{print $2}')
    EDGES=$(echo "$OUTPUT" | grep "Edges:" | awk '{print $2}')
    ITER=$(echo "$OUTPUT" | grep "Iterations:" | awk '{print $2}')
    TIME=$(echo "$OUTPUT" | grep "Time:" | awk '{print $2}')
    DIFF=$(echo "$OUTPUT" | grep "Last diff:" | awk '{print $3}')

    echo "$DATASET,$NODES,$EDGES,$THREADS,$ITER,$TIME,$DIFF" >> $OUT
  done
done

cat $OUT
