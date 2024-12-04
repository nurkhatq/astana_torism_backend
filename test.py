import requests

url = "http://127.0.0.1:8000/api/users/profile/me/"
headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzMyMjU0MzIxLCJpYXQiOjE3MzIyNTA3MjEsImp0aSI6ImNkODQwMmZjMTQ5NjQxMjlhMmUxN2Q4YTE1MGY5YmIwIiwidXNlcl9pZCI6Mn0.3hzs51YgFpuDAfxnKCKcil3q4dcGVD-5jKf8n3W_zSs"  # Replace with your token
}

response = requests.get(url, headers=headers)
print(response.json())
