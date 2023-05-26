import numpy as np
import pandas as pd
# import matplotlib.pyplot as plt
import re
import random
import warnings

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
# from xgboost import XGBClassifier
# from sklearn.metrics import roc_auc_score, confusion_matrix, plot_confusion_matrix, plot_precision_recall_curve


warnings.simplefilter("ignore")
data = pd.read_csv('Training set.csv')
data = data.sample(frac=1).reset_index(drop=True)
# print(data)

train =data
trainX = data['Question']
trainY = data['Type'].values

# valid = data[61:63]
# validX = valid['Question']
# validY = valid['Type'].values

vectorizer = TfidfVectorizer()

trainX = vectorizer.fit_transform(trainX)
# validX = vectorizer.transform(validX)

lr_classifier = LogisticRegression(C=1.)
lr_classifier.fit(trainX, trainY)
print('loaded')
# print(f"Validation Accuracy of Logsitic Regression Classifier is: {(lr_classifier.score(validX, validY))*100:.2f}%")


def Handle(Q):
    print(Q)
    VecQ=[Q]
    VecQ = vectorizer.transform(VecQ)
    Answer = lr_classifier.predict(VecQ)
    return Answer
    
    
