import pandas as pd
from openai import OpenAI
import numpy as np
import os

def generate_tag(data):

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

    new_tags = data[['Name', 'Description', 'Tags', 'Generated Tags']]

    return new_tags



if __name__ == '__main__':
    data = pd.read_csv('HHS.csv', usecols=['Name', 'Description', 'Tags'])

    output_data = generate_tag(data)

    print(output_data)