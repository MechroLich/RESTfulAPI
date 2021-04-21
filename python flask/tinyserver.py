from flask import Flask, request
from newsapi import NewsApiClient
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
import logging, xmlrpc.client, requests, json, pandas as pd,pika

from flask import request
app = Flask(__name__)

#additional setup
def setup_logger(name, log_file, level=logging.INFO):
    """To setup as many loggers as you want"""

    handler = logging.FileHandler(log_file)  
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger

#log file setup
userLog = 'user.log'
cmdLog = 'calls.log'

formatter = logging.Formatter('%(asctime)s %(message)s', datefmt='%d/%m/%Y %H:%M:%S')

logging.basicConfig(filename=cmdLog,level=logging.DEBUG,format='%(asctime)s %(message)s', datefmt='%d/%m/%Y %H:%M:%S')

users = setup_logger('user', userLog)

@app.route('/')
def first():

    return 'Hello, World!'

@app.route('/insertStudent')
def insertstudent():
    studentid = request.args.get('studentid')
    studentname = request.args.get('studentname')
    studentdob = request.args.get('studentdob')

    users.info('Insert student' + studentid + '-' + studentname + '-' + studentdob)
    return 'Insert student' + studentid + '-' + studentname + '-' + studentdob

@app.route('/justweather')
def weather():
    api_key = "c739afaac3bc00406b776060a89e983a"
  
    # base_url variable to store url 
    base_url = "http://api.openweathermap.org/data/2.5/forecast?"
    
    # Give city name 
    city_name = request.args.get('city')
    
    # complete_url variable to store 
    # complete url address 
    complete_url = base_url + "appid=" + api_key + "&q=" + city_name  +"&units=metric"
    
    # get method of requests module 
    # return response object 
    response = requests.get(complete_url) 
    
    # json method of response object  
    # convert json format data into 
    # python format data 
    x = response.json() 
    
    # declare rabbitmq queue
    # Now x contains list of nested dictionaries 
    # Check the value of "cod" key is equal to 
    # "404", means city is found otherwise, 
    # city is not found 
    if x["cod"] != "404": 
        i=0
        ret = "{"
        while(i<= 39):
            y=x["list"]
            z=y[i]
            main = z["main"]
            curtemp = main["temp"]
            weather = z["weather"]
            q=weather[0]
            desc = q["description"]
            req = requests.post("http://localhost/rabbitmq/send.php/?date="+z["dt_txt"] +"&description="+desc+"&temperature="+ str(curtemp))
            jsondata = '{"date" : "'+z["dt_txt"]+'", "current temp" : "'+str(curtemp)+'", "description" :"'+ desc+'"},'
            
            ret = ret + jsondata
            i = i+8
        ret = json.dumps(ret[:-1]+"}")
        ret = json.loads(ret)
        return (ret)    
    else: 
        return(" City Not Found ")

@app.route('/updates')
def updates():
    f = open('update.txt', 'r')
    x = f.readlines()

    output = '{'

    for item in x:
        #   "line1": "item1",
        output = output + '"line": "'+item + '",'
    f.close()

    output = output[:-1]

    output = output + '}'

    return output   

@app.route('/ping')
def ping():
    return 'Pong'

@app.route('/callClient')
def call_rpc():
    temp = int(request.args.get('temp'))
    with xmlrpc.client.ServerProxy("http://localhost:8001/") as proxy:
        return proxy.temperature(temp)

@app.route('/students')
def call_graphql(): 
    # Select your transport with a defined url endpoint
    transport = AIOHTTPTransport(url="http://localhost:4000/graphql")

    # Create a GraphQL client using the defined transport
    client = Client(transport=transport, fetch_schema_from_transport=True)

    studentid = request.args.get('studentid')
    studentname = request.args.get('studentname')
    studentdob = request.args.get('studentdob')
    if(studentdob is not None):
        #query by dob
        query = gql(
                    """
                    query QueryByDob($dob:String!)
                    {
                    studentQueryByDob(studentdob:$dob)
                    {
                        studentid
                        studentdob
                        studentname
                    } 
                    }                  
                    """   ) 
        params = {
            "dob" : studentdob
        }
        result = client.execute(query, variable_values= params)
        return(result)
    elif(studentid is not None):
        #query by id
        query = gql(
                    """
                    query QueryById($id:String!)
                    {
                    studentQueryById(studentid:$id)
                    {
                        studentid
                        studentdob
                        studentname
                    } 
                    }                  
                    """   ) 
        params = {
            "id" : studentid
        }
        result = client.execute(query, variable_values= params)
        return(result)
    elif(studentname is not None):
        query = gql(
                    """
                    query QueryByName($name:String!)
                    {
                    studentQueryByName(studentname:$name)
                    {
                        studentid
                        studentdob
                        studentname
                    } 
                    }                  
                    """   ) 
        params = {
            "name" : studentname
        }
        result = client.execute(query, variable_values= params)
        return(result)
    else:
        return "please enter a single attribute" + studentid + '-' + studentname + '-' + studentdob