# -*- coding: utf-8 -*-
import serial
import time

def init_msg(medicine, phone_num = '18710895799'):
    global send_seq 
    global command_dic
    global ser
    global send_string

    send_seq = 1
    command_dic = {'1':'AT','2':'AT+CCID','3':'AT+CSQ','4':'AT+CREG?','5':'AT+CMGF=0', '6':'AT+CSCS="UCS2"','7':'AT+CMGS=21'}
#    ser = serial.Serial('/dev/tty.usbserial', 115200,timeout=0.2)

    content = get_content(medicine)
    send_string = '0001000BA1'+convert_phone_num(phone_num)+'0008'+dec2hex(len(content)/2)+content


"""
Turn the decimal number into a two-upper-letter hexadecimal number
"""
def dec2hex(num):
    hex_num = hex(num)
    form_num = str(hex_num)[2:]
    if len(form_num) == 1:
        form_num = list(form_num)
        tmp = form_num[0]
        form_num[0] = '0'
        form_num.append(tmp)
        form_num = ''.join(form_num)
    form_num = form_num.upper()
    return form_num


def convert_phone_num(num):
    if len(num)%2 == 1:
        num = num + 'F'
    else:
        pass
    num_len = len(num)
    num = list(num)
    for n in range(0, num_len):
        if n % 2 == 0:
            tmp = num[n+1]
            num[n+1] = num[n]
            num[n] = tmp
        else:
            pass
    return ''.join(num)
#    print num
            

"""
turn unicode characters into unicode number
"""
def content2unicode(unistring):
    content = ""
    for ch in unistring:
        num = ord(ch)
        hex_num = str(hex(num))[2:]
        if not len(hex_num) == 4:
            zeros = '0'*(4-len(hex_num))
            content = content + ''.join([zeros, hex_num])
        else:
            content = content + hex_num
    content = content.upper()
    return content


"""
content:
    2015-xx-xx xx:xx
    XX药品被取出，您可以选择立即回电
"""
def get_content(medicine):
    #turn the medicine name into unicode number, separated by ','
    med_content = ""
    for m in medicine:
        med_content = med_content + m + u','
    med_content = list(med_content)
    med_content.pop()
    med_content = ''.join(med_content)
        
    #get the current time
    t = time.ctime().split(' ')
    cur_time_year = t.pop()
    cur_time_clock = t.pop()
    cur_time_date = t.pop()
    cur_time_month = t[1]
    month_dic = {'Jan':1, 'Feb':2, 'Mar':3, 'Apr':4, 'May':5, 'Jun':6, 'Jul':7, 'Aug':8, 'Sep':9, 'Oct':10, 'Nov':11, 'Dec':12}
    cur_time = cur_time_year + '-' + str(month_dic[cur_time_month]) + cur_time_date + ' ' + cur_time_clock + '\n'
    
    other_string = u"药品被取出，您可以选择立即回电"
    
    content = cur_time + med_content + other_string
#    print content
    uni_content = content2unicode(content)
#    print uni_content
    return uni_content

"""
get the reply and find out whether there are some errors
"""
def read():
    global ser
    global send_seq
    cmd = ser.readline()
    ret = ser.readall()[-4:]
    print(send_seq)
    if ret == 'OK\r\n':
        send_seq = send_seq + 1
        write()
    else:
        print("Command:"+dic['%d'%send_seq]+" error!")

"""
send commands to the m660
"""
def write():
    global ser
    global send_seq
    global command_dic
    if send_seq >=1 and send_seq <= 6:
        ser.write(dic['%d'%send_seq]+'\r')
        read()
        time.sleep(0.2)
    elif send_seq == 7:
        ser.write(dic['%d'%send_seq]+'\r')
        time.sleep(0.5)
    else:
        pass

def write_content():
    global ser
    global send_seq
    global send_string
    if send_seq == 7:
        ser.write(send_string + chr(0x1A))
        print('sent')
        time.sleep(5)
        ret = ser.readall()[-4:]
        if ret == 'OK\r\n':
            print('Send Successfully!')
        else:
            print('Failed to Send!')
    else:
        pass


#write()
#time.sleep(1)
#write_content()

#convert_phone_num('18710895799')
#print dec2hex(22)
#t = time.ctime().split(' ')
#for st in t:
#    print(content2unicode(st)),
medicine = [u'阿莫西林', u'急支糖浆', u'抗生素']
#get_content(medicine)
init_msg(medicine)
print send_string
