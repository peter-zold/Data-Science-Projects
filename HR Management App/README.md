# Introduction
I have created an HR Management Application for a fictitious company database. In addition to CRUD operations (Create, Read, Update, Delete), the application is capable of statistical evaluation of data and prediction based on a machine learning model.



https://github.com/peter-zold/Data-Analytics-Projects/assets/116908950/719674fc-a3d1-482e-8c42-bd903292e3f1



# Detailed description of features
## Initialize database
Strictly speaking, it is not part of the application itself, as the latter works with an existing database. This module creates an SQL database (sqlite3) from a csv file. The constraints on the columns of the table containing the data are adapted to the needs of the company.

## HR Management Application
### Register new data
It is possible to register new employee data into the system. The program asks for employee's data one by one via text prompts.

### Delete data
Rows can be deleted from the database if, for example, a new employee has been entered incorrectly. The application will take care to allow the user to check the details of the employee to be deleted and will also ask for confirmation.

### Modify data
It is also possible to change the attributes of employees in the database. The application will take care to allow the user to check the details of the employee to be modified and will also ask for confirmation.

### Get data
The application allows you to search quickly by name, by ID or filter by any criteria. It is also possible to sort the retrieved data by some criteria. I also added a useful feature to save the results of a query for later analysis.

### Statistical analysis
The data can be grouped by up to three attributes, and the statistical indicators (min, Q1, median, Q3, max, stddev, avg, sum) of an arbitrary numeric quantity are evaluated. It is also possible to pre-filter the data.

### Predict attrition
The app's most unique feature is its ability to predict whether an employee is likely to leave in the near and distant future. It uses a machine learning model* built on the existing data. It also allows the user to modify the data and adapt it to the future to make the prediction. The program can also generate visualisations of the main factors influencing departure. So this feature is a powerful tool to help a company fight attrition and help plan for the present and the future.

*The machine learning model is based on XGBoost and scores around 90% in accuracy, recall, precision and f1. A careful selection of relevant features and thorough feature engineering preceded the construction of the model

## Used technologies and tools
- Python (with numpy, pandas, scikit-learn, xgboost and so on) 
- SQL (sqlite3 and sqlean extension)

## Used dataset
I used a modified version of the following dataset. I added names generated by random name generator to it.
Source: https://www.kaggle.com/datasets/pavansubhasht/ibm-hr-analytics-attrition-dataset

## Future plans:
- I want to make a graphical interface for the application
- I would like to extend the statistical analysis functions.
