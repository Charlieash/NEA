import mysql.connector
mydb = mysql.connector.connect(
    host="localhost",                    #connects to the instance
    user="root",
    passwd="password",
    )
mycursor = mydb.cursor()
mycursor.execute("CREATE DATABASE mydb") #creates the database

mydb = mysql.connector.connect( #connects to the database
  host="localhost",
  user="root",
  passwd="password", 
  database="mydb"
)

mycursor = mydb.cursor()

mycursor.execute("CREATE TABLE `Route` (`idRoute` int(11) NOT NULL AUTO_INCREMENT,`BusNum` varchar(45) NOT NULL,`RouteLength` varchar(45) NOT NULL, PRIMARY KEY (`idRoute`));")
#creates the table Route
mycursor.execute("CREATE TABLE `stop` (`idStop` int(11) NOT NULL AUTO_INCREMENT,`StopName` varchar(45) NOT NULL AUTO_INCREMENT,PRIMARY KEY (`idStop`));")
#creates the table stop
mycursor.execute("CREATE TABLE `times` (`Primary key` int(11) NOT NULL AUTO_INCREMENT,`Routeid` int(11) NOT NULL,`Stopid` int(11) NOT NULL,`time` varchar(45) NOT NULL,PRIMARY KEY (`Primary key`));")
#creates the table times
mycursor.execute("ALTER TABLE `times` ADD CONSTRAINT `times_fk0` FOREIGN KEY (`Routeid`) REFERENCES `Route`(`idRoute`);")
#creates a link between Routeid and idRoute
mycursor.execute("ALTER TABLE `times` ADD CONSTRAINT `times_fk1` FOREIGN KEY (`Stopid`) REFERENCES `stop`(`idStop`);")
#creates a link between Stopid and idStop
