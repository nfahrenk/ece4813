import pymysql
import xlrd
import pdb
import math as math
import json
from geoip import geolite2

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
    statement = "CREATE TABLE MyMalware (" + heads[0] + " varchar(64) NOT NULL, " + heads[1] + " varchar(20), " + heads[2] + " datetime(6), " + heads[3] + " varchar(30), " + heads[4] + " FLOAT, " + heads[5] + " varchar(50), " + heads[7] + " varchar(50), "  + heads[9] + " varchar(500), longitude varchar(20), latitude varchar(20), PRIMARY KEY (" + heads[0] + ")) "
    print statement
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

def insert_data_row(row):
    statement = "INSERT INTO MyMalware VALUES("

    for i in range(0, len(row)):
        if i == 4:
            statement = statement + str(row[i]) + ", "
        else:
            statement = statement + "'" + str(row[i]) + "', "
    statement = statement[:-2]
    statement = statement + ")"
    # print statement
    # print ""

    try:
        exec_sql(statement)
    except pymysql.err.IntegrityError:
        pass
        # print statement

def insert_data():
    with open('results.txt','r') as infile: 
        for line in infile:
            d = json.loads(line)
            sample = d['sample']
            ingest_date = sample['ingest_date']
            sus_score = d['sample']['suspicion']['score']
            sha256 = d['sample']['hashes']['sha256']
            file_type = d['sample']['type']
            file_name = d['pcap']['name']
            sources = '(UNKNOWN) at ' + d['sample']['sources'][0]['customer']['customer_since']
            http = d['network']['http']
            ips = []
            for ip in http:
                ips.append(d['network']['http'][0]['ip'])

            if len(ips) < 1:
                ips = 'None'
            else:
                ips = ips[0]

            lon = 'None'
            lat = 'None'

            if ip != 'None' and ip is not None:
                match = geolite2.lookup(ip['ip'])
                if match is not None:
                    lon = match.location[0]
                    lat = match.location[1]

            str_d = str(d)
            place = str_d.find('Detect')

            av = 'None'
            if place != -1:
                str_d = str_d[place:(place + 100)]
                place = str_d.find("'")
                str_d = str_d[place:]
                str_d = str_d[1:]
                place = str_d.find("'")
                str_d = str_d[place:]
                str_d = str_d[1:]
                s_end = str_d.find("'")
                av = str_d[:s_end]

            row = [
                sha256,
                file_type,
                ingest_date,
                file_name,
                sus_score,
                sources,
                av,
                ips,
                lon,
                lat
            ]
            insert_data_row(row)

def get_all():
    cur = conn.cursor()
    cur.execute("SELECT * FROM MyMalware;")
    result = cur.fetchall()
    # for row in result:
    #     print row
    #     print ""
    print len(result)

def insert_rows(num_rows):
    i = 2
    while i < 2 * num_rows:
        insert_row(i)
        i = i + 2

def insert_rows2(num_rows):
    for i in range(400, num_rows):
        insert_row(i)

def delete_table():
    statement = "DELETE FROM MyMalware"
    try:
        exec_sql(statement)
    except pymysql.err.IntegrityError:
        print "IntegrityError"

def drop_table():
    statement = "DROP TABLE MyMalware"
    try:
        exec_sql(statement)
    except pymysql.err.IntegrityError:
        print "IntegrityError"

# drop_table()
# create_table()
# insert_rows2(1141)
# delete_table()
insert_data()
get_all()
conn.close()
