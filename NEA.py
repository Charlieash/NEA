#NEA
#First draft for finding all possible bus routes between any two points
import time
import mysql.connector
from datetime import datetime
def ConnectToDatabase():
    mydb = mysql.connector.connect(
        host="localhost",                    #connects to the database
        user="root",
        passwd="LucieLeia0804",
        database="mydb",
        )
    mycursor = mydb.cursor()
    return(mycursor)

def format(variable):
    variable = str(variable).replace(",","")
    variable = str(variable).replace("(","")
    variable = str(variable).replace(")","") 
    return(variable)
def error(StartTime, StartLocation, EndLocation):
    StartLocation = StartLocation.strip()
    EndLocation =EndLocation.strip()
    count = 0
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
        if StartLocation == (Stops[i][0]) or EndLocation ==(Stops[i][0]):
            count = count+1
    if count != 2:
        return("Error")
    try:
        errorCatch = int(StartTime[0]) + int(StartTime[1])
        if int(StartTime[0]) > 23 or int(StartTime[0]) < 00 or int(StartTime[1]) > 59 or int(StartTime[1])<00:
            return("Error")
    except:
        return("Error")


def ErrorCaught():
    print("Error")
    return("error")


def StartUp():
    Info = []
    with open("data.txt","r") as File:
        for row in File:
            Info.append(row)
    StartLocation = Info[0] #Get the starting location for the bus
    EndLocation = Info[1] #Get the end location for the bus
    StartTime = Info[2] #Get the wanted arrival time
    if ":" not in StartTime:
        ErrorCaught()
    StartTime = StartTime.split(":")
    Error = error(StartTime, StartLocation, EndLocation)
    if Error == "Error":
        ErrorCaught()
        return(Error)
    EndTime = []
    EndTime.append(int(StartTime[0])+1) #no one wants to wait for a bus for longer than an hour
    EndTime.append(StartTime[1])
    EndTime = str(EndTime[0])+ ":" + str(EndTime[1])
    StartTime = StartTime[0] +":"+ StartTime[1]
    StartTime = StartTime.rstrip()
    EndTime = EndTime.rstrip()
    StartLocation = StartLocation.rstrip()
    EndLocation = EndLocation.rstrip()
    Location = LocationId(StartLocation, EndLocation)
    StartLocationId= Location[0]
    EndLocationId = Location[1]
    return(StartLocation, EndLocation, StartTime, EndTime, StartLocationId, EndLocationId)

def LocationId(StartLocation, EndLocation):
    mydb = mysql.connector.connect(
        host="localhost",                    #connects to the database
        user="root",
        passwd="LucieLeia0804",
        database="mydb",
        )
    StartLocation = str(StartLocation).replace(",","")
    StartLocation = str(StartLocation).replace("(","")
    StartLocation = str(StartLocation).replace(")","") 
    myCursor = mydb.cursor()
    myCursor.execute(("SELECT idStop FROM stop WHERE StopName = '%s'")%(StartLocation))
    StartLocationId = myCursor.fetchall()
    StartLocationId = str(StartLocationId[0]).replace(",","")
    StartLocationId = str(StartLocationId).replace("(","")
    StartLocationId = str(StartLocationId).replace(")","") 
    StartLocationId = int(StartLocationId)
    myCursor.execute(("SELECT idStop FROM stop WHERE StopName = '%s'")%(EndLocation))
    EndLocationId = myCursor.fetchall()
    EndLocationId = str(EndLocationId[0]).replace(",","")
    EndLocationId = str(EndLocationId).replace("(","")
    EndLocationId = str(EndLocationId).replace(")","") 
    EndLocationId = int(EndLocationId)
    return(StartLocationId, EndLocationId)

def TimeRange(TimeStart, TimeEnd, StartLocationId):
    mydb = mysql.connector.connect(
        host="localhost",                    #connects to the database
        user="root",
        passwd="LucieLeia0804",
        database="mydb",
        )
    myCursor = mydb.cursor()
    myCursor.execute(("""SELECT Routeid FROM times WHERE Time > '%s' AND Time < '%s' AND StopID = '%s'""")%(TimeStart ,TimeEnd ,StartLocationId))  #searches the databases for all routes leaving the given stop within the time range
    Routes = myCursor.fetchall()
    for i in range(len(Routes)):
        Routes[i] = str(Routes[i][0]).replace(",","")
        Routes[i] = str(Routes[i]).replace("(","")
        Routes[i] = str(Routes[i]).replace(")","")
        Routes[i] = int(Routes[i])
    print(Routes)
    return(Routes)


def OneBus(routes,TimeStart, TimeEnd, StartLocationId , EndLocationId):
    RoutesInTime=[]
    mydb = mysql.connector.connect(
        host="localhost",                    #connects to the database
        user="root",
        passwd="LucieLeia0804",
        database="mydb",
        )
    myCursor = mydb.cursor()
    for u in range(len(routes)):
        myCursor.execute(("SELECT Time from times WHERE StopId = '{}' AND RouteID = '{}' AND Time > '{}' AND Time < '{}'").format(StartLocationId,routes[u], TimeStart, TimeEnd)) #Finds the time range
        Times = myCursor.fetchall()
        Times = str(Times[0]).replace(",","")
        Times = str(Times).replace("(","")
        Times = str(Times).replace(")","") 
        myCursor.execute(("SELECT RouteId FROM times WHERE StopId = {} AND RouteId = {} AND Time>{}").format(EndLocationId,routes[u],Times)) #selects the routes from all routes leaving the bus stop in the time range which end at the wanted bus stop
        RoutesInTime = myCursor.fetchall() #appends the final product to a list
    return(RoutesInTime) 



def MultipleBusses(routes,TimeStart, TimeEnd, results, StartLocationId, EndLocationId):
    mydb = mysql.connector.connect(
        host="localhost",                    #connects to the database
        user="root",
        passwd="LucieLeia0804",
        database="mydb",
        )
    myCursor = mydb.cursor()
    List = routes
    Routes = []
    for i in range(len(List)):
        myCursor.execute(("SELECT StopId FROM times WHERE RouteId = {} AND StopId != {}").format(List[i], StartLocationId))
        Stops = myCursor.fetchall()
        for u in range(len(Stops)):
            StartLocationId=Stops[u][0]
            Routes.append([])
            Routes[u].append(Stops[u][0])
            route = TimeRange(TimeStart, TimeEnd, StartLocationId)
            for o in range(len(Routes)):
                if Routes[o]== Stops[u][0]:
                    Routes[o].append(route)
        for k in range(len(Routes)):
            routes = Routes[k]
            routesinTime= OneBus(routes,TimeStart, TimeEnd, StartLocationId , EndLocationId)
            results.append(routesinTime)
    return(results, results)



DataInput = StartUp()
#with open("It_works.txt","w") as Huh: #Test to see if php runs this script 
    #Huh.write("Thing")
time.sleep(5)
TimeStart = DataInput[2]
TimeEnd = DataInput[3]
EndLocation = DataInput[1]
StartLocation = DataInput[0]
StartLocationId = DataInput[4]
EndLocationId = DataInput[5]
routes = TimeRange(TimeStart, TimeEnd, StartLocationId)
results = OneBus(routes,TimeStart, TimeEnd, StartLocationId, EndLocationId)
results = MultipleBusses(routes,TimeStart, TimeEnd, results, StartLocationId, EndLocationId)