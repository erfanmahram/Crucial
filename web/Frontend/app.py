from flask import Flask
from flask import request, render_template

import requests
import os
import pandas as pd
import json

app = Flask(__name__)
project_dir = os.path.dirname(os.path.abspath(__file__))


@app.route('/', methods=["GET", "POST"])
def index():
    # json_file = file_dir + r'data_set_1.json'
    # with open(json_file) as f:
    #     js_object = json.load(f)
    #     df = pd.read_json(json.dumps(js_object))
    return render_template('home.html')


@app.route('/products', methods=["GET", "POST"])
def products():
    return render_template('products.html')


@app.route('/table', methods=["GET", "POST"])
def update_table():
    name = request.form.get("data")
    brand = request.form.get("brand")
    params = {'name': name, 'brand': brand}
    payload = {}
    headers = {}
    url = "http://127.0.0.1:4000/search?query="
    response = requests.request("GET", url, headers=headers, data=payload, params=params)
    my_json = response.content.decode('utf8').replace("'", '"').replace('None', '"?"').replace('""', '"').replace(', "],', '],')

    data = json.loads(my_json)
    json_file = json.dumps(data, sort_keys=False)
    print(json_file)
    return json_file


@app.route('/pipe', methods=["GET", "POST"])
def pipe():
    data = request.form.get("data")
    payload = {}
    headers = {}
    url = "http://127.0.0.1:4000/brand-name?query=" + str(data)
    response = requests.request("GET", url, headers=headers, data=payload)
    return response.json()


@app.route('/pipes', methods=["GET", "POST"])
def pipes():
    name = request.form.get("data")
    brand = request.form.get("brand")
    params = {'name': name, 'brand': brand}
    payload = {}
    headers = {}
    url = "http://127.0.0.1:4000/name?query="
    response = requests.request("GET", url, headers=headers, data=payload, params=params)
    return response.json()


if __name__ == "__main__":
    app.run(debug=True, port=5000)
