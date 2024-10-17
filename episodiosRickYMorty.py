import requests
import json

API_URL = 'https://rickandmortyapi.com/api/episode'

def obtener_datos(url):
    """Obtener datos de la URL proporcionada y manejar errores HTTP."""
    try:
        respuesta = requests.get(url)
        respuesta.raise_for_status()
        return respuesta.json()
    except requests.exceptions.RequestException as e:
        print(f'Error al obtener datos de {url}: {e}')
        return None

def obtener_episodios():
    """Obtener la lista de episodios disponibles."""
    episodios_data = obtener_datos(API_URL)
    if episodios_data:
        return episodios_data.get('results', [])
    return []

def mostrar_episodios(episodios):
    """Mostrar la lista de episodios."""
    print("Episodios disponibles:")
    for episodio in episodios:
        print(f"{episodio['id']}: {episodio['name']}")

def obtener_personajes_por_episodio(episodio):
    """Obtener nombres de personajes del episodio especificado."""
    datos_episodio = obtener_datos(f'{API_URL}/{episodio}')
    
    if not datos_episodio:
        return []

    urls_personajes = datos_episodio.get('characters', [])
    personajes = []

    for url in urls_personajes:
        datos_personaje = obtener_datos(url)
        if datos_personaje:
            personajes.append(datos_personaje.get('name'))

    return personajes

def guardar_personajes_en_archivo(episodio, personajes):
    """Guardar la lista de personajes en un archivo JSON."""
    nombre_archivo = f'episodio_{episodio}_personajes.json'
    try:
        with open(nombre_archivo, 'w') as archivo:
            json.dump(personajes, archivo, indent=4)
    except IOError as e:
        print(f'Error al guardar el archivo: {e}')

def main():
    """Función principal de ejecución."""
    episodios = obtener_episodios()
    mostrar_episodios(episodios)

    try:
        episodio_id = int(input("Introduce el número del episodio que deseas consultar: "))
        
        if any(episodio['id'] == episodio_id for episodio in episodios):
            personajes = obtener_personajes_por_episodio(episodio_id)
            guardar_personajes_en_archivo(episodio_id, personajes)
            print(f'Personajes en el episodio {episodio_id}:')
            for personaje in personajes:
                print(f"- {personaje}")
        else:
            print("El episodio seleccionado no existe. Por favor, elige un número válido.")
    except ValueError:
        print("Entrada no valida. Por favor, introduce un episodio valido")
    except Exception as e:
        print(f'Ha ocurrido un error: {e}')

if __name__ == "__main__":
    main()