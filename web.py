import time
import stocktalk
import os
from flask import Flask, render_template, request, redirect, jsonify
from pattern.en import tag
import tinys3
import json

with open('credentials.json', 'r') as f:
    creds = json.load(f)

S3_SECRET_KEY = creds['S3_SECRET_KEY']
S3_ACCESS_KEY = creds['S3_ACCESS_KEY']

app = Flask(__name__)
app.debug = True

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/create', methods=['POST'])
def create():
    words = request.form.getlist('word[]')
    texts = request.form.getlist('text[]')
    parts = zip(words, texts)
    parts = [{'query': p[0], 'text': p[1]} for p in parts if p[0] != '' and p[1] != '']
    if len(parts) == 0:
        return jsonify({'url': None})
    parts = parts[0:3]
    outfile = 'static/vids/msg_' + str(int(time.time())) + '.mp4'
    composition = stocktalk.compose(parts)
    filetype = 'gif'
    if request.form.get('filetype') == 'mp4':
        filetype = 'mp4'
    final = stocktalk.save_out(composition, outfile=outfile, filetype=filetype)

    conn = tinys3.Connection(S3_ACCESS_KEY,S3_SECRET_KEY)
    f = open(final, 'rb')
    conn.upload(final.split('/')[-1], f, 'authenticcommunication')
    f.close()

    os.remove(final)

    return jsonify({'url': 'http://authenticcommunication.s3.amazonaws.com/' + final.split('/')[-1]})


@app.route('/keyword', methods=['GET'])
def keyword():
    phrase = request.args.get('text', '')
    words = [w for w, pos in tag(phrase) if pos in ['VB', 'VBD', 'VBN', 'JJ', 'NN', 'NNS', 'NNP', 'NP']]
    print tag(phrase)
    words = [w for w in words if len(w) > 2]
    return jsonify({'keywords': words})


# @app.route('/text', methods=['GET'])
# def split_up():
#     text = request.args.get('text')
#     phrases = 

if __name__ == '__main__':
    app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)))
