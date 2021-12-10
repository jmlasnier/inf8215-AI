"""
Team:
<<<<< TEAM NAME >>>>>
Authors:
<<<<< NOM COMPLET #1 - MATRICULE #1 >>>>>
<<<<< NOM COMPLET #2 - MATRICULE #2 >>>>>
"""

from wine_testers import WineTester

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split


class MyWineTester(WineTester):
    def __init__(self):
        # TODO: initialiser votre modèle ici:
        self.all_features_list = ['id','color', 'fixed acidity', 'volatile acidity', 'citric acid',
       'residual sugar', 'chlorides', 'free sulfur dioxide',
       'total sulfur dioxide', 'density', 'pH', 'sulphates', 'alcohol']
        self.model = None
        

    def train(self, X_train, y_train):
        """
        train the current model on train_data
        :param X_train: 2D array of data points.
                each line is a different example.
                each column is a different feature.
                the first column is the example ID.
        :param y_train: 2D array of labels.
                each line is a different example.
                the first column is the example ID.
                the second column is the example label.
        """
        # TODO: entrainer un modèle sur X_train & y_train
        #X
        
        X = pd.DataFrame(X_train, columns=self.all_features_list)
        X = X.drop(['id','color'], axis=1)
        X = np.array(X)
        
        Y = pd.DataFrame(y_train, columns=['id','quality'])
        Y = Y.drop(['id'], axis=1)
        Y = np.array(Y)
        
        X_train, X_test, label_train, label_test = train_test_split(X,Y, test_size=0.2, random_state=0)

        #Entrainement du model de regression
        #create regressor object
        self.model = RandomForestClassifier(n_estimators=10000, random_state=42, criterion="gini", max_features="auto" )
        self.model.fit(X_train, label_train)


    def predict(self, X_data):
        """
        predict the labels of the test_data with the current model
        and return a list of predictions of this form:
        [
            [<ID>, <prediction>],
            [<ID>, <prediction>],
            [<ID>, <prediction>],
            ...
        ]
        :param X_data: 2D array of data points.
                each line is a different example.
                each column is a different feature.
                the first column is the example ID.
        :return: a 2D list of predictions with 2 columns: ID and prediction
        """
        # TODO: make predictions on X_data and return them
        data = pd.DataFrame(X_data, columns=self.all_features_list)
        
        data = data.drop(['id','color'], axis=1)
        
        predictions = self.model.predict(data.values)
        
        predictions =  np.append(np.array(list(range(len(predictions)))),np.array(predictions), axis=0).reshape(2,len(predictions)).transpose()
        
        return list(predictions)
