import pymongo
from pymongo import MongoClient
import dns
import datetime 
from datetime import datetime
from fastapi import FastAPI
from email.message import EmailMessage
import ssl
import smtplib

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS access to everyone, change in prod if possible
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


ROWS = 9
COLUMNS = 9
parkingData = {}

cluster = MongoClient("mongodb+srv://Parkingroup:qwerty87654321@parkinglot.joirc8l.mongodb.net/?retryWrites=true&w=majority")

db = cluster["parking"]
vehicledata= db["vehicledata"]
lotdata= db["parkinglotmatrix"]

global unformattedLot
unformattedLot = {}



@app.get("/v1/add/{type}/{id}/{color}/{name}/{email}")
def addCarToLot(id, type, color, name, email):
    time = datetime.now()
    parkingData[id] = {"name": name, "type": type, "color": color, "timeofentry" : time, "email": email}
    vehicledata.update_one({'_id': id},  {"$set": parkingData}, upsert=True)
    unformattedLot[id] = type
    formattedLot = [[], [], []]
    print(unformattedLot)
    for vehicle in unformattedLot:
        if unformattedLot[vehicle] == "bike":
            formattedLot[0].append(vehicle)
        elif unformattedLot[vehicle] == "car":
            formattedLot[1].append(vehicle)
        elif unformattedLot[vehicle] == "truck":
            formattedLot[2].append(vehicle)
    if len(formattedLot[0]) % 2 != 0:
        formattedLot[0].append(0)
    bikesGrouped = []
    for bike in range(0, len(formattedLot[0]), 2):
        bikesGrouped.append([formattedLot[0][bike], formattedLot[0][bike + 1]])
    formattedLot[0] = bikesGrouped
    numVehicles = 0
    for bike in formattedLot[0]:
        numVehicles += 1
    for vehicles in formattedLot[1]:
        numVehicles += 1
    for vehicles in formattedLot[2]:
        numVehicles += 2
    global ROWS
    global COLUMNS
    totalSpots = ROWS * COLUMNS
    if numVehicles != totalSpots:
        for emptySpot in range(totalSpots - numVehicles):
            formattedLot[1].append(0)
    positionList = []
    for vehicles in formattedLot:
        for vehicle in vehicles:
            positionList.append(vehicle)
    for vehicle in positionList:
        if id in str(vehicle):
            pos = positionList.index(vehicle)
    trucksGrouped = []
    for truck in formattedLot[2]:
        trucksGrouped.append(truck)
        trucksGrouped.append(truck)
        trucksGrouped.append("barrier")
    formattedLot[2] = trucksGrouped
    finalLot = {}
    finalLot["bikes"] = formattedLot[0]
    finalLot["cars"] = formattedLot[1]
    finalLot["trucks"] = formattedLot[2]
    lotdata.update_one({'_id': 1},  {"$set":{"finalLot":finalLot}}, upsert=True)
    i = parkingData[id]
    j = i["email"]
    sendMail(j, pos, name, id)
    return finalLot

@app.get("/v1/changegrid/{num}")
def changeGrid(num):
    global ROWS
    global COLUMNS
    print(ROWS)
    ROWS = int(num)
    print(ROWS)
    COLUMNS = int(1)
    return {"200": "ok"}


@app.get("/v1/showall")
def showCarsInLot():
    cursor = lotdata.find({})
    try:
        document = cursor[0]
    except:
        document = {"finalLot": {"bikes": [], "cars": [], "trucks": []}}
        for emptySpot in range(ROWS * COLUMNS):
            document["finalLot"]["cars"].append(0)
    return document


@app.get("/v1/clearall")
def showCarsInLot():
    document = {"finalLot": {"bikes": [], "cars": [], "trucks": []}}
    for emptySpot in range(ROWS * COLUMNS):
        document["finalLot"]["cars"].append(0)
    print(document)
    lotdata.update_one({'_id': 1},  {"$set":{"finalLot":document["finalLot"]}}, upsert=True)
    return document
        
        
@app.get("/v1/remove/{id}")
def removeCarFromLot(id):
  vehdict = list(vehicledata.find({ '_id' : id}))
  print(vehdict)
  globalFormattedLot = list(lotdata.find({'_id': 1}))
  b = datetime.now()
  print("HR")
  print(vehdict)
  a = vehdict[0][id]["timeofentry"]
  vehtype = vehdict[0][id]["type"]
  for vehicles in globalFormattedLot[0]["finalLot"]["bikes"]:
      for bike in vehicles:
          if bike == id:
              vehicles[vehicles.index(bike)] = 0
  for vehicle in globalFormattedLot[0]["finalLot"]["cars"]:
          if vehicle == id:
            globalFormattedLot[0]["finalLot"]["cars"][globalFormattedLot[0]["finalLot"]["cars"].index(vehicle)] = 0
  for vehicle in globalFormattedLot[0]["finalLot"]["trucks"]:
          if vehicle == id:
            globalFormattedLot[0]["finalLot"]["trucks"][globalFormattedLot[0]["finalLot"]["trucks"].index(vehicle)] = 0
  for vehicle in globalFormattedLot[0]["finalLot"]["trucks"]:
          if vehicle == id:
            globalFormattedLot[0]["finalLot"]["trucks"][globalFormattedLot[0]["finalLot"]["trucks"].index(vehicle)] = 0
  c=b-a
  c = c.seconds / 60 / 30
  if vehtype == "car":
    basefee = 1 #1 rial per halfnhour
    TotalFee = str(c*basefee)
  elif vehtype == "bike":
    basefee = 0.5 #500baiza per halfnhour  
    TotalFee = str(c*basefee)
    print(TotalFee)
  elif vehtype == "truck":
    basefee = 2 #2 rials per halfnhour 
    TotalFee = str(c*basefee)
  finalLot = {}
  finalLot["bikes"] = globalFormattedLot[0]["finalLot"]["bikes"]
  finalLot["cars"] = globalFormattedLot[0]["finalLot"]["cars"]
  finalLot["trucks"] = globalFormattedLot[0]["finalLot"]["trucks"]
  lotdata.update_one({'_id': 1},  {"$set":{"finalLot":finalLot}}, upsert=True)
  formattedLot = globalFormattedLot
  del unformattedLot[id]
  return TotalFee[:6]

@app.get("/v1/getdetails/{id}")
def CarDetails(id):
  vehdict = vehicledata.find({"_id": id})
  for j in vehdict:
    l = j[id]
    return l

@app.get("/v1/alldetails")
def CarDetails():
  vehdict = list(vehicledata.find({}))
  return vehdict
    

    
def sendMail(j, pos, modelName, id):
  email_sender = "parkinglotsmailer@gmail.com"
  email_password = "cflswspzbrpckpsv"
  email_reciever = j+"@gmail.com"
  q = lotdata.find({"_id":1})
  subject = "Parking Lot Q3 - As'Salam St"
  body = f"Your Vehicle {modelName} with Plate Number {id} is Parked at N{str(pos + 2)}. Thank You!"
  em=EmailMessage()
  em["From"]=email_sender
  em["To"] = email_reciever
  em["Subject"]=subject
  em.set_content(body)
  context = ssl.create_default_context()
  
  with smtplib.SMTP_SSL('smtp.gmail.com', 465, context = context) as smtp:
      smtp.login(email_sender, email_password)
      smtp.sendmail(email_sender, email_reciever, em.as_string())
        

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
    
