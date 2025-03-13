# Import necessary libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import Ridge
from sklearn.linear_model import Lasso
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.model_selection import learning_curve
from sklearn import svm

# Load the dataset
df = pd.read_csv('cryptocurrency_data.csv')
print(df)
# Split the dataset into training and test sets
X = df.drop(['Close', 'Symbol', 'Open_time'], axis=1)
y = df['Close']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Define features and labels
features = X_train.columns
labels = y_train

# Preprocess the data
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Create the model and choose an appropriate algorithm
model = LinearRegression()

# Grid search for hyperparameters tuning
params = {'fit_intercept':[True,False], 'normalize':[True,False], 'copy_X':[True, False]}
grid_search = GridSearchCV(model, params, cv=5, n_jobs=-1)
grid_search.fit(X_train,y_train)

# Train the model
model.fit(X_train, y_train)

# Regularization techniques
ridge_model = Ridge(alpha=0.1)
ridge_model.fit(X_train, y_train)

lasso_model = Lasso(alpha=0.1)
lasso_model.fit(X_train, y_train)


# Evaluate the model's performance
score = model.score(X_test, y_test)
ridge_score = ridge_model.score(X_test, y_test)
lasso_score = lasso_model.score(X_test, y_test)

# Use the model to make predictions
predictions = model.predict(X_test)
ridge_predictions = ridge_model.predict(X_test)
lasso_predictions = lasso_model.predict(X_test)

# Retrain the model
df_new = pd.read_csv('new_cryptocurrency_data.csv')
X_new = df_new.drop(['Close', 'Symbol', 'Open_time'], axis=1)
y_new = df_new['Close']
X_new_train, X_new_test, y_new_train, y_new_test = train_test_split(X_new, y_new, test_size=0.2, random_state=42)
X_new_train = scaler.fit_transform(X_new_train)
X_new_test = scaler.transform(X_new_test)

# Train the model
model.fit(X_new_train, y_new_train)
ridge_model.fit(X_new_train, y_new_train)
lasso_model.fit(X_new_train, y_new_train)

# Evaluate the updated model's performance
score_new = model.score(X_new_test, y_new_test)
ridge_score_new = ridge_model.score(X_new_test, y_new_test)
lasso_score_new = lasso_model.score(X_new_test, y_new_test)

# Calculate the metrics for both models
score_old = model.score(X_test, y_test)
score_new = model.score(X_new_test, y_new_test)

# Plot the learning curves
train_sizes, train_scores, test_scores = learning_curve(model, X_train, y_train)
train_sizes_new, train_scores_new, test_scores_new = learning_curve(model, X_new_train, y_new_train)
plt.plot(train_sizes, train_scores, color='b', label='Old model')
plt.plot(train_sizes_new, train_scores_new, color='r', label='New model')
plt.xlabel('Training samples')
plt.ylabel('Accuracy')
plt.title('Learning curves')
plt.legend()
plt.show()

# Save the model
import joblib
joblib.dump(model, 'cryptocurrency_model.pkl')
joblib.dump(ridge_model, 'ridge_model.pkl')
joblib.dump(lasso_model, 'lasso_model.pkl')