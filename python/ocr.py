from google.cloud import vision
from google.cloud import videointelligence

import io
import numpy as np

def video_detect_text(path, silence=True):
    """Detect text in a local video and return a list of detected text details."""
    video_client = videointelligence.VideoIntelligenceServiceClient()
    features = [videointelligence.Feature.TEXT_DETECTION]
    video_context = videointelligence.VideoContext()

    with io.open(path, "rb") as file:
        input_content = file.read()

    operation = video_client.annotate_video(
        request={
            "features": features,
            "input_content": input_content,
            "video_context": video_context,
        }
    )

    result = operation.result(timeout=300)
    annotation_result = result.annotation_results[0]

    detected_texts = []

    for text_annotation in annotation_result.text_annotations:
        text = text_annotation.text
        text_segment = text_annotation.segments[0]
        start_time = text_segment.segment.start_time_offset
        end_time = text_segment.segment.end_time_offset

        confidence = text_segment.confidence
        frame = text_segment.frames[0]

        bbox_vertices = [(vertex.x, vertex.y) for vertex in frame.rotated_bounding_box.vertices]

        detected_texts.append({
            "text": text,
            "confidence": confidence,
            "bbox": bbox_vertices,
            "start_time": start_time.seconds + start_time.microseconds * 1e-6,
            "end_time": end_time.seconds + end_time.microseconds * 1e-6
        })

        if not silence:
            print(f'Word: {text}, Confidence: {confidence}')
            print(f'Bounding Box: {bbox_vertices}')
            print(f'Start Time: {start_time.seconds + start_time.microseconds * 1e-6}')
            print(f'End Time: {end_time.seconds + end_time.microseconds * 1e-6}')
            

    return detected_texts



def detect_text(path, silence=True):

    client = vision.ImageAnnotatorClient()

    with open(path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    text_detection_params = vision.TextDetectionParams(enable_text_detection_confidence_score=True)
    image_context = vision.ImageContext(text_detection_params=text_detection_params)
    response = client.text_detection(image=image, image_context=image_context)
    ordered_text = response.text_annotations[0].description
    texts_w_bbox = []

    for page in response.full_text_annotation.pages:
        for block in page.blocks:
            for paragraph in block.paragraphs:
                for word in paragraph.words:
                    word_text = ''.join([symbol.text for symbol in word.symbols])
                    confidence = word.confidence

                    # Extracting bounding box
                    vertices = [(vertex.x, vertex.y) for vertex in word.bounding_box.vertices]
                    bounding_box = {
                        "top_left": vertices[0],
                        "top_right": vertices[1],
                        "bottom_right": vertices[2],
                        "bottom_left": vertices[3]
                    }

                    texts_w_bbox.append({
                        "word": word_text,
                        "confidence": confidence,
                        "bounding_box": bounding_box
                    })

                    if not silence:
                        print(f'Word: {word_text}, Confidence: {confidence}')
                        print(f'Bounding Box: {bounding_box}')

    if response.error.message:
        raise Exception(
            "{}\nFor more info on error messages, check: "
            "https://cloud.google.com/apis/design/errors".format(response.error.message)
        )
    return ordered_text, texts_w_bbox

if __name__ == "__main__":
    video_path = './data/coke.mov'
    photo_path = './data/clindamycin.jpg'
    video_detect_text(video_path, silence=False)
    detect_text(photo_path, silence=False)