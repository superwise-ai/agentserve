import requests

url = "http://localhost:8000/invoke"

response = requests.post(
    url,
    json={"input": "please tell me a about the history of the world", "stream": True},
    stream=True,
)
for i, line in enumerate(response.iter_lines()):
    if line:
        decoded_line = line.decode("utf-8").strip()
        print(decoded_line)
