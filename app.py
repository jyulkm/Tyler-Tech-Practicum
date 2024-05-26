from flask import Flask, request, render_template, send_file
import pandas as pd
import os
from openai import OpenAI


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['GENERATED_FOLDER'] = 'generated'

# Ensure the folders exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['GENERATED_FOLDER'], exist_ok=True)

def generate_tags(dataframe):
    data = dataframe.copy()
    data['name_description'] = data['Name'] + ' ' + data['Description']

    tags = data.dropna().reset_index(drop='index')

    data["Generated Tags"] = None

    client = OpenAI(api_key=os.getenv("API_KEY"))

    for i in range(data.shape[0]):
        completion = client.chat.completions.create(
            model="gpt-4-turbo-2024-04-09",
            messages=[
            {"role": "system", "content": "You are a tag generating assistant, skilled in extracting key information based on description."},
            {"role": "user", "content": f"This is example of tags based on name and description: {tags}. Generate 10 tags like example based on name and description: {data['name_description'].iloc[i]}"}
            ]
        )


        data['Generated Tags'][i] = completion.choices[0].message.content.replace('\n', ' ')

    return data[['Name', 'Description', 'Tags', 'Generated Tags']]

@app.route('/')
def index():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file and file.filename.endswith('.csv'):
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        dataframe = pd.read_csv(filepath, usecols=['Name', 'Description', 'Tags'])
        processed_df = generate_tags(dataframe)

        # Save the processed dataframe to a CSV in memory
        output_filepath = os.path.join(app.config['GENERATED_FOLDER'], 'output_' + file.filename)
        processed_df.to_csv(output_filepath, index=False)

        # Convert the dataframe to HTML table
        table_html = processed_df.to_html(classes='table table-striped', index=False)
        
        # Pass the HTML table and CSV data to the template
        return render_template('results.html', table_html=table_html, filename='output_' + file.filename)
    else:
        return 'Invalid file format. Please upload a CSV file.'

    
@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    output_filepath = os.path.join(app.config['GENERATED_FOLDER'], filename)
    return send_file(output_filepath, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
