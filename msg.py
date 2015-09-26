# -*- coding: utf-8 -*-
"""
This module use m660 to send msg to the phone number which is given.
It needs a medicine list to fill the content of the msg.
"""
import serial
import time
class msg:
    def __init__(self, medicine, phone_num = '18710895799'):
        self.send_seq = 1
        self.receive_num = phone_num
        self.command_dic = {'1':'AT','2':'AT+CCID','3':'AT+CSQ','4':'AT+CREG?','5':'AT+CMGF=0', '6':'AT+CSCS="UCS2"','7':'AT+CMGS='}
#        self.ser = serial.Serial('/dev/tty.usbserial', 115200,timeout=0.2)
        self.ser = serial.Serial('/dev/ttyAMA0', 115200, timeout=0.2)
        self.mdlist = medicine
        self.content = self.get_content(self.mdlist)
        self.send_string = '0001000BA1'+self.convert_phone_num(self.receive_num)+'0008'+self.dec2hex(len(self.content)/2)+self.content


    """
    Turn the decimal number into a two-upper-letter hexadecimal number
    """
    def dec2hex(self, num):
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

    def convert_phone_num(self, num):
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
    #   print num
            

    """
    turn unicode characters into unicode number
    """
    def content2unicode(self, unistring):
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
    def get_content(self, medicine):
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
    #   print content
        uni_content = self.content2unicode(content)
    #   print uni_content
        return uni_content

    """
    get the reply and find out whether there are some errors
    """
    def read(self):
        cmd = self.ser.readline()
        ret = self.ser.readall()[-4:]
        print(self.send_seq)
        if ret == 'OK\r\n':
            self.send_seq = self.send_seq + 1
            self.write()
        else:
            print("Command:"+self.command_dic['%d'%self.send_seq]+" error!")

    """
    send commands to the m660
    """
    def write(self):
        if self.send_seq >=1 and self.send_seq <= 6:
            self.ser.write(self.command_dic['%d'%self.send_seq]+'\r')
            self.read()
            time.sleep(0.2)
        elif self.send_seq == 7:
            command = self.command_dic['%d'%self.send_seq]+str((len(self.send_string)-2)/2)
            #print command
            self.ser.write(command+'\r')
            time.sleep(0.5)
        else:
            pass

    def write_content(self):
        print("medicine list: " + ''.join(self.mdlist))
        #print("phone number: " + self.receive_num)
        if self.send_seq == 7:
            self.ser.write(self.send_string + chr(0x1A))
            print('sent')
            time.sleep(8)
            ret = self.ser.readall()[-4:]
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
#medicine = [u'阿莫西林', u'急支糖浆', u'抗生素']
#get_content(medicine)
#init_msg(medicine)
#print send_string
