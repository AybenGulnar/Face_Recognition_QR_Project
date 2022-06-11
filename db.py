import sqlite3
from datetime import datetime, timedelta

class Database:
    def __init__(self,db):
        self.connection = sqlite3.connect(db)
        self.cursor = self.connection.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS personnel (id INTEGER PRIMARY KEY,personnelName text NOT NULL,photoPath text NOT NULL)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS attendance (id INTEGER PRIMARY KEY,personnelName text NOT NULL,attendanceDate text NOT NULL)")
        self.connection.commit()
    
    def fetch(self):
        self.cursor.execute("SELECT * from personnel")
        rows = self.cursor.fetchall()
        return rows
    
    def fetchAttendance(self):
        self.cursor.execute("SELECT * from attendance")
        rows = self.cursor.fetchall()
        # print(rows)
        return rows

    def insert(self,name,photopath):
        self.cursor.execute("INSERT INTO personnel VALUES(NULL,?,?)",(name,photopath))
        self.connection.commit()
    
    def insertAttendance(self,name,attendanceDate):
        self.cursor.execute("INSERT INTO attendance VALUES(NULL,?,?)",(name,attendanceDate))
        self.connection.commit()

    def remove(self,id):
        self.cursor.execute("DELETE FROM personnel WHERE id=?",(id,))
        self.connection.commit()

    def markAttendance(self,name):
        nameList = []
        dateList = []  
        tuple = []        
        for index, tuple in enumerate(self.fetchAttendance()):
            # print(tuple[2][:10])
            nameList.append(tuple[1])
            dateList.append(tuple[2])#[:10]

        dict = {nameList[i]: dateList[i] for i in range(len(nameList))}

        if tuple == []:
            attendanceDate = datetime.now()
            self.insertAttendance(name,attendanceDate)
        elif name not in nameList:
            attendanceDate = datetime.now()
            self.insertAttendance(name,attendanceDate)
        elif name in nameList:
            # print(dict[name])
            today = str(datetime.now())
            todayByDate = today[:10]
            # print(today[:10])
            
            lastAttendanceByDate  = str(dict[name][:10])
            lastAttandanceHour = str(dict[name][11:16])
            
            
            lastAttendanceTime = datetime.strptime(lastAttandanceHour, '%H:%M')
            currTime = datetime.strptime(today[11:16], '%H:%M')

            if lastAttendanceByDate != todayByDate:
                attendanceDate = datetime.now()
                self.insertAttendance(name,attendanceDate)

            elif lastAttendanceByDate == todayByDate:
                addedTime  = lastAttendanceTime + timedelta(minutes=10)
                addedTimeStr = str(addedTime.time())
                finalTime = datetime.strptime(addedTimeStr[:5], '%H:%M')
                if finalTime < currTime:
                    attendanceDate = datetime.now()
                    self.insertAttendance(name,attendanceDate)
    

    def __del__(self):
        self.connection.close()
    

#db = Database('records.db')
# db.insertAttendance('Emre Alagoz','05.01.2022')
#db.markAttendance('EMre')
#db.markAttendance('xy')
#print(db.fetchAttendance())