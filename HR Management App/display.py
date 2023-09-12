class Display:

    def display_welcome(self):
        print()
        print("--------------------------Welcome to HR Management Application!--------------------------------")
        print("Here you can modify, insert or delete employee data, view statistics and make churn predictions")

    def display_main_menu(self):
        print()
        print("-------------Main Menu-----------")
        print("Insert the number of the command!")
        print()
        print("1. Register new employee's data")
        print("2. Modify employees' data")
        print("3. Delete employees' data")
        print("4. Get employees' data")
        print("5. Get statistics")
        print("6. Make attrition prediction")
        print("0. Exit program")
        print()
        print("Your command:")

    def display_get_data_menu(self):
        print()
        print("--------------Get Data Menu---------------")
        print("You can save Employee_ids searched by name")
        print("or got by filtering for further analysis")
        print()
        print("Insert the number of the command!")
        print()
        print("1. Search by name")
        print("2. Search by Employee_id")
        print("3. Filter (and sort) database")
        print("0. Return to main menu")

    def display_prediction_menu(self):
        print()
        print("-------------------------------Predict Attrition---------------------------------")
        print("You can make attrition predictions on filtered dataset for actual and future data")
        print()
        print("Insert the number of the command!")
        print()
        print("1. Make prediction")
        print("2. Make prediction for the future")
        print("3. View key influencers of attrition")
        print("0. Return to main menu")

    def display_data(self, row):
        display_string = f"""
        ##########################################
        #                                        #
        #{(row[1] + " " + row[2]).center(40)}#
        #                                        #
        ##########################################

        Personal Info:

        | Employee_id |   FirstName   |    LastName   |  Age  |  Gender  | DistanceFromHome | Attrition |
        -------------------------------------------------------------------------------------------------
        |{str(row[0]).center(13)}|{row[1].center(15)}|{row[2].center(15)}|{str(row[3]).center(7)}|{row[4].center(10)}|{str(row[8]).center(18)}|{row[7].center(11)}|

        Job Info:

        |       Department     |         JobRole         | JobLevel | JobInvolvement | MonthlyIncome | OverTime | StockOptionLevel |
        ----------------------------------------------------------------------------------------------------------------------------
        |{row[5].center(22)}|{row[6].center(25)}|{str(row[9]).center(10)}|{str(row[10]).center(16)}|{str(row[11]).center(15)}|{row[12].center(10)}|{str(row[13]).center(18)}|


        Job History:

        | TotalWorkingYears | TrainingTimesLastYear | YearsAtCompany | YearsInCurrentRole | YearsWithCurrentManager |
        -------------------------------------------------------------------------------------------------------------
        |{str(row[14]).center(19)}|{str(row[15]).center(23)}|{str(row[16]).center(16)}|{str(row[17]).center(20)}|{str(row[18]).center(25)}|
        """
        print(display_string)

    def display_statistics_rows(self, attributes, row):
        # if no attribute, show prepend empty string for proper display
        if len(attributes) == 1 and attributes[0] == "":
            row = list(row)
            row.insert(0, "")

        # split rows for attributes and statistics
        attribute_values = row[:len(attributes)]
        stat_values = row[len(attributes):]

        # create display for rows
        row_attribute_bottom = "-" * 26
        row_stat_bottom = "-" * 109

        # function for attribute display
        def get_row_attribute(attribute):
            return f"|{str(attribute).center(25)}"

        # fill lines with stat numbers
        row_stat = ""
        for stat_value in stat_values:
            row_stat += f"|{str(stat_value).center(11)}"
        row_stat += "|"

        # fill lines with attributes' names
        row_attributes = ""
        for attribute in attribute_values:
            row_attributes += get_row_attribute(attribute)

        print(row_attributes + row_stat)
        print(row_attribute_bottom * len(attributes) + row_stat_bottom)


    def display_statistics_header(self, attributes, stat):
        # function for attribute display
        def get_header_attribute(attribute):
            return f"|{str(attribute).center(25)}"

        header_attribute_top = "#" * 26
        header_attribute_fill = "|" + " " * 25
        header_attribute_bottom = "#" * 26

        header_stat_top = "#" * 109
        header_stat_title = f"|{str(stat).center(107)}|"
        header_stat_middle = "|" + "-" * 107 + "|"
        header_stat_metrics = "|   COUNT   |    MIN    | 1st QUART |   MEDIAN  | 3rd QUART |    MAX    |    STD    |  AVERAGE  |    SUM    |"
        header_stat_bottom = "#" * 109

        header_attributes = ""
        for attribute in attributes:
            header_attributes += get_header_attribute(attribute)

        print(header_attribute_top * len(attributes) + header_stat_top)
        print(header_attribute_fill * len(attributes) + header_stat_title)
        print(header_attributes + header_stat_middle)
        print(header_attribute_fill * len(attributes) + header_stat_metrics)
        print(header_attribute_bottom * len(attributes) + header_stat_bottom)
