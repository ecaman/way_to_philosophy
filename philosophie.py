#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Ne pas se soucier de ces imports
import setpath
from flask import Flask, render_template, session, request, redirect, flash
from getpage import getPage

app = Flask(__name__)

app.secret_key = "TODO: mettre une valeur secrète ici"

cheat = 0
current_links = []

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', message="Hello, World!")

# Si vous définissez de nouvelles routes, faites-le ici
@app.route('/new_game', methods=['POST'])
def new_game():
    global cheat
    cheat = 0
    global current_links
    current_links = []
    session['article'] = request.form['start']
    session['score'] = 0
    first_page_title, first_page_links = getPage(session['article'])
    first_page_links = [x[1] for x in first_page_links]
    if(str(session['article']).lower() == "philosophie"):
        message = "Un peu trop simple de commencer par Philosophie"
        return render_template('index.html', message=message)
    elif(first_page_title == None):
        message="Votre page n'éxiste pas"
        return render_template('index.html', message=message)
    elif(len(first_page_links) == 0):
        message="La page demandée ne comporte pas de liens"
        return render_template('index.html', message=message)
    elif("Philosophie" in first_page_links):
        message="Votre page de départ contient déjà un lien vers Philosophie"
        return render_template('index.html', message=message)
    else:
        return redirect('/game')


@app.route('/game', methods=['GET'])
def game():
    global cheat
    cheat += 1
    global current_links

    if(session['article'] == "Philosophie"):
        mes = "Félicitation vous avez gagné en " + str(session['score']) + ' coups'
        flash(mes, category='message')
        return redirect('/')
    else:
        title, links = getPage(session['article'])
        current_links = [x[0] for x in links]
        current = title
        if(len(links) == 0):
            return render_template('index.html', message="Ohlala! Pas de lien depuis cette page, vous avez perdu :'( ")
        session['links'] = links
    return render_template('game.html', cheat = cheat, current = current)


@app.route('/move', methods=['POST'])
def move():
    global cheat
    cheat = 0
    session['score'] += 1
    if(request.form['destination'] in current_links):
        session['article'] = request.form['destination']
        return redirect('/game')
    else:
        return render_template('index.html', message=str(request.form['destination']) + str(current_links))


if __name__ == '__main__':
    app.run(debug=True, threaded=True)
