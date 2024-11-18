from requests import post


url = "http://127.0.0.1:8000/api/register/"
data = {
    "email": "user1@gmail.com",
    "psw": 12345,
}

response = post(url, data=data)

if response.status_code == 201:
    print("User created successfully:", response.json())
else:
    print("Error:", response.json())