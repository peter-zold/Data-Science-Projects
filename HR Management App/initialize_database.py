import csv
import sqlean as sqlite3


def initialize_database():
    # read the csv file
    with open('HR_database.csv', 'r') as csvfile:
        # create the object of csv.reader()
        csv_file_reader = csv.reader(csvfile, delimiter=',')
        # skip the header
        next(csv_file_reader, None)
        # create fileds
        Employee_id = ''
        Age = ''
        FirstName = ''
        LastName = ''
        Gender = ''
        Department = ''
        JobRole = ''
        Attrition = ''
        DistanceFromHome = ''
        JobLevel = ''
        JobInvolvement = ''
        MonthlyIncome = ''
        OverTime = ''
        StockOptionLevel = ''
        TotalWorkingYears = ''
        TrainingTimesLastYear = ''
        YearsAtCompany = ''
        YearsInCurrentRole = ''
        YearsWithCurrentManager = ''

        ##### create a database table using sqlite3###

        # 1. create query
        table_query = '''
        CREATE TABLE if not Exists hr 
        (
        Employee_id INTEGER PRIMARY KEY,
        FirstName TEXT NOT NULL,
        LastName TEXT NOT NULL,
        Age INTEGER  CHECK (Age BETWEEN 14 AND 99),
        Gender TEXT  CHECK (Gender IN ('Female', "Male")),
        Department TEXT CHECK (Department IN ('Sales', 'Research & Development', 'Human Resources')),
        JobRole TEXT CHECK (JobRole IN ('Manager', 'Sales Executive', 'Sales Representative',
                            'Healthcare Representative', 'Laboratory Technician', 'Manufacturing Director',
                            'Research Director', 'Research Scientist', 'Human Resources')),
        Attrition TEXT DEFAULT "No" CHECK (Attrition IN ('Yes', 'No')),
        DistanceFromHome INTEGER NOT NULL,
        JobLevel INTEGER CHECK (JobLevel BETWEEN 1 AND 5),
        JobInvolvement INTEGER CHECK (JobInvolvement BETWEEN 1 AND 4),
        MonthlyIncome INTEGER NOT NULL,
        OverTime TEXT CHECK (OverTime IN ('Yes', 'No')),
        StockOptionLevel INTEGER CHECK (StockOptionLevel BETWEEN 0 AND 3),
        TotalWorkingYears INTEGER NOT NULL,
        TrainingTimesLastYear INTEGER DEFAULT 0,
        YearsAtCompany INTEGER DEFAULT 0,
        YearsInCurrentRole INTEGER DEFAULT 0,
        YearsWithCurrentManager INTEGER DEFAULT 0
        );
        '''

        # 2. create database
        connection = sqlite3.connect('HR_database.db')
        cursor = connection.cursor()
        # 3. execute table query to create table
        cursor.execute(table_query)

        # 4. parse csv data
        for row in csv_file_reader:
            # skip the first row
            for i in range(len(row)):
                # assign each field its value
                Employee_id = int(row[0])
                Age = int(row[1])
                Gender = row[2]
                Department = row[3]
                JobRole = row[4]
                Attrition = row[5]
                DistanceFromHome = int(row[6])
                JobLevel = int(row[7])
                JobInvolvement = int(row[8])
                MonthlyIncome = int(row[9])
                OverTime = row[10]
                StockOptionLevel = int(row[11])
                TotalWorkingYears = int(row[12])
                TrainingTimesLastYear = int(row[13])
                YearsAtCompany = int(row[14])
                YearsInCurrentRole = int(row[15])
                YearsWithCurrentManager = int(row[16])
                FirstName = row[17]
                LastName = row[18]

            # 5. create insert query
            InsertQuery = f"""INSERT INTO hr 

            (
            Employee_id,
        FirstName,
        LastName,
        Age,
        Gender,
        Department,
        JobRole,
        Attrition,
        DistanceFromHome,
        JobLevel,
        JobInvolvement,
        MonthlyIncome,
        OverTime,
        StockOptionLevel,
        TotalWorkingYears,
        TrainingTimesLastYear,
        YearsAtCompany,
        YearsInCurrentRole,
        YearsWithCurrentManager
        )
        VALUES (
        {Employee_id},
        '{FirstName}',
        '{LastName}',
        {Age},
        '{Gender}',
        '{Department}',
        '{JobRole}',
        '{Attrition}',
        {DistanceFromHome},
        {JobLevel},
        {JobInvolvement},
        {MonthlyIncome},
        '{OverTime}',
        {StockOptionLevel},
        {TotalWorkingYears},
        {TrainingTimesLastYear},
        {YearsAtCompany},
        {YearsInCurrentRole},
        {YearsWithCurrentManager});
        """
            # 6. Execute query
            cursor.execute(InsertQuery)
        # 7. commit changes
        connection.commit()

        # 8. connection close
        connection.close()


if __name__ == '__main__':
    initialize_database()


