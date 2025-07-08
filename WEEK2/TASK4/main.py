import os
import uuid
from flask import Flask, render_template, request, redirect, flash, url_for, send_from_directory
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = '013027uvxyz'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MEDIA_DIR = os.path.join(BASE_DIR, 'media')
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}

app.config['UPLOAD_PATH'] = MEDIA_DIR
app.config['MAX_CONTENT_LENGTH'] = 4 * 1024 * 1024  

os.makedirs(MEDIA_DIR, exist_ok=True)

def is_valid_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        image = request.files.get('image')

        if not image or image.filename == '':
            flash("No image file selected.")
            return redirect(request.url)

        if not is_valid_file(image.filename) or not image.mimetype.startswith('image/'):
            flash("Invalid file type. Only images are allowed.")
            return redirect(request.url)

        extension = image.filename.rsplit('.', 1)[1].lower()
        new_name = f"{uuid.uuid4().hex}.{extension}"
        saved_path = os.path.join(app.config['UPLOAD_PATH'], secure_filename(new_name))
        image.save(saved_path)

        file_link = url_for('serve_image', filename=new_name, _external=True)
        flash(f"Image uploaded successfully! Access it here: {file_link}")
        return redirect(url_for('upload_image'))

    return render_template('uploads.html')

@app.route('/media/<filename>')
def serve_image(filename):
    return send_from_directory(app.config['UPLOAD_PATH'], filename)

if __name__ == '__main__':
    app.run(debug=True)
