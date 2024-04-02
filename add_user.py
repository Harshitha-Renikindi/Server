import requests

# URL of your Flask application
url = 'http://localhost:5000/users'

# User data to be added
new_user = {
    'username': 'user4',
    'password': 'password1234',
    'role': 'student'
}

# Send POST request to add the new user
response = requests.post(url, json=new_user)

# Print response
print(response.json())
