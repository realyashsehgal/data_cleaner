from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
import pandas as pd
from src.data_cleaner import clean_data

app = Flask(__name__, template_folder='templates', static_folder='static') 

app.config['UPLOAD_FILES'] = 'Data/raw'  
app.config['CLEANED_DATA'] = 'Data/cleaned'

os.makedirs(app.config['UPLOAD_FILES'], exist_ok=True)
os.makedirs(app.config['CLEANED_DATA'], exist_ok=True)
global global_file
@app.route('/')
def upload_file():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return redirect(request.url) 
    
    global file
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)  
    
    # print(global_file.filename)
    global file_path
    file_path = os.path.join(app.config['UPLOAD_FILES'], file.filename)
    file.save(file_path)
    # print(global_file)
    
    button_clicked = request.form['action']
    if button_clicked == 'upload':
        return render_template('upload.html',filename=file.filename)
    return redirect(request.url) 

@app.route('/display', methods=['POST'])
def display():
    # Ensure that the global_file is available
    # if global_file or global_file.filename == '':
    #     return redirect(url_for('upload'))  # Redirect if no file is uploaded

    print("Display function invoked")
    file_path = os.path.join(app.config['UPLOAD_FILES'], file.filename)
    df = pd.read_csv(file_path)
    table_html = df.to_html(classes='table table-striped', index=False)

    return render_template('upload.html',table_html=table_html,filename=file.filename)


@app.route('/clean', methods=['POST'])
def clean():
    cleaned_filepath = os.path.join(app.config['CLEANED_DATA'], f'cleaned_{file.filename}')
    print("upload clicked")
    clean_data(file_path, cleaned_filepath) 
    return redirect(url_for('result', filename=f'cleaned_{file.filename}'))

@app.route('/result/<filename>')
def result(filename):
    cleaned_filepath = os.path.join(app.config['CLEANED_DATA'], filename)

 
    df = pd.read_csv(cleaned_filepath)

    table_html = df.to_html(classes='table table-striped', index=False)

    return render_template('result.html', table_html=table_html,filename= filename)

@app.route('/download/<filename>')
def download_file(filename):
    print(filename)
    return send_from_directory(app.config['CLEANED_DATA'], filename,as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
