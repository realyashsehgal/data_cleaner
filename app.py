from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
import pandas as pd
from src.data_cleaner import clean_data

app = Flask(__name__, template_folder='templates', static_folder='static') 

app.config['UPLOAD_FILES'] = 'data/raw'  
app.config['CLEANED_DATA'] = 'data/cleaned'

os.makedirs(app.config['UPLOAD_FILES'], exist_ok=True)
os.makedirs(app.config['CLEANED_DATA'], exist_ok=True)

@app.route('/')
def upload_file():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return redirect(request.url) 
    
    file = request.files['file']

    if file.filename == '':
        return redirect(request.url)  
    
    file_path = os.path.join(app.config['UPLOAD_FILES'], file.filename)
    file.save(file_path)

    cleaned_filepath = os.path.join(app.config['CLEANED_DATA'], f'cleaned_{file.filename}')
    clean_data(file_path, cleaned_filepath) 

    return redirect(url_for('result', filename=f'cleaned_{file.filename}'))

@app.route('/result/<filename>')
def result(filename):
    cleaned_filepath = os.path.join(app.config['CLEANED_DATA'], filename)

 
    df = pd.read_csv(cleaned_filepath)

    table_html = df.to_html(classes='table table-striped', index=False)

    return render_template('result.html', table_html=table_html)

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['CLEANED_DATA'], filename)

if __name__ == '__main__':
    app.run(debug=True)
