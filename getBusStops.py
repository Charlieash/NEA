import mysql.connector
stops = ""
mydb = mysql.connector.connect(
    host="localhost",                    #connects to the database
    user="root",
    passwd="LucieLeia0804",
    database="mydb",
    )
myCursor = mydb.cursor()
myCursor.execute("SELECT StopName FROM stop")
Stops = myCursor.fetchall()
for i in range(len(Stops)):
    stop = str(Stops[i]).replace(",","")
    stop = str(stop).replace("(","")
    stop = str(stop).replace(")","")
    stop = str(stop).replace("'", "")
    stop = str(stop).replace("'", "")
    if i != len(Stops)-1:
        stops= stops + stop + ", " 
    else:
        stops = stops + stop
print(stops)