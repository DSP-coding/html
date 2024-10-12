from sense_hat import SenseHat
import time

class SenseHatManager:
    def __init__(self):
        self.sense = SenseHat()

    def display_pattern(self, pattern, duration=5):
        """Display the pattern on the Sense HAT for a specified duration."""
        self.sense.clear()  # Clear the display first

        # Center the 4x4 pattern at (2, 2)
        for i in range(4):
            for j in range(4):
                # Set the pixel to green if pattern is True, otherwise set to black
                self.sense.set_pixel(i + 2, j + 2, [0, 255, 0] if pattern[i][j] else [0, 0, 0])

        # Set the outer pixels to red
        for i in range(8):
            for j in range(8):
                if not (2 <= i < 6 and 2 <= j < 6):  # Only set red for outer pixels
                    self.sense.set_pixel(i, j, [255, 0, 0])  # Red for outer part

        time.sleep(duration)  # Show pattern for specified duration
        self.sense.clear()  # Clear the display after showing the pattern

    def show_orientation(self):
        """Show the orientation pattern before starting the game."""
        A = [
            [0, 0, 255, 255, 255, 255, 0, 0],
            [0, 255, 0, 0, 0, 0, 255, 0],
            [255, 0, 0, 0, 0, 0, 0, 255],
            [255, 0, 0, 255, 255, 0, 0, 255],
            [255, 0, 0, 0, 0, 0, 0, 255],
            [255, 0, 0, 0, 0, 0, 0, 255],
            [255, 255, 255, 255, 255, 255, 255, 255],
            [255, 0, 0, 0, 0, 0, 0, 255]
        ]
        for i in range(8):
            for j in range(8):
                self.sense.set_pixel(i, j, [A[i][j], 0, 0])
        time.sleep(1)  # Display orientation for 5 seconds
        self.sense.clear()  # Clear the display
