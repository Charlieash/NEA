#NEA
#First draft for finding all possible bus routes between any two points
import time
def StartUp():
    Info = []
    with open("data.txt","r") as File:
        for row in File:
            Info.append(row)
    StartLocation = Info[0] #Get the starting location for the bus
    EndLocation = Info[1] #Get the end location for the bus
    StartTime = Info[2] #Get the wanted arrival time
    if ":" not in StartTime:
        return("Error")
    StartTime = StartTime.split(":")
    try:
        errorCatch = int(StartTime[0]) + int(StartTime[1])
        if StartTime[0] > 23 or StartTime[0] < 00 or StartTime[1] > 59 or StartTime[1]<00:
            return("Error")
    except:
        return("Error")
    EndTime = []
    EndTime.append(int(StartTime[0])+1) #no one wants to wait for a bus for longer than an hour
    EndTime.append(StartTime[1])
    EndTime = str(EndTime[0])+ ":" + str(EndTime[1]) 
    return(StartLocation, EndLocation, StartTime, EndTime)
def ConnectToDatabase():
    import mysql.connector
    mydb = mysql.connector.connect(
        host="localhost",                    #connects to the database
        user="root",
        passwd="LucieLeia0804",
        database="mysql"
        )
    mycursor = mydb.cursor()
    return(mycursor)
def TimeRange(TimeStart, TimeEnd, StartLocation, ConnectToDataBase):
    Routes = []
    myCursor = ConnectToDataBase()
    myCursor.execute("SELECT RouteId FROM times WHERE Time > {} AND Time < {} AND StopId = {}").format(TimeStart,TimeEnd,StartLocation)  #searches the databases for all routes leaving the given stop within the time range
    for i in range(len(myCursor)):
        Routes.append(i)
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

def MultipleBusses(routes, TimeRange, OneBus,TimeStart, TimeEnd):
    List = routes
    results = []
    reference = []
    myCursor = ConnectToDatabase()
    for i in range(len(List)):
        myCursor.execute("SELECT StopId FROM times WHERE RouteId = {}").format(List[i])
        StartLocation = myCursor
        routes = TimeRange(TimeStart,TimeEnd,StartLocation)
        routesinTime= OneBus(routes)
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