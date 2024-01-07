# everything that's not relate to authentication that use can navigate to we're going to put it in here.
from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import *
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/', methods=[
    'GET',
    'POST'
])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')
        if len(note) < 1:
            flash('Content Required', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note Added!', category='success')

        

    return render_template("home.html", user=current_user)

@views.route('/delete-note', methods=[
    'POST'
])
def delete_note():
    note = json.loads(request.data)
    print(note)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:     # this is security check, to see if the note is indedd that user's note, otherwise can't delete it.
            db.session.delete(note)
            db.session.commit()
    
    return jsonify({})
    
