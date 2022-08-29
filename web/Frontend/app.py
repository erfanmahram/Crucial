from flask import request, render_template, Flask
import requests
import json
import inflection


def headings(key):
    return inflection.titleize(key)


app = Flask(__name__)
app.jinja_env.filters.update(headings=headings)


@app.route('/', methods=["GET", "POST"])
def index():
    return render_template('home.html')


@app.route('/products/<id>', methods=["GET", "POST"])
def products(id):
    payload = {}
    headers = {}
    url = "http://127.0.0.1:4000/product?query=" + str(id)
    response = requests.request("GET", url, headers=headers, data=payload, timeout=60)
    ram = list()
    ssd = list()
    extssd = list()
    print(response.json())
    for item in response.json():
        if item['Category'] == 'RAM' or item['Category'] == 'memory':
            ram.append(item)
        elif item['Category'] == 'SSD' or item['Category'] == 'ssd':
            ssd.append(item)
        else:
            extssd.append(item)
    return render_template('products.html', data={'ram': ram, 'ssd': ssd, 'extssd': extssd})


@app.route('/table', methods=["GET", "POST"])
def update_table():
    name = request.form.get("data")
    brand = request.form.get("brand")
    params = {'name': name, 'brand': brand}
    payload = {}
    headers = {}
    url = "http://127.0.0.1:4000/search?"
    response = requests.request("GET", url, headers=headers, data=payload, params=params, timeout=60)
    return json.dumps(response.json())


@app.route('/pipe', methods=["GET", "POST"])
def pipe():
    data = request.form.get("data")
    payload = {}
    headers = {}
    url = "http://127.0.0.1:4000/brand-name?query=" + str(data)
    response = requests.request("GET", url, headers=headers, data=payload, timeout=60)
    return response.json()


@app.route('/pipes', methods=["GET", "POST"])
def pipes():
    name = request.form.get("data")
    brand = request.form.get("brand")
    params = {'name': name, 'brand': brand}
    payload = {}
    headers = {}
    url = "http://127.0.0.1:4000/name?query="
    response = requests.request("GET", url, headers=headers, data=payload, params=params, timeout=60)
    return response.json()


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=5000)
