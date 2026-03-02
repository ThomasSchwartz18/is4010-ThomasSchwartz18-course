import requests


def get_api_data(url):
    """Fetch and parse JSON data from an API URL."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as error:
        print(f"Error making request: {error}")
        return None
    except ValueError:
        print("Error: Failed to decode JSON from response.")
        return None


if __name__ == "__main__":
    pokemon_url = "https://pokeapi.co/api/v2/pokemon/snorlax"
    pokemon_data = get_api_data(pokemon_url)

    if pokemon_data:
        print(f"Successfully fetched data for: {pokemon_data['name'].title()}")
        print(f"Weight: {pokemon_data['weight']} hectograms")
        print("Abilities:")
        for ability in pokemon_data["abilities"]:
            print(f"  - {ability['ability']['name']}")