#codigo mas completo()

import requests
import re
import json

API_KEY = '8672905b631a8a0b3a41a62affffec7f'

def validar_fecha(fecha):
    return re.match(r"^\d{4}-\d{2}-\d{2}$", fecha) is not None

def obtener_generos():
    url = f"https://api.themoviedb.org/3/genre/movie/list?api_key={API_KEY}&language=es"
    response = requests.get(url)
    return response.json()["genres"]

def buscar_peliculas(generos, desde, hasta, top_n=10, orden="desc"):
    ids_generos = ",".join(str(g["id"]) for g in generos)
    url = (
        f"https://api.themoviedb.org/3/discover/movie?api_key={API_KEY}&language=es"
        f"&sort_by=vote_average.{orden}&vote_count.gte=100"
        f"&with_genres={ids_generos}"
        f"&primary_release_date.gte={desde}&primary_release_date.lte={hasta}"
        f"&page=1"
    )
    response = requests.get(url)
    return response.json()["results"][:top_n]

def mostrar_menu():
    print("=== Catálogo de Películas ===\n")

    generos = obtener_generos()
    print("Géneros disponibles:")
    for i, g in enumerate(generos, 1):
        print(f"{i}. {g['name']}")

    indices = input("\nIngresa los números de los géneros separados por comas (ej. 1,3): ")
    indices = [int(i.strip()) - 1 for i in indices.split(",")]
    generos_elegidos = [generos[i] for i in indices]

    desde = input("\nDesde qué fecha (formato YYYY-MM-DD): ")
    while not validar_fecha(desde):
        desde = input("Fecha inválida. Intenta de nuevo (YYYY-MM-DD): ")

    hasta = input("Hasta qué fecha (formato YYYY-MM-DD): ")
    while not validar_fecha(hasta):
        hasta = input("Fecha inválida. Intenta de nuevo (YYYY-MM-DD): ")

    while True:
        orden = input("¿Deseas ver las mejores o peores películas? (mejores/peores): ").strip().lower()
        if orden in ["mejores", "peores"]:
            break
        print("Opción no válida. Escribe 'mejores' o 'peores'.")

    orden = "desc" if orden == "mejores" else "asc"


    top_n = input("¿Cuántas películas deseas ver? (por defecto 10): ")
    top_n = int(top_n) if top_n.isdigit() else 10

    peliculas = buscar_peliculas(generos_elegidos, desde, hasta, top_n, orden)

    print("\n=== Resultados ===\n")
    for i, peli in enumerate(peliculas, 1):
        print(f"{i}. {peli['title']} ({peli['release_date']}) - {peli['vote_average']}")

    # Exportar a JSON
    with open("peliculas_resultado.json", "w", encoding="utf-8") as f:
        json.dump(peliculas, f, ensure_ascii=False, indent=4)
    print("\nResultados guardados en 'peliculas_resultado.json'.")

     # Exportar a TXT
    with open("peliculas_resultado.txt", "w", encoding="utf-8") as f:
        for i, peli in enumerate(peliculas, 1):
            f.write(f"{i}. {peli['title']} ({peli['release_date']}) - {peli['vote_average']}\n")
    print("Resultados también guardados en 'peliculas_resultado.txt'.")

if __name__ == "__main__":
    mostrar_menu()
