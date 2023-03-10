from flask import Blueprint, render_template, redirect, url_for, session
from encounter_setup import setup_bp

def add_enemy(enemy_path, id):
    with open(enemy_path, 'r') as stats:
        full_stats = stats.read()
    
        stats.seek(0, 0)

        type = stats.readline()
        name = type[0:-1] + f' {id}'
        [stats.readline() for i in range(4)]
        max_HP = int(stats.readline()[0:2])
        current_HP = max_HP

    return {
        'full_stats': full_stats,
        'name': name,
        'max_HP': max_HP,
        'current_HP': current_HP
    }



encounter_bp = Blueprint('encounter', __name__)

@encounter_bp.route('/init')
def init_encounter():
    # Monsters
    monsters_setup = session['selected_monsters']
    monsters_setup = [add_enemy(f'monsters/{enemy}.txt', 0) for enemy in monsters_setup]

    types_of_monsters = []
    for enemy in monsters_setup:
        if any(types_of_monsters) == True:
            matching_type = False
            for type in types_of_monsters:
                if enemy['full_stats'] == type:
                    matching_type = True
            if matching_type == False:
                types_of_monsters.append(enemy['full_stats'])
        else:
            types_of_monsters.append((enemy['full_stats']))

    monsters = []
    for type in types_of_monsters:
        monsters_of_type = [monster for monster in monsters_setup if monster['full_stats'] == type]
        for i in range(len(monsters_of_type)):
            new_monster_path = type.split('\n')[0].lower()
            monsters.append(add_enemy(f'monsters/{new_monster_path}.txt', i + 1))

    session['monster_types'] = types_of_monsters
    session['monsters'] = monsters


    # Initiative
    initiative_list = session['initiative_list']

    initiative_list = sorted(initiative_list, key=lambda x: x[1])
    initiative_list = [initiative_roll[0] for initiative_roll in initiative_list]
    for initiative in initiative_list:
        if initiative == False:
            initiative_list.remove(initiative)

    session['initiative'] = initiative_list


    return redirect(url_for('dm-tools.encounter.main'))

@encounter_bp.route('/')
def main():
    monsters = session['monsters']
    monster_types = session['monster_types']
    initiative = session['initiative']

    session['monsters'] = monsters
    session['monster_types'] = monster_types
    session['initiative'] = initiative

    return render_template('encounter.html', monsters=monsters, monster_types=[type.split('\n') for type in monster_types], initiative=initiative)

encounter_bp.register_blueprint(setup_bp, url_prefix='/setup/')