import random
import time
import threading
from sensehat_manager import SenseHatManager
from database_manager import DatabaseManager

class GameController:
    def __init__(self, username, db_config):
        # Initialise the game with the player's username and database configuration
        self.username = username  # Player's name
        self.patterns = []  # List to store generated patterns
        self.round_count = 0  # Number of rounds played
        self.max_rounds = 5  # Maximum rounds in the game
        self.correct_answers = 0  # Number of correct answers
        self.total_time_taken = 0  # Total time taken for all rounds combined
        self.sense_hat_manager = SenseHatManager()  # Manages the Sense HAT display
        self.db_manager = DatabaseManager(db_config)  # Manages the database
        self.start_time = None  # Start time for each round
        self.display_thread = None  # Thread for displaying patterns on the Sense HAT

    def start_round(self):
        """Start a new round of the game."""
        # This method starts a round by generating and showing a new pattern
        self.sense_hat_manager.show_orientation()  # Display orientation message on Sense HAT
        pattern = self.generate_pattern()  # Generate a random 4x4 pattern
        self.patterns.append(pattern)  # Add the pattern to the list of patterns
        self.round_count += 1  # Increase the round count
        self.start_time = time.time()  # Record the start time of the round

        # Create and start a thread to display the pattern on the Sense HAT
        self.display_thread = threading.Thread(target=self.display_pattern_thread, args=(pattern, 8))
        self.display_thread.start()

    def display_pattern_thread(self, pattern, duration):
        """Display a pattern on the Sense HAT for a given duration."""
        # This runs in a separate thread to display the pattern without blocking other actions
        self.sense_hat_manager.display_pattern(pattern, duration)

    def generate_pattern(self):
        """Generate a random 4x4 pattern of True (light) and False (dark)."""
        return [[random.choice([True, False]) for _ in range(4)] for _ in range(4)]  # Create a 4x4 grid

    def calculate_efficiency(self):
        """Calculate the player's efficiency based on correct answers and time taken."""
        if self.round_count > 0:
            average_time = self.total_time_taken / self.round_count  # Calculate average time per round
            efficiency = (self.correct_answers / self.max_rounds) * 100  # Calculate efficiency as a percentage
            adjusted_efficiency = efficiency - average_time  # Adjust efficiency by time taken
            print(f"Calculated efficiency for {self.username}: {adjusted_efficiency}")  # Debug line
            return max(adjusted_efficiency, 0)  # Ensure efficiency is not negative
        return 0  # Return 0 if no rounds played

    def save_score(self):
        """Save the player's score to the database."""
        score = self.calculate_efficiency()  # Calculate the player's score
        print(f"Calculated efficiency score for {self.username}: {score}")  # Debug line
        self.db_manager.save_score(self.username, score)  # Save the score using the DatabaseManager

    def calculate_score(self, user_pattern, correct_pattern):
        """Compare the player's pattern with the correct pattern and calculate score."""
        score = 0
        # Loop through both patterns and count how many squares match
        for i in range(4):
            for j in range(4):
                if user_pattern[i][j] == correct_pattern[i][j]:
                    score += 1  # Increase score for each matching square
        return score

    def reset_game(self):
        """Reset the game variables to start fresh."""
        self.patterns = []  # Clear the patterns
        self.round_count = 0  # Reset round count
        self.correct_answers = 0  # Reset the number of correct answers
        self.total_time_taken = 0  # Reset the total time taken
        self.start_time = None  # Reset the start time
