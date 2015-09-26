#-*- coding=utf-8 -*-
import serial
import time
from msg import msg
from medicine import medicine
import RPi.GPIO as GPIO

"""
GPIO LIST:
11 ------- motor ------- OUT
12 ------- LED_LOCK  ------- IN
13 ------- LED_CHECK1 ------- IN
15 ------- touch ------- IN
"""
"""
Init the IO
"""
def IO_init():
    global p
    global have_motor_inited
    #flag that marks whether the motor has been inited
    have_motor_inited = False
    GPIO.setmode(GPIO.BOARD)
    #motor
    GPIO.setup(11, GPIO.OUT)
    #LED which detects whether the box is open
    GPIO.setup(12, GPIO.IN)
    #LED which detects whether specific medicine is moved
    GPIO.setup(13, GPIO.IN)
    #touch sensor
    GPIO.setup(15, GPIO.IN)
    #set PWN output of GPIO
    p =  GPIO.PWM(11, 50)

"""
Check if someone touches the touch sensor.
If touched, the sensor takes on high voltage
not the other way.
"""
def touched():
    if GPIO.input(15) == GPIO.HIGH:
        print "touched!"
        print "goto trytoopen()"
        return True
    else:
        return False

"""
Angle ranges from 0 to 180 degree,
corresponding with pwm ranging from 2.5 to 12.5
pwm = 2.5 -------- close
pwm = 12.5 ------- open
"""
def motor_move(pwm):
    global have_motor_inited
    global p
    print "pwm =", pwm
    if have_motor_inited == False:
        p.start(pwm)
        have_motor_inited = True
    else:
        p.ChangeDutyCycle(pwm)
    time.sleep(0.4)

"""
Send the list moved_md to the given phone number by message
"""
def sendmsg():
    global moved_md
    #create a class of msg
    m = msg(moved_md, phone_num="13991219316")
    print("medicine list:" + ','.join(moved_md))
    print("phone number:" + m.receive_num)
    #set the GSM module
    m.write()
    #write message content in chinese
    m.write_content()


"""
Return HIGH signal when there is nothing before it,
otherwise, return LOW signal.
Seq tells the func which led to check.
"""
def checkled(seq):
    dic = {}
    for n in seq:
        dic[n] = GPIO.input(n)
    return dic

"""
This function describes the  state that the box is opened and 
someone are pretending to pick out some medicine.
This function will check all the LEDs that monitor medicine and
push all moved medicine into a list called moved_md.
When the LED beside the motor finds out that the box is closed,
it will goto the function "trytoclose".
"""
def when_opened():
    print "in when_open()"
    global led_seq
    global mdlist
    global moved_md
    while(GPIO.input(12) == 1):
        dic = checkled(led_seq)
        for led in dic:
            if dic[led] == GPIO.HIGH:
                for md in mdlist:
                    if md.name in moved_md:
                        pass    
                    elif md.led_num == led:
                        moved_md.append(md.name)
            else:
                pass
    if GPIO.input(12) == 0:
        trytoclose()
    
"""
This function describes the state that the box is closed
"""
def when_closed():
    print "in when_close()"
#    global moved_md
    motor_move(2.5)
    time.sleep(1)
#    print moved_md

"""
This function describes the standby state, and any touch on
the touch sensor will activate the medikit.
"""
def trytoopen():
    print "in trytoopen()"
    if touched():
        n = 50
        motor_move(12.5)
        while(GPIO.input(12) == 0 and n > 0):
            time.sleep(0.1)
            n = n - 1
        if n == 0:
            when_closed()
        else:
            when_opened()
    else:
        when_closed()

"""
This function describes the state that when you finished
his operation, and closed the box, the motor would wait 
for a few seconds rather than lock the box right now because 
you might forget something.
"""
def trytoclose():
    print "in trytoclose()"
    n = 40
    while(GPIO.input(12) == 0 and n > 0):
        time.sleep(0.1)
        n = n - 1
    if n == 0:
        sendmsg()
        print moved_md
        when_closed()
    else:
        when_opened()


if __name__ == "__main__":
    try:
        IO_init()
        led_seq = [13]
        mdlist = [medicine(led_seq[0], u'阿莫西林')]
        moved_md = []
        while True:
            trytoopen()

    except KeyboardInterrupt:
        pass

    p.stop()
    GPIO.cleanup()
    

