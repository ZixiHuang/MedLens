import io, os
from numpy import random
import numpy as np
from google.cloud import vision
import pandas as pd
import cv2
from PIL import Image

def object_tracking(frame, client):

    # get bbox
    pillow_image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    with io.BytesIO() as byte_stream:
        pillow_image.save(byte_stream, format='JPEG')
        frame_bytes = byte_stream.getvalue()

    image = vision.Image(content=frame_bytes)
    objects = client.object_localization(image=image)
    objects = objects.localized_object_annotations


    return objects, pillow_image.size[0], pillow_image.size[1]


def draw_bbox(frame, objects, width, height):


    for object_ in objects:

        bounding = object_.bounding_poly
        x1, y1 = int(bounding.normalized_vertices[0].x * width), int(bounding.normalized_vertices[0].y * height)
        x2, y2 = int(bounding.normalized_vertices[1].x * width), int(bounding.normalized_vertices[1].y * height)
        x3, y3 = int(bounding.normalized_vertices[2].x * width), int(bounding.normalized_vertices[2].y * height)
        x4, y4 = int(bounding.normalized_vertices[3].x * width), int(bounding.normalized_vertices[3].y * height)

        cv2.rectangle(frame, (int(x1), int(y1)),
                                      (int(x3), int(y3)),
                                      (0, 0, 255), 4)

        cv2.putText(frame, object_.name, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    return frame