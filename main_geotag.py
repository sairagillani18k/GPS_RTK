
import serial
import pynmea2
import piexif
from geopy.geocoders import Nominatim
from depthai_sdk import OakCamera
import cv2
import numpy as np
# Serial port settings for ZED-F9P
port = 'COM8'  # Replace with the appropriate serial port of your ZED-F9P module
baudrate = 9600  # Replace with the baud rate of your ZED-F9P module
ser = serial.Serial(port, baudrate)
# Geocoding settings
geolocator = Nominatim(user_agent="GetLoc")
# OAK-D Lite camera setup
with OakCamera() as oak:
    color = oak.create_camera('color')
    def cb(packet):
        frame = packet.frame
        # Save the frame as a JPG file
        cv2.imwrite("frame.jpg", frame)
        # Read GPS data from ZED-F9P
        line = ser.readline().decode('utf-8', errors='ignore').strip()
        try:
            msg = pynmea2.parse(line)
        except pynmea2.ParseError:
            return
        if isinstance(msg, pynmea2.GGA):
            latitude = msg.latitude
            longitude = msg.longitude
            # Reverse geocode to get address
            location = geolocator.reverse(f"{latitude}, {longitude}")
            address = location.address
            # Convert latitude and longitude to the required format
            latitude_deg = int(abs(latitude))
            latitude_min = int((abs(latitude) - latitude_deg) * 60)
            latitude_sec = round(((abs(latitude) - latitude_deg) * 60 - latitude_min) * 60, 2)
            latitude_ref = 'N' if latitude >= 0 else 'S'
            longitude_deg = int(abs(longitude))
            longitude_min = int((abs(longitude) - longitude_deg) * 60)
            longitude_sec = round(((abs(longitude) - longitude_deg) * 60 - longitude_min) * 60, 2)
            longitude_ref = 'E' if longitude >= 0 else 'W'
            # Geotag the image frame
            exif_data = piexif.load("frame.jpg", "jpeg")  # Load the frame as a JPG file
            exif_data['0th'][piexif.ImageIFD.ImageDescription] = address.encode('utf-8')
            exif_data['GPS'][piexif.GPSIFD.GPSLatitudeRef] = latitude_ref
            exif_data['GPS'][piexif.GPSIFD.GPSLatitude] = ((latitude_deg, 1), (latitude_min, 1), (int(latitude_sec * 100), 100))
            exif_data['GPS'][piexif.GPSIFD.GPSLongitudeRef] = longitude_ref
            exif_data['GPS'][piexif.GPSIFD.GPSLongitude] = ((longitude_deg, 1), (longitude_min, 1), (int(longitude_sec * 100), 100))
            exif_bytes = piexif.dump(exif_data)
            # Save the geotagged image
            output_path = 'geotagged_image.jpg'  # Replace with the desired path for the geotagged image
            piexif.insert(exif_bytes, "frame.jpg", output_path)  # Specify the input file as "frame.jpg"
        cv2.imshow('Real-Time Feed', frame)
    # Display the real-time feed with geotagging
    oak.visualize(color, callback=cb)
    oak.start(blocking=True)  # This call will block until the app is stopped (by pressing 'Q' button)
# Close the serial port when done
ser.close()