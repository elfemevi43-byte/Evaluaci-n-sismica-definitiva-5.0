import rasterio
import pandas as pd

REDUCCION = 20  # cambia a 10 o 15

with rasterio.open("VS30.tif") as src:
    banda = src.read(1)
    transform = src.transform
    nodata = src.nodata

    filas, columnas = banda.shape
    print(f"Tamaño del raster: {filas} x {columnas}")

    datos = []
    contador = 0

    for row in range(0, filas, REDUCCION):
        for col in range(0, columnas, REDUCCION):

            valor = banda[row, col]

            if valor == nodata:
                continue

            lon, lat = rasterio.transform.xy(transform, row, col)

            datos.append([lat, lon, int(valor)])
            contador += 1

    print(f"Puntos guardados: {contador}")

df = pd.DataFrame(datos, columns=["lat", "lon", "valor"])
df.to_csv("vs30_reducido.csv", index=False)

print("Conversión optimizada terminada.")