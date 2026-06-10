#!/bin/bash

EXEC=src/pagerank
RAW=results/raw_times.csv

echo "dataset,nodes,edges,threads,iterations,rep,time,last_diff" > $RAW

for DATASET in web-Stanford web-Google web-BerkStan
do
  for THREADS in 1 2 4 8
  do
    for REP in 1 2 3 4 5
    do
      FILE=/mnt/c/PageRankData/${DATASET}.txt
      OUTPUT=$($EXEC $FILE 100 0.85 $THREADS)

      NODES=$(echo "$OUTPUT" | grep "Nodes:" | awk '{print $2}')
      EDGES=$(echo "$OUTPUT" | grep "Edges:" | awk '{print $2}')
      ITER=$(echo "$OUTPUT" | grep "Iterations:" | awk '{print $2}')
      TIME=$(echo "$OUTPUT" | grep "Time:" | awk '{print $2}')
      DIFF=$(echo "$OUTPUT" | grep "Last diff:" | awk '{print $3}')

      echo "$DATASET,$NODES,$EDGES,$THREADS,$ITER,$REP,$TIME,$DIFF" >> $RAW
      echo "$DATASET threads=$THREADS rep=$REP time=$TIME"
    done
  done
done
