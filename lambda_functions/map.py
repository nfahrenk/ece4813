import pymysql
from geoip import geolite2
from flask import Flask, jsonify, render_template

app = Flask(__name__, static_url_path="")

USERNAME = 'root'
PASSWORD = 'password'
DB_NAME = 'DBPROJECT'
END_POINT = 'ece4813-project-rds.cvei3yvcg2ng.us-east-2.rds.amazonaws.com'

def get_ips():
    conn = pymysql.connect(host=END_POINT, port=3306, user=USERNAME, passwd=PASSWORD, db=DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT * FROM Malware;")
    conn.commit()
    result = cur.fetchall()
    cur.close()
    conn.close()

    x = [-180]
    y = [-90]

    for row in result:
        ips = str(row[9]).split(";")
        for ip in ips:
            if ip != 'None' and ip is not None:
                match = geolite2.lookup(ip)
                if match is not None:
                    x.append(match.location[0])
                    y.append(match.location[1])
            
            if len(x) == 9:
                x.append(180)
                y.append(90)
                return tuple([x, y])
        
    x.append(180)
    y.append(90)
    return tuple([x, y])

# get_ips()

def lambda_handler(event, context):
    locations = get_ips()
    response = {
        'longitudes': locations[0],
        'latitudes': locations[1]
    }
    return response

# @app.route('/')
# def hello_world():
#     locations = get_ips()
#     return render_template('dashboard.html', longitudes=locations[0], latitudes=locations[1])

# if __name__ == '__main__':
#     app.run(debug=True, port=5000)