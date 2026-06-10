# Datasets

Los datasets usados en este proyecto son grafos web públicos de SNAP Stanford.

Comandos de descarga:

~~~bash
curl --ssl-no-revoke -L -o web-Stanford.txt.gz https://snap.stanford.edu/data/web-Stanford.txt.gz
curl --ssl-no-revoke -L -o web-Google.txt.gz https://snap.stanford.edu/data/web-Google.txt.gz
curl --ssl-no-revoke -L -o web-BerkStan.txt.gz https://snap.stanford.edu/data/web-BerkStan.txt.gz
~~~

Después de descargar los archivos, se deben descomprimir los `.gz` y colocar los `.txt` en esta carpeta:

~~~text
data/web-Stanford.txt
data/web-Google.txt
data/web-BerkStan.txt
~~~

Estos archivos no se incluyen en el repositorio de GitHub debido a su tamaño.
