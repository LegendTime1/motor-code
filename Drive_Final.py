import motorclient
import motorclient2
import current_sensor
import keyboard
import time

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
    #motorclient.motor(int(m), int(n))
    #motorclient2.motor(int(n), int(m))
    print(str(m)+" "+str(n))
    return(m, n)


def w_Pressed():
    global m
    global n
    mnew = 5
    nnew = 5
    m,n = speedIncrement(m,n,mnew,nnew)

def a_Pressed():
   global m
   global n

#    while (m!=0 and n!=0):
#     f_Pressed()
#     time.sleep(0.1)

   while (keyboard.is_pressed("a")):
    mnew = 250-m
    nnew = -70-n
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

       

    while (keyboard.is_pressed("d")):
        mnew = -70-m
        nnew = 250-n
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

    if keyboard.is_pressed("w"):
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
        mnew = 0
        nnew = 0
        m,n = speedIncrement(m,n,mnew,nnew)
    # keyboard.on_press_key("a", lambda _:a_Pressed())
    # keyboard.on_press_key("s", lambda _:s_Pressed())
    # keyboard.on_press_key("d", lambda _:d_Pressed())
    # keyboard.on_press_key("f", lambda _:f_Pressed())
    #print(1)
    current_sensor.sensor()
    time.sleep(0.25)