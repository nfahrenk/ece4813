import MySQLdb

if __name__ == '__main__':
    conn = MySQLdb.connect(
        host = "ece4813-project-rds.cvei3yvcg2ng.us-east-2.rds.amazonaws.com",
        user = "root",
        passwd = "password",
        db = "DBPROJECT", 
        port = 3306
    )
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT av_detec FROM Malware;")
    results = conn.fetchall()
    print results
    cursor.close()
    conn.close()