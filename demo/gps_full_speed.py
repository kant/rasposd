import serial

#####Global Variables######################################
#be sure to declare the variable as 'global var' in the fxn
ser = 0

#####FUNCTIONS#############################################
#initialize serial connection 
def init_serial(baud):
    global ser #must be declared in each fxn used
    ser = serial.Serial()
    ser.baudrate = baud
    ser.port = '/dev/ttyAMA0' 

    #you must specify a timeout (in seconds) so that the
    # serial port doesn't hang
    ser.timeout = 1
    ser.open() #open the serial port

    # print port open or closed
    if ser.isOpen():
        print 'Open: ' + ser.portstr

#####SETUP################################################
#this is a good spot to run your initializations 
init_serial(9600)
#prints what is sent in on the serial port
print("set gps speed to 115200")
ser.write("$PMTK251,115200*1F\r\n") #write to the serial port
ser.close()
init_serial(115200)
print("set gps to 10Hz")
ser.write("$PMTK220,100*2F\r\n") #write to the serial port
bytes = ser.readline() # check aknowledge

#while 1:
    #bytes = ser.readline() #reads in bytes followed by a newline 
    #print 'You received: ' + bytes #print to the console
    # break #jump out of loop 
#hit ctr-c to close python window
