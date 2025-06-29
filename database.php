<!-- this file is not in use -->
<?php
header('Content-Type: application/json');

// Database configuration
$servername = "localhost";
$username = "your_username";  // Change to your XAMPP username (typically 'root')
$password = "your_password";  // Change to your XAMPP password (typically empty)
$dbname = "media_issuance";   // Create this database first

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);

// Check connection
if ($conn->connect_error) {
    die(json_encode(['success' => false, 'message' => 'Connection failed: ' . $conn->connect_error]));
}

// Get POST data
$data = json_decode(file_get_contents('php://input'), true);

// Prepare and bind
$stmt = $conn->prepare("INSERT INTO media_issuance_records (
    media_type, media_id, recipient_name, recipient_pin, 
    issue_date, issued_by_name, issued_by_pin, 
    media_category, remarks
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)");

$stmt->bind_param(
    "sssssssss",
    $data['mediaType'],
    $data['mediaId'],
    $data['recipientName'],
    $data['recipientPin'],
    $data['issueDate'],
    $data['issuedByName'],
    $data['issuedByPin'],
    $data['mediaCategory'],
    $data['remarks']
);

// Execute query
if ($stmt->execute()) {
    echo json_encode(['success' => true, 'message' => 'Record added successfully']);
} else {
    echo json_encode(['success' => false, 'message' => 'Error: ' . $stmt->error]);
}

$stmt->close();
$conn->close();
?>
