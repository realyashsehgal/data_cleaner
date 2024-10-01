from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
from src.data_cleaner import clean_data
import pandas as pd

app = Flask(__name__)

# Config paths - ensure these match the actual folder names in your project
app.config['UPLOAD_FILES'] = 'data/raw'  # Check folder name case-sensitivity
app.config['CLEANED_DATA'] = 'data/cleaned'

# Ensure the directories exist (create them if not)
os.makedirs(app.config['UPLOAD_FILES'], exist_ok=True)
os.makedirs(app.config['CLEANED_DATA'], exist_ok=True)


@app.route('/')
def upload_file():
    return render_template('upload.html')


@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return redirect(request.url)  # If no file part in the request, refresh the page
    
    file = request.files['file']

    if file.filename == '':
        return redirect(request.url)  # If the user does not select a file, refresh the page
    
    # Save the uploaded file to the raw data folder
    file_path = os.path.join(app.config['UPLOAD_FILES'], file.filename)
    file.save(file_path)

    # Create the cleaned file path and pass it to your data cleaner function
    cleaned_filepath = os.path.join(app.config['CLEANED_DATA'], f'cleaned_{file.filename}')
    clean_data(file_path, cleaned_filepath)  # Call the cleaning function

    # Redirect to a result page to show the cleaned file (ensure result route exists)
    return redirect(url_for('result', filename=f'cleaned_{file.filename}'))


# Route to display result or cleaned data (placeholder route)
# @app.route('/result')
# def result():
#     return "Cleaning complete. Your file has been cleaned."
@app.route('/result/<filename>')
def result(filename):
    # Read the cleaned file into a DataFrame
    cleaned_filepath = os.path.join(app.config['CLEANED_DATA'], filename)
    df = pd.read_csv(cleaned_filepath)

    # Convert the DataFrame to an HTML table
    table_html = df.to_html(classes='table table-striped', index=False)

    # Render the result template and pass the table HTML
    return render_template('result.html', table_html=table_html)


@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['CLEANED_DATA'], filename)


if __name__ == '__main__':
    app.run(debug=True)
