from flask import Flask, render_template, flash, request, url_for
from werkzeug.utils import redirect
from wtforms import Form, BooleanField, StringField, PasswordField, validators, SelectField
from wtforms.validators import DataRequired

REMOTE_HOST='admin@172.30.23.112'
BASELINE_PATH='/home/admin/Server/storage.rpr/www/html/rpr-plugins/'
JOBS_PATH='/home/admin/Server/RPRServers/jenkins_server/data/jobs'
JOBS_LIST=["RadeonProRenderBlender2.8PluginAuto", "RadeonProRenderBlender2.8PluginManual", "RadeonProRenderBlender2.8Plugin-WeeklyFull"
           ,"RadeonProRenderBlender2.81Test", "RadeonProRenderCoreAuto", "RadeonProRenderCoreManual", "RadeonProRenderCreoPluginManual"
           ,"RadeonProRenderMaxPluginAuto", "RadeonProRenderMaxPluginManual", "RadeonProRenderMaxPlugin-WeeklyFull", "RadeonProRenderMayaPluginAuto"
           ,"RadeonProRenderMayaPluginManual", "RadeonProRenderMayaPlugin-WeeklyFull"
           ]
RPR_PREFIX = "RadeonProRender"

app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

def refreshJob(form):
    form.job.choices = [j for j in list(filter(lambda x: x.startswith(RPR_PREFIX+form.tool.data), JOBS_LIST))]

class SelectionForm(Form):
    tool = SelectField("Tool", choices=[("Maya","Maya"),("Blender","Blender"),("Max","Max"),("Core","Core"), ("Creo","Creo")])
    job = SelectField("Job", choices=[])
    build = SelectField("Build", choices=[(394,"#394"),(393,"#393")])
    test_group = SelectField("Test Group", choices=[("SM","Smoke"), ("IBL", "IBL")])
    test_case = SelectField("Test Case", choices=[("SM_01","SM_01"),("SM_02","SM_02")])

@app.route('/', methods=['GET', 'POST'])
def hello_user():
    form = SelectionForm(request.form)
    form.job.choices = [j for j in list(filter(lambda x: x.startswith(RPR_PREFIX+form.tool.data), JOBS_LIST))]
    return render_template('renderForm.html', form=form)

if __name__ == "__main__":
    app.run()

'''@app.route('/login', methods=['GET', 'POST'])
def login():
    return \'''
        <form method="post">
            <p><input type=text name=username>
            <p><input type=submit value=Login>
        </form>
    \'''

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User(form.username.data, form.email.data,
                    form.password.data)
        flash('Thanks for registering')
        return redirect(url_for('login'))
    return render_template('renderForm.html', form=form)
    
class RegisrationForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the TOS', [validators.DataRequired()])    
    '''
