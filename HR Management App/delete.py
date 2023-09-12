import sqlean as sqlite3


class Delete:
    def __init__(self, connection, cursor, display):
        self.connection = connection
        self.cursor = cursor
        self.display = display

    def delete_data(self):
        while True:
            print("Only delete data if it was wrongly registered!")
            print("Use modify otherwise!")
            print("Please type in employee's first name")
            FirstName = input()
            print("Please type in employee's last name")
            LastName = input()
            try:
                self.cursor.execute(f"SELECT * FROM hr WHERE FirstName = '{FirstName}' AND LastName = '{LastName}'")
                fetched_data = self.cursor.fetchall()
                if len(fetched_data) == 0:
                    print(f"There's no employee named {FirstName} {LastName}!")
                elif len(fetched_data) == 1:
                    self.display.display_data(fetched_data[0])
                    print(f"Are you sure you want to delete {FirstName} {LastName}? [yes / no]")
                    decision = input()
                    if decision.lower() == "yes":
                        try:
                            self.cursor.execute(f"DELETE FROM hr WHERE FirstName = '{FirstName}' AND LastName = '{LastName}'")
                            self.connection.commit()
                            print(f"{FirstName} {LastName} was deleted successfully!")
                        except sqlite3.Error as e:
                            print('SQLite error: %s' % (' '.join(e.args)))
                            print("Something went wrong!")
                    else:
                        print("No records were deleted")
                        return
                else:
                    for row in fetched_data:
                        self.display.display_data(row)
                    print("Type in Employee_id for the employee you want to delete")
                    delete_id = int(input())
                    try:
                        self.cursor.execute(f"DELETE FROM hr WHERE Employee_id = {delete_id}")
                        self.connection.commit()
                        print(f"{FirstName} {LastName} was deleted successfully!")
                    except sqlite3.Error as e:
                        print('SQLite error: %s' % (' '.join(e.args)))
                        print("Something went wrong!")
            except sqlite3.Error as e:
                print('SQLite error: %s' % (' '.join(e.args)))
                print("Something went wrong!")
            print()
            print("Do you want to delete another employee's data? [yes / no]")
            delete_another = input()
            while delete_another not in ["yes", "no"]:
                print("valid answers: [yes / no]")
                delete_another = input()
            if delete_another == "yes":
                continue
            else:
                break
