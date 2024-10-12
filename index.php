<?php
// MySQL database connection credentials
$servername = "localhost";
$username = "flaskuser";
$password = "pi64";  // Correct password variable
$dbname = "iq_test_v2";  // Updated database name

// Create connection to MySQL using the correct password variable
$conn = new mysqli($servername, $username, $password, $dbname);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Validate the username input
    $user = htmlspecialchars(trim($_POST['username']));

    // Redirect to the Flask game page with the username
    header("Location: http://" . $_SERVER['HTTP_HOST'] . ":5000/game/$user");
    exit();
}

// Fetch the top 10 high scores from MySQL
$sql = "SELECT username, score, timestamp FROM scores ORDER BY score DESC LIMIT 10";
$result = $conn->query($sql);

// Check if the query was successful
if (!$result) {
    die("Error fetching scores: " . $conn->error);
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Cognitive Test</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center; /* Center content horizontally */
            justify-content: center; /* Center content vertically */
            min-height: 100vh; /* Full viewport height */
            margin: 0;
            background-color: #f4f4f4; /* Light background color */
        }
        h1, h2, h3 {
            text-align: center; /* Center headings */
        }
        form {
            margin-bottom: 20px; /* Space below form */
            text-align: center; /* Center form elements */
        }
        table {
            border-collapse: collapse; /* Remove gaps between table cells */
            margin-top: 20px; /* Space above the table */
        }
        th, td {
            border: 1px solid #000; /* Border for table cells */
            padding: 8px; /* Padding inside cells */
            text-align: center; /* Center text in table */
        }
        button {
            margin-top: 10px; /* Space above the button */
            padding: 10px 20px; /* Button padding */
            font-size: 16px; /* Button font size */
        }
    </style>
</head>
<body>
    <h1>Welcome to the Cognitive Test</h1>
    <h3>This Game Is Tests Reaction Time And Pattern Recognition To Imporve Cognitive Functions</h3>
    <form method="POST" action="index.php">
        <input type="text" name="username" placeholder="Enter your username" required>
        <button type="submit">Start Game</button>
    </form>
    
    <h2>High Scores</h2>
    <table>
        <tr>
            <th>Username</th>
            <th>Score (%)</th>
            <th>Date</th>
        </tr>
        <?php
        // Display the high scores
        if ($result->num_rows > 0) {
            while($row = $result->fetch_assoc()) {
                echo "<tr><td>" . htmlspecialchars($row["username"]) . "</td><td>" . htmlspecialchars($row["score"]) . "</td><td>" . htmlspecialchars($row["timestamp"]) . "</td></tr>";
            }
        } else {
            echo "<tr><td colspan='3'>No high scores yet</td></tr>";
        }
        ?>
    </table>
    
    <?php 
    // Close the database connection
    $conn->close(); 
    ?>
</body>
</html>
