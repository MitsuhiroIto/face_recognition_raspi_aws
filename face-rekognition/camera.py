import cv2
import time
import datetime
import boto3
import os

resource_s3 = boto3.resource('s3')
cap = cv2.VideoCapture(0)
while True:
    d = datetime.datetime.today()
    now = d.strftime("%Y_%m_%d_%H_%M_%S")
    ret, frame = cap.read()
    image_url =  'image/' + now + ".jpg"
    cv2.imwrite(image_url, frame)
    resource_s3.Bucket('mitsu-face-rekognition').upload_file(image_url, image_url)
    time.sleep(10)
    os.remove(image_url)
