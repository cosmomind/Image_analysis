
from pymongo import  MongoClient
import urllib.parse
import datetime

username = urllib.parse.quote_plus('riya')
password = urllib.parse.quote_plus('Astrid@36')

cluster = MongoClient("mongodb+srv://" + username +":"+ password+
                      "@" + "\cluster0.yn5qziw.mongodb.net" +"/?authSource=admin&retryWrites=true&w=majority")

db = cluster["covid"]
collection = db["patient"]


#insert period as a document inside our mongodb
def insert_period(name,age,stdob,phone,aadhar,gender,pincode,address):
  

    date = stdob[:5] +stdob[5:7] +  stdob[7:]
    return collection.insert_one({"name":name,"age":age,"date": date,"phone":phone,"aadhar":aadhar
                                  ,"gender":gender,"pincode":pincode,"address":address})

