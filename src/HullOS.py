#import logging

from Config import PIXELBOT_NAME
from SerialHandler import Handler
import time
# NOTE: The pixelbot expetcs durations in 10ths of a second
# hence the x10 multiplier

#
#log=logging.getLogger("HullOS")
#log.setLevel(logging.DEBUG)

comms=Handler()

botFound=comms.hasPixelbot()
    
print(f"HullOS: Pixelbot found: {botFound}")
    

DEF_DURATION_MULTIPLIER=1000 # convert seconds to Pixelbot values
MOTOR_SETTLE=0.1


def unexpectedReply(cmd,reply):
    print("Got unexpected reply {reply} to {cmd}")
    return False

def failed(cmd):
    print("{cmd} failed")
    return False

class Motors:
    
    def __init__(self):
        pass

    def move(self,dist=0,duration=0):
        # returns True if command is ok, False otherwise
        if duration==0:
            comms.tx(f"*MF{dist}")
        else:
            comms.tx(f"*MF{dist},{duration*DEF_DURATION_MULTIPLIER}")
        reply=comms.rx()
        if reply=="*MFFail":
            return failed("Motor move")
        elif reply=="MFOK":
            return True
        else:
            return unexpectedReply("motor move",reply)

    def rotate(self,angle=0,duration=0):
        if duration==0:
            comms.tx(f"*MR{angle}")
        else:
            comms.tx(f"*MR{angle},{duration*DEF_DURATION_MULTIPLIER}")
        reply=comms.rx()
        if reply=="*MRFail":
            return failed("Motor rotate")
        elif reply=="MROK":
            return True
        else:
            return unexectedReply("motor rotate",reply)


    def arc(self,radius=0,angle=0,duration=0):
        if duration==0:
            comms.tx(f"*MA{radius},{angle}")
        else:
            comms.tx(f"*MA{radius},{angle},{duration*DEF_DURATION_MULTIPLIER}")
        reply=comms.rx()
        if reply=="MAFail":
            return failed("Motor arc")
        elif reply=="MAOK":
            return True
        else:
            return unexpectedReply("motor arc",reply)
        
    def moveMotors(self,left=0,right=0,duration=0):
        # specify different distances for each motor
        if duration==0:
            comms.tx(f"*MM{left},{right}")
        else:
            comms.tx(f"*MM{left},{right},{duration*DEF_DURATION_MULTIPLIER}")
        reply = comms.rx()
        if reply == "MMFail":
            return fail("move motors")
        elif reply == "MMOK":
            return True
        else:
            return unexepctedReply("move motors",reply)
        
    def areMoving(self):
        comms.tx("*MC")
        reply=comms.rx()
        if reply=="MCOK":
            reply=comms.rx()
        if reply=="MCMove":
            return True
        elif reply=="MCstopped":
            return False
        else:
            return unexpectedReply("MC",reply)

    def stop(self):
        comms.tx("*MS")
        reply=comms.rx()
        if reply=="MSOK":
            return True
        elif reply=="MSFAIL":
            return failed("MS")
        else:
            return unexpectedReply("MS",reply)
        
    def setWheelConfig(self,left=69,right=69,spacing=110):
        comms.tx(f"*MW{left},{right},{spacing}")
        reply=comms.rx()
        if reply=="MWOK":
            return True
        elif reply=="MWFAIL":
            return failed("MW")
        else:
            return unexpectedReply("MW",reply)

    def getWheelConfig(self):
        comms.tx(f"*MV")
        reply=comms.rx()
        if reply=="MVOK":
            reply=comms.rx()
            while reply is not None:
                print(reply)
            return True
        elif reply=="MVFAIL":
            return failed("MV")
        else:
            return unexpectedReply("MV",reply)
        
