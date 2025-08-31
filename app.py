from flask import Flask, request, jsonify, Response, render_template
from ytmusicapi import YTMusic
import yt_dlp
import requests
import os

app = Flask(__name__)
yt = YTMusic()

# Ana sayfa
'templates' klasörü içinde index.html olmalı
@app.route('/')
def index():
    return render_template('index.html')

# Şarkı arama
@app.route('/search')
def search():
    query = request.args.get('q')
    results = yt.search(query, filter="songs")
    return jsonify(results)

# Proxy link üzerinden stream
@app.route('/stream')
def stream():
    video_id = request.args.get('id')
    if not video_id:
        return "No video id provided", 400

    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"https://music.youtube.com/watch?v={video_id}", download=False)
        url = info['url']

    def generate():
        with requests.get(url, stream=True) as r:
            for chunk in r.iter_content(chunk_size=4096):
                if chunk:
                    yield chunk

    return Response(generate(), content_type='audio/mp4')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
