import requests
import json

# Get a list of all pokemon species
def get_species():
    # Get csv file
    req = requests.get('https://raw.githubusercontent.com/PokeAPI/pokeapi/master/data/v2/csv/pokemon_species.csv')
    data = req.text
    # Prepare data for iteration
    rows = data.split('\n')
    del rows[0]
    del rows[-1]
    # Loop through data
    pokemon = []
    for row in rows:
        current = row.split(',')
        pokemon.append(current[1])

    return pokemon


if __name__ == '__main__':
    # Get list of pokemon
    species = get_species()
    # Open species file and write new data
    species_file = open('data/species.json', 'w')
    species_file.write(json.dumps(species) + '\n')
    species_file.close()
