import sqlean as sqlite3
from display import Display
from delete import Delete
from register import Register
from modify import Modify
from get_data import GetData
from statistics import Statistics
from predict import Predict


class HrManagementApp:
    def __init__(self):
        sqlite3.extensions.enable_all()
        self.connection = sqlite3.connect("HR_database.db")
        self.cursor = self.connection.cursor()
        self.display = Display()
        self.delete = Delete(connection=self.connection, cursor=self.cursor, display=self.display)
        self.register = Register(connection=self.connection, cursor=self.cursor)
        self.modify = Modify(connection=self.connection, cursor=self.cursor, display=self.display)
        self.get_data = GetData(cursor=self.cursor, display=self.display)
        self.statistics = Statistics(connection=self.connection, cursor=self.cursor, display=self.display, get_data=self.get_data)
        self.predict = Predict(connection=self.connection, get_data=self.get_data, display=self.display)

    def run_app(self):
        self.display.display_welcome()
        while True:
            self.display.display_main_menu()
            match input():
                case "1":
                    self.register.register_new_data()
                case "2":
                    self.modify.modify_data()
                case "3":
                    self.delete.delete_data()
                case "4":
                    self.get_data.get_data_execute()
                case "5":
                    self.statistics.get_statistics()
                case "6":
                    self.predict.prediction_execute()
                case "0":
                    self.connection.close()
                    print("Bye!")
                    exit()
                case _:
                    print("Not valid command")



