from flask import Flask, render_template, request
import pokebase as pb
import time
import json
app = Flask(__name__)

@app.route('/')
def index():
    return 'Welcome! Go to /pokemon/{pokemon id} to check out data!'


@app.route('/pokemon/<pid>')
@app.route('/pokemon/<pid>/')
def fetch_pokemon(pid):
    start_time = time.time()
    pid = pid.lower()
    # Verify that pokemon exists
    print('Checking that pokemon exists...')
    pokemon = pokemon_exists(pid)
    if not pokemon:
        return 'Invalid Pokemon entered; please check spelling'

    pid = pid.capitalize()
    print('Fetching sprite...')
    shiny = request.args.get('shiny')
    if shiny:
        print('User selected the shiny sprite!')
        sprite = pokemon.sprites.front_shiny
    else:
        sprite = pokemon.sprites.front_default
    print('Getting types...')
    types = get_types(pokemon)
    print('Getting wrs...')
    wrs = weaknesses(pokemon)
    final_wrs = []
    for t, e in wrs.items():
        prefix = ''
        if e == 0:
            prefix = 'NO EFFECT'
        elif e < 1:
            prefix = 'Not very effective'
        elif e <= 2:
            prefix = 'Super effective'
        elif e <= 4:
            prefix = 'SUPER EFFECTIVE'
        final_wrs.append('{}: {} type moves do {}% damage against {}.'.format(prefix, t.capitalize(), int(e * 100), pid))
    print('Rendering template...')
    return render_template('pokemon.html', name=pid, sprite_url=sprite, types=types, wrs=final_wrs, run_time=time.time() - start_time)


def pokemon_exists(pid):
    pid = pid.lower()
    try:
        pokemon = pb.pokemon(pid)
    except:
        return False
    else:
        return pokemon


def get_types(pokemon):
    types = pokemon.types
    result = []
    for t in types:
        result.append(t.type.name.capitalize())
    return result


def weaknesses(pokemon):
    types = pokemon.types
    wrs = {}
    tids = []
    for t in types:
        tids.append(t.type.name)

    for t in tids:
        data = pb.type_(t).damage_relations
        for immunity in data.no_damage_from:
            wrs[immunity['name']] = 0
        for half in data.half_damage_from:
            if half['name'] not in list(wrs.keys()):
                wrs[half['name']] = 0.5
            else:
                wrs[half['name']] /= 2
        for double in data.double_damage_from:
            if double['name'] not in list(wrs.keys()):
                wrs[double['name']] = 2
            else:
                wrs[double['name']] *= 2

    for t in list(wrs.keys()):
        if wrs[t] == 1:
            del wrs[t]

    return wrs

