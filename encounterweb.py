from flask import Blueprint, render_template, redirect, url_for, session, request
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
        'id': id,
        'type': type,
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

    session['current_turn'] = 0
    session['num_of_turns'] = len(initiative_list)
    session['round'] = 1

    return redirect(url_for('dm-tools.encounter.main'))

@encounter_bp.route('/', methods=['GET', 'POST'])
def main():
    monsters: list[dict] = session['monsters']
    monster_types = session['monster_types']
    initiative = session['initiative']
    current_turn =  session['current_turn']
    current_round = session['round']

    if request.method == 'POST':
        for monster in monsters:
            form_name = monster['name']
            if request.form.get(f'{form_name} +') == '+':
                monster['current_HP'] += 1
            if request.form.get(f'{form_name} -') == '-':
                monster['current_HP'] -= 1

        if request.form.get('add_monster') == 'Add monster(s)':
            session['selected_monsters'] = []
            session['add_monsters'] = True
            session['monsters'] = monsters
            session['monster_types'] = monster_types
            session['initiative'] = initiative
            return redirect(url_for('dm-tools.encounter.setup.monsters'))
        
        if request.form.get('next_turn') == 'Move to Next Turn':
            current_turn += 1
            if current_turn > session['num_of_turns'] - 1:
                current_turn = 0
                current_round += 1


    session['monsters'] = monsters
    session['monster_types'] = monster_types
    session['initiative'] = initiative
    session['current_turn'] = current_turn
    session['round'] = current_round

    return render_template('encounter.html', monsters=monsters, monster_types=[type.split('\n') for type in monster_types], initiative=initiative, current_turn=current_turn, current_round=current_round)

@encounter_bp.route('/add-monsters')
def add_monsters():
    new_monsters = session['selected_monsters']
    new_monsters = [add_enemy(f'monsters/{enemy}.txt', 0) for enemy in new_monsters]
    monster_types = session['monster_types']
    old_monsters = session['monsters']

    for enemy in new_monsters:
            matching_type = False
            for type in monster_types:
                if type == enemy['full_stats']:
                    matching_type = True
                    highest_id = 0
                    for og_monster in old_monsters:
                        if og_monster['id'] >= highest_id and og_monster['full_stats'] == type:
                            highest_id = og_monster['id']
                    enemy['id'] = highest_id + 1
                    enemy_id = enemy['id']
                    enemy['name'] = enemy['type'][0:-1] + f' {enemy_id}'
            if matching_type == False:
                enemy['id'] = 1
                enemy_id = enemy['id']
                enemy['name'] = enemy['type'][0:-1] + f' {enemy_id}'
                
                        
            old_monsters.append(enemy)
            old_monsters.sort(key=lambda x: x['name'][0:-2])
    
    session['monsters'] = old_monsters

    return redirect(url_for('dm-tools.encounter.main'))

encounter_bp.register_blueprint(setup_bp, url_prefix='/setup/')