import sqlean as sqlite3


class Modify:
    def __init__(self, connection, cursor, display):
        self.connection = connection
        self.cursor = cursor
        self.display = display

    def modify_data(self):
        print("------------------Modify data-----------------")
        print("Here you can modify employees' registered data")
        print()
        while True:
            print("Please select employee you want to modify")
            print("Please type in employee's first name")
            FirstName = input()
            print("Please type in employee's last name")
            LastName = input()
            try:
                # search for data
                self.cursor.execute(f"SELECT * FROM hr WHERE FirstName = '{FirstName}' AND LastName = '{LastName}'")
                fetched_data = self.cursor.fetchall()

                # no match
                if len(fetched_data) == 0:
                    print(f"There's no employee named {FirstName} {LastName}!")

                # only one match
                elif len(fetched_data) == 1:
                    self.display.display_data(fetched_data[0])
                    print(f"Are you sure you want to modify {FirstName} {LastName}? [yes / no]")
                    modify_validate = input()
                    while modify_validate not in ["yes", "no"]:
                        print("valid answers: [yes / no]")
                        modify_validate = input()
                    if modify_validate == "yes":
                        # ask for select column and type in value
                        column, value = self.get_column_and_value()
                        try:
                            # use update query
                            if value is int:
                                self.cursor.execute(
                                    f"UPDATE hr SET {column} = {value} WHERE FirstName = '{FirstName}' AND LastName = '{LastName}'")
                            else:
                                self.cursor.execute(
                                    f"UPDATE hr SET {column} = '{value}' WHERE FirstName = '{FirstName}' AND LastName = '{LastName}'")
                            self.connection.commit()
                            print(f"{FirstName} {LastName} was modified successfully!")
                        except sqlite3.Error as e:
                            print('SQLite error: %s' % (' '.join(e.args)))
                            print("Something went wrong, no records were modified!")
                    else:
                        print("No records were modified")

                # multiple matches
                else:
                    for row in fetched_data:
                        self.display.display_data(row)
                    # Select an individual based on id
                    print("Type in Employee_id for the employee you want to modify")
                    try:
                        modify_id = int(input())
                    except ValueError:
                        print("Not valid Employee_id!")
                        modify_id = "Not valid"

                    column, value = self.get_column_and_value()

                    try:
                        if value is int:
                            self.cursor.execute(
                                f"UPDATE hr SET {column} = {value} WHERE Employee_id = {modify_id}")
                        else:
                            self.cursor.execute(
                                f"UPDATE hr SET {column} = '{value}' WHERE Employee_id = {modify_id}")
                        self.connection.commit()
                        print(f"{FirstName} {LastName} was modified successfully!")

                    except sqlite3.Error as e:
                        print('SQLite error: %s' % (' '.join(e.args)))
                        print("Something went wrong, no records were modified!")

            except sqlite3.Error as e:
                print('SQLite error: %s' % (' '.join(e.args)))
                print("Something went wrong!")
            print()
            print("Do you want to modify another employee's data? [yes / no]")
            modify_another = input()
            while modify_another not in ["yes", "no"]:
                print("valid answers: [yes / no]")
                modify_another = input()
            if modify_another == "yes":
                continue
            else:
                break


    def get_column_and_value(self):
        print("Please type in attribute you want to modify from the following list:")
        print()
        print(
            "FirstName, LastName, Age, Gender, Department, JobRole, Attrition, DistanceFromHome, JobLevel, JobInvolvement, MonthlyIncome,")
        print(
            "OverTime, StockOptionLevel, TotalWorkingYears, TrainingTimesLastYear, YearsAtCompany, YearsInCurrentRole, YearsWithCurrentManager")
        attribute= input()
        print()
        try:
            match attribute:
                case "FirstName":
                    print("Type in First Name:")
                    value = input()
                case "LastName":
                    print("Type in Last Name:")
                    value = input()
                case "Age":
                    print("Type in Age [14-99]:")
                    value = int(input())
                case "Gender":
                    print("Type in Gender [Female / Male]:")
                    value = input()
                case "Department":
                    print(" Type in Department [Sales / Research & Development / Human Resources]:")
                    value = input()
                case "JobRole":
                    print("""
                    Type in Job Roles [Manager / Sales Executive / Sales Representative / 
                    Healthcare Representative / Laboratory Technician / Manufacturing Director / 
                    Research Director / Research Scientist / Human Resources""")
                    value = input()
                case "DistanceFromHome":
                    print("Type in the office distance from home [miles]:")
                    value = int(input())
                case "JobLevel":
                    print("Type in employee's job level [1-5]:")
                    value = int(input())
                case "JobInvolvement":
                    print("Type in employee's job involvement [1-4]:")
                    value = int(input())
                case "MonthlyIncome":
                    print("Type in employee's monthly income:")
                    value = int(input())
                case "OverTime":
                    print("Is employee likely to work overTime [Yes / No]:")
                    value = input()
                case "StockOptionLevel":
                    print("Type in employee's stock option level [0-3]:")
                    value = int(input())
                case "TotalWorkingYears":
                    print("Type in how many years did the employee work overall:")
                    value = int(input())
                case "Attrition":
                    print("Did the employee leave [Yes] or come back [No]?")
                    value = input()
                case "TrainingTimesLastYear":
                    print("Type in training times last year:")
                    value = int(input())
                case "YearsAtCompany":
                    print("Type in how many years the employee spent at the company")
                    value = int(input())
                case "YearsInCurrentRole":
                    print("Type in how many years the employee worked at current role")
                    value = int(input())
                case "YearsWithCurrentManager":
                    print("Type in how many years the employee worked with current manager")
                    value = int(input())
                case _:
                    print("Not a valid column!")
                    column = "Not valid"
                    value = "Not valid"

        except ValueError:
            print("Not valid data!")
            attribute = "Not Valid"
            value = "Not Valid"

        return attribute, value
