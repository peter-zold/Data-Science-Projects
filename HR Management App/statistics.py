import sqlean as sqlite3

class Statistics:
    def __init__(self, connection, cursor, display, get_data):
        self.connection = connection
        self.cursor = cursor
        self.display = display
        self.get_data = get_data

    def get_statistics(self):
        print("---------------------------Statistics----------------------------")
        print("You can get many statistical values for grouped and filtered data")
        print()
        # get attributes to group by
        attributes_list, attributes_for_select, attributes_for_groupby = self.get_grouby_attributes()
        print()
        # get numerical attribute for statistics
        stat_attribute = self.get_stat_attribute()
        print()
        # get filter conditions

        filter_conditions = self.get_data.get_filter_conditions()
        print()
        stat_query = f"""
        SELECT
            {attributes_for_select}
            COUNT({stat_attribute}),
            MIN({stat_attribute}),
            PERCENTILE_25({stat_attribute}),
            MEDIAN({stat_attribute}),
            PERCENTILE_75({stat_attribute}),
            MAX({stat_attribute}),
            ROUND(STDDEV({stat_attribute}),2),
            ROUND(AVG({stat_attribute}),2),
            SUM({stat_attribute})
        FROM 
            hr
        {filter_conditions}
        {attributes_for_groupby};
        """

        try:
            self.cursor.execute(stat_query)
            fetched_data = self.cursor.fetchall()
            self.display.display_statistics_header(attributes=attributes_list, stat=stat_attribute)
            for row in fetched_data:
                self.display.display_statistics_rows(attributes=attributes_list, row=row)

        except sqlite3.Error as e:
            print('SQLite error: %s' % (' '.join(e.args)))
            print("Something went wrong!")


    def get_grouby_attributes(self):
        print("Do you want to group data by maximum 3 attributes? [yes / no]")

        groupby_validate = input()
        while groupby_validate not in ["yes", "no"]:
            print("valid answers: [yes / no]")
            groupby_validate = input()

        if groupby_validate == "yes":
            # list attributes in the following list
            attributes_list = []
            # set up a counter to ensure maximum 3 attributes to group by
            counter = 0

            while True:
                count = 0
                print()
                print("Please type in attribute you want to group by from the following list:")
                print()
                print(
                    "Age, Gender, Department, JobRole, Attrition, JobLevel, JobInvolvement, OverTime, StockOptionLevel")
                print(
                    "TrainingTimesLastYear, YearsAtCompany, YearsInCurrentRole, YearsWithCurrentManager")
                attributes_list.append(input())

                # counter increment after selecting attribute
                counter += 1
                if counter < 3:
                    print("Do you want to group data by another attributes? [yes / no]")
                    another_groupby_validate = input()
                    while another_groupby_validate not in ["yes", "no"]:
                        print("valid answers: [yes / no]")
                        another_groupby_validate = input()
                    if another_groupby_validate == "yes":
                        continue
                    else:
                        break
                else:
                    print("You have selected all the 3 attributes")
                    break

            # Return list of attributes for select and group by commands
            attributes_for_select = ",".join(attributes_list) + ","
            attributes_for_groupby = "GROUP BY " + attributes_for_select[:-1]

            return attributes_list, attributes_for_select, attributes_for_groupby
        else:
            return [], "", ""


    def get_stat_attribute(self):
        print()
        print("Please type in attribute you want use for statistical analysis from the following list:")
        print()
        print(
            "Age, DistanceFromHome, JobLevel, JobInvolvement, MonthlyIncome,  StockOptionLevel, TotalWorkingYears")
        print(
            "TrainingTimesLastYear, YearsAtCompany, YearsInCurrentRole, YearsWithCurrentManager")
        return input()