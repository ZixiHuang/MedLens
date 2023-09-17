import io, os
import cv2
import numpy as np
from google.cloud import vision
from . import object_tracking as ot
from . import ocr
import asyncio
from concurrent.futures import ThreadPoolExecutor
from . import openaiAPI as openai

async def async_object_detection(client, frame):
    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor() as pool:
        objects, img_width, img_height = await loop.run_in_executor(pool, ot.object_tracking, frame, client)
    return objects, img_width, img_height

async def async_ocr(client, drug_objects, img_width, img_height):
    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor() as pool:
        results = await asyncio.gather(
            *[loop.run_in_executor(pool, ocr.get_ocr_result, client, objs, img_width, img_height, True) for objs in drug_objects]
        )
    return results

def is_valid_bbox(object):
    vertices = object.bounding_poly.normalized_vertices
    width = abs(vertices[1].x - vertices[0].x)
    height = abs(vertices[2].y - vertices[0].y)
    return width > 0.1 and height > 0.1

def analyze_img():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    client = vision.ImageAnnotatorClient()
    vid = cv2.VideoCapture(0)

    count = 0
    objects = None
    accumulated_objects = []

    loop = asyncio.get_event_loop()

    detection_scale_factor = 0.5  # for example, reduce resolution to half

    while(True):
        ret, frame = vid.read()
        frame = cv2.flip(frame, 1)

        if (count % 2 == 0):
            resized_frame = cv2.resize(frame, (0, 0), fx=detection_scale_factor, fy=detection_scale_factor)
            
            # Perform object detection asynchronously
            
            objects, img_width, img_height = loop.run_until_complete(async_object_detection(client, resized_frame))
            img_height /= detection_scale_factor
            img_width /= detection_scale_factor
            drug_object = [(frame, object_) for object_ in objects if object_.score >= 0.6 and object_.name == 'Packaged goods' and is_valid_bbox(object_)]
            if drug_object:
                accumulated_objects.append(drug_object)

            if count % 15 == 0 and accumulated_objects:
                
                # Perform OCR asynchronously using the accumulated objects
                print("entering ocr")
                print(len(accumulated_objects))
                results = loop.run_until_complete(async_ocr(client, accumulated_objects, img_width, img_height))
                full_texts = [result[0] for result in results]
                # print(openai.generate_response("19 yo, allergic to sea food", "".join(full_texts)))
                # print(full_texts)
                accumulated_objects = []  # Clear the accumulated objects

                count = 0

        if objects:
            annot_frame = ot.draw_bbox(frame, drug_object, img_width, img_height)
        else:
            annot_frame = frame

        # cv2.imshow('Video', annot_frame)
        # key = cv2.waitKey(1)

        # if key == ord('q'):
        #     break

        count += 1

        ret, buffer = cv2.imencode('.jpg', frame)

        frame = buffer.tobytes()
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


    # vid.release()
    # cv2.destroyAllWindows()