class Pixelring:
    def __init__(self):
        pass

    def colourCandle(self,colour=(0,0,0)):
        # colour can be a single letter or an rgb tuple
        if type(colour) is tuple:
            # expecting rgb
            r,g,b=colour
            comms.tx(f"*PC{r},{g},{b}")
            reply = comms.rx()
            if reply is None or reply=="PCOK":
                return True
            elif reply=="PCFAIL":
                return failed("PC")
            else:
                return unexpectedReply(reply)

        # colour is a single letter
        colour=colour.upper()
        if colour not in ["R","G","B","Y","M","C","W","K"]:
            raise Exception("Invalid colour letter {colour}")
        comms.tx(f"*PN{colour}")
        reply=comms.rx()
        if reply is None or reply=="PNOK":
            return True
        elif reply=="PNFAIL":
            return failed("PN")
        else:
            return unexpectedReply("PN",reply)

    def off(self):
        comms.tx("*PO")
        reply=comms.rx()
        if reply is None or reply=="POOK":
            return True
        elif reply=="POFAIL":
            return failed("PO")
        else:
            return unexpectedReply("PO",reply)

    def flicker(self,speed=1):
        if speed<1 or speed>20:
            print("Flicker speed must be in the range 1-20")
            return False
        
        comms.tx(f"*PF{speed}")
        reply=comms.rx()
        if reply is None or reply=="PFOK":
            return True
        elif reply=="PFFAIL":
            return failed("PF")
        else:
            return unexpectedReply("PF",reply)


    def setPixel(self,index=0,rgb=(0,0,0)):
        r,g,b=rgb
        comms.tx(f"*PI{index},{r},{g},{b}")
        reply=comms.rx()
        if reply is None or reply=="PIOK":
            return True
        elif reply=="PIFAIL":
            return failed("PI")
        else:
            return unexpectedReply("PI",reply)

    def crossfade(self,speed=1,rgb=(0,0,0)):
        if speed<1 or speed>20:
            print("crossfade speed must be in range 1..20")
            return False
        
        if type(rgb) is tuple:
            r,g,b=rgb
            comms.tx(f"*PX{speed},{r},{g},{b}")
            reply=comms.rx()
            if reply is None or reply=="PXOK":
                return True
            elif reply=="PXFAIL":
                return failed("PX")
            else:
                return unexpectedReply("PX",reply)
        else:
            print("Expected an RGB tuple for crossfade target colour")
            return False

    def animate(self,enable=True):
        if enable:
            cmd="PA"
        else:
            cmd="PS"
            
        comms.tx("*"+cmd)
        reply=comms.rx()
        if reply is None or reply[2:]=="OK":
            return True
        elif reply[2:]=="FAIL":
            return failed(cmd)
        else:
            return unexpectedReply(cmd,reply)       

    def random(self):
        comms.tx("*PR")
        reply=comms.rx()
        if reply is None or reply=="PROK":
            return True
        elif reply=="PRFAIL":
            return failed("PR")
        else:
            return unexpectedReply("PR",reply) 

class DistanceSensor:
    def __init__(self):
        self.maxRange=1000

    def distance(self):
        
        dist=self.maxRange # out of range
                
        comms.tx("*ID")
        reply=comms.rx()
        
        if reply is None or reply=="IDFAIL":
            print("Distance sensor not responding.")
            return self.maxRange

        if reply=="IDOK":
            reply=comms.rx()
             
            # the reply might not be a number
            try:
                return int(reply)
            except:
                print (f"distance sensor reply was not a number. Got {reply}")
                return self.maxRange
    
        print("Unexpected reply to ID. Got {reply}")
        return self.maxRange
    
class Speaker:
    def __init__(self):
        pass
    
    def delay(self,seconds):
        # non-blocking
        start=time.monotonic()
        while (time.monotonic()-start)<seconds:
            pass

    def play(self,freq=0,duration=0,pauseAfter=0,wait=True):
        print(F"PLAY {freq} {duration} {pauseAfter} {wait}")
        wait="W" if wait else "N"
        comms.tx(f"*ST{int(freq)},{int(duration*DEF_DURATION_MULTIPLIER)},{wait}")
        reply=comms.rx()
        if reply is None or reply=="SOUNDOK":
            # wait for note duration
            self.delay(duration)
            if pauseAfter:
                self.delay(pauseAfter)
        else:
            print(f"Unexpected response to play sound {reply}")
            self.delay(duration)
            if pauseAfter:
                self.delay(pauseAfter)

class Control:
    def __init__(self):
        pass

    def stop(self):
        # halts the embedded program so that it doesn't interfere
        # with python scripts
        #comms.tx("*RH") - this stops the motors running
        pass
        
    def isConnected(self):
        # are we connected to the Pixelbot?
        comms.tx("*IV")
        reply=comms.rx()
        if reply=="IVOK":
            reply=comms.rx() # this should be HULLOS
            # any reply at all means we are connected
            return True
        
        # any other response could be from some other machine
        print("Pixelbot is not responding. Got {reply}")
        return False

    def pixelbotName(self):
        return PIXELBOT_NAME
    
    def name(self):
        return PIXELBOT_NAME
    
    def clear(self):
        # clear any embedded program
        comms.tx("*RC")

    def status(self):
        comms.tx("*IS") # get status
        reply=comms.rx()
        if reply is None:
            return "Timeout fetching status"
        else:
            states=["PROGRAM STOPPED","PROGRAM PAUSED","PROGRAM ACTIVE","PROGRAM AWAITING MOVE COMPLETION","PROGRAM AWAITING DELAY COMPLETION","SYSTEM CONFIGURATION CONNECTION" ]
            return states[int(reply)]

    def setMessagingLevel(self,level=0):
        comms.tx(f"*IM{level}")
