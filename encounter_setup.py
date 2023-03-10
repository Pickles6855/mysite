from flask import Blueprint, session, render_template, url_for, redirect, request
from os import listdir

setup_bp = Blueprint('setup', __name__)

@setup_bp.route('/', methods=['GET', 'POST'])
def setup_encounter():
    session['selected_monsters'] = []
    return redirect(url_for('dm-tools.encounter.setup.monsters'))


@setup_bp.route('/monsters', methods=['GET', 'POST'])
def monsters():

    loaded_monsters = sorted([monster[0:-4] for monster in listdir('monsters')])
    selected_monsters = session['selected_monsters']

    if request.method == 'POST':
        for monster in loaded_monsters:
            if request.form.get(monster) == monster.capitalize():
                selected_monsters.append(monster)

        for monster in selected_monsters:
            if request.form.get(f'remove_{monster}') == monster.capitalize():
                selected_monsters.pop(selected_monsters.index(monster))
            
        if request.form.get('submit') == 'Select Monsters':
            session['selected_monsters'] = sorted(selected_monsters)
            session['initiative_list'] = []
            return redirect(url_for('dm-tools.encounter.setup.initiative'))

    session['selected_monsters'] = sorted(selected_monsters)

    return render_template('choose_monsters.html', loaded_monsters=loaded_monsters, selected_monsters=session['selected_monsters'])


@setup_bp.route('/initiative', methods=['GET', 'POST'])
def initiative():
    initiative_list = session['initiative_list']

    if request.method == 'POST':
        initiative_list.append((request.form.get('name'), request.form.get('roll')))
        if request.form.get('start') == 'Start Encounter':
            session['initiative_list'] = initiative_list
            return redirect(url_for('dm-tools.encounter.init_encounter'))
        print(initiative_list)

    session['initiative_list'] = initiative_list

    return render_template('initiative.html')


@setup_bp.route('/load')
def load_encounter():
    return render_template('load_encounter.html')