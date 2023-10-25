from cmath import log
from crypt import methods
import os
import string
from flask import Blueprint, render_template, send_from_directory, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user

from sqlalchemy import desc

from .defaultSub import GetSupp
from .models import Note, Subject, User, Invite
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET','POST'])
def welcome():
    return render_template("subject.html", user=current_user, User=User, subject=Subject.query.filter_by(name='test').first(), Subject=Subject)


@views.route('/my', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')
        subj = request.form.get('subject')
        newTitle = request.form.get('title')

        if len(note) < 3:
            flash('La note est trop courte', category='error')
        else:
            current_subject = Subject.query.filter_by(name=subj).first()
            if current_subject:
                new_note = Note(data=note, user_id=current_user.id, subject_id=current_subject.id, title=newTitle)
                db.session.add(new_note)
                db.session.commit()
                flash('Note publié !', category='info')
                return redirect(url_for('views.home'))
            else:
                flash('Sujet invalide.', category='error')


    return render_template("home.html", user=current_user, Subject = Subject, User = User, isHome = True)

@views.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(views.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@views.route('/delete-note', methods=['POST'])
@login_required
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    snote = Note.query.get(noteId)
    if snote and snote.user_id == current_user.id :
        db.session.delete(snote)
        db.session.commit()
        flash('Note suprpimé', category='info')
    else:
        flash("Impossible de faire ceci", category='error')
    return jsonify({})


@views.route('/manage-subjects', methods=['GET','POST'])
@login_required
def add_subject():
    if request.method == 'POST':
        if str(list(request.form.to_dict(flat=False))[0]) == "addSub":
            new_subject = request.form.get('addSub')
            if len(new_subject) < 3:
                flash('Nom trop court', category='error')
            else:
                try_sub = Subject.query.filter_by(name=new_subject).first()
                if try_sub:
                    flash("Ce sujet existe déja", category='error')
                else:
                    NewSubject = Subject(name=new_subject)
                    db.session.add(NewSubject)
                    db.session.commit()
                    flash("Sujet ajouter !", category='info')
        else:
            target = request.form.get("removeSub")
            try_sub = Subject.query.filter_by(name=target).first()
            if try_sub:
                if(request.form.get("customRadio")) == 'MV':
                    mv = GetSupp()
                    for note in try_sub.notes:
                        note.subject_id = mv.id
                        db.session.commit()
                else:
                    for note in try_sub.notes:
                        db.session.delete(note)
                        db.session.commit()

                db.session.delete(try_sub)
                db.session.commit()
                flash("Sujet suprrimé", category='info')
            else:
                flash("Sujet inexistant", category='error')

    return render_template("admin/edit_subjects.html", user=current_user, Subject=Subject)




@views.route('/subject/<name>', methods=['GET','POST'])
def send_subject(name):
    return render_template("subject.html", user=current_user, User=User, subject=Subject.query.filter_by(name=name).first(), Subject=Subject)


@views.route('/manage-code', methods=['GET', 'POST'])
@login_required
def manage_code():
    if request.method == 'POST':
        c = request.form.get("code")
        exist = Invite.query.filter_by(code=c).first() #check if user is alerady in
        if exist:
            flash("Ce code existe déja", category='error')
        else:
            newInv = Invite(code = c, usages=0)
            db.session.add(newInv)
            db.session.commit()
            flash("Code ajouté", category='sucesse')

            
    f = open("./logs/code.log", "r")
    l = f.read()
    f.close()
    return render_template("admin/manage_code.html", user=current_user, Subject=Subject, Invite=Invite, logs=l)


@views.route('/manage-user', methods= ['GET','POST'])
@login_required
def manage_user():
    if request.method == 'POST':
        print(request.form)
    page = request.args.get('sort')
    if page == 'role':
            ulist = db.session.query(User).order_by(desc(User.role))
    elif page == 'name':
        ulist = db.session.query(User).order_by(desc(User.pseudo))
    else:
            ulist = db.session.query(User).order_by(desc(User.id))
    return render_template("admin/manage_user.html", user=current_user, Subject=Subject, users=ulist)
    
 
@views.route('/user/<u>', methods= ['GET'])
@login_required
def user(u):
    page = request.args.get('page', 0, type=int)
    T = User.query.filter_by(pseudo=u).first()
    if T:
        return render_template("user.html", user=current_user, User=User, Subject=Subject, target=T, code=Invite.query.filter_by(id=T.code_id).first(), page=page)
    else:
        return render_template("test.html", user=current_user, Subject=Subject) # TODO page 404 user

@views.route('/test', methods= ['GET','POST'])
def test():
    if request.method == 'POST':
        print(request.form)
    return render_template("test.html", user=current_user, Subject=Subject)