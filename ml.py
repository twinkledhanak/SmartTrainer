import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Importing the dataset
dataset = pd.read_csv('dataset_latest.csv')
X = dataset.iloc[:, :13].values
y = dataset.iloc[:, -1].values

# Splitting the dataset into the Training set and Test set
from sklearn.cross_validation import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25, random_state = 0)
x_scale_1=[[20,67,162,1,25.52964487,0,0,0,0,1,0,0,0]]
# Feature Scaling
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)
x_scale_1=sc.transform(x_scale_1)

print(x_scale_1)
# Fitting classifier to the Training set
# Create your classifier here
from sklearn.svm import SVC
svm_model_linear = SVC(kernel = 'linear', C = 1).fit(X_train, y_train)
svm_predictions = svm_model_linear.predict(X_test)
pred_scale=svm_model_linear.predict(x_scale_1)
# Predicting the Test set results
#y_pred = classifier.predict(X_test)

# Making the Confusion Matrix
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, svm_predictions)
from sklearn.metrics import accuracy_score

print(accuracy_score(y_test,svm_predictions))