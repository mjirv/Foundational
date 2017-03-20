from nltk.tokenize import TweetTokenizer
from sklearn.externals import joblib
from sklearn.naive_bayes import MultinomialNB
import numpy as np
import os

def fill_features(words):
    X_temp = np.zeros([1, len(bag_of_words)])
    X_e_temp = np.zeros([1, len(bag_of_words_extroversion)])
    word_index = 0
    for word in bag_of_words:
        if word in words:
            X_temp[0][word_index] = words.count(word)
            X_e_temp[0][bag_of_words_extroversion.index(word)] = 1
        word_index += 1
    return (X_temp, X_e_temp)

mnbs = []
mnbs_e = []

bag_of_words = joblib.load('model/initial_model_counts_bag_of_words.pkl')
bag_of_words_extroversion = joblib.load('model/initial_model_bag_of_words.pkl')
for i in range(0, 4):
    letter = "ocan"[i]
    mnbs.append(joblib.load('model/initial_model_counts_' + letter + '.pkl'))
mnbs_e = joblib.load('model/initial_model_extroversion_e.pkl')

# Get text from Twitter and score each input handle
tokenizer = TweetTokenizer(strip_handles=True)

# Commented out because this is only needed the first time around
#with open('output/prediction_service_output.csv', 'a') as outfile:
#    outfile.write('O,C,A,N,E\n')

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
        X, X_e = fill_features(text)

        # Score
        scores = []
        for i in range(len("ocan")):
            scores.append(str(int(mnbs[i].predict(X)[0])))
        scores.append(str(int(mnbs_e.predict(X_e)[0])))

        # Output to file
        with open('output/prediction_service_output.csv', 'a') as outfile:
            outfile.write(handle + ',' + ','.join(scores) + '\n')
