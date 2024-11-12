import serial
import time
from datetime import datetime, timedelta

ser = serial.Serial()
ser.baudrate = 115200
ser.port = "/dev/ttyACM0"

connection = False

while not connection:
    try:
        ser.open()
        print('Connected!')
        connection = True
    except:
        print('CONNECTION FAILED - RETRYING')
        time.sleep(5)


while True:
    with open('event.txt', 'r') as file:
        in_event = file.readline()
    out_event = datetime.fromisoformat(in_event)

    date = datetime.now()
    next_day = (date + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    time_until_next_day = (next_day - date).total_seconds()
    time_until = out_event - date
    seconds_until = time_until.total_seconds()
    minutes_until = int(seconds_until // 60) + 1
    hours_until = int(minutes_until // 60) + 1
    days_until = int(hours_until // 24) + 1
    iseconds_until = int(seconds_until)
    if days_until > 1:
        print(str(days_until), "days")
        ser.write("D".encode() + str(days_until).encode())
        time.sleep(3)
    elif hours_until > 1:
        print(str(hours_until), "hours")
        ser.write("H".encode() + str(hours_until).encode())
        time.sleep(1)
    elif minutes_until > 1:
        print(str(minutes_until), "minutes")
        ser.write("M".encode() + str(minutes_until).encode())
        time.sleep(1)
    elif iseconds_until > 0:
        print(str(iseconds_until), "seconds")
        ser.write("S".encode() + str(iseconds_until).encode())
        time.sleep(1)
    else:
        ser.write('DDD'.encode())
        time.sleep(5)
