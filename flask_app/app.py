from flask import Flask, render_template, request, redirect, url_for
from game_controller import GameController
from database_manager import DatabaseManager
import time

app = Flask(__name__)

# Initialise the database setup
db_config = {
    'user': 'flaskuser',
    'password': 'pi64',
    'host': 'localhost',
    'database': 'iq_test_v2'
}

# Global variable for the Game_Controller instance
controller = None

@app.route('/start/<user>', methods=['GET', 'POST'])
def start_game(user):
    global controller
    controller = GameController(user, db_config)  # Create a new Game Controller instance
    controller.start_round()  # Start the first round
    return redirect(url_for('game', user=user))  # Redirect to the game route and sets uesr 

@app.route('/game/<user>', methods=['GET', 'POST'])
def game(user):
    global controller

    # Initialise the controller if the user is new or round is reset
    if controller is None:
        controller = GameController(user, db_config)

    if request.method == 'POST':
        user_pattern = [[request.form.get(f'cell_{i}_{j}') == 'on' for j in range(4)] for i in range(4)]
        
        if controller.round_count <= 0 or controller.round_count > len(controller.patterns):
            return "Error: Invalid round count or no pattern generated", 400
        
        correct_pattern = controller.patterns[controller.round_count - 1]
        score = controller.calculate_score(user_pattern, correct_pattern)

        # Only start the timer after the user submits their input
        if controller.start_time is None:
            controller.start_timer()  # Start the timer when the user submits input
        else:
            reaction_time = time.time() - controller.start_time  # Calculate reaction time
            controller.total_time_taken += reaction_time  # Add to total time taken

        if score == 16:  # Check if the user answered correctly
            controller.correct_answers += 1  # Increment correct answers

        if controller.round_count >= controller.max_rounds:
            score_value = controller.calculate_efficiency()  # Get score for redirection
            controller.save_score()  # Save efficiency as score
            print(f"Score to be displayed: {score_value:.1f}")  # Debug line
            controller = None  # Reset the controller for a new game
            return redirect(url_for('score', user=user, score=f"{score_value:.1f}"))  # Format score
        else:
            controller.start_round()
    else:
        # Start a new game or a new round
        if controller.round_count == 0 or controller.round_count > len(controller.patterns):
            controller.start_round()

    return render_template('game.html', round=controller.round_count, max_rounds=controller.max_rounds, pattern=controller.patterns[controller.round_count - 1])

@app.route('/score/<user>/<score>')
def score(user, score):
    return render_template('score.html', user=user, score=score)  # Display the score

# -------main loop to run app-------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
