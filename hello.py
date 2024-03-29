from flask import Flask, render_template, request, send_file
import os

app = Flask(__name__)

# Define a directory to store uploaded files
UPLOAD_FOLDER = 'uploads'
DOWNLOAD_FOLDER = 'downloads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER

# Ensure the upload and download directories exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['DOWNLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('home.html')
@app.route('/video_to_video')
def vtv():
    return render_template("vtv.html")
@app.route('/upload_vtv', methods=['POST'])
def upload_file_vtv():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            return "No file part"
        
        file = request.files['file']
        
        # If the user does not select a file, the browser submits an empty file without a filename
        if file.filename == '':
            return "No selected file"
        
        # Save the uploaded file to the upload folder
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        
        # Check if the file was saved successfully
        if os.path.exists(filepath):
            return render_template('upload_success.html', filename=file.filename)
        else:
            return "Failed to upload " + file.filename

@app.route('/download/<filename>')
def download_file(filename):
    # Generate the path to the file
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    # Check if the file exists before trying to send it
    if os.path.exists(filepath):
        # Move the file to the download folder
        os.rename(filepath, os.path.join(app.config['DOWNLOAD_FOLDER'], filename))
        # Send the file as an attachment
        return send_file(os.path.join(app.config['DOWNLOAD_FOLDER'], filename), as_attachment=True)
    else:
        return "File not found"

if __name__ == '__main__':
    app.run()
