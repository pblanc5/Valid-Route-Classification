import nltk
import random

good_data = open('../training/good_routes', 'r').read()
bad_data1 = open('../training/bad_routes1', 'r').read()
bad_data2 = open('../training/bad_routes2', 'r').read()

documents = []

for r in good_data.split('\n'):
    documents.append((r, 'good'))
    
for r in bad_data1.split('\n'):
    documents.append((r, 'bad'))
    
for r in bad_data2.split('\n'):
    documents.append((r, 'bad'))

good_words = nltk.word_tokenize(good_data)
bad_words1 = nltk.word_tokenize(bad_data1)
bad_words2 = nltk.word_tokenize(bad_data2)

all_words = []

for w in good_words:
    all_words.append(w.lower())
    
for w in bad_words1:
    all_words.append(w.lower())
    
for w in bad_words2:
    all_words.append(w.lower())


all_words = nltk.FreqDist(all_words)
word_features = list(all_words.keys())

def find_features(document):
    words = nltk.word_tokenize(document)
    features = {}
    for w in word_features:
        features[w] = (w in words)
    return features

featuresets = [(find_features(rev), category) for (rev, category) in documents]
random.shuffle(featuresets)
train_set, test_set = featuresets[:10000], featuresets[10000:]

classifier = nltk.NaiveBayesClassifier.train(train_set)
print("Naive Bayes Accuracy:", nltk.classify.accuracy(classifier, test_set) * 100)
classifier.show_most_informative_features(25)

import numpy
import scipy
from nltk.classify import SklearnClassifier
from sklearn.naive_bayes import MultinomialNB, GaussianNB, BernoulliNB

MNB_classifier = SklearnClassifier(MultinomialNB())
MNB_classifier.train(train_set)
print("MNB Accuracy:", nltk.classify.accuracy(MNB_classifier, test_set) * 100)

BNB_classifier = SklearnClassifier(BernoulliNB())
BNB_classifier.train(train_set)
print("BNB Accuracy:", nltk.classify.accuracy(BNB_classifier, test_set) * 100)

from sklearn.linear_model import LogisticRegression, SGDClassifier

LR_classifier = SklearnClassifier(LogisticRegression())
LR_classifier.train(train_set)
print("LR Accuracy:", nltk.classify.accuracy(LR_classifier, test_set) * 100)

SGD_classifier = SklearnClassifier(SGDClassifier())
SGD_classifier.train(train_set)
print("SGD Accuracy:", nltk.classify.accuracy(SGD_classifier, test_set) * 100)

from sklearn.svm import SVC, LinearSVC, NuSVC

LSVC_classifier = SklearnClassifier(LinearSVC())
LSVC_classifier.train(train_set)
print("LSVC Accuracy:", nltk.classify.accuracy(LSVC_classifier, test_set) * 100)

NuSVC_classifier = SklearnClassifier(NuSVC())
NuSVC_classifier.train(train_set)
print("NuSVC Accuracy:", nltk.classify.accuracy(NuSVC_classifier, test_set) * 100)

from nltk.classify import ClassifierI
from statistics import mode

class VoteClassifier(ClassifierI):
    
    def __init__(self, *classifiers):
        self._classifiers = classifiers
        
    def classify(self, features):
        votes = []
        for classifier in self._classifiers:
            vote = classifier.classify(features)
            votes.append(vote)
        return mode(votes)
    
    def confidence(self, features):
        votes = []
        for classifier in self._classifiers:
            vote = classifier.classify(features)
            votes.append(vote)
            
        choice_votes = votes.count(mode(votes))
        conf = choice_votes / len(votes)
        return conf
    
    
V_classifier = VoteClassifier(classifier, MNB_classifier, BNB_classifier, LR_classifier, 
                              SGD_classifier,LSVC_classifier, NuSVC_classifier)
print("Vote Accuracy:", nltk.classify.accuracy(V_classifier, test_set) * 100)

for i in range(0,100):
    print("Classification:", V_classifier.classify(test_set[i][0]), 
          "Confidence:", "{:5.2f}".format(V_classifier.confidence(test_set[i][0]) * 100), 
          "Actual Class:", test_set[i][1])
    
    
