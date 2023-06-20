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
from county_code import countyName
import state_code
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
# from xgboost import XGBClassifier
# from xgboost import XGBClassifier
# from sklearn.metrics import roc_auc_score, confusion_matrix, plot_confusion_matrix, plot_precision_recall_curve
# data = data.sample(frac=1).reset_index(drop=True)
# split_pcent = 0.1
# split = int(split_pcent * len(data))

# Shuffles dataframe
# data = data.sample(frac=1).reset_index(drop=True)
# valid = data[:split]
weekCase=state_code.dict_for_regular_data['week case info']
weekDeath=state_code.dict_for_regular_data['week death info']
weekTest=state_code.dict_for_regular_data['test info']
weekHosp=state_code.dict_for_regular_data['Hosp info']

stateCode=list(state_code.state_codes.keys())
stateFullName=list(map(str.lower,state_code.states.values()))
countyName=list(map(str.lower,countyName))
vac=state_code.dict_for_vac

# state=''
# county=''
def check_state(Q):
     
        for stateName in stateFullName:
                if(stateName in Q.lower()):
                    return 1 
        for stateName in stateCode:
                if stateName in Q:
                        return 1
        return 0
def check_county(Q): 
        Q=Q.lower() 
        for name in countyName:    
                if(name in Q):
                    return 1
        return 0  
    
def create_features(data):
    # Check if the text contains corresponding keywords
    data['length'] = data['Question'].apply(len)
    data['comma'] = data['Question'].apply(lambda x: 1 if ',' in x else 0)
    data['word_count'] = data['Question'].apply(lambda x: len(str(x).split(" ")))
    data['have_state'] = data['Question'].apply(lambda x:check_state(x))
    data['have_county'] = data['Question'].apply(lambda x:check_county(x))
    data['week_case_info'] = data['Question'].apply(lambda x: 1 if any(word in x.lower() for word in weekCase) else 0)
    data['week_death_info'] = data['Question'].apply(lambda x: 1 if any(word in x.lower() for word in weekDeath) else 0)
    data['test_info'] = data['Question'].apply(lambda x: 1 if any(word in x.lower() for word in weekTest) else 0)
    data['hosp_info'] = data['Question'].apply(lambda x: 1 if any(word in x.lower() for word in weekHosp) else 0)
    return data

def create_features_single(Q,state,county):
    features = {}
    features['Question'] = Q
    features['comma'] = 1 if ',' in Q else 0
    features['length'] = len(Q)
    features['word_count'] =len(str(Q).split(" "))
    features['have_state'] = state
    features['have_county'] = county
    features['week_case_info'] = 1 if any(word in Q.lower() for word in weekCase) else 0
    features['week_death_info'] = 1 if any(word in Q.lower() for word in weekDeath) else 0
    features['test_info'] = 1 if any(word in Q.lower() for word in weekTest) else 0
    features['hosp_info'] = 1 if any(word in Q.lower() for word in weekHosp) else 0
    return pd.DataFrame([features])
 
warnings.simplefilter("ignore")

#Load training set
data = pd.read_csv('Training set.csv')

# create features
data = create_features(data)
print(data.to_string())
#Shuffle and split the Training set
train, valid = train_test_split(data, test_size=0.2,shuffle=True)

# Training Sets
trainX = train.drop('Type', axis=1)
trainY = train['Type'].values

# Validation Sets
validX = valid.drop('Type', axis=1)
validY = valid['Type'].values

# preprocessor
preprocessor = ColumnTransformer(
    transformers=[
        ('tfidf', TfidfVectorizer(), 'Question'),
        ('num', StandardScaler(), ['length','word_count','have_state','have_county', 'week_case_info', 'week_death_info', 'test_info', 'hosp_info'])
    ])

#Combine vectorizer with classifier in a pipeline
model_pipeline = Pipeline(steps=[
  ('preprocessor', preprocessor),
  ('classifier', RandomForestClassifier())
])

# train the model
model_pipeline.fit(trainX, trainY)

# validate the model
valid_predictions = model_pipeline.predict(validX)
print(f"Validation Accuracy of Random Forest Classifier is: {(model_pipeline.score(validX, validY))*100:.2f}%")

# model_pipeline = Pipeline(steps=[
#   ('preprocessor', preprocessor),
#   ('classifier', LogisticRegression(C=1.))
# ])
# model_pipeline.fit(trainX, trainY)

# # validate the model
# valid_predictions = model_pipeline.predict(validX)
# print(f"Validation Accuracy of Logistic Regression is: {(model_pipeline.score(validX, validY))*100:.2f}%")

# # model_pipeline = Pipeline(steps=[
# #   ('preprocessor', preprocessor),
# #   ('classifier', MultinomialNB())
# # ])
# # model_pipeline.fit(trainX, trainY)

# # # validate the model
# # valid_predictions = model_pipeline.predict(validX)
# # print(f"Validation Accuracy of MultinomialNB is: {(model_pipeline.score(validX, validY))*100:.2f}%")

# model_pipeline = Pipeline(steps=[
#   ('preprocessor', preprocessor),
#   ('classifier', DecisionTreeClassifier())
# ])
# model_pipeline.fit(trainX, trainY)

# # validate the model
# valid_predictions = model_pipeline.predict(validX)
# print(f"Validation Accuracy of DecisionTree Classifier is: {(model_pipeline.score(validX, validY))*100:.2f}%")

# model_pipeline = Pipeline(steps=[
#   ('preprocessor', preprocessor),
#   ('classifier', KNeighborsClassifier())
# ])
# model_pipeline.fit(trainX, trainY)

# # validate the model
# valid_predictions = model_pipeline.predict(validX)
# print(f"Validation Accuracy of KNeighbors Classifier is: {(model_pipeline.score(validX, validY))*100:.2f}%")

# model_pipeline = Pipeline(steps=[
#   ('preprocessor', preprocessor),
#   ('classifier', XGBClassifier())
# ])
# model_pipeline.fit(trainX, trainY)

# # validate the model
# valid_predictions = model_pipeline.predict(validX)
# print(f"Validation Accuracy of XGBClassifier is: {(model_pipeline.score(validX, validY))*100:.2f}%")

def Handle(Q,state,county):
    print(Q)
    features = create_features_single(Q,state,county)
    Answer = model_pipeline.predict(features)
    return Answer
    
    
