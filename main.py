import serial
import pynmea2
port = 'COM8'  # Replace with the appropriate serial port of your ZED-F9P module
baudrate = 9600  # Replace with the baud rate of your ZED-F9P module
ser = serial.Serial(port, baudrate)
while True:
    line = ser.readline().decode('utf-8').strip()
    try:
        msg = pynmea2.parse(line)
    except pynmea2.ParseError:
        continue
    if isinstance(msg, pynmea2.GGA):
        latitude = msg.latitude
        longitude = msg.longitude
        altitude = msg.altitude 
        print('Latitude:', latitude)
        print('Longitude:', longitude)
        print('altitude:', altitude)
# Close the serial port when done
ser.close()