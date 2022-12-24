from flask import Flask, request
import requests
import re

app = Flask(__name__)

@app.route("/")
def check_input():
    # Flask route to receive incomming traffic into the vpc
    # Checks requests for potential threats

    input = request.json.get("sql")

    # Check if the input contains any SQL injection patterns
    pattern = r"(['\"])|(--)|(%23)|(%5C)|(%22)"
    if re.search(pattern, input):
        return "SQL injection detected! Please remove any malicious input and try again."

        # If the input is determined to be safe, send an HTTP request to the specified address
    else:
        requests.post("http://137.31.34.15", request.json)
        return "Input is safe. HTTP request has been sent."

if __name__ == "__main__":
  app.run()
