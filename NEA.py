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
            return()
        else:
            myCursor.execute(("SELECT time from times WHERE StopId = '{}' AND Routeid = '{}' AND time > '{}' AND time < '{}' AND RouteId != '{}'").format(StartLocationId,routes[u], TimeStart, TimeEnd, results[0]))
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



def MultipleBusses(routes,TimeStart, TimeEnd, results, StartLocationId, EndLocationId, myCursor):
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
                if Routes[o][0]== Stops[0]:
                    Routes[i].append(route)
        if len(Stops) > 0:
            if len(results[(len(results)-1)])> 1:
                routes = Routes[i][1]
                routesinTime= OneBus(routes,TimeStart, TimeEnd, StartLocationId , EndLocationId, results, myCursor)
                results.append(routesinTime)
    return(results)

def Interpret(results, myCursor, OGstartLocationID):
    Times = []
    Stops = []
    string =",".join('"%s"' % i for i in results)
    myCursor.execute(("SELECT BusNum FROM route WHERE idRoute IN ({})").format(string))
    variable = myCursor.fetchall()
    for m in range(len(variable)):
        Stops.append(format(variable[m]))
    for g in range(len(results)):
        myCursor.execute(("SELECT time FROM times WHERE Routeid = {} AND StopID = {}").format(results[g], OGstartLocationID))
        variable = myCursor.fetchall()
        Times.append(format(variable))
    for k in range(len(Stops)):
        Times[k] = Times[k].replace("[", "")
        Times[k] =Times[k].replace("]", "")
        Times[k] =Times[k].replace("'", "")
        Stops[k] =Stops[k].replace("'", "")
        print(Stops[k]+ ": "+ Times[k])

mydb = mysql.connector.connect(
    host="localhost",                    #connects to the database
    user="root",
    passwd="LucieLeia0804",
    database="mydb",
    )
myCursor = mydb.cursor()

DataInput = StartUp(myCursor)
#with open("It_works.txt","w") as Huh: #Test to see if php runs this script 
    #Huh.write("Thing")
TimeStart = DataInput[2]
TimeEnd = DataInput[3]
EndLocation = DataInput[1]
StartLocation = DataInput[0]
StartLocationId = DataInput[4]
OGstartLocationID = StartLocationId
EndLocationId = DataInput[5]
routes = TimeRange(TimeStart, TimeEnd, StartLocationId, myCursor)
results = ["100000000000000000000","1000000000000000000000"]
results = OneBus(routes,TimeStart, TimeEnd, StartLocationId, EndLocationId, results, myCursor)
Results= MultipleBusses(routes,TimeStart, TimeEnd, results, StartLocationId, EndLocationId, myCursor)
for i in range(len(Results)):
    if Results[i] not in results:
        results.append(Results[i])
print(results)
Interpret(results, myCursor, OGstartLocationID)

