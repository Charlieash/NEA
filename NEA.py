#NEA
#First draft for finding all possible bus routes between any two points
import time
import mysql.connector
from datetime import datetime

def format(variable):
    variable = str(variable).replace(",","")
    variable = str(variable).replace("(","")
    variable = str(variable).replace(")","") 
    return(variable)
    
def error(StartTime, StartLocation, EndLocation, myCursor):
    StartLocation = StartLocation.strip()
    EndLocation =EndLocation.strip()
    count = 0
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


def StartUp(myCursor):
    #try:
        Info = []
        with open("data.txt","r") as File:
            for row in File:
                Info.append(row)
        StartLocation = Info[0]
        EndLocation = Info[1]
        for k in range(len(Info[0])):
            if StartLocation[k] == "_":
                StartLocation = StartLocation.replace("_", " ") #Get the starting location for the bus
        for j in range(len(Info[1])):
            if EndLocation[j] == "_":
                EndLocation = EndLocation.replace("_", " ") #Get the end location for the bus
        StartTime = Info[2] #Get the wanted arrival time
        if ":" not in StartTime:
            ErrorCaught()
        StartTime = StartTime.split(":")
        Error = error(StartTime, StartLocation, EndLocation, myCursor)
        if Error == "Error":
            ErrorCaught()
            return(Error)
        EndTime = []
        EndTime.append(int(StartTime[0])+1) #no one wants to wait for a bus for longer than an hour
        EndTime.append(StartTime[1])
        EndTime = str(0)+str(EndTime[0])+ ":" + str(EndTime[1])
        StartTime = StartTime[0] +":"+ StartTime[1]
        StartTime = StartTime.rstrip()
        EndTime = EndTime.rstrip()
        StartLocation = StartLocation.rstrip()
        EndLocation = EndLocation.rstrip()
        Location = LocationId(StartLocation, EndLocation, myCursor)
        StartLocationId= Location[0]
        EndLocationId = Location[1]
        return(StartLocation, EndLocation, StartTime, EndTime, StartLocationId, EndLocationId)
    #except:
        #ErrorCaught()

def LocationId(StartLocation, EndLocation, myCursor):
    StartLocation = str(StartLocation).replace(",","")
    StartLocation = str(StartLocation).replace("(","")
    StartLocation = str(StartLocation).replace(")","") 
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

def TimeRange(TimeStart, TimeEnd, StartLocationId, myCursor):
    myCursor.execute(("""SELECT Routeid FROM times WHERE Time > '%s' AND Time < '%s' AND StopID = '%s'""")%(TimeStart ,TimeEnd ,StartLocationId))  #searches the databases for all routes leaving the given stop within the time range
    Routes = myCursor.fetchall()
    for i in range(len(Routes)):
        Routes[i] = str(Routes[i][0]).replace(",","")
        Routes[i] = str(Routes[i]).replace("(","")
        Routes[i] = str(Routes[i]).replace(")","")
        Routes[i] = int(Routes[i])
    return(Routes)


def OneBus(routes,TimeStart, TimeEnd, StartLocationId , EndLocationId, results, myCursor):
    RoutesInTime=[]
    for u in range(len(routes)):
        string =",".join('"%s"' % i for i in results)
        if len(results) > 1:
            myCursor.execute(("SELECT time from times WHERE StopId = '{}' AND Routeid = '{}' AND time > '{}' AND time < '{}' AND RouteId NOT IN ({})").format(StartLocationId,routes[u], TimeStart, TimeEnd,string)) #Finds the time range
        elif len(results)==0:
            myCursor.execute(("SELECT time from times WHERE StopId = '{}' AND Routeid = '{}' AND time > '{}' AND time < '{}'").format(StartLocationId,routes[u], TimeStart, TimeEnd))
        else:
            myCursor.execute(("SELECT time from times WHERE StopId = '{}' AND Routeid = '{}' AND time > '{}' AND time < '{}' AND RouteId != '{}'").format(StartLocationId,routes[u], TimeStart, TimeEnd, results[0][0]))
        Times = myCursor.fetchall()
        if len(Times)>0:
            Times = str(Times[0]).replace(",","")
            Times = str(Times).replace("(","")
            Times = str(Times).replace(")","") 
            Times = str(Times).strip('\'')
            myCursor.execute(("SELECT RouteId FROM times WHERE StopId = '{}' AND RouteId = '{}' AND time > '{}'").format(EndLocationId,routes[u],Times)) #selects the routes from all routes leaving the bus stop in the time range which end at the wanted bus stop
            variable = myCursor.fetchall() #appends the final product to a list
            if len(variable)>0:
                RoutesIn = format(variable)
                RoutesInTime.append(RoutesIn[1]) 
    return(RoutesInTime) 



