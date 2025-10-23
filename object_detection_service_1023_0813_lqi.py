# 代码生成时间: 2025-10-23 08:13:50
import tornado.ioloop
import tornado.web
import cv2
from PIL import Image
import numpy as np
import torch
import torchvision.transforms as transforms
from torchvision.models.detection import fasterrcnn_resnet50_fpn
from torchvision.models.detection.faster_rcnn import FastRCNNPredictor

# ObjectDetectionHandler handles requests for object detection
class ObjectDetectionHandler(tornado.web.RequestHandler):
    def initialize(self, model):
        self.model = model

    # This method is called when an HTTP GET request is received
    def get(self):
        # Respond with a simple message for now
        self.write("Object Detection Service is Running.")

    # This method is called when an HTTP POST request is received
    def post(self):
        # Check if the request contains an image file
        if 'image' not in self.request.files:
            self.set_status(400)
            self.write('No image provided.')
            return

        # Load the image file from the request
        image = self.get_argument('file', None)
        if image is None:
            self.set_status(400)
            self.write('No file found in the request.')
            return

        try:
            # Convert the image to a suitable format for the detection model
            image = cv2.imdecode(np.fromstring(image, np.uint8), cv2.IMREAD_COLOR)
            image = Image.fromarray(image)
            
            # Apply transformations to the image
            transform = transforms.Compose([transforms.ToTensor()])
            image = transform(image)
            image = image.unsqueeze(0)
            
            # Perform object detection using the model
            outputs = self.model([image])
            results = self.process_detection_outputs(outputs)
            self.write(results)
        except Exception as e:
            self.set_status(500)
            self.write(f'An error occurred: {str(e)}')

    def process_detection_outputs(self, outputs):
        # Process the model's output to extract detected objects
        scores = outputs[0]['scores'].detach().numpy()
        class_ids = outputs[0]['labels'].detach().numpy()
        boxes = outputs[0]['boxes'].detach().numpy()
        
        results = []
        for score, class_id, box in zip(scores, class_ids, boxes):
            if score > 0.5:  # Filter out low confidence detections
                result = {
                    'class_id': class_id,
                    'score': score,
                    'box': box.tolist()
                }
                results.append(result)
        return results

# Prepare the object detection model
def prepare_model():
    model = fasterrcnn_resnet50_fpn(pretrained=True)
    # Get the number of input features for the classifier
    in_features = model.roi_heads.box_predictor.cls_score.in_features
    # Replace the pre-trained head with a new one
    model.roi_heads.box_predictor = FastRCNNPredictor(in_features, num_classes=91)
    model.eval()
    return model

# Define the main application class
class Application(tornado.web.Application):
    def __init__(self):
        handler = ObjectDetectionHandler
        handler_model = prepare_model()
        tornado.web.Application.__init__(self, [
            (r"/object_detection", handler, dict(model=handler_model)),
        ])

# Main function to run the Tornado application
def main():
    app = Application()
    app.listen(8888)
    print("Server is running on port 8888")
    tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    main()