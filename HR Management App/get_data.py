import sqlean as sqlite3

class GetData:
    def __init__(self, cursor, display):
        self.cursor = cursor
        self.display = display
        self.list_of_ids = []

    def get_list_of_ids(self):
        return self.list_of_ids

    def get_data_execute(self):
        while True:
            self.display.display_get_data_menu()
            match input():
                case "1":
                    self.get_data_by_name()
                case "2":
                    self.get_data_by_id()
                case "3":
                    self.filter_database()
                case "0":
                    print("Bye!")
                    break
                case _:
                    print("Not valid command")


    def get_data_by_id(self):
        print("Do you want to get employees in the saved list? [yes / no]")
        show_list_validate = input()
        while show_list_validate not in ["yes", "no"]:
            print("valid answers: [yes / no]")
            show_list_validate = input()
        if show_list_validate == "yes":
            emp_ids = ",".join([str(employee_id) for employee_id in self.list_of_ids])
        else:
            print("Please type in one or multiple comma separated Employee_ids:")
            emp_ids = input()
        try:
            self.cursor.execute(f"SELECT * FROM hr WHERE Employee_id IN ({emp_ids})")
            fetched_data = self.cursor.fetchall()
            if len(fetched_data) > 0:
                for row in fetched_data:
                    self.display.display_data(row)
            else:
                print(f"No employee has Employee_id: {emp_ids}!")
        except sqlite3.Error as e:
            print('SQLite error: %s' % (' '.join(e.args)))
            print("Something went wrong!")

    def get_data_by_name(self):
        print("Please type in first name:")
        FirstName = input()
        print("Please type in last name:")
        LastName = input()
        try:
            self.cursor.execute(f"SELECT * FROM hr WHERE FirstName = '{FirstName}' AND LastName = '{LastName}'")
            fetched_data = self.cursor.fetchall()
            # if no match
            if len(fetched_data) == 0:
                print(f"There's no employee named {FirstName} {LastName}!")

            # only one match
            elif len(fetched_data) == 1:
                self.display.display_data(fetched_data[0])
                print(f"Do you want to save to memory the Employee_id of {FirstName} {LastName}? [yes / no]")
                save_validate = input()
                while save_validate not in ["yes", "no"]:
                    print("valid answers: [yes / no]")
                    save_validate = input()
                if save_validate == "yes":
                    # save Employee_id to list
                    self.list_of_ids.append(str(fetched_data[0][0]))
                    print("Save was successful!")
                else:
                    print("Nothing was saved")

            # multiple matches
            else:
                for row in fetched_data:
                    self.display.display_data(row)
                # Select an individual based on id
                print(f"Do you want to save to memory the Employee_id of one bearer of name {FirstName} {LastName}? [yes / no]")
                save_validate = input()
                while save_validate not in ["yes", "no"]:
                    print("valid answers: [yes / no]")
                    save_validate = input()
                if save_validate == "yes":
                    # save Employee_id to list
                    print("Type in Employee_id to save")
                    try:
                        id_to_save = int(input())
                        self.list_of_ids.append(id_to_save)
                        print("Save was successful!")
                    except ValueError:
                        print("Not valid id!")
                else:
                    print("Nothing was saved")

        except sqlite3.Error as e:
            print('SQLite error: %s' % (' '.join(e.args)))
            print("Something went wrong!")


    def filter_database(self):
        # get filter conditions
        filtering_conditions = self.get_filter_conditions()
        print()
        # get sorting conditions
        sorting_conditions = self.get_sorting_conditions()
        try:
            # search for data
            self.cursor.execute(f"SELECT * FROM hr {filtering_conditions} {sorting_conditions};")
            fetched_data = self.cursor.fetchall()
            for row in fetched_data:
                self.display.display_data(row)
            print("Do you want to save the ids of the filtered employees? [yes / no]")
            save_filtered_data = input()
            while save_filtered_data not in ["yes", "no"]:
                print("valid answers: [yes / no]")
                save_filtered_data = input()
            if save_filtered_data == "yes":
                for row in fetched_data:
                    self.list_of_ids.append(str(row[0]))
                print("Save was successful!")
            else:
                print("Nothing was saved")
        except sqlite3.Error as e:
            print('SQLite error: %s' % (' '.join(e.args)))
            print("Something went wrong!")

    def get_filter_conditions(self):
        print("Do you want to filter data? [yes / no]")
        filter_validate = input()
        while filter_validate not in ["yes", "no"]:
            print("valid answers: [yes / no]")
            filter_validate = input()

        if filter_validate == "yes":

            print("Do you want to filter by saved ids? [yes / no]")
            filter_by_id_validate = input()
            while filter_by_id_validate not in ["yes", "no"]:
                print("valid answers: [yes / no]")
                filter_by_id_validate = input()

            if filter_by_id_validate == "yes":
                emp_ids = ",".join(self.list_of_ids)
                return f"WHERE Employee_id IN ({emp_ids})"
            else:
                conditions = []
                # Get filter conditions and save to list above
                while True:
                    print()
                    print("Type in an attribute to filter data on.")
                    print()
                    print(
                        "Employee_id, FirstName, LastName, Age, Gender, Department, JobRole, Attrition, DistanceFromHome, JobLevel, JobInvolvement, MonthlyIncome,")
                    print(
                        "OverTime, StockOptionLevel, TotalWorkingYears, TrainingTimesLastYear, YearsAtCompany, YearsInCurrentRole, YearsWithCurrentManager")
                    attribute = input()
                    print()
                    match attribute:
                        case "Employee_id":
                            print("Type in one or multiple comma separated Employee_ids")
                            condition_ei = f"Employee_id IN ({input()})"
                            conditions.append(condition_ei)
                        case "FirstName":
                            print("Type in first name to have and exact match,")
                            print("Or use a segment of the name and supplement it with '%' wildcard symbol,")
                            print("e.g. %ter will match Peter, Carter,  %ter% will match Peter, Terence, Masterton")
                            condition_f_n = "FirstName LIKE " + "'" + input() + "'"
                            conditions.append(condition_f_n)
                        case "LastName":
                            print("Type in last name to have and exact match,")
                            print("Or use a segment of the name and supplement it with '%' wildcard symbol,")
                            print("e.g. %ker will match Baker, Meaker,  %ter% will match Baker, Kerry, Akers")
                            condition_l_n = "LastName LIKE " + "'" + input() + "'"
                            conditions.append(condition_l_n)
                        case "Age":
                            print("Type in exact age like '=33' or multiple ages like 'IN (18,39,56)' ")
                            print("Or use expressions like '>20' or 'BETWEEN 20 AND 50'")
                            print("Write without the single quote symbols!")
                            condition_age = "Age " + input()
                            conditions.append(condition_age)
                        case "Gender":
                            print("Type in Gender: Female or Male:")
                            condition_g = "Gender = " + "'" + input() + "'"
                            conditions.append(condition_g)
                        case "Department":
                            print("Type one or multiple comma separated departments")
                            print("from Sales , Research & Development , Human Resources:")
                            input_dep = "','".join([word.strip() for word in input().split(",")])
                            condition_dep = f"Department IN ('{input_dep}')"
                            conditions.append(condition_dep)
                        case "JobRole":
                            print("Type one or multiple comma separated job roles")
                            print("""
                            from Manager , Sales Executive , Sales Representative , 
                            Healthcare Representative , Laboratory Technician , Manufacturing Director , 
                            Research Director , Research Scientist , Human Resources""")
                            input_jr = "','".join([word.strip() for word in input().split(",")])
                            condition_jr = f"JobRole IN ('{input_jr}')"
                            conditions.append(condition_jr)
                        case "DistanceFromHome":
                            print("For filtering distance from home use expressions like '<5' or 'BETWEEN 2 AND 5'")
                            print("Write without the single quote symbols!")
                            condition_dist = "DistanceFromHome " + input()
                            conditions.append(condition_dist)
                        case "JobLevel":
                            print("Type in one or multiple comma separated job levels from 1 to 5:")
                            condition_jl = f"JobLevel IN ({input()})"
                            conditions.append(condition_jl)
                        case "JobInvolvement":
                            print("Type in one or multiple comma separated job involvement level from 1 to 4:")
                            condition_ji = f"JobInvolvement IN ({input()})"
                            conditions.append(condition_ji)
                        case "MonthlyIncome":
                            print("For monthly income use expressions like '<3000' or 'BETWEEN 4000 AND 8000'")
                            print("Write without the single quote symbols!")
                            condition_mi = "MonthlyIncome " + input()
                            conditions.append(condition_mi)
                        case "OverTime":
                            print("Type in answer to is employee working overtime: Yes or No:")
                            condition_ot = "OverTime = " + "'" + input() + "'"
                            conditions.append(condition_ot)
                        case "StockOptionLevel":
                            print("Type in one or multiple comma separated stock option level from 0 to 3:")
                            condition_sol = f"StockOptionLevel IN ({input()})"
                            conditions.append(condition_sol)
                        case "TotalWorkingYears":
                            print("For total working years use expressions like '<10' or '=3' or 'BETWEEN 5 AND 15'")
                            print("Write without the single quote symbols!")
                            condition_twy = "TotalWorkingYears " + input()
                            conditions.append(condition_twy)
                        case "Attrition":
                            print("Type in answer to did employee leave: Yes or No:")
                            condition_at = "Attrition = " + "'" + input() + "'"
                            conditions.append(condition_at)
                        case "TrainingTimesLastYear":
                            print("For training times last year use expressions like '<3' or '=4' or 'BETWEEN 2 AND 6'")
                            print("Write without the single quote symbols!")
                            condition_ttly = "TrainingTimesLastYear " + input()
                            conditions.append(condition_ttly)
                        case "YearsAtCompany":
                            print("For years at company use expressions like '<6' or '=4' or 'BETWEEN 2 AND 6'")
                            print("Write without the single quote symbols!")
                            condition_yac = "YearsAtCompany " + input()
                            conditions.append(condition_yac)
                        case "YearsInCurrentRole":
                            print("For years in current role use expressions like '<6' or '=4' or 'BETWEEN 2 AND 6'")
                            print("Write without the single quote symbols!")
                            condition_yicr = "YearsInCurrentRole " + input()
                            conditions.append(condition_yicr)
                        case "YearsWithCurrentManager":
                            print("For years with current manager use expressions like '<6' or '=4' or 'BETWEEN 2 AND 6'")
                            print("Write without the single quote symbols!")
                            condition_ywcm = "YearsWithCurrentManager " + input()
                            conditions.append(condition_ywcm)
                        case _:
                            print("Not a valid column!")
                    print()
                    print("Do you want to choose another attribute to filter on? [yes / no]")
                    filter_another = input()
                    while filter_another not in ["yes", "no"]:
                        print("valid answers: [yes / no]")
                        filter_another = input()
                    if filter_another == "yes":
                        continue
                    else:
                        break

            # returned formatted filter conditions
            formatted_conditions = "WHERE " + " AND ".join(conditions)
            return formatted_conditions

        else:
            return ""



    def get_sorting_conditions(self):
        print("Do you want to sort the data? [yes / no]")
        validate_sort = input()
        while validate_sort not in ["yes", "no"]:
            print("valid answers: [yes / no]")
            validate_sort = input()
        if validate_sort == "yes":
            conditions = []
            while True:
                print()
                print("Type in an attribute to sort data on.")
                print()
                print(
                    "FirstName, LastName, Age, Gender, Department, JobRole, Attrition, DistanceFromHome, JobLevel, JobInvolvement, MonthlyIncome,")
                print(
                    "OverTime, StockOptionLevel, TotalWorkingYears, TrainingTimesLastYear, YearsAtCompany, YearsInCurrentRole, YearsWithCurrentManager")
                attribute = input()
                print("Do you want to sort ascending or descending? [ASC / DESC]")
                asc_or_desc = input()
                while asc_or_desc not in ["ASC", "DESC"]:
                    print("valid answers: [ASC / DESC]")
                    asc_or_desc = input()
                conditions.append(attribute + " " + asc_or_desc)
                print()
                print("Do you want to sort by another attribute? [yes / no]")
                sort_another = input()
                while sort_another not in ["yes", "no"]:
                    print("valid answers: [yes / no]")
                    sort_another = input()
                if sort_another == "yes":
                    continue
                else:
                    break

            # return formatted sorting conditions
            formatted_conditions = "ORDER BY " + ", ".join(conditions)
            return formatted_conditions
        else:
            print("No sorting done")
            return ""


