from flask import Flask, render_template, request
from pymongo import MongoClient
from flask import send_from_directory
import csv

app = Flask(__name__)

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://root:0306@cluster1.uhady06.mongodb.net/?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

db = client['your_database']
collection = db['your_collection']

csv_file_path = 'plant_specs.csv'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/static/images/image1.jpg')
def serve_image(filename):
    return send_from_directory(os.path.join(app.root_path, 'static', 'images'), filename)

@app.route('/upload', methods=['POST'])
def upload():
    with open(csv_file_path, 'r') as csvfile:
        csv_data = csv.DictReader(csvfile)
        collection.insert_many(csv_data)

    return 'Data Uploaded Successfully'

@app.route('/search', methods=['POST'])
def search():
    name = request.form['name']
    result = collection.find_one({'Name': name})
    return render_template('result.html', result=result)


if __name__ == '__main__':
    app.run(debug=True)
