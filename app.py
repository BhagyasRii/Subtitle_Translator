from flask import Flask, request, render_template, send_file
import os
from basic_translator import translate_srt

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'translated'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Sample language map: code => full name
LANGUAGES = {
    'en': 'English',
    'te': 'Telugu',
    'hi': 'Hindi',
    'ta': 'Tamil',
    'ml': 'Malayalam',
    'kn': 'Kannada',
    'bn': 'Bengali',
    'gu': 'Gujarati',
    'mr': 'Marathi'
}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['srtfile']
        src_lang = request.form['src_lang']
        dest_lang = request.form['dest_lang']

        if file and file.filename.endswith('.srt'):
            input_path = os.path.join(UPLOAD_FOLDER, file.filename)
            output_path = os.path.join(OUTPUT_FOLDER, f'{src_lang}_to_{dest_lang}_' + file.filename)

            file.save(input_path)
            translate_srt(input_path, output_path, src_lang=src_lang, dest_lang=dest_lang)

            return send_file(output_path, as_attachment=True)

    return render_template('index.html', languages=LANGUAGES)

if __name__ == '__main__':
    app.run(debug=True)
