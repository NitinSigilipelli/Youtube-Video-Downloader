from flask import Flask, render_template, request, send_file
from pytubefix import YouTube
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    video_url = request.form['video_url']
    try:
        yt = YouTube(video_url)
        # List all available video streams
        streams = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc()
        for stream in streams:
            print(f'{stream.resolution} - {stream.itag}')
        
        # Select the highest resolution stream
        stream = streams.first()
        file_path = 'temp_video.mp4'
        stream.download(filename=file_path)
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        return f"An error occurred: {e}"

if __name__ == '__main__':
    app.run(debug=True)
