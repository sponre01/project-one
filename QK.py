# # Natural Language Processing with Kaggle Quora Classification Competition

# ## Load Data

# We needed to store the data in AWS S3 so that we can use sagemaker to run our machine learning models.
# Link: https://www.kaggle.com/c/quora-insincere-questions-classification/data

# files: embeddings.zip, sample_submission.csv.zip, test.csv.zip, train.csv.zip
import sys
import nltk

import pandas as pd
import numpy as np
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.classify.scikitlearn import SklearnClassifier


# ## Preprocess Data

#separate data into our labels --> Y, and texts --> text_messages

# text_messages

# use regular expressions to replace email addresses, URLs, phone numbers, other numbers
#link: http://regexlib.com/?AspxAutoDetectCookieSupport=1

def process_data(text_messages):
    # Replace email addresses with 'email'
    processed = text_messages.str.replace(r'^.+@[^\.].*\.[a-z]{2,}$',
                                    'emailaddress')

    # Replace URLs with 'webaddress'
    processed = processed.str.replace(r'^http\://[a-zA-Z0-9\-\.]+\.[a-zA-Z]{2,3}(/\S*)?$',
                                    'webaddress')

    # Replace money symbols with 'moneysymb' (£ can by typed with ALT key + 156)
    processed = processed.str.replace(r'£|\$', 'moneysymb')
        
    # Replace 10 digit phone numbers (formats include paranthesis, spaces, no spaces, dashes) with 'phonenumber'
    processed = processed.str.replace(r'^\(?[\d]{3}\)?[\s-]?[\d]{3}[\s-]?[\d]{4}$',
                                    'phonenumbr')
        
    # Replace numbers with 'numbr'
    processed = processed.str.replace(r'\d+(\.\d+)?', 'numbr')

    # note: we end in 'r' instead of 'er' to prevent lemmatization 

    # Remove punctuation
    processed = processed.str.replace(r'[^\w\d\s]', ' ')

    # Replace whitespace between terms with a single space
    processed = processed.str.replace(r'\s+', ' ')

    # Remove leading and trailing whitespace
    processed = processed.str.replace(r'^\s+|\s+?$', '')

    # change words to lower case - Hello, HELLO, hello are all the same word
    processed = processed.str.lower()
    return processed

# processed = process_data(text_messages)
# processed_test = process_data(test_messages)

def stop_stem(processed):
    nltk.download('stopwords')

    # remove stop words from text messages

    stop_words = set(stopwords.words('english'))

    processed = processed.apply(lambda x: ' '.join(
        term for term in x.split() if term not in stop_words))

    # Remove word stems using a Porter stemmer
    ps = nltk.PorterStemmer()

    processed = processed.apply(lambda x: ' '.join(
        ps.stem(term) for term in x.split()))
    
    return processed

# processed = stop_stem(processed)
# processed_test = stop_stem(processed)

# ## Generating Features
def generate_words(processed):
    nltk.download('punkt')
    # create bag-of-words
    all_words = []

    for message in processed:
        words = word_tokenize(message)
        for w in words:
            all_words.append(w)
            
    all_words = nltk.FreqDist(all_words)
    return all_words

# all_words = generate_words(processed)

# print the total number of words and the 15 most common words
# print('Number of words: {}'.format(len(all_words)))
# print('Most common words: {}'.format(all_words.most_common(15)))


# use the 1500 most common words as features
# word_features = list(all_words.keys())[:1500]

#THIS CAN BE CHANGED

# The find_features function will determine which of the 1500 word features are contained in the review
def find_features(message, features):
    word_features=features
    words = word_tokenize(message)
    features = {}
    for word in word_features:
        features[word] = (word in words)

    return features

# Lets see an example!
# features = find_features(processed[0])
# for key, value in features.items():
#     if value == True:
#         print(key)


# # ----------------------------DILL CHECKPOINT------------------------------

# # To Save a session:
# import dill
# dill.dump_session('notebook_env.db')

# # To restore a session
# import dill
# dill.load_session('notebook_env.db')

# Now lets do it for all the messages
# messages = zip(processed, Y)
# test_messages = zip(processed[0:15000], Y[0:15000])
# msgs = zip(processed, Y)


# define a seed for reproducibility
# import numpy as np
# seed = 1
# np.random.seed = seed
# np.random.shuffle(test_messages)

# # call find_features function for each SMS message
# featuresets = [(find_features(text), label) for (text, label) in test_messages] #msgs or test_messages
# test_features = [find_features(test) for test in processed_test]
# # featuresets = processed.map(find_features)


# # we can split the featuresets into training and testing datasets using sklearn
# # split the data into training and testing datasets
# training, testing = model_selection.train_test_split(featuresets, test_size = 0.25, random_state=seed)


# print(len(training))
# print(len(testing))


# # ## Scikit-Learn Classifiers with NLTK
# # We can use sklearn algorithms in NLTK

# model = SklearnClassifier(SVC(kernel = 'linear'))

# # train the model on the training data
# model.train(training)

# # and test on the testing dataset!
# accuracy = nltk.classify.accuracy(model, testing)*100
# svc_predicted = nltk.classify(model, test_features)
# print(type(svc_predicted))
# svc_predicted.to_csv("Results")
# print("SVC Accuracy: {}".format(accuracy))

# # Define models to train
# names = ["K Nearest Neighbors", "Decision Tree", "Random Forest", "Logistic Regression", "SGD Classifier",
#          "Naive Bayes", "SVM Linear"]

# classifiers = [
#     KNeighborsClassifier(),
#     DecisionTreeClassifier(),
#     RandomForestClassifier(),
#     LogisticRegression(),
#     SGDClassifier(max_iter = 100),
#     MultinomialNB(),
#     SVC(kernel = 'linear')
# ]

# models = zip(names, classifiers)

# for name, model in models:
#     nltk_model = SklearnClassifier(model)
#     nltk_model.train(training)
#     accuracy = nltk.classify.accuracy(nltk_model, testing)*100
#     print("{} Accuracy: {}".format(name, accuracy))


# # Ensemble methods - Voting classifier

# names = ["K Nearest Neighbors", "Decision Tree", "Random Forest", "Logistic Regression", "SGD Classifier",
#          "Naive Bayes", "SVM Linear"]

# classifiers = [
#     KNeighborsClassifier(),
#     DecisionTreeClassifier(),
#     RandomForestClassifier(),
#     LogisticRegression(),
#     SGDClassifier(max_iter = 100),
#     MultinomialNB(),
#     SVC(kernel = 'linear')
# ]

# models = zip(names, classifiers)

# nltk_ensemble = SklearnClassifier(VotingClassifier(estimators = models, voting = 'hard', n_jobs = -1))
# nltk_ensemble.train(training)
# accuracy = nltk.classify.accuracy(nltk_model, testing)*100
# print("Voting Classifier: Accuracy: {}".format(accuracy))


# # make class label prediction for testing set
# txt_features, labels = zip(*testing)

# prediction = nltk_ensemble.classify_many(txt_features)

# # print a confusion matrix and a classification report
# print(classification_report(labels, prediction))

# pd.DataFrame(
#     confusion_matrix(labels, prediction),
#     index = [['actual', 'actual'], ['ham', 'spam']],
#     columns = [['predicted', 'predicted'], ['ham', 'spam']])



