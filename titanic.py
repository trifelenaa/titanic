# -*- coding: utf-8 -*-
"""titanic

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1e6y7ZLW3snZuNwC1CRZtCW7SyuKdLGR5

# Загрузка данных и библиотек

Загрузить данные можно отсюда: [*диск*](https://disk.yandex.ru/d/qMrhTIIA_CZIqQ)
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import SGDClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neural_network import MLPClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score

# Read in data into a dataframe
data = pd.read_csv('train.csv')

# Display top of dataframe
data.head()

"""# Препроцессинг для обучающей выборки"""

data.info()

data.isnull().sum()

data['Age'] = data['Age'].fillna(data.groupby(['Sex', 'Pclass'])['Age'].transform('median'))

data['Embarked'].fillna(data['Embarked'].mode()[0], inplace=True)

data = pd.get_dummies (data, columns=['Sex','Embarked'], drop_first = True )

data['Name'] = data['Name'].apply(lambda x: x.split(', ')[1].split('. ')[0])

from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()

data['Ticket'] = le.fit_transform(data['Ticket'])
data['Name'] = le.fit_transform(data['Name'])

X = data.drop(columns = ['PassengerId','Survived', 'Cabin'],axis=1)
y = data['Survived']

corr = X.corr()
corr.style.background_gradient(cmap='coolwarm')

"""# Обучение и валидация"""

#разделим обучающую выборку на две части, одна из которых валидационная
X_train, X_val, Y_train, Y_val = train_test_split(X,y, test_size=0.2, random_state=37)

#напишем для удобства функцию, выполняющую поиск по сетке и выдающую результаты подсчета accuracy на валидационной части

def grid_search_val (model, parameters):

    model = GridSearchCV(model, parameters, verbose=1,n_jobs=-1,cv=3)
    model.fit(X_train, Y_train)

    val_predictions = model.predict(X_val)
    val_data_accuracy = accuracy_score(Y_val, val_predictions)

    return str(model.best_params_), str(model.best_score_), val_data_accuracy, model

#стохастический
model_sgd = SGDClassifier()

parameters_sgd = {'loss':('hinge', 'log_loss',  'squared_error',  'epsilon_insensitive' ),
              'alpha':[0.01, 1e-3, 1e-4, 3e-4],
              'penalty':('l2', 'l1', 'elasticnet')}

#нейронные
model_neural = MLPClassifier()

parameters_neural = {'activation':('logistic', 'tanh', 'relu'),
              'solver':('lbfgs', 'sgd', 'adam'),
              'learning_rate_init':[0.1, 0.01, 3e-4, 1e-3]}

#градиентный бустинг
model_boost = GradientBoostingClassifier()

parameters_boost = {'loss':('log_loss', 'exponential'),
              'learning_rate':[0.1, 0.01, 3e-4, 1e-3],
              'n_estimators':[10,50,75,100,150],
              'criterion':('friedman_mse', 'squared_error')}

#случайный лес
model_trees = RandomForestClassifier()

parameters_trees = {'n_estimators':[1,5,10,20,50,100],
          'max_depth':[5,10,15,20,30],
          'min_samples_leaf':[1,5,10,20],
          'random_state':[42, 37]}

#наивный байесовский
model_gaus= GaussianNB()

parameters_gaus = {'var_smoothing':[1e-9, 3e-9,1e-8, 1e-7]}

#лог регрессия????

best_params_boost, best_score_boost, val_data_accuracy_boost, model_boost = grid_search_val(model_boost,
                                                                              parameters_boost)

print('Best hyperparameters for boosting are: '+ best_params_boost)
print('Best score for boosting is: '+ best_score_boost )
print('Accuracy score of validation data for boosting : ', val_data_accuracy_boost)

best_params_trees, best_score_trees, val_data_accuracy_trees, model_trees = grid_search_val(model_trees,
                                                                              parameters_trees)

print('Best hyperparameters for forest are: '+ best_params_trees)
print('Best score for forest is: '+ best_score_trees )
print('Accuracy score of validation data for forest : ', val_data_accuracy_trees)

best_params_neural, best_score_neural, val_data_accuracy_neural, model_neural = grid_search_val(model_neural,
                                                                              parameters_neural)

print('Best hyperparameters for neural are: '+ best_params_neural)
print('Best score for neural is: '+ best_score_neural )
print('Accuracy score of validation data for neural : ', val_data_accuracy_neural)

best_params_sgd, best_score_sgd, val_data_accuracy_sgd, model_sgd = grid_search_val(model_sgd,
                                                                              parameters_sgd)

print('Best hyperparameters for sgd are: '+ best_params_sgd)
print('Best score for sgd is: '+ best_score_sgd )
print('Accuracy score of validation data for sgd : ', val_data_accuracy_sgd)

best_params_gaus, best_score_gaus, val_data_accuracy_gaus, model_gaus = grid_search_val(model_gaus,
                                                                              parameters_gaus)

print('Best hyperparameters for gaus are: '+ best_params_gaus)
print('Best score for gaus is: '+ best_score_gaus )
print('Accuracy score of validation data for gaus : ', val_data_accuracy_gaus)

"""# Препроцессинг тестовых данных, аналогичный обучающему"""

test_data = pd.read_csv('test.csv')

test_data.isnull().sum()

test_data['Age'] = test_data['Age'].fillna(test_data.groupby(['Sex', 'Pclass'])['Age'].transform('median'))

test_data = pd.get_dummies (test_data, columns=['Sex','Embarked'], drop_first = True )

test_data['Fare'] = test_data['Fare'].fillna(test_data['Fare'].median())

test_data['Name'] = test_data['Name'].apply(lambda x: x.split(', ')[1].split('. ')[0])

test_data['Ticket'] = le.fit_transform(test_data['Ticket'])
test_data['Name'] = le.fit_transform(test_data['Name'])

X_test = test_data.drop(columns = ['PassengerId','Cabin'],axis=1)

#предсказания  на тестовой части
predictions = model_boost.predict(X_test)

#подсчет accuracy
test_Y = pd.read_csv('gender_submission.csv')
Y_test = test_Y['Survived']
test_data_accuracy = accuracy_score(Y_test, predictions)
print('Accuracy на тестовой выборке:', test_data_accuracy)

#запись результатов в файл
output = pd.DataFrame({'PassengerId': test_data.PassengerId, 'Survived': predictions})
output.to_csv('submission.csv', index=False)