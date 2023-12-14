from flask import Flask, request
import requests
import os
import json

app = Flask(__name__)

def get_api_key() -> str:
    secret = os.environ.get("COMPUTE_API_KEY")
    if secret:
        return secret
    else:
        # local testing
        with open('.key') as f:
            return f.read()

@app.route("/")
def hello():
    return "Add workers to the Spark cluster with a POST request to add"

@app.route("/test")
def test():
    return get_api_key()

@app.route("/add", methods=['POST'])
def add():
    if request.method == 'POST':
        token = get_api_key()
        num = request.json['num']
        ret = addWorker(token, num)
        return ret
    else:
        return "Use POST to add"  # replace with form template

def addWorker(token, num):
    with open('payload.json') as p:
        tdata = json.load(p)
    
    tdata['name'] = 'slave' + str(num)
    data = json.dumps(tdata)
    
    url = 'https://www.googleapis.com/compute/v1/projects/spark-371009/zones/europe-west1-b/instances'
    headers = {"Authorization": "Bearer " + token, "Content-Type": "application/json"}
    
    resp = requests.post(url, headers=headers, data=data)
    
    if resp.status_code == 200:
        return "Done"
    else:
        print(resp.content)
        return "Error\n" + resp.content.decode('utf-8') + '\n\n\n' + data

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='8080')
