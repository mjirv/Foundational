from nltk.tokenize import TweetTokenizer
from sklearn.externals import joblib
from sklearn.naive_bayes import MultinomialNB
import numpy as np
import os

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
    return X_temp

SEGMENTS = {
    "o": ["creativity", "innovation", "intellectual stimulation"],
    "c": ["achievement", "order", "efficiency"],
    "a": ["communal goals", "interpersonal harmony"],
    "n": ["threats", "uncertainty"],
    "e": ["rewards", "social attention"]
    }

mnbs = []
mnbs_e = []

bag_of_words = joblib.load('model/regression__bag_of_words.pkl')
for i in range(0, 5):
    letter = "ocean"[i]
    mnbs.append(joblib.load('model/regression_' + letter + '.pkl'))

# Get text from Twitter and score each input handle
tokenizer = TweetTokenizer(strip_handles=True)

# Commented out because this is only needed the first time around
with open('output/prediction_service_output_regression.csv', 'a') as outfile:
    outfile.write('O,C,E,A,N\n')
with open('output/prediction_service_regression_segments.csv', 'a') as outfile:
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
        for i in range(len("ocean")):
            scores.append(str(int(mnbs[i].predict(X)[0])))

        # Turn the scores into marketing segments
        with open('output/prediction_service_regression_segments.csv', 'a') as outfile:
            outfile.write(handle + ',')
            for key, seg in SEGMENTS.items():
                for s in seg:
                    if int(scores["ocean".index(key)]) > 50:
                        outfile.write('1')
                    else:
                        outfile.write('0')
                    
                    # Don't add a comma at the end of the line
                    if (key, seg) != list(SEGMENTS.items())[-1] or s != SEGMENTS[key][-1]:
                        outfile.write(',')
                        
            outfile.write('\n')

        # Output to file
        with open('output/prediction_service_output_regression.csv', 'a') as outfile:
            outfile.write(handle + ',' + ','.join(scores) + '\n')
