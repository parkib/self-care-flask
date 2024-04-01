import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.naive_bayes import GaussianNB

class HeartModel:
    _instance = None
    
    def __init__(self):
        self.model = None
        self.dt = None
        self.features = ['age', 'sex', 'cp', 'trtpbs', 'chol', 'exng']
        self.target = 'heart'
        self.heart_data = None

    def _clean(self, url):
        # Load the dataset
        self.heart_data = pd.read_csv(url)
        
        # Drop unnecessary columns
        self.heart_data.drop(['fbs', 'restecg', 'thalachh', 'oldpeak'], axis=1, inplace=True)

        # Convert boolean columns to integers
        self.heart_data['sex'] = self.heart_data['sex'].apply(lambda x: 1 if x == 'male' else 0)
        self.heart_data['exng'] = self.heart_data['exng'].apply(lambda x: 1 if x == 'Yes' else 0)
    
        # Drop rows with missing values
        self.heart_data.dropna(inplace=True)

    def _train(self):
        # Split the data into features and target
        X = self.heart_data[self.features]
        y = self.heart_data[self.target]
        
        # Perform train-test split
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
        
        # Train the logistic regression model
        self.model = LogisticRegression(max_iter=1000)
        self.model.fit(X_train, y_train)
        
        # Train a decision tree classifier
        self.dt = DecisionTreeClassifier()
        self.dt.fit(X_train, y_train)
        
        # Train Gaussian Naive Bayes
        self.gnb = GaussianNB()
        self.gnb.fit(X_train, y_train)
        
    @classmethod
    def get_instance(cls, url):
        if cls._instance is None:
            cls._instance = cls()
            cls._instance._clean(url)
            cls._instance._train()
        return cls._instance

    def predict(self, individual):
        individual_df = pd.DataFrame(individual, index=[0])
        individual_df['sex'] = individual_df['sex'].apply(lambda x: 1 if x == 'Male' else 0)
        individual_df['exng'] = individual_df['exng'].apply(lambda x: 1 if x == 'Yes' else 0)
        heart = np.squeeze(self.model.predict_proba(individual_df))
        return {'heart': heart}

    def feature_weights(self):
        importances = self.dt.feature_importances_
        return {feature: importance for feature, importance in zip(self.features, importances)}

def initHeart():
    url = 'https://drive.google.com/file/d/1kJcitXtlysIg1pCPQxV-lMSVTFsLWOkv'
    HeartModel.get_instance(url)
    
def testHeart():
    HeartModel_instance = HeartModel.get_instance(url)
    
    individual = {
        'age': 14,
        'sex': 'Male',
        'cp': 2,
        'trtpbs': 130,
        'chol': 204,
        'exng': 0,
    }
    

    HeartModel = HeartModel.get_instance()
    print(" Step 2:", HeartModel.get_instance.__doc__)
   
    # print the survival probability
    print(" Step 3:", HeartModel.predict.__doc__)
    probability = HeartModel.predict(individual)
    print('\t Heart probability: {:.2%}',(probability.get('heart')))  
    print()
    
    # print the feature weights in the prediction model
    print(" Step 4:", HeartModel.feature_weights.__doc__)
    importances = HeartModel.feature_weights()
    for feature, importance in importances.items():
        print("\t\t", feature, f"{importance:.2%}") # importance of each feature, each key/value pair
        
if __name__ == "__main__":
    print(" Begin:", testHeart.__doc__)
    testHeart()
    
    probability = HeartModel_instance.predict(individual)
    print('Heart probability:', probability.get('heart'))

    importances = HeartModel_instance.feature_weights()
    for feature, importance in importances.items():
        print(feature, 'importance:', importance)

if __name__ == "__main__":
    url = 'https://drive.google.com/file/d/1kJcitXtlysIg1pCPQxV-lMSVTFsLWOkv'
    initHeart()
    testHeart()
    