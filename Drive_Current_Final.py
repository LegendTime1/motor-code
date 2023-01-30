import motorclient
import motorclient2
import current_sensor
import keyboard
import time
turn = 100
m = 0
n = 0
mnew = 0
nnew = 0

def speedIncrement(m, n, mnew, nnew):
    if(m < 256 and m > -256):
        if(n < 256 and n > -256):
                m += mnew
                n += nnew
        elif(n >= 256):
                m += mnew
                n = 255
        else:
                m += mnew
                n = -255
    elif(m >= 256):
        if(n < 256 and n > -256):
                m = 255
                n += nnew
        elif(n >= 256):
                m = 255
                n = 255
        else:
                m = 255
                n = -255
    else:
        if(n < 256 and n > -256):
                m = -255
                n += nnew
        elif(n >= 256):
                m = -255
                n = 255
        else:
                m = -255
                n = -255
    motorclient.motor(int(m), int(n))
    motorclient2.motor(int(n), int(m))
    print(str(m)+" "+str(n))
    return(m, n)


def w_Pressed():
    global m
    global n
    mnew = 5
    nnew = 5
    m,n = speedIncrement(m,n,mnew,nnew)
    #if (linearAccelerator < 5):

def a_Pressed():
   global m
   global n
   mnew = -turn-m
   nnew = turn-n
   m,n = speedIncrement(m,n,mnew,nnew)
   while (m!=0 and n!=0):
    f_Pressed() 
    time.sleep(0.1) 


def s_Pressed(): 
    global m
    global n
    mnew = -5
    nnew = -5
    m,n = speedIncrement(m,n,mnew,nnew)


def d_Pressed():
    global m
    global n
    mnew = turn-m
    nnew = -turn-n
    m,n = speedIncrement(m,n,mnew,nnew)
    while (m!=0 and n!=0):
        f_Pressed() 
        time.sleep(0.1)


def f_Pressed():
    global m
    global n
    mnew = 0
    nnew = 0
    m = m//2
    n = n//2
    m,n = speedIncrement(m,n,mnew,nnew)


while True:
    current_value = current_sensor.server()
    print(current_value)
    if current_value < 25 :
        #while (arrowIsPresent != 1):
        #    w_Pressed()
        #w_Pressed() untill depth 1m
        #if (directionOfArrow == "Left"):
            w_Pressed()
            #s_Pressed()
            #d_Pressed()
            #a_Pressed()

        #print(1)
        '''if keyboard.is_pressed("w"):
            w_Pressed()
        elif keyboard.is_pressed("a"):
            a_Pressed()
        elif keyboard.is_pressed("s"):
            s_Pressed()
        elif keyboard.is_pressed('d'):
            d_Pressed()
        elif keyboard.is_pressed("f"):
            f_Pressed()
        else :
            #print("h")
            mnew = 0
            nnew = 0
            m,n = speedIncrement(m,n,mnew,nnew)
        if keyboard.is_pressed("l"):
            turn +=5
            print("New turning speed : "+str(turn))
        elif keyboard.is_pressed("k"):
            turn-=5
            print("New turning speed : "+str(turn))
        elif keyboard.is_pressed("r"):
            turn = 100
            print("Turn speed reset to : "+str(turn))
        time.sleep(0.25)
    


    '''
    else :
        mnew = -m
        nnew = -n
        m,n = speedIncrement(m,n,mnew,nnew)
        print("Current Limit breached, motor set to standstill.")
   





