import MySQLdb

# ('Unix.Trojan.Mirai-5607483-0',), 
# ('Win.Trojan.L-43',), 
# ('Unix.Trojan.Mirai-5932143-0',), 
# ('Unix.Trojan.Mirai-1',), 
# ('Unix.Trojan.Spike-6301360-0',), 
# ('Unix.Trojan.SSHScan-6335682-0',), 
# ('Unix.Trojan.Gafgyt-111',), 
# ('Unix.Trojan.DDoS_XOR-1',), 
# ('Legacy.Trojan.Agent-1388639',), 
# ('Unix.Trojan.Mirai-5678467-0',), 
# ('Unix.Trojan.Flooder-353',), 
# ('Unix.Trojan.Agent-37008',), 
# ('Unix.Exploit.CVE_2016_5195-2',)

if __name__ == '__main__':
    conn = MySQLdb.connect(
        host = "ece4813-project-rds.cvei3yvcg2ng.us-east-2.rds.amazonaws.com",
        user = "root",
        passwd = "password",
        db = "DBPROJECT", 
        port = 3306
    )
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Malware LIMIT 1 OFFSET 8;")
    results = cursor.fetchall()
    print results
    cursor.close()
    conn.close()