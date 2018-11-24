from flask import Flask, render_template, flash, request, redirect, url_for
from forms import RegistrationForm, LoginForm
import sys
import os



app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY')


@app.route('/')
@app.route('/home')
def home():
    context = {
        'title':"Welcome",
        }
    return render_template("home.html",context=context)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    context = {
        'form':form,
        }
    if form.validate_on_submit():
        print(form.data, file=sys.stdout)
        flash(f'Successfully for Logged In!', 'success')
        return redirect(url_for('home'))
    return render_template("login.html",context=context)

@app.route('/register', methods=['GET', 'POST'])
def register():
    # print('This is error output', file=sys.stderr)
    form = RegistrationForm()
    context = {
        'form':form,
        }

    if form.validate_on_submit():
        print(form.data, file=sys.stdout)
        flash(f'Account Created successfully for { form.username.data }!', 'success')
        return redirect(url_for('home'))
    return render_template("register.html",context=context)



if __name__ == '__main__':
    app.run(debug =True)
