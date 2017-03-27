from nltk.tokenize import TweetTokenizer
from sklearn.decomposition import PCA
from sklearn.externals import joblib
from sklearn.linear_model import LogisticRegression
import numpy as np
import os

pca = joblib.load('model/pca_pca.pkl')
def fill_features(words):
    X_temp = np.zeros([1, len(bag_of_words) + 1])
    word_index = 0
    chars = 0
    num_words = 0
    for word in bag_of_words:
        if word in words:
            X_temp[0][word_index] = words.count(word)
            chars += len(word)
            num_words += 1
        word_index += 1
    if num_words > 0:
        X_temp[0][-1] = chars / num_words
    else:
        X_temp[0][-1] = 0

    # Use PCA to reduce dimensionality for better generalizability
    X_new = pca.transform(X_temp)
    return X_new

SEGMENTS = {
    "o": ["creativity", "innovation", "intellectual stimulation"],
    "c": ["achievement", "order", "efficiency"],
    "a": ["communal goals", "interpersonal harmony"],
    "n": ["threats", "uncertainty"],
    "e": ["rewards", "social attention"]
    }

mnbs = []
mnbs_e = []

bag_of_words = joblib.load('model/pca_bag_of_words.pkl')
for i in range(0, 5):
    letter = "ocean"[i]
    mnbs.append(joblib.load('model/pca_' + letter + '.pkl'))

# Get text from Twitter and score each input handle
tokenizer = TweetTokenizer(strip_handles=True)

# Commented out because this is only needed the first time around
with open('output/prediction_service_output_pca.csv', 'a') as outfile:
    outfile.write('O,C,E,A,N\n')
with open('output/prediction_service_pca_segments.csv', 'a') as outfile:
    outfile.write('user,')
    for key, seg in SEGMENTS.items():
        outfile.write(','.join(seg))
        if (key, seg) != list(SEGMENTS.items())[-1]:
            outfile.write(',')
    outfile.write('\n')

with open('predict_handles.txt', 'r') as handle_file:
    # Read usernames from file
    handles = handle_file.read().split('\n')
    for handle in handles[:-1]:
        # Call Twitter API
        os.system('python get_status.py ' + handle)

        # Tokenize text
        text = []
        with open('statuses/statuses_' + handle + '_output.txt', 'r', encoding='utf8') as tweet_text:
            text = tokenizer.tokenize(tweet_text.read().replace('\nTWEETLINEBREAK\n', ' '))

        # Turn into features
        X = fill_features(text)

        # Score
        scores = []
        print(X.shape)
        for i in range(len("ocean")):
            # Print the second element of the probability array because it's the '1' prob
            scores.append(str(float(mnbs[i].predict_proba(X)[0][1])))

        # Turn the scores into marketing segments
        with open('output/prediction_service_pca_segments.csv', 'a') as outfile:
            outfile.write(handle + ',')
            for key, seg in SEGMENTS.items():
                for s in seg:
                    if float(scores["ocean".index(key)]) > 0.5:
                        outfile.write('1')
                    else:
                        outfile.write('0')
                    
                    # Don't add a comma at the end of the line
                    if (key, seg) != list(SEGMENTS.items())[-1] or s != SEGMENTS[key][-1]:
                        outfile.write(',')
                        
            outfile.write('\n')

        # Output to file
        with open('output/prediction_service_output_pca.csv', 'a') as outfile:
            outfile.write(handle + ',' + ','.join(scores) + '\n')
