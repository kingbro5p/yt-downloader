import os
import yt_dlp
from flask import Flask, render_template, request, send_file, flash, redirect, url_for

app = Flask(__name__)
app.secret_key = "yt_downloader_secret_key_2026"

DOWNLOAD_FOLDER = "downloads"
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

@app.route('/', methods=['GET'])
def index():
    video_url = request.args.get('url')

    if video_url:
        try:
            cookie_path = 'cookies.txt'

            ydl_opts = {
                'format': 'best[ext=mp4]/best',
                'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
                'quiet': True,
                # Bot Block বাইপাস করার জন্য iOS/Android ক্লায়েন্ট বাইপাস
                'extractor_args': {
                    'youtube': {
                        'player_client': ['ios', 'android', 'web']
                    }
                }
            }

            # যদি cookies.txt ফাইল থাকে তবে তা অটোমেটিক ব্যবহার করবে
            if os.path.exists(cookie_path):
                ydl_opts['cookiefile'] = cookie_path

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(video_url, download=True)
                filename = ydl.prepare_filename(info)

            return send_file(filename, as_attachment=True)

        except Exception as e:
            flash(f"ডাউনলোড করতে সমস্যা হয়েছে: {str(e)}")
            return redirect(url_for('index'))

    return render_template('index.html')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
