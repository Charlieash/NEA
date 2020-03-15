#NEA
#First draft for finding all possible bus routes between any two points
import time
import mysql.connector
from datetime import datetime

def format(variable): #this function strips all brackets and commas from a string as that is the format they come out of the database which is difficult to process 
    variable = str(variable).replace(",","") 
    variable = str(variable).replace("(","")
    variable = str(variable).replace(")","") 
    return(variable)
    
def error(StartTime, StartLocation, EndLocation, myCursor): #function checks the inputted data from the homepage to check whether it is usable 
    StartLocation = StartLocation.strip()
    EndLocation =EndLocation.strip() #strips /n etc from StartLocation and EndLocation
    count = 0 #this variable will be used to show that there between StartLocation and EndLocation there are 2 valid bus stops
    myCursor.execute("SELECT StopName FROM stop")
    Stops = myCursor.fetchall()
    
    for i in range(len(Stops)):     
        if StartLocation == (Stops[i][0]) or EndLocation ==(Stops[i][0]):
            count = count+1
    if count != 2:
        return("Error") #if there are more or less than 2 valid bus stops there has been a problem and hence there is an error 
    try:
        errorCatch = int(StartTime[0]) + int(StartTime[1]) #attempts to convert each part of the inputted time to an integer, if this fails they are not numbers hence in the incorrect format
        if int(StartTime[0]) > 23 or int(StartTime[0]) < 00 or int(StartTime[1]) > 59 or int(StartTime[1])<00: #makes sure the times are within the possible region for time formats
            return("Error")
    except:
        return("Error")


def ErrorCaught():
    print("Error") #by printing "error" the php can read it and display the error page 
    return("error")


def StartUp(myCursor):
    try:
        Info = []
        with open("data.txt","r") as File: #gets the input data from the homepage which was saved in "data.txt"
            for row in File:
                Info.append(row)#inputs said data to a 2d list
        StartLocation = Info[0]#gets starting location
        EndLocation = Info[1]#gets ending location
        for k in range(len(Info[0])):
            if StartLocation[k] == "_":
                StartLocation = StartLocation.replace("_", " ") #the bus stop are displayed as single strings seperated by underscores which have to be removed so that they can be processed
        for j in range(len(Info[1])):
            if EndLocation[j] == "_":
                EndLocation = EndLocation.replace("_", " ") #same thing as what happens to StartLocation
        StartTime = Info[2] #Get the wanted arrival time
        if ":" not in StartTime: #Starttime should be in the format int:int so if there is no : it is in an incorrect format
            ErrorCaught() 
        StartTime = StartTime.split(":") #splits StartTime into two seperate integers so that they can be processed seperately 
        Error = error(StartTime, StartLocation, EndLocation, myCursor)
        if Error == "Error":
            ErrorCaught()
            return(Error) #breaks the process
        EndTime = []
        EndTime.append(int(StartTime[0])+1) #no one wants to wait for a bus for longer than an hour
        EndTime.append(StartTime[1])#end time is just starttime with an extra hour
        EndTime = str(0)+str(EndTime[0])+ ":" + str(EndTime[1]) #puts EndTime in the correct format
        StartTime = StartTime[0] +":"+ StartTime[1] #reformats StartTime
        StartTime = StartTime.rstrip() #removes and /n s etc from StartTime, Endtime, StartLocation and EndLocation
        EndTime = EndTime.rstrip()
        StartLocation = StartLocation.rstrip()
        EndLocation = EndLocation.rstrip()
        Location = LocationId(StartLocation, EndLocation, myCursor) #this function finds the Id of the Starting Bus stop and the Ending Bus stop
        StartLocationId= Location[0]
        EndLocationId = Location[1]
        return(StartLocation, EndLocation, StartTime, EndTime, StartLocationId, EndLocationId)
    except:
        ErrorCaught() #if this process fails there has been an error 

def LocationId(StartLocation, EndLocation, myCursor):
    variable = StartLocation
    StartLocation = format(variable)
    myCursor.execute(("SELECT idStop FROM stop WHERE StopName = '%s'")%(StartLocation)) #gets the id of the starting location
    variable = myCursor.fetchall()
    StartLocationId = format(variable)
    StartLocationId = int(StartLocationId)
    myCursor.execute(("SELECT idStop FROM stop WHERE StopName = '%s'")%(EndLocation))#gets the id of the ending location
    variable = myCursor.fetchall()
    EndLocationId = format(variable)
    EndLocationId = int(EndLocationId)
    return(StartLocationId, EndLocationId) #returns both ids

def TimeRange(TimeStart, TimeEnd, StartLocationId, myCursor):
    myCursor.execute(("""SELECT Routeid FROM times WHERE Time > '%s' AND Time < '%s' AND StopID = '%s'""")%(TimeStart ,TimeEnd ,StartLocationId))  #searches the databases for all routes leaving the given stop within the time range
    Routes = myCursor.fetchall() #fetches all the routes as a list
    for i in range(len(Routes)):
        variable = str(Routes[i])
        Routes[i] = format(variable) #formats each route appropriately 
        Routes[i] = int(Routes[i])
    return(Routes)#returns the list of routes


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
    BusNum = []
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
        BusNum.append(format(variable[m]))
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
    for k in range(len(BusNum)):
        Times[k] = Times[k].replace("[", "")
        Times[k] =Times[k].replace("]", "")
        Times[k] =Times[k].replace("'", "")
        BusNum[k] =BusNum[k].replace("'", "")
        final = (BusNum[k]+ " @ "+ Times[k])
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