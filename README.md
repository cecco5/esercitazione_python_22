# esercitazione_python_22

Tra i materiali in allegato troverete:

    - Un DEM della lombardia a 100m in UTM ED50 32N (EPSG:32032)  
    - Una cartella contenete shapefile puntuali dei comuni lombardi divisi per provincia
    - Un'altra cartella contenente lo stesso tipo di dato ma in formato csv
    - Il sistema di riferimento degli shapefile e delle coordinate dei csv è UTM WGS84 32N (EPSG:32632), quindi un sistema di riferimento differente da quello del DEM.

Al fine del superamento dell'esame sarà necessario scrivere e COMMENTARE DETTAGLIATAMENTE almeno lo script dell'esercizio 1. 
Per chi volesse approfondire, vi lascio altri due esercizi opzionali.

ESERCIZIO 1:
Scrivere un'unica FUNZIONE in cui viene interrogato il DEM andando ad aggiungere ad ogni csv il valore di quota corrispondente alle coordinate indicate, successivamente trasformare i csv in shapefile. Gli shapefile finali dovranno avere tutti gli attributi presenti nei csv iniziali con aggiunta la quota. Sarà quindi necessario ripetere il procedimento su tutti i file della cartella utilizzando il ciclo glob. ATTENZIONE il DEM ha un sistema di riferimento differente da quello delle coordinate dei csv, sarà quindi necessario riproiettarlo (questo lo potete fare all'esterno della funzione).
sostanzialmente questo esercizio corrisponde a scrivere come una funzione l'ultimo script fatto a lezione andando, ovviamente, a adattarlo alla nuova tipologia di csv utilizzati.

ESERCIZIO 2 (opzionale):
Sostanzialmente l'esercizio è uguale all'esercizio 1 ma questa volta non dovrete utilizzare il csv ma ciclando direttamente gli shapefile nell'apposita cartella. Come noterete, gli shapefile non hanno tra gli attributi i valori delle coordinate che dovrete estrarle dalla geometria.

ESERCIZIO 3 (opzionale):
Questo in questo esercizio, più complesso, bisognerà riproiettare gli shapefile con lo stesso sistema di riferimento del DEM (UTM ED50 32N) per poi interrogarli per ottenere in valore della quota. Quindi i nuovi shapefile creati dovranno avere come sistema di riferimento UTM ED50 32N, in questo caso il sistema di riferimento non dovete scriverlo voi ma estrarlo dal DEM.

Per gli esercizi 2 e 3 può tornarvi molto utile questo esempio:
https://gis.stackexchange.com/questions/46893/getting-pixel-value-of-gdal-raster-under-ogr-point-without-numpy?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa
