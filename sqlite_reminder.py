import sqlite3
import datetime

class DataBase:

    def __init__(self):
        self.con = sqlite3.connect("reminder.db")

        self.c = self.con.cursor()

        # c.execute("""CREATE TABLE reminder (
        #                 id text,
        #                 parameter text,
        #                 time text)""")

        #self.c.execute("""ALTER TABLE reminder ADD city text""")
        #self.c.execute("""ALTER TABLE reminder DROP COLUMN time""")

    def set_reminder(self, id, parameter, city):
        with self.con:
            self.c.execute("INSERT INTO reminder VALUES(:id, :parameter, :city  )",
                      {'id': id, 'parameter': parameter, 'city': city})

    def get_reminder(self, id):
        self.c.execute("SELECT * FROM reminder WHERE id=:id", {'id': id})
        return self.c.fetchall()

    def remove_reminder(self, id, parameter, city):
        with self.con:
            self.c.execute("DELETE from reminder WHERE parameter= :par AND city = :c AND id = :id",
                      {'par': parameter, 'c': city, 'id': id})


    def close(self):
        self.con.commit()
        self.con.close()

#print(datetime.datetime.utcnow().strftime('%d-%m-%Y, checking time: %H:%M:%S'))

#d = DataBase()

# d.set_reminder("5", "five", "five oklok")
# d.set_reminder(6, "sfive", "six oklok")
# print(d.get_reminder(6))

#d.remove_reminder("380919107", "clouds", "Kiev")

#d.close()

#c.execute("INSERT INTO reminder VALUES ('1', 'parameter', 'time')")
#set_reminer("2", "par", "tt" )


#c.execute("SELECT * FROM reminder WHERE id='1'")
#c.execute("SELECT * FROM reminder WHERE id='2'")
#remove_rem("par")
#print(c.fetchone())
#print(get_reminder("1"))




