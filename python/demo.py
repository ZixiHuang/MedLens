# Imports the Google Cloud client library
import io, os
from numpy import random
import numpy as np
from google.cloud import vision
import pandas as pd
import cv2
import object_tracking as ot
import ocr


if __name__ == '__main__':

    # localize_objects( "/Users/joanna/Desktop/hophacks/drug.jpeg")

    client = vision.ImageAnnotatorClient()

    # define a video capture object
    vid = cv2.VideoCapture(0)

    count = 0
    objects = None

    while(True):
      
        ret, frame = vid.read()
        frame = cv2.flip(frame, 1)
        
    
        if (count % 5 == 0):
            detection_scale_factor = 0.5  # for example, reduce resolution to half
            resized_frame = cv2.resize(frame, (0, 0), fx=detection_scale_factor, fy=detection_scale_factor)

            objects, img_width, img_height = ot.object_tracking(resized_frame, client)
            img_height /= detection_scale_factor
            img_width /= detection_scale_factor
            # filter drug objects
            drug_object = []
            for object_ in objects:
                if object_.score < 0.6:
                    continue
                if object_.name != 'Packaged goods':
                    continue

                drug_object.append(object_)
                break

            text, details = ocr.get_ocr_result(client, frame, drug_object, img_width, img_height)
            print(details) if len(details) > 0 else None
            

            count = 0

        if objects:
            annot_frame = ot.draw_bbox(frame, drug_object, img_width, img_height)
        else:
            annot_frame = frame

        cv2.imshow('Video', annot_frame)
        key = cv2.waitKey(1)

        if key == ord('q'):
            break

        count += 1
  
    # After the loop release the cap object
    vid.release()
    # Destroy all the windows
    cv2.destroyAllWindows()