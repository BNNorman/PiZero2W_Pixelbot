# Interpreter.py
#
# A script is wrapped in async calls then given to exec() to run
# It is possible to 'puase' the script but not to force it to
# start at a given line.
#
# it is possible to set variables whilst the script is running
# and so they may cause behavioural changes


import sys
import HullOS
import time
import re
import threading
from mqtt import MQTT_CLIENT

from Config import PYTHON_INDENT, PIXELBOT_NAME

STORED_SCRIPT = "StoredScript.py"

reLoop = re.compile("^(\s*)(while|for)\s")  # test for a loop
reIndent = re.compile("^(\s*)(.*)")  # extract current indent
reQuote=re.compile("(\"|\')")
# these script lines will be ignored
reBlank = re.compile("^\s*$")  # blank line
reComment = re.compile("^\s*#.*$")  # comment

DEBUG_SCRIPT = True

class ScriptRunner():

    def __init__(self):

        self.Lock = threading.Lock()

        #### modules
        self.mqttClient=MQTT_CLIENT()


        # devices
        self.motors = HullOS.Motors()
        self.neopixels = HullOS.Pixelring()
        self.lidar = HullOS.DistanceSensor()
        self.sound = HullOS.Speaker()
        self.control=HullOS.Control() # not for user programs

        self.control.clear() # delete any embedded program so we have full control


        #############################################################
        self.script = None  # the current running script
        self._threadRunning=False
        ###############################################################
        #
        # globalVars & localVars are used by the python exec() function
        #
        # users programs can access the devices using the dict keys
        # like this
        # e.g. motors.move(dist,duration)

        self.globalVars = {# distance returns the distance of any object in front of
            # the bot or None (if out of range)
            "distance": self.lidar.distance,

            # sound control, obviously
            "speaker": self.sound,

            # motor control
            "motors": self.motors,

            # pixel ring control
            "neopixels": self.neopixels,


            # MQTT
            "mqtt": self.mqttClient,

            # Pixelbot name
            "myname": self.control.name(),
            
            # thread control
            "_threadExit":False
            
        }

        # provided for exec
        self.localVars = {}
        
        # start with the current script, if there is one
        #self.begin()

    def exitRunningThread(self):
        self.globalVars["_threadExit"]=True
        # _threadRunning is set to False when execScript terminates
        while self._threadRunning:
            time.sleep(0.1)
        
    def __del__(self):
        self.exitRunningThread()
        self.mqttClient.stop()
        print("Interpreter stopped")

    def stopScript(self):
        print("Running stopScript")
        self.exitRunningThread()
        return "Script stopped."

    def startScript(self, reload=False):
        # meant to be called from HttpServer to start a script running
        if reload:
            self.script = None  # force a reload when runScript() next runs
            status = "Script will reload from {STORED_SCRIPT}"
        else:
            status = "Script will start soon"

        print("starting the script")
        self.exitRunningThread()
        self.begin()



        return status

    def _wrapper(self,script):
        # parts needed to run a script

        forceExit=["if _exitThread:",PYTHON_INDENT+"raise ScriptExit"]
        
        wrapped = ["class ScriptExit(Exception):"]
        wrapped.append(PYTHON_INDENT+"pass")

        # add indentation
        insert_exit_before_next_line=False # set True if a when or for has been found
        for line in script:
          
            line=line.rstrip()
            b=reBlank.match(line)
            c=reComment.match(line)
            if b or c:
                continue
            else:
                # get the current line indent
               
                m=reIndent.match(line)
                if m:
                    indent=m.group(1)
                    line = indent+m.group(2)
                else:
                    indent=0
                    #line=PYTHON_INDENT+line
                    
                if insert_exit_before_next_line:
                     for l in forceExit:
                         wrapped.append(indent+l)
                     insert_exit_before_next_line=False
                
                wrapped.append(line)
                
                # check if line was a 'when' or 'for' loop
              
                m=reLoop.match(line)
                if m:
                    insert_exit_before_next_line=True

        # this starts the task after creating an entry execTask in locals{}
        # that allows us to cancel the task
        #wrapped.append("except Exception as e:") # required to be able to cancel
        #wrapped.append(PYTHON_INDENT+"print(f'script thread has stopped. Exception {e}')")

        script=""
       
        return "\n".join(wrapped)

    def loadScript(self):

        # for runScript() to use
        with self.Lock:
            try:
                with open(STORED_SCRIPT) as f:
                    script = f.readlines()
                    script = self._wrapper(script)
                # do we have a current script?
                if len(script) == 0:
                    print(f"{STORED_SCRIPT} was empty")
                    self.script = None
                else:
                    print(f"{STORED_SCRIPT} loaded ok")
                    self.script = script

            except Exception as e:
                print(f"Error wrapping {STORED_SCRIPT} : {e} ")
                self.script = None

    def storeScript(self, script):
        # does not affect the running script
        with open(STORED_SCRIPT, "w") as f:
            f.write(script)

    def getScript(self):
        # used by HttpServer when user downloads the current script
        with open(STORED_SCRIPT, "r") as f:
            return f.read()
        
    def storeScriptAndRun(self, script):
        # needs a button on the web page
        with open(STORED_SCRIPT, "w") as f:
            f.write(script)
        self.script = None # forces begin code to load and wrap it
        
        self.begin()

    def execScript(self):
        print("Interpreter runLoop starting\nscript=",self.script)
        
        #with open("Wrapped.py") as f:
        #    self.script=f.read()
        #    print("len wrapped=",len(self.script))
        #    return
        
        try:
            self._threadRunning=True
            exec(self.script, self.globalVars, self.localVars)  # only returns when script ends

        except Exception as e:
            print(f"EXEC Exception running script: {e}")

        self._threadRunning=False
        print("Interpreter execScript finished")

    def begin(self):
        #
        if self.script is None:
            self.loadScript()  # attempts to populate self.script

        if self.script is None:
            print("No script found")
            return
        print("interpreter begin")
        self.exitRunningThread()
        self.globalVars["_exitThread"]=False
        thread=threading.Thread(target=self.execScript(),args=())
        thread.start()

    # these are the bultin modules which the script can use
    # called in the script as myname(), distance() and delay(nn) - see self.globals above

    def _delay(self, duration):
        time.sleep(duration)

    def _distance(self):
        return self.ds.distance()

    def _myname(self):
        return PIXELBOT_NAME


if __name__ == "__main__":

    interp = ScriptRunner()

    try:

        #interp.begin() done by __init__

        while interp._threadRunning:
            pass

    except Exception as e:
        print(f"MAIN Exception {e}")

    finally:
       print("Finished")
