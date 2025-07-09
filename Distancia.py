import requests

def geocodificar(ciudad, api_key):
    url = "https://graphhopper.com/api/1/geocode"
    params = {
        "q": ciudad,
        "locale": "es",
        "limit": 1,
        "key": api_key
    }
    r = requests.get(url, params=params)
    datos = r.json()
    if datos["hits"]:
        punto = datos["hits"][0]["point"]
        return punto["lat"], punto["lng"]
    else:
        raise Exception(f"No se encontró la ciudad: {ciudad}")

def obtener_ruta(lat_origen, lng_origen, lat_destino, lng_destino, transporte, api_key):
    url = "https://graphhopper.com/api/1/route"
    params = {
        "point": [f"{lat_origen},{lng_origen}", f"{lat_destino},{lng_destino}"],
        "vehicle": transporte,
        "locale": "es",
        "instructions": "true",
        "calc_points": "true",
        "key": api_key
    }
    r = requests.get(url, params=params)
    return r.json()

def mostrar_resultados(ruta):
    path = ruta["paths"][0]
    distancia_km = path["distance"] / 1000
    distancia_mi = distancia_km * 0.621371
    duracion_min = path["time"] / 60000

    print(f"\nDistancia: {distancia_km:.2f} km / {distancia_mi:.2f} mi")
    print(f"Duración estimada: {duracion_min:.1f} minutos")

    print("\nNarrativa del viaje:")
    for paso in path["instructions"]:
        print(f"- {paso['text']}")

def seleccionar_transporte():
    print("\nSeleccione el medio de transporte:")
    print("1. Auto")
    print("2. Bicicleta")
    print("3. Caminando")
    opcion = input("Opción [1-3]: ")
    if opcion == "2":
        return "bike"
    elif opcion == "3":
        return "foot"
    else:
        return "car"

def main():
    api_key = "cd673793-7963-4ffe-a5e9-f21a702b5eab"

    while True:
        print("\nIngrese 's' para salir.")
        origen = input("Ciudad de Origen: ")
        if origen.lower() == 's':
            break
        destino = input("Ciudad de Destino: ")
        if destino.lower() == 's':
            break

        try:
            transporte = seleccionar_transporte()
            lat_o, lng_o = geocodificar(origen, api_key)
            lat_d, lng_d = geocodificar(destino, api_key)
            ruta = obtener_ruta(lat_o, lng_o, lat_d, lng_d, transporte, api_key)
            mostrar_resultados(ruta)
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
