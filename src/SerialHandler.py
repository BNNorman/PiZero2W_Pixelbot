# queues outgoing commands to the Pixelbot
import serial


DEBUG=False # used for testing messages that would be sent to the bot (which isn't attached)

if DEBUG:
    import logging

    logging.basicConfig(filename="SerialHandler.log",level=logging.DEBUG)
    logging.getLogger('parso.python').disabled=True
    logging.getLogger('parso.python.diff').disabled=True
    logging.getLogger('parso.cache').disabled=True
    logging.getLogger('parso.cache.pickle').disabled=True


TERMINATOR="\r" # 0x0D

class Handler:

    def __init__(self):
        self.ser=serial.Serial("/dev/serial0", baudrate=115200,timeout=1)

        # check that a pixelbot is connected and
        # serial comms works
        self._hasPixelbot=False
        
        if self._isConnected():
            self._hasPixelbot=True
        else:
            msg="SerialHandler - no Pixelbot found"
            logging.warning(msg)
            raise Exception(msg)

    def __del__(self):
        self.ser.close()
        
    def _isConnected(self):
        logging.info("Querying Pixelbot to find out if it is connected")
        self.tx("*IV")
        reply=self.rx() # confirmation expected
        if reply=="IVOK":
            reply=self.rx() # version string expected
            
        if reply is not None and reply[:6]=="HullOS":
                self.tx("*IM1") # enable command responses
                reply=self.rx()
                print(f"Messages enabled {reply}")
                return True
        return False        
        

    def tx(self,cmd):
        if self.ser.in_waiting: # flush out unexpected stuff
            self.rx()
        if DEBUG:
            logging.debug(f"tx {cmd}")
            print(f"tx {cmd}")
        # cmd is a string. We need to add a CR for pixelbot
        data=cmd+TERMINATOR
        dataBytes=bytearray(data.encode())
        
        if self.ser.write(dataBytes)!=len(dataBytes):
            print("did not write all the data")
        self.ser.flush() # wait till all chars have been sent
        
    def rx(self):
        
        line=self.ser.readline()

        if line is None:
            print("No serial input")
            return None

        line=line.rstrip()
        
        if DEBUG:
            logging.debug(f"rx {line}")
            print(f"rx {line}")
                
        try:
            return line.decode()
        except UnicodeError:
            return line
        
    def listen(self):
        # not used
        # used to soak up any delay in the pixelbot responding (ugh)
        print("listening")
        while not self.ser.in_waiting:
            pass
        return self.rx()

    def hasPixelbot(self):
        return self._hasPixelbot
    



if __name__=="__main__":
    import time
    comms=Handler()
    
    def send(cmd):
        print("=>",cmd)
        comms.tx(cmd)
        reply=comms.rx() # waits for uart.any() then reads
        if reply is not None:
            print("<=",reply)
        
    # flush any left over rubbish from input
    
    if comms.ser.in_waiting():
        dross=comms.rx()
    
    send("*RC")
    send("MF1000") 
    
    count=0
    try:
        while True:
            print(f"\nPass {count}")
            count+=1
            send("*IV") # delayed response
            send("*ID") # delayed response if any
            colour=colours[idx]
            idx=(idx+1)%len(colours)
            send(f"*PN{colour}") # works
            time.sleep(5)
    
    
    except:
        send("*PO")
    
    