def MultipleBusses(routes,TimeStart, TimeEnd, results, StartLocationId, EndLocationId, myCursor, OGstartLocationID):
    List = routes
    Routes = []
    for i in range(len(List)):
        myCursor.execute(("SELECT StopId FROM times WHERE RouteId = '{}' AND StopId != '{}'").format(List[i], StartLocationId))
        Stops = myCursor.fetchall()
        for a in range(len(Stops)):
            variable = Stops[a]
            Stops[a] = format(variable)
        for u in range(len(Stops)):
            StartLocationId=Stops[u][0]
            Routes.append([])
            Routes[i].append(Stops[u][0])
            route = TimeRange(TimeStart, TimeEnd, StartLocationId, myCursor)
            for o in range(len(Routes)):
                if Routes[o] != []:
                    if Routes[o][0]== Stops[0]:
                        Routes[i].append(route)
        if len(Stops) > 0:
           # try:
                if len(Routes[(len(Routes)-1)])> 1:
                    routes = Routes[i][1]
                    routesinTime= OneBus(routes,TimeStart, TimeEnd, StartLocationId , EndLocationId, results, myCursor)
                    if routesinTime != [] and routesinTime != ():
                        results.append(routesinTime)
                        EndLocationId = StartLocationId
                        StartLocationId = OGstartLocationID
                        routes = TimeRange(TimeStart, TimeEnd, StartLocationId, myCursor)
                        routesinTime= OneBus(routes,TimeStart, TimeEnd, StartLocationId , EndLocationId, results, myCursor)
                        if routesinTime != [] and routesinTime != ():
                            results.append(routesinTime)
                    
            #except:
            #    print()
    return(results)

def Interpret(results, myCursor, OGstartLocationID, OGTimeStart):
    Final = []
    FInal =""
    TimeLen = ""
    Times = []
    Stops = []
    string = ""
    for a in range(len(results)):
        if a == len(results)-1:
            string = string + results[a][0]
        else:
            string = string + results[a][0]+", "
    OGTimeStart = OGTimeStart.split(":")
    myCursor.execute(("SELECT BusNum FROM route WHERE idRoute IN ({})").format(string))
    variable = myCursor.fetchall()
    for m in range(len(variable)):
        Stops.append(format(variable[m]))
    for g in range(len(results)):
        try:
            minutes = 0
            myCursor.execute(("SELECT time FROM times WHERE Routeid = {} AND StopID = {}").format(results[g][0], OGstartLocationID))
            variable = myCursor.fetchall()
            Times.append(format(variable))
            time = Times[g].replace("[", "")
            time =time.replace("]", "")
            time = time.replace("'", "")
            time =time.replace("'", "")
            time = time.split(":")
            minutes = minutes + ((-int(OGTimeStart[0]) + int(time[0]))*60)
            TimeLen = TimeLen+ str(minutes+(-int(OGTimeStart[1]) + int(time[1]))) +"\n"
        except:
            print()
    for k in range(len(Stops)):
        Times[k] = Times[k].replace("[", "")
        Times[k] =Times[k].replace("]", "")
        Times[k] =Times[k].replace("'", "")
        Stops[k] =Stops[k].replace("'", "")
        final = (Stops[k]+ " @ "+ Times[k])
        Final.append(final + ", ")
    Final.reverse()
    for l in range(len(Final)):
        FInal = FInal + Final[l]
    with open("data.txt","w") as File:
        File.write(FInal)
    with open("times.txt", "w") as File:
        File.write(TimeLen)

mydb = mysql.connector.connect(
    host="localhost",                    #connects to the database
    user="root",
    passwd="LucieLeia0804",
    database="mydb",
    )
myCursor = mydb.cursor()

DataInput = StartUp(myCursor)
TimeStart = DataInput[2]
TimeEnd = DataInput[3]
EndLocation = DataInput[1]
StartLocation = DataInput[0]
StartLocationId = DataInput[4]
OGTimeStart = TimeStart
OGstartLocationID = StartLocationId
EndLocationId = DataInput[5]
routes = TimeRange(TimeStart, TimeEnd, StartLocationId, myCursor)
results = ["100000000000000000000","1000000000000000000000"]
results = OneBus(routes,TimeStart, TimeEnd, StartLocationId, EndLocationId, results, myCursor)
Results= MultipleBusses(routes,TimeStart, TimeEnd, results, StartLocationId, EndLocationId, myCursor, OGstartLocationID)
for i in range(len(Results)):
    if Results[i] not in results:
        results.append(Results[i])
print(results)
Interpret(results, myCursor, OGstartLocationID, OGTimeStart)