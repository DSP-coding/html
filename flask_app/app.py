from flask import Flask, render_template, request, redirect, url_for
from game_controller import GameController
from database_manager import DatabaseManager
import time

# Create a Flask app instance
app = Flask(__name__)

# Initialize the database configuration for connecting to MySQL
db_config = {
    'user': 'flaskuser',  # Database username
    'password': 'pi64',   # Database password
    'host': 'localhost',  # Database host (local server)
    'database': 'iq_test_v2'  # Name of the database
}

# Create a global variable for storing the GameController instance
controller = None

# Route to start the game for a specific user
@app.route('/start/<user>', methods=['GET', 'POST'])
def start_game(user):
    global controller  # Access the global controller variable
    # Create a new GameController instance for this user
    controller = GameController(user, db_config)
    # Start the first round of the game
    controller.start_round()
    # Redirect to the game route with the current user
    return redirect(url_for('game', user=user))

# Route to handle the game logic
@app.route('/game/<user>', methods=['GET', 'POST'])
def game(user):
    global controller  # Access the global controller

    # If the controller doesn't exist (e.g., the game was restarted), create a new one
    if controller is None:
        controller = GameController(user, db_config)

    # If the user submits a pattern (via POST request)
    if request.method == 'POST':
        # Capture the pattern the user selected on the web interface
        user_pattern = [[request.form.get(f'cell_{i}_{j}') == 'on' for j in range(4)] for i in range(4)]
        
        # Ensure a valid round is running, otherwise return an error
        if controller.round_count <= 0 or controller.round_count > len(controller.patterns):
            return "Error: Invalid round count or no pattern generated", 400
        
        # Get the correct pattern for this round from the controller
        correct_pattern = controller.patterns[controller.round_count - 1]
        # Calculate how many squares the user got correct
        score = controller.calculate_score(user_pattern, correct_pattern)

        # Start the timer for the user if it hasn't been started yet
        if controller.start_time is None:
            controller.start_timer()  # Start the timer
        else:
            # Calculate the time taken by the user to submit the pattern
            reaction_time = time.time() - controller.start_time
            # Add the time taken to the total time
            controller.total_time_taken += reaction_time

        # If the user got the pattern fully correct (all 16 squares)
        if score == 16:
            # Increment the number of correct answers
            controller.correct_answers += 1

        # If the game has reached the final round
        if controller.round_count >= controller.max_rounds:
            # Calculate the user's efficiency (which is their score)
            score_value = controller.calculate_efficiency()
            # Save the user's score in the database
            controller.save_score()
            print(f"Score to be displayed: {score_value:.1f}")  # Debug line for checking score
            controller = None  # Reset the controller for a new game
            # Redirect to the score page to display the final score
            return redirect(url_for('score', user=user, score=f"{score_value:.1f}"))
        else:
            # Start a new round if the game isn't finished
            controller.start_round()

    # If the user loads the page (via GET request)
    else:
        # Start the first round if it hasn't been started yet
        if controller.round_count == 0 or controller.round_count > len(controller.patterns):
            controller.start_round()

    # Render the game interface (HTML) with the current round and pattern
    return render_template('game.html', round=controller.round_count, max_rounds=controller.max_rounds, pattern=controller.patterns[controller.round_count - 1])

# Route to display the final score after the game
@app.route('/score/<user>/<score>')
def score(user, score):
    # Render the score page with the user's score
    return render_template('score.html', user=user, score=score)

# -------main loop to run the app-------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
