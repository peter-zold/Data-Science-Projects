import math
import numpy as np
import pandas as pd
import xgboost as xgb
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score
from sklearn.model_selection import GridSearchCV
from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler,StandardScaler
import warnings


class Predict:
    def __init__(self, connection, get_data, display):
        self.connection = connection
        self.get_data = get_data
        self.display = display
        self.df_original = None
        self.model = None

    def prediction_execute(self):
        # initialize dataframe and model once
        if self.df_original is None or self.model is None:
            self.initialize_df_and_model()
        while True:
            # display menu
            self.display.display_prediction_menu()
            match input():
                case "1":
                    self.make_prediction()
                case "2":
                    self.make_future_prediction()
                case "3":
                    self.print_key_influencers()
                case "0":
                    break
                case _:
                    print("Not valid command")

    def make_prediction(self):
        print("Make prediction on filtered dataset")
        print()

        # import filtered data
        df = self.import_data()

        # transform data for prediction
        x_test, df_predict = self.transform_test_data(df)

        # make prediction with model and display results
        self.get_prediction_display(x_test=x_test, df_predict=df_predict)

    def make_future_prediction(self):
        print("Make prediction on filtered dataset")
        print("which simulates status X years later")
        print()
        # import filtered data
        df = self.import_data()

        print("How many years do you want to pass?")

        while True:
            try:
                years = int(input())
                break
            except ValueError:
                print("Error: years not in integer format")
                print("Please try again")
        # adapt values for the future
        print()
        print("For future estimation some info is needed:")
        print()
        print("Estimated yearly wage rise in percentage.")
        print("Expected format for e.g. 5% rise is '5' (without quotes)")
        while True:
            try:
                wage_rise = int(input())
                wage_rise_dec = 1 + wage_rise / 100
                break
            except ValueError:
                print("Error: years not in integer format")
                print("Please try again")

        print("Estimated increase in job level")
        print("Expected format: 0, 1, 2, 3, 4")
        while True:
            try:
                jl_rise = int(input())
                break
            except ValueError:
                print("Error: years not in integer format")
                print("Please try again")

        print("Estimated change in job involvement")
        print("Expected format: -3, -2, -1, 0, 1, 2, 3")
        while True:
            try:
                ji_change = int(input())
                break
            except ValueError:
                print("Error: years not in integer format")
                print("Please try again")

        print("Estimated change in stock option level")
        print("Expected format: -3, -2, -1, 0, 1, 2, 3")
        while True:
            try:
                sol_change = int(input())
                break
            except ValueError:
                print("Error: years not in integer format")
                print("Please try again")

        print("Will likely to work overtime? [Yes / No / unchanged]")
        overtime = input()

        # apply value transformations:
        df["Age"] = df["Age"] + years
        df["TotalWorkingYears"] = df["TotalWorkingYears"] + years
        df["YearsAtCompany"] = df["YearsAtCompany"] + years
        df["YearsInCurrentRole"] = df["YearsInCurrentRole"] + years
        df["YearsWithCurrentManager"] = df["YearsWithCurrentManager"] + years
        df["MonthlyIncome"] = df["MonthlyIncome"] * math.pow(wage_rise_dec, years)
        df["JobLevel"] = df["JobLevel"].apply(lambda x: x + jl_rise if (x + jl_rise) <= 5 else 5)
        df["JobInvolvement"] = df["JobInvolvement"].apply(lambda x: x + ji_change if 1 <= (x + ji_change) <= 4 else 1 if (x + ji_change) < 1 else 4)
        df["OverTime"] = df["OverTime"] if overtime == "unchanged" else overtime
        df["StockOptionLevel"] = df["StockOptionLevel"].apply(lambda x: x + sol_change if 0 <= (x + sol_change) <= 3 else 1 if (x + sol_change) < 0 else 3)

        # transform data for prediction
        x_test, df_predict = self.transform_test_data(df)

        # make prediction with model and display results
        self.get_prediction_display(x_test=x_test, df_predict=df_predict)


    def train_model(self, dataframe):
        print("Please wait around half a minute for the prediction model to be built")
        # Make a copy and only kepp relevant columns for analysis.
        # Other columns have insignificant correlation with attrition
        df = dataframe.copy(deep=True).loc[:,
             ["Age", "Attrition", "DistanceFromHome", "JobLevel", "JobInvolvement", "MonthlyIncome", "OverTime",
              "StockOptionLevel", "TotalWorkingYears", "TrainingTimesLastYear", "YearsAtCompany", "YearsInCurrentRole",
              "YearsWithCurrentManager"]]

        # Encode Overtime and Attrition columns to numeric
        encode = {"Attrition": {"Yes": 1, "No": 0}, "OverTime": {"Yes": 1, "No": 0}}
        df = df.replace(encode)

        # split target (attrition) column from the rest
        cols = list(df.columns)
        cols.remove('Attrition')

        # Oversampling, because attrition = Yes was present at low percentage
        over = SMOTE(sampling_strategy=0.85)
        f1 = df.loc[:, cols]
        t1 = df.loc[:, 'Attrition']

        steps = [('over', over)]
        pipeline = Pipeline(steps=steps)
        f1, t1 = pipeline.fit_resample(f1, t1)

        # splitting data to train and test the model
        x_train, x_test, y_train, y_test = train_test_split(f1, t1, test_size=0.15, random_state=42)

        mms = MinMaxScaler()  # Normalization
        ss = StandardScaler()  # Standardization

        # Normalization
        x_train['MonthlyIncome'] = mms.fit_transform(x_train[['MonthlyIncome']])
        x_test['MonthlyIncome'] = mms.transform(x_test[['MonthlyIncome']])
        x_train['TotalWorkingYears'] = mms.fit_transform(x_train[['TotalWorkingYears']])
        x_test['TotalWorkingYears'] = mms.transform(x_test[['TotalWorkingYears']])
        x_train['YearsAtCompany'] = mms.fit_transform(x_train[['YearsAtCompany']])
        x_test['YearsAtCompany'] = mms.transform(x_test[['YearsAtCompany']])
        x_train['YearsInCurrentRole'] = mms.fit_transform(x_train[['YearsInCurrentRole']])
        x_test['YearsInCurrentRole'] = mms.transform(x_test[['YearsInCurrentRole']])
        x_train['YearsWithCurrentManager'] = mms.fit_transform(x_train[['YearsWithCurrentManager']])
        x_test['YearsWithCurrentManager'] = mms.transform(x_test[['YearsWithCurrentManager']])

        # Standardization
        x_train['Age'] = ss.fit_transform(x_train[['Age']])
        x_test['Age'] = ss.transform(x_test[['Age']])
        x_train['JobInvolvement'] = ss.fit_transform(x_train[['JobInvolvement']])
        x_test['JobInvolvement'] = ss.transform(x_test[['JobInvolvement']])
        x_train['JobLevel'] = ss.fit_transform(x_train[['JobLevel']])
        x_test['JobLevel'] = ss.transform(x_test[['JobLevel']])
        x_train['OverTime'] = ss.fit_transform(x_train[['OverTime']])
        x_test['OverTime'] = ss.transform(x_test[['OverTime']])
        x_train['StockOptionLevel'] = ss.fit_transform(x_train[['StockOptionLevel']])
        x_test['StockOptionLevel'] = ss.transform(x_test[['StockOptionLevel']])
        x_train['TrainingTimesLastYear'] = ss.fit_transform(x_train[['TrainingTimesLastYear']])
        x_test['TrainingTimesLastYear'] = ss.transform(x_test[['TrainingTimesLastYear']])
        x_train['DistanceFromHome'] = ss.fit_transform(x_train[['DistanceFromHome']])
        x_test['DistanceFromHome'] = ss.transform(x_test[['DistanceFromHome']])

        # Initialize XGBoost Model

        model = xgb.XGBClassifier(
            objective='binary:logistic',
            nthread=4,
            seed=42
        )

        # Define parameter grid
        parameters = {
            'max_depth': range(2, 10, 1),
            'n_estimators': range(60, 220, 40),
            'learning_rate': [0.01, 0.05, 0.1]
        }

        # Grid search
        CV_model = GridSearchCV(
            estimator=model,
            param_grid=parameters,
            scoring='roc_auc',
            n_jobs=10,
            cv=10,
            verbose=False
        )
        CV_model.fit(x_train, y_train)

        # Best parameters
        learning_rate = CV_model.best_params_["learning_rate"]
        max_depth = CV_model.best_params_["max_depth"]
        n_estimators = CV_model.best_params_["n_estimators"]

        # build a model with best parameters
        model1 = xgb.XGBClassifier(objective='binary:logistic', nthread=4, seed=42, n_estimators=n_estimators,
                                   max_depth=max_depth, learning_rate=learning_rate)
        model1.fit(x_train, y_train)

        # Now lets predict with the test data
        y_test_pred = model1.predict(x_test)
        print()
        print("The model's performance scores:")
        print("Accuracy score: " + str(round(accuracy_score(y_test, y_test_pred), 4)))
        print("Precision score: " + str(round(precision_score(y_test, y_test_pred), 4)))
        print("Recall score: " + str(round(recall_score(y_test, y_test_pred), 4)))
        print("F1 score: " + str(round(f1_score(y_test, y_test_pred), 4)))
        print()

        return model1

    def transform_test_data(self, df):
        # create segment of df for identification for use during printing prediction results
        df_predict = df.loc[:, ["Employee_id", "FirstName", "LastName"]]

        # only keep columns relevant for machine learning model prediction
        x_test = df.loc[:,
             ["Age", "DistanceFromHome", "JobLevel", "JobInvolvement", "MonthlyIncome", "OverTime",
              "StockOptionLevel", "TotalWorkingYears", "TrainingTimesLastYear", "YearsAtCompany", "YearsInCurrentRole",
              "YearsWithCurrentManager"]]

        # Encode Overtime  to numeric
        encode = {"OverTime": {"Yes": 1, "No": 0}}
        x_test = x_test.replace(encode)

        mms = MinMaxScaler()  # Normalization
        ss = StandardScaler()  # Standardization

        # Normalization
        x_test['MonthlyIncome'] = mms.fit_transform(x_test[['MonthlyIncome']])
        x_test['TotalWorkingYears'] = mms.fit_transform(x_test[['TotalWorkingYears']])
        x_test['YearsAtCompany'] = mms.fit_transform(x_test[['YearsAtCompany']])
        x_test['YearsInCurrentRole'] = mms.fit_transform(x_test[['YearsInCurrentRole']])
        x_test['YearsWithCurrentManager'] = mms.fit_transform(x_test[['YearsWithCurrentManager']])

        # Standardization
        x_test['Age'] = ss.fit_transform(x_test[['Age']])
        x_test['JobInvolvement'] = ss.fit_transform(x_test[['JobInvolvement']])
        x_test['JobLevel'] = ss.fit_transform(x_test[['JobLevel']])
        x_test['OverTime'] = ss.fit_transform(x_test[['OverTime']])
        x_test['StockOptionLevel'] = ss.fit_transform(x_test[['StockOptionLevel']])
        x_test['TrainingTimesLastYear'] = ss.fit_transform(x_test[['TrainingTimesLastYear']])
        x_test['DistanceFromHome'] = ss.fit_transform(x_test[['DistanceFromHome']])

        return x_test, df_predict

    def import_data(self):
        # ignore warnings
        warnings.simplefilter(action='ignore', category=UserWarning)

        # get filter for prediction dataset
        filter_conditions = self.get_data.get_filter_conditions()

        # make pandas dataframe from filtered sql
        query_for_filtered = f"SELECT * FROM hr {filter_conditions}"
        df = pd.read_sql(query_for_filtered, con=self.connection)
        return df

    def get_prediction_display(self, x_test, df_predict):
        # make prediction
        predict_array = self.model.predict(x_test)
        # join prediction array with records of identity
        df_predict["Possible Attrition"] = predict_array
        # change back values to yes / no
        df_predict["Possible Attrition"] = df_predict["Possible Attrition"].apply(lambda x: "Yes" if x == 1 else "No")

        # print table
        print("Employees possible attrition:")
        pd.options.display.float_format = "{:.0f}".format
        with pd.option_context('display.max_rows', None,
                               'display.max_columns', None,
                               'display.precision', 3,
                               ):
            print(df_predict)

    def print_key_influencers(self):
        print("Importance of attributes")
        feature_importance = self.model.feature_importances_
        sorted_idx = np.argsort(feature_importance)
        fig = plt.figure(figsize=(12, 6))
        plt.barh(range(len(sorted_idx)), feature_importance[sorted_idx], align='center')
        plt.yticks(range(len(sorted_idx)),
                   np.array(["Age", "DistanceFromHome", "JobLevel", "JobInvolvement", "MonthlyIncome", "OverTime",
                "StockOptionLevel", "TotalWorkingYears", "TrainingTimesLastYear", "YearsAtCompany", "YearsInCurrentRole",
                "YearsWithCurrentManager"])[sorted_idx])
        plt.title('Attribute Importance')
        plt.show()

    def initialize_df_and_model(self):
        # make pandas dataframe from original sql
        warnings.simplefilter(action='ignore', category=UserWarning)
        query_for_original = f"SELECT * FROM hr"
        self.df_original = pd.read_sql(query_for_original, con=self.connection)

        # train model on original dataframe
        self.model = self.train_model(self.df_original)
