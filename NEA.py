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
    EndTime = Info[2] #Get the wanted arrival time
    Endtime = EndTime.split(":")
    StartTime = []
    StartTime.append(int(Endtime[0])-1) #no one wants to be on a bus for longer than an hour
    StartTime.append(Endtime[1])
    StartTime = str(StartTime[0])+ ":" + str(StartTime[1]) 
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

def OneBus(routes, EndLocation):
    RoutesInTime=[]
    myCursor = ConnectToDatabase()
    for u in range(len(routes)):
        myCursor.execute("SELECT RouteId FROM times WHERE StopId = {} AND RouteId = {}").format(EndLocation,RoutesInTime[u]) #selects the routes from all routes leaving the bus stop in the time range which end at the wanted bus stop
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
    
Thing = StartUp()
#with open("It_works.txt","w") as Huh: #Test to see if php runs this script 
    #Huh.write("Thing")
time.sleep(5)
TimeStart = Thing[2]
TimeEnd = Thing[3]
EndLocation = Thing[1]
StartLocation = Thing[0]