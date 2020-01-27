#NEA
#First draft for finding all possible bus routes between any two points
import time
import mysql.connector
def ConnectToDatabase():
    mydb = mysql.connector.connect(
        host="localhost",                    #connects to the database
        user="root",
        passwd="LucieLeia0804",
        database="mydb",
        )
    mycursor = mydb.cursor()
    return(mycursor)



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
    print(Stops)
    print(StartLocation)
    print(EndLocation)
    
    for i in range(len(Stops)):
        print(Stops[i])       
        if StartLocation == (Stops[i][0]) or EndLocation ==(Stops[i][0]):
            count = count+1
        print(count)
    if count != 2:
        print("1")
        return("Error")
    try:
        errorCatch = int(StartTime[0]) + int(StartTime[1])
        if int(StartTime[0]) > 23 or int(StartTime[0]) < 00 or int(StartTime[1]) > 59 or int(StartTime[1])<00:
            print("2")
            return("Error")
    except:
        print("3")
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
    return(StartLocation, EndLocation, StartTime, EndTime)



def TimeRange(TimeStart, TimeEnd, StartLocation):
    Routes = []
    myCursor = ConnectToDatabase()
    myCursor.execute("SELECT RouteId FROM times WHERE Time > {} AND Time < {} AND StopId = {}").format(TimeStart,TimeEnd,StartLocation)  #searches the databases for all routes leaving the given stop within the time range
    for i in range(len(myCursor)):
        Routes.append(myCursor[i])
    print(Routes)
    return(Routes)



def OneBus(routes, EndLocation, StartLocation, TimeStart, TimeEnd):
    RoutesInTime=[]
    myCursor = ConnectToDatabase()
    for u in range(len(routes)):
        Times = myCursor.execute("SELECT Time from times WHERE StopId = {} AND RouteID = {} AND Time > {} AND Time < {}").format(StartLocation,routes[u], TimeStart, TimeEnd) #Finds the time range
        myCursor.execute("SELECT RouteId FROM times WHERE StopId = {} AND RouteId = {} AND Time>{}").format(EndLocation,routes[u],Times) #selects the routes from all routes leaving the bus stop in the time range which end at the wanted bus stop
        RoutesInTime.append(myCursor) #appends the final product to a list
    return(RoutesInTime) 



def MultipleBusses(routes,TimeStart, TimeEnd):
    List = routes
    results = []
    reference = []
    myCursor = ConnectToDatabase()
    for i in range(len(List)):
        myCursor.execute("SELECT StopId FROM times WHERE RouteId = {}").format(List[i])
        StartLocation = myCursor
        routes = TimeRange(TimeStart,TimeEnd,StartLocation)
        routesinTime= OneBus(routes, EndLocation, StartLocation, TimeStart, TimeEnd)
        results.append(routesinTime)
        reference.append(List[i])



DataInput = StartUp()
#with open("It_works.txt","w") as Huh: #Test to see if php runs this script 
    #Huh.write("Thing")
time.sleep(5)
TimeStart = DataInput[2]
TimeEnd = DataInput[3]
EndLocation = DataInput[1]
StartLocation = DataInput[0]