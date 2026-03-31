from flask import Flask, render_template, request, send_file
import yt_dlp
import os
import uuid

app = Flask(__name__)

# ডাউনলোড ফোল্ডার তৈরি
DOWNLOAD_FOLDER = 'downloads'
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form.get('url')
    quality = request.form.get('quality', '192')
    
    if not url:
        return "No URL provided", 400
    
    try:
        # ইউনিক ফাইল নাম
        filename = f"audio_{uuid.uuid4().hex[:8]}"
        
        options = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(DOWNLOAD_FOLDER, f'{filename}.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': quality,
            }],
            'quiet': True,
            'no_warnings': True,
        }
        
        with yt_dlp.YoutubeDL(options) as ydl:
            info = ydl.extract_info(url, download=True)
            title = info.get('title', 'audio')
            
        # ফাইল পাথ
        mp3_file = os.path.join(DOWNLOAD_FOLDER, f'{filename}.mp3')
        
        if os.path.exists(mp3_file):
            return send_file(
                mp3_file,
                as_attachment=True,
                download_name=f"{title}.mp3",
                mimetype='audio/mpeg'
            )
        else:
            return "File not found", 404
            
    except Exception as e:
        return f"Error: {str(e)}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)