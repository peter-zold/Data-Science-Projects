import sqlean as sqlite3


class Register:
    def __init__(self, connection, cursor):
        self.connection = connection
        self.cursor = cursor

    def register_new_data(self):
        print("------------Register new data------------")
        print("You can register new employees' data here")
        print()
        while True:
            print("Please type in the following information about the new employee:")
            print("First Name:")
            try:
                FirstName = input()
                print("Last Name:")
                LastName = input()
                print("Age [14-99]:")
                Age = int(input())
                print("Gender [Female / Male]:")
                Gender = input()
                print("Department [Sales / Research & Development / Human Resources]:")
                Department = input()
                if Department == "Sales":
                    job_roles = "Manager / Sales Executive / Sales Representative"
                elif Department == "Research & Development":
                    job_roles = """Healthcare Representative / Laboratory Technician / Manager /
                                Manufacturing Director / Research Director / Research Scientist"""
                else:
                    job_roles = "Human Resources / Manager"
                print(f"Job Role [{job_roles}]:")
                JobRole = input()
                print("Distance from home [miles]:")
                DistanceFromHome = int(input())
                print("Job level [1-5]:")
                JobLevel = int(input())
                print("Job involvement [1-4]:")
                JobInvolvement = int(input())
                print("Monthly income:")
                MonthlyIncome = int(input())
                print("Likely to work overTime [Yes / No]:")
                OverTime = input()
                print("Stock option level [0-3]:")
                StockOptionLevel = int(input())
                print("Total working years:")
                TotalWorkingYears = int(input())

                # write an insert to query with the input data
                InsertQuery = f"""
                        INSERT INTO hr (
                                FirstName,
                                LastName,
                                Age,
                                Gender,
                                Department,
                                JobRole,
                                DistanceFromHome,
                                JobLevel,
                                JobInvolvement,
                                MonthlyIncome,
                                OverTime,
                                StockOptionLevel,
                                TotalWorkingYears
                                )
                                VALUES (
                                '{FirstName}',
                                '{LastName}',
                                {Age},
                                '{Gender}',
                                '{Department}',
                                '{JobRole}',
                                {DistanceFromHome},
                                {JobLevel},
                                {JobInvolvement},
                                {MonthlyIncome},
                                '{OverTime}',
                                {StockOptionLevel},
                                {TotalWorkingYears});
                                """
                print("Are you sure do you want to register the following:")
                print(
                    f'name: {FirstName} {LastName}, age: {Age}, gender: {Gender}, dept: {Department}, role: {JobRole}, dist: {DistanceFromHome}, level: {JobLevel}, involvement: {JobInvolvement}, income: {MonthlyIncome}, overtime: {OverTime}, stock: {StockOptionLevel}, work years: {TotalWorkingYears}')
                print("yes / no")
                register_validate = input()
                while register_validate not in ["yes", "no"]:
                    print("valid answers: [yes / no]")
                    register_validate = input()
                if register_validate == "yes":
                    try:
                        # Execute query
                        self.cursor.execute(InsertQuery)
                        # commit changes
                        self.connection.commit()
                        print("Registration successful!")
                    except sqlite3.Error as e:
                        print('SQLite error: %s' % (' '.join(e.args)))
                        print("Something went wrong!")
                else:
                    print("Nothing was registered!")
            except ValueError:
                print("Not Valid Data")
            print()
            print("Do you want to register another employee's data? [yes / no]")
            register_another = input()
            while register_another not in ["yes", "no"]:
                print("valid answers: [yes / no]")
                register_another = input()
            if register_another == "yes":
                continue
            else:
                break


