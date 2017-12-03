import pymysql
import xlrd

USERNAME = ''
PASSWORD = ''
DB_NAME = ''
END_POINT = ''

conn = pymysql.connect(host=END_POINT, port=3306, user=USERNAME, passwd=PASSWORD, db=DB_NAME)

workbook = xlrd.open_workbook('data.xls')
sheet = workbook.sheet_by_index(0)
heads = []
for i in range(0, 10):
    heads.append(sheet.cell(0, i).value)

def exec_sql(statement):
    #print (statement)
    cur = conn.cursor()
    cur.execute(statement)
    cur.close()

def create_table():
    statement = "CREATE TABLE Malware (" + heads[0] + " varchar(64) NOT NULL, " + heads[1] + " varchar(20), " + heads[2] + " varchar(20), " + heads[3] + " varchar(30), " + heads[4] + " FLOAT, " + heads[5] + " varchar(50), " + heads[6] + " varchar(20), " + heads[7] + " varchar(50), " + heads[8] + " varchar(250), " + heads[9] + " varchar(500), " + "PRIMARY KEY (" + heads[0] + ")) "
    exec_sql(statement)

def insert_row(index):
    statement = "INSERT INTO Malware VALUES("
    sha = str(sheet.cell(index, 0).value)
    sha = sha[:32]
    statement = statement + "'" + sha + "', "
    for i in range(1, 9):
        val = str(sheet.cell(index, i).value)
        if len(val) > 0:
            if i != 4:
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

    exec_sql(statement)

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
# insert_rows(10)
# get_all()
conn.close()
