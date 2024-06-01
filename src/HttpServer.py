from MicroPyServer import Server
import URLlib
import Interpreter
from Config import WEBSERVER_PAGES,WEBSERVER_PORT

myServer=Server(port=WEBSERVER_PORT)
interp=Interpreter.ScriptRunner()

def fetchWebPage(TextArea,Output):
    """
    Fetch the Editor.html web page and substitute some values
    :param TextArea: string to replace %%TEXTAREA%%
    :param Output: string used to replce %%OUTPUT%%
    :return: subsituted string (web page)
    """
    with open(WEBSERVER_PAGES+"/Editor.html") as f:
        data=f.read()
    
    data=data.replace("%%TEXTAREA%%",TextArea)
    data=data.replace("%%OUTPUT%%",Output)
    return data

cachedProgram=""

def sendData(data,status="200 OK"):
    myServer.send(f"HTTP/1.0 {status}\r\n")
    myServer.send("Content-Type: text/html\r\n\r\n")
    myServer.send(data)

# the following are action responses to button presses
def home(request):
    print("home route")
    if cachedProgram=="":
        sendData(fetchWebPage("",""))
    else:
        sendData(fetchWebPage(cachedProgram,"Showing last editor program"))

def upload(request):
    print("route upload")
    program=URLlib.parse(request)

    if len(program)>0:
        cachedProgram=program
        interp.storeScriptAndRun(program)
        sendData(fetchWebPage(cachedProgram,"uploaded program ok"))
    else:
        status="Whoops, nothing uploaded!"
        sendData(fetchWebPage("",status))

def stop(request):
    interp.stopScript()
    sendData(fetchWebPage(cachedProgram,"Stop Ok"))
    
def run(request):
    print("route run")
    interp.startScript()
    sendData(fetchWebPage(cachedProgram,"Run requested Ok"))

def download(request):
    print("route download")
    cachedProgram=interp.getScript()
    sendData(fetchWebPage(cachedProgram,"download Ok"))
 
def clear(request):
    print("route clear")
    cachedProgram=""
    sendData(fetchWebPage(cachedProgram,"Editor cleared Ok. Pixelbot still has previous script."))

myServer.add_route("/",home,method="GET")

# uploading can be GET for data <=2048 bytes and POST for higher
# buffer size in MicroPyServer is 4096 bytes
myServer.add_route("/upload",upload,method="POST")
myServer.add_route("/upload",upload,method="GET")

myServer.add_route("/download",download,method="GET")
myServer.add_route("/run",run,method="GET")
myServer.add_route("/clear",clear,method="GET")
myServer.add_route("/stop",stop,method="GET")
myServer.start()

import asyncio
# needed to keep the polling going
polling=True
def poller():
    print("Polling started")
    while polling:
        myServer.poll()
        time.sleep(0.1)
    print("poller stopped")
    
import threading
import time

thread=threading.Thread(target=poller,args=())
thread.start()

interp.begin()


try:
    while True:
        time.sleep(1)
except:
    polling=False
    interp.stopScript()
