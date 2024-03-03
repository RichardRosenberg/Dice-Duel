#Author: Richard Rosenberg
#Date: Nov 14, 2023
#Purpose: A Game of Dice Duel with your friend

from flask import Flask, render_template, request, session, redirect, url_for
import os
import secrets
import random

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        #save user data in session for both players
        session['player1'] = {
            'username': request.form['player1'],
            'avatar': request.form['avatar1'],
            'score': 0
        }
        session['player2'] = {
            'username': request.form['player2'],
            'avatar': request.form['avatar2'],
            'score': 0
        }
        return redirect(url_for('game'))
    return render_template('index.html')

#roll dice function to be called when needed
def roll_dice():
    return random.randint(1, 6)

@app.route('/roll_dice', methods=['GET', 'POST'])
def roll_dice_route():
    #get the session info and check which player turn it is, then roll (when roll is clicked)
    player1_turn = session.get('player1_turn', True)
    current_player = 'player1' if player1_turn else 'player2'
    other_player = 'player2' if player1_turn else 'player1'
    roll_result = roll_dice()
    #statements for if player rolls 1 or if score hits 20+ with appropriate roll_message
    if roll_result == 1:
        session[current_player]['score'] = 0
        session['roll_message'] = f"{session[current_player]['username']} rolled a 1, {session[other_player]['username']}'s turn."
        session['player1_turn'] = not player1_turn
    else:
        session[current_player]['score'] += roll_result
        if session[current_player]['score'] >= 20:
            session['roll_message'] = f"{session[current_player]['username']} wins with {session[current_player]['score']} points!"
        else:
            session['roll_message'] = f"{session[current_player]['username']} rolled a {roll_result}, Roll again or Pass."
    session[f'{current_player}_roll'] = roll_result
    session.pop(f'{other_player}_roll', None)
    return redirect(url_for('game'))

@app.route('/pass')
def pass_turn():
    player1_turn = session.get('player1_turn', True)
    current_player = 'player1' if player1_turn else 'player2'
    session.pop(f'{current_player}_roll', None)
    #change turns
    session['player1_turn'] = not player1_turn
    return redirect(url_for('game'))

#basic route for before game starts
@app.route('/game')
def game():
    player1 = session.get('player1', {})
    player2 = session.get('player2', {})
    player1_turn = session.get('player1_turn', True)
    welcome_message = f"Welcome {player1.get('username', 'Player 1')} and {player2.get('username', 'Player 2')} to Dice Duel!"
    return render_template('game.html', welcome_message=welcome_message, player1=player1, player2=player2, player1_turn=player1_turn)
    
#basic route for new game
@app.route('/new_game')
def new_game():
    session['player1']['score'] = 0
    session['player2']['score'] = 0
    session['player1_turn'] = True
    session.pop('roll_message', None)
    return redirect(url_for('game'))
if __name__ == '__main__':
    app.run(debug=True)
