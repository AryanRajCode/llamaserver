from flask import Flask, render_template, request
import socket

app = Flask(__name__)

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Get the local machine name and port
host = "0.0.0.0"
port = 12345

# Connect to the server
client_socket.connect((host, port))

# Function to send messages to the server
def send_message(message):
    client_socket.send(message.encode('utf-8'))
    response = client_socket.recv(1024).decode('utf-8')
    return response

@app.route('/')
def index():
    return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chat with Server</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #1e1e1e; /* Dark background */
            color: #e0e0e0; /* Light text color */
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            transition: background-color 0.3s, color 0.3s;
        }
        .container {
            width: 100%;
            max-width: 800px;
            margin: 20px;
            padding: 20px;
            border-radius: 8px;
            background-color: #2c2c2c; /* Slightly lighter background */
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
            position: relative;
            display: flex;
            flex-direction: column;
            transition: background-color 0.3s;
            height: 80vh; /* Set a height for the container */
        }
        h1 {
            text-align: center;
            margin-bottom: 20px;
        }
        #response {
            flex: 1;
            padding: 10px;
            border: 1px solid #444;
            border-radius: 5px;
            background-color: #3a3a3a; /* Darker background for chat */
            margin-bottom: 10px;
            overflow-y: auto; /* Enable vertical scrollbar */
        }
        .message {
            margin-bottom: 10px;
            padding: 10px;
            border-radius: 5px;
        }
        .user-message {
            background-color: #007bff;
            color: #fff;
            align-self: flex-end;
        }
        .server-message {
            background-color: #444;
            color: #e0e0e0;
            align-self: flex-start;
        }
        form {
            display: flex;
            flex-direction: column;
        }
        textarea[name="message"] {
            width: 100%;
            padding: 15px;
            font-size: 16px;
            border: 1px solid #555;
            border-radius: 5px;
            outline: none;
            resize: none;
            background-color: #2c2c2c;
            color: #e0e0e0;
            margin-bottom: 10px;
        }
        button[type="submit"] {
            padding: 15px;
            font-size: 16px;
            background-color: #007bff;
            color: #fff;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        button[type="submit"]:hover {
            background-color: #0056b3;
        }
        .loader {
            position: absolute;
            top: 20px;
            right: 20px;
            display: none;
        }
        .spinner {
            width: 40px;
            height: 40px;
            border-radius: 50%;
            border: 4px solid transparent;
            border-top-color: #007bff;
            animation: spin 1s linear infinite;
        }
        @keyframes spin {
            0% {
                transform: rotate(0deg);
            }
            100% {
                transform: rotate(360deg);
            }
        }
        .toggle-mode {
            position: absolute;
            top: 20px;
            right: 20px;
            cursor: pointer;
            font-size: 20px;
        }
        /* Light mode styles */
        .light-mode body {
            background-color: #f9f9f9;
            color: #333;
        }
        .light-mode .container {
            background-color: #fff;
        }
        .light-mode #response,
        .light-mode .message {
            background-color: #f0f0f0;
        }
        .light-mode .user-message {
            background-color: #007bff;
            color: #fff;
        }
        .light-mode .server-message {
            background-color: #e0e0e0;
            color: #333;
        }
        .light-mode textarea[name="message"] {
            background-color: #fff;
            color: #333;
            border: 1px solid #ccc;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Chat with Server</h1>
        <div id="response">Welcome! How can I help you today?</div>
        <form action="/send_message" method="post">
            <textarea name="message" placeholder="Enter your message..."></textarea>
            <button type="submit">Send</button>
            <div class="loader">
                <div class="spinner"></div>
            </div>
        </form>
    </div>
    <div class="toggle-mode" onclick="toggleNightMode()">
        🌙
    </div>

    <script>
        const form = document.querySelector('form');
        const container = document.querySelector('.container');
        const loader = form.querySelector('.loader');
        const responseDiv = document.getElementById('response');
        const toggleModeButton = document.querySelector('.toggle-mode');

        form.onsubmit = async function(event) {
            event.preventDefault();
            const messageTextarea = form.querySelector('textarea[name="message"]');
            const userMessage = messageTextarea.value.trim();

            if (userMessage === "") return;

            // Display user's message
            const userMessageDiv = document.createElement('div');
            userMessageDiv.className = 'message user-message';
            userMessageDiv.innerText = `You: ${userMessage}`;
            responseDiv.appendChild(userMessageDiv);
            responseDiv.scrollTop = responseDiv.scrollHeight;

            // Clear textarea
            messageTextarea.value = '';

            loader.style.display = 'block';

            // Send message to the server
            let formData = new FormData();
            formData.append('message', userMessage);
            let response = await fetch('/send_message', {
                method: 'POST',
                body: formData
            });
            let text = await response.text();

            // Display server's response
            const serverMessageDiv = document.createElement('div');
            serverMessageDiv.className = 'message server-message';
            serverMessageDiv.innerText = `Server: ${text}`;
            responseDiv.appendChild(serverMessageDiv);
            responseDiv.scrollTop = responseDiv.scrollHeight;

            loader.style.display = 'none';
        };

        function toggleNightMode() {
            document.body.classList.toggle('light-mode');
            if (document.body.classList.contains('light-mode')) {
                toggleModeButton.innerText = '🌙';
            } else {
                toggleModeButton.innerText = '☀️';
            }
        }
    </script>
</body>
"""

@app.route('/send_message', methods=['POST'])
def send_message_route():
    if request.method == 'POST':
        message = request.form['message']
        response = send_message(message)
        return response

# if __name__ == '__main__':
#     app.run(debug=True)
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=4040)