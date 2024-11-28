#!/bin/sh
ARQUIVODADOS=/home/pi/ESZB026-17-4-2024C/lab07/gnuplot/dados.txt
ARQUIVOSAIDA=/home/pi/ESZB026-17-4-2024C/lab07/gnuplot/dados.png

gnuplot << EOF
set title "Título"
set ylabel "Eixo Y"
set xlabel "Eixo X"
set terminal png
set output "$ARQUIVOSAIDA"
plot "$ARQUIVODADOS" \
     linecolor rgb '#ffcccc' \
     linetype 1 \
     linewidth 5 \
     pointtype 2 \
     pointsize 1.0 \
     title "meus dados" \
     with linespoints
EOF

