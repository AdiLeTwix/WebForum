from crypt import methods
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import Subject, User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from datetime import datetime

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        #check if user exist
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password): #check password
                login_user(user, remember=True)
                flash('Connexion réussie.', category='info')
                dest = request.args.get('next', url_for('views.home'))
                return redirect(dest)
        flash('Mot de passe ou email invalide !', category='error')
    return render_template("login.html", display=True, user=current_user, Subject=Subject)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Vous êtes désormais déconnecté.', category='warning')
    return redirect(url_for('auth.login'))
    
@auth.route('/sign-up', methods=['GET', 'POST'])
def singup():
    if request.method == 'POST':
        email = request.form.get('email')
        pseudo = request.form.get('pseudo')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        code = request.form.get('code')
        # precheck
        if len(pseudo) < 2 or len(pseudo) > 12 :
            flash("Pseudo invalide !", category='error')
        elif len(password1)==0 or password1 != password2:
            flash("Les mots de passe ne sont pas indentique / invalide !", category='error')
        elif len(code) < 3: 
        # TODO : le code d'inivatation
            flash("Code d'inivation invalide !", category='error')
        
        else: # add user to the database
            # write the in log
            f = open("./logs/code.log", "a")
            time = datetime.now()
            f.write(f"{email};{pseudo};{code};{time}\n")
            f.close()
            user = User.query.filter_by(email=email).first() #check if user is alerady in
            if user:
                flash("Email invalide", category='error')
            else:
                NewUser = User(email=email, pseudo=pseudo, password=generate_password_hash(password1, method='sha256'), role=1) # todo : code d'invit link au role
                db.session.add(NewUser)
                db.session.commit()
                login_user(NewUser)
                flash('Compte créer avec succées !', category='info')
                return redirect(url_for('views.home'))
    return render_template("sign_up.html", user=current_user, Subject=Subject)