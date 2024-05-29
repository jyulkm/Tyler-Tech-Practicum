import matplotlib.pyplot as plt
from matplotlib import figure
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer


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

    data[['Name_Desc', 'Top_Keywords']].to_csv('output.csv', index=False)

    return data[['Name', 'Description', 'Tags', 'Top_Keywords']]



if __name__ == '__main__':
    np.set_printoptions(threshold=np.inf, linewidth=np.inf)
    pd.set_option('display.max_seq_items', None)
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)

    data = pd.read_csv('HHS.csv', usecols=['Name', 'Description', 'Tags'])

    output_data = tfidf(data)

    print(output_data)
