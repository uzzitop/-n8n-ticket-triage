import csv  
aciertos=0
total=0
fallos=[]
with open("results.csv", newline="", encoding="utf-8") as archivo:
    filas = list(csv.DictReader(archivo,delimiter=";"))

for fila in filas:
    total += 1
    if fila["modelo"].strip().lower()==fila["esperada"].strip().lower():
        aciertos+=1
    else   :
        fallos.append(fila["n"])
print(f"Aciertos: {aciertos} de {total}")
print("Fallaron los mensajes:", ", ".join(fallos) if fallos else "ninguno")