import pymysql
import xlrd
import pdb
import math as math

USERNAME = 'root'
PASSWORD = 'password'
DB_NAME = 'DBPROJECT'
END_POINT = 'ece4813-project-rds.cvei3yvcg2ng.us-east-2.rds.amazonaws.com'

conn = pymysql.connect(host=END_POINT, port=3306, user=USERNAME, passwd=PASSWORD, db=DB_NAME)

workbook = xlrd.open_workbook('data2.xls')
sheet = workbook.sheet_by_index(0)
heads = []
for i in range(0, 10):
    heads.append(sheet.cell(0, i).value)

def exec_sql(statement):
    #print (statement)
    cur = conn.cursor()
    cur.execute(statement)
    conn.commit()
    cur.close()

def create_table():
    statement = "CREATE TABLE Malware (" + heads[0] + " varchar(64) NOT NULL, " + heads[1] + " varchar(20), " + heads[2] + " varchar(20), " + heads[3] + " varchar(30), " + heads[4] + " FLOAT, " + heads[5] + " varchar(50), " + heads[6] + " varchar(20), " + heads[7] + " varchar(50), " + heads[8] + " varchar(250), " + heads[9] + " varchar(500), " + "PRIMARY KEY (" + heads[0] + ")) "
    exec_sql(statement)

def insert_row(index):
    statement = "INSERT INTO Malware VALUES("
    try:
        sha = str(sheet.cell(index, 0).value)
    except:
        pdb.set_trace()
    sha = sha[:32]
    statement = statement + "'" + sha + "', "
    for i in range(1, 9):
        val = str(sheet.cell(index, i).value)
        if len(val) > 0:
            if i == 2:
                time = sheet.cell(index, i).value
                hour = math.floor(time * 24.0)

                time = time - (hour / 24.0)
                minute = math.floor(time * 60.0 * 24)

                time = time - (minute / (60 * 24))
                second = math.floor(time * 60 * 60 * 24)

                if hour > 11:
                    val = " PM"
                    hour = hour - 12
                else:
                    val = " AM"

                if hour == 0:
                    hour = 12

                minute = int(minute)
                if minute < 10:
                    minute = "0" + str(minute)
                else:
                    minute = str(minute)
                
                second = int(second)
                if second < 10:
                    second = "0" + str(second)
                else:
                    second = str(second)

                val = str(int(hour)) + ":" + minute + ":" + second + val
                statement = statement + "'" + val + "', "

            elif i != 4:
                statement = statement + "'" + val + "', "
            else:
                statement = statement + val + ", "
        else:
            statement = statement + "NULL, "

    val = str(sheet.cell(index, 9).value)
    if len(val) > 0:
        statement = statement + "'" + val + "')"
    else:
        statement = statement + "NULL)"
    try:
        exec_sql(statement)
    except pymysql.err.IntegrityError:
        print "IntegrityError"

def get_all():
    cur = conn.cursor()
    cur.execute("SELECT * FROM Malware;")
    result = cur.fetchall()
    for row in result:
        print row
        print ""

def insert_rows(num_rows):
    i = 2
    while i < 2 * num_rows:
        insert_row(i)
        i = i + 2

# create_table()
insert_rows(359)
get_all()
conn.close()
