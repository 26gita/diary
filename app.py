from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
import certifi
from datetime import datetime

url = 'mongodb+srv://test:sparta@cluster0.rxufawr.mongodb.net/?retryWrites=true&w=majority'
client = MongoClient(url, tlsCAFile=certifi.where())  # Create a db named 'dbsparta'.
db = client.sparta

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/diary', methods=['GET'])
def show_diary():
    articles = list(db.diary.find({}, {'_id': False}))
    # sample_receive = request.args.get('sample_give')
    # print(sample_receive)
    return jsonify({'articles': articles})

@app.route('/diary', methods=['POST'])
def save_diary():
    # sample_receive = request.form.get('sample_give')
    # print(sample_receive)
    title_receive = request.form.get('title_give')
    content_receive = request.form.get('content_give')

    today = datetime.now()
    mytime = today.strftime('%Y-%m-%d-%H-%M-%S')

    file = request.files['file_give']
    extension = file.filename.split('.')[-1]
    filename = f'file-{mytime}.{extension}'
    save_to = f'static/{filename}'
    file.save(save_to)

    profile = request.files['profile_give']
    extension = profile.filename.split('.')[-1]
    profilename = f'profile-{mytime}.{extension}'
    save_to = f'static/{profilename}'
    profile.save(save_to)

    time = today.strftime('%Y-%m-%d')

    doc = {
        'file' : filename,
        'profile' : profilename,
        'title': title_receive,
        'content': content_receive,
        'time': time,
    }
    db.diary.insert_one(doc)
    return jsonify({'message': 'Data saved!'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)