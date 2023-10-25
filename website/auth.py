from crypt import methods
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import Subject, User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

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
        print(request.form)
        # verifier les info
        if len(pseudo) < 2 or len(pseudo) > 12 : #precheck
            flash("Pseudo invalide !", category='error')
        elif len(password1)==0 or password1 != password2:
            flash("Les mots de passe ne sont pas valide !", category='error')
        elif len(code) < 3: 
        # TODO : le code d'inivatation
            flash("Code d'inivation invalide !", category='error')
        
        else: #add user to the database
            user = User.query.filter_by(email=email).first() #check if user is alerady in
            if user:
                flash("Email invalide", category='error')
            else:
                NewUser = User(email=email, pseudo=pseudo, password=generate_password_hash(password1, method='sha256'), role=2)
                db.session.add(NewUser)
                db.session.commit()
                login_user(NewUser)
                flash('Compte créer avec succées !', category='info')
                return redirect(url_for('views.home'))
    return render_template("sign_up.html", user=current_user, Subject=Subject)