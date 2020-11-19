# -*- coding: utf-8 -*-
#!/usr/bin/python
# import RPi.GPIO as GPIO
import sys
# GPIO.setmode(GPIO.BCM)
# GPIO.setup(17, GPIO.OUT)
precision = 2
try:
    tFile = open('/sys/class/thermal/thermal_zone0/temp')
    temp = float(tFile.read())
    cpuFile = open('/sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq')
    cpu_freq = float(cpuFile.read())
    print('CPU Clock: ',"{:.{}f}".format(cpu_freq/1000,precision),'MHz')
    tempC = temp/1000
    if tempC > 43.5:
        # GPIO.output(17, 1)
        print('CPU Temp: ', "{:.{}f}".format(tempC, precision),str("\u00b0"),'Celsius')
        print('CPU is Warm')
        # GPIO.cleanup()
    else:
        # GPIO.output(17, 0)
        print('CPU Temp: ', "{:.{}f}".format(tempC, precision),str("\u00b0"),'Celsius')
        print('CPU is Cold')
        # GPIO.cleanup()
except:
    tFile.close()
    cpuFile.close()
    # GPIO.cleanup()
    sys.exit()