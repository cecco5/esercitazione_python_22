"""ESERCIZIO 1:
Scrivere un'unica FUNZIONE in cui viene interrogato il DEM andando ad aggiungere ad ogni csv il valore di quota
corrispondente alle coordinate indicate, successivamente trasformare i csv in shapefile. Gli shapefile finali dovranno
avere tutti gli attributi presenti nei csv iniziali con aggiunta la quota. Sarà quindi necessario ripetere
 il procedimento su tutti i file della cartella utilizzando il ciclo glob. ATTENZIONE il DEM ha un sistema
 di riferimento differente da quello delle coordinate dei csv, sarà quindi necessario
 riproiettarlo (questo lo potete fare all'esterno della funzione).
sostanzialmente questo esercizio corrisponde a scrivere come una funzione l'ultimo script fatto a lezione andando,
ovviamente, a adattarlo alla nuova tipologia di csv utilizzati.
"""