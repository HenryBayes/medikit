# -*- coding=utf-8 -*-
from msg import msg
md =  [u'阿莫西林', u'急支糖浆', u'抗生素']
m = msg(md, phone_num = "18829210221")

print("medicine list: " + ''.join(md))
print("phone number: " + m.receive_num)

m.write()
m.write_content()

