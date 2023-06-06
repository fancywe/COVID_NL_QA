import numpy as np
import pandas as pd
# import matplotlib.pyplot as plt
import re
import random
import warnings
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
# from xgboost import XGBClassifier
# from sklearn.metrics import roc_auc_score, confusion_matrix, plot_confusion_matrix, plot_precision_recall_curve
# data = data.sample(frac=1).reset_index(drop=True)
# split_pcent = 0.1
# split = int(split_pcent * len(data))

# Shuffles dataframe
# data = data.sample(frac=1).reset_index(drop=True)


warnings.simplefilter("ignore")

#Load training set
data = pd.read_csv('Training set.csv')
#Shuffle and split the Training set
train, valid = train_test_split(data, test_size=0.1,shuffle=True)

# Training Sets
print(type(train),type(valid))
trainX = train['Question']
trainY = train['Type'].values

# Validation Sets
# valid = data[:split]
validX = valid['Question']
validY = valid['Type'].values

#Load the vectorizer, fit on training set and do the transform on validation set
vectorizer = TfidfVectorizer()
trainX = vectorizer.fit_transform(trainX)
validX = vectorizer.transform(validX)

#Use Random Forest classify algorithm 
rf_classifier = RandomForestClassifier()
rf_classifier.fit(trainX, trainY)

#Loading complete prompt
print('loaded')


def Handle(Q):
    print(Q)
    VecQ=[Q]
    VecQ = vectorizer.transform(VecQ)
    Answer = rf_classifier.predict(VecQ)
    return Answer
    
    
