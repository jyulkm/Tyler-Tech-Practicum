from flask import Flask, request, render_template, send_file
import pandas as pd
import os
from openai import OpenAI


app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER 

def generate_tags(dataframe):
    data = dataframe.copy()
    data['name_description'] = data['Name'] + ' ' + data['Description']

    tags = data.dropna().reset_index(drop='index')
    no_tag = data[data['Tags'].isna()].reset_index(drop='index')

    client = OpenAI(api_key="sk-proj-OW3BIPRXsb4uhiwB1vO9T3BlbkFJNBekzWtxf16Wl2qBHmVS")

    for i in range(no_tag.shape[0]):
        completion = client.chat.completions.create(
            model="gpt-4-turbo-2024-04-09",
            messages=[
            {"role": "system", "content": "You are a tag generating assistant, skilled in extracting key information based on description."},
            {"role": "user", "content": f"This is example of tags based on name and description: {tags}. Generate 10 tags like example based on name and description: {no_tag['name_description'].iloc[i]}"}
            ]
        )

        print('-------------------------------------------------')
        print(no_tag['name_description'].iloc[i])
        no_tag['Tags'][i] = completion.choices[0].message.content.replace('\n', ' ')
        print(completion.choices[0].message.content.replace('\n', ' '))
    # Example function to generate tags based on data
    #dataframe['Tag'] = 'Tag_' + dataframe['Column1'].astype(str)
    return no_tag

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
        output_filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'output_' + file.filename)
        processed_df.to_csv(output_filepath, index=False)
        return send_file(output_filepath, as_attachment=True)
    else:
        return 'Invalid file format. Please upload a CSV file.'

if __name__ == '__main__':
    app.run(debug=True)
