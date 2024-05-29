import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from matplotlib import figure
import argparse

from openai import OpenAI
from sklearn.feature_extraction.text import TfidfVectorizer

def generate_openai(data):
    API = 'sk-proj-3kc5M0DRmFMw70XGgRcST3BlbkFJMmajvYAxkFwg9oK5a8EW'

    data['name_description'] = data['Name'] + ' ' + data['Description']

    tags = data.dropna().reset_index(drop='index')

    data["Generated Tags"] = None

    client = OpenAI(api_key=API)

    for i in range(data.shape[0]):
        completion = client.chat.completions.create(
            model="gpt-4-turbo-2024-04-09",
            messages=[
            {"role": "system", "content": "You are a tag generating assistant, skilled in extracting key information based on description."},
            {"role": "user", "content": f"This is example of tags based on name and description: {tags}. Generate 10 tags like example based on name and description: {data['name_description'].iloc[i]}"}
            ]
        )
        print(i)

        data['Generated Tags'][i] = completion.choices[0].message.content.replace('\n', ' ')

    new_tags = data[['Name', 'Description', 'Tags', 'Generated Tags']]

    new_tags.to_csv('output.csv', index=False)

    return new_tags

def yake(data):
    return

def tfidf(data):
    data['Name'].fillna('', inplace=True)
    data['Description'].fillna('', inplace=True)

    data['Name_Desc'] = data['Name'] + " " + data['Description']

    # TF-IDF Vectorizor (Remove stop words)
    vectorizer = TfidfVectorizer(stop_words='english')

    tfidf_matrix = vectorizer.fit_transform(data['Name_Desc'])

    feature_names = vectorizer.get_feature_names_out()
    top_keywords = []

    for vector in tfidf_matrix:
        scores = zip(feature_names, vector.toarray().flatten())
        sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)[:5] # 5 Keywords
        top_keywords.append([feature for feature, _ in sorted_scores])

    data['Top_Keywords'] = top_keywords

    data[['Name', 'Description', 'Tags', 'Top_Keywords']].to_csv('output.csv', index=False)

    return data[['Name', 'Description', 'Tags', 'Top_Keywords']]



if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-method', type=str, default='openai')
    parser.add_argument('-data', type=str, default='sample')

                
    opt = parser.parse_args()

    data = pd.read_csv(f'./data/{opt.data}.csv', usecols=['Name', 'Description', 'Tags'])

    if opt.method == 'openai':
        output_data = generate_openai(data)
    elif opt.method == 'yake':
        output_data = yake(data)
    else:
        output_data = tfidf(data)