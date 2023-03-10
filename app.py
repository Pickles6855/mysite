from flask import Flask, render_template, url_for, request
from datetime import datetime
from os.path import join
from dm_tools import dm_tools_bp

app = Flask(__name__)
app.secret_key = 'ilikepickles'

@app.route('/')
def home():
    return render_template('home.html', 
                           links={'home': url_for('home'), 
                                  'projects': url_for('projects'), 
                                  'about': url_for('aboutme'), 
                                  'survey': url_for('survey'),
                                  'dm-tools': url_for('dm-tools.start')
                                  }
                           )

@app.route('/projects')
def projects():
    return render_template('projects.html', links={'home': url_for('home'), 
                                  'projects': url_for('projects'), 
                                  'about': url_for('aboutme'), 
                                  'survey': url_for('survey')
                                  }
                            )

@app.route('/about-me')
def aboutme():
    return render_template('aboutme.html', links={'home': url_for('home'), 
                                  'projects': url_for('projects'), 
                                  'about': url_for('aboutme'), 
                                  'survey': url_for('survey')
                                  }
                           )

@app.route('/survey', methods=['GET', 'POST'])
def survey():
    if request.method == 'POST':
        fname = request.form.get('first_name')
        lname=request.form.get('last_name')
        with open(join('data', 'survey.txt'), 'a') as survey_data:
            current_time = datetime.now()
            survey_data.write(f'[{current_time}] {fname} {lname}\n')

        return render_template('surveycomplete.html', fname=fname, lname=lname, links={'home': url_for('home'), 
                                  'projects': url_for('projects'), 
                                  'about': url_for('aboutme'), 
                                  'survey': url_for('survey')
                                  }
                               )
    
    return render_template('survey.html', links={'home': url_for('home'), 
                                  'projects': url_for('projects'), 
                                  'about': url_for('aboutme'), 
                                  'survey': url_for('survey')
                                  }
                               )

app.register_blueprint(dm_tools_bp, url_prefix='/dm-tools/')


if __name__ == '__main__':
    app.run(debug=True, port=8800)