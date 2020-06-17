import cv2
import numpy as np
from pathlib import Path


YOLO_CFG    = './static/yolo/yolov3.cfg'
YOLO_WEIGHT = './static/yolo/yolov3_last.weights'
YOLO_NAME   = './static/yolo/yolo.names'
PATH_SAVE_DETECTED =  './static/images/predict.jpg'
def load_yolo():
    net = cv2.dnn.readNetFromDarknet( YOLO_CFG,YOLO_WEIGHT)
    classes = []
    with open(YOLO_NAME, "r") as f:
        classes = [line.strip() for line in f.readlines()]
    layers_names = net.getLayerNames()
    output_layers = [layers_names[i[0]-1] for i in net.getUnconnectedOutLayers()]
    colors = np.random.uniform(0, 255, size=(len(classes), 3))
    return net, classes, colors, output_layers

def load_image(img_path):
    # image loading
    img = cv2.imread(img_path)
    if np.sum(img) != 0:
        img = cv2.resize(img, None, fx=0.4, fy=0.4)
        height, width, channels = img.shape
        return img, height, width, channels
    else:
        print('khong co anh')
        pass

def detect_objects(img, net, outputLayers):
    #blob = cv2.dnn.blobFromImage(img, scalefactor=0.00392, size=(320, 320), mean=(0, 0, 0), swapRB=True, crop=False)
    blob = cv2.dnn.blobFromImage(img, 1/255.0, (416, 416), swapRB=True, crop=False)
    net.setInput(blob)
    ln = net.getLayerNames()
    ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]
    outputs = net.forward(ln)
    return blob, outputs

def get_box_dimensions(outputs, height, width):
    boxes = []
    confs = []
    class_ids = []
    for output in outputs:
        for detect in output:
            scores = detect[5:]
            class_id = np.argmax(scores)
            conf = scores[class_id]
            if conf > 0.1:
                center_x = int(detect[0] * width)
                center_y = int(detect[1] * height)
                w = int(detect[2] * width)
                h = int(detect[3] * height)
                x = int(center_x - w/2)
                y = int(center_y - h / 2)
                boxes.append([x, y, w, h])
                confs.append(float(conf))
                class_ids.append(class_id)
    return boxes, confs, class_ids

def draw_labels(boxes, confs, colors, class_ids, classes, img): 
    indexes = cv2.dnn.NMSBoxes(boxes, confs, 0.1, 0.1)
    font = cv2.FONT_HERSHEY_PLAIN
    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            color = colors[i]
            cv2.rectangle(img, (x,y), (x+w, y+h), color, 2)
            cv2.putText(img, label, (x, y - 5), font, 1, color, 1)
    cv2.imwrite(PATH_SAVE_DETECTED,img)
   
def image_detect(img_path):
    # img_path = Path(img_path)
    # img_name = img_path.name 
    model, classes, colors, output_layers = load_yolo()
    image, height, width, channels = load_image(img_path)
    blob, outputs = detect_objects(image, model, output_layers)
    boxes, confs, class_ids = get_box_dimensions(outputs, height, width)
    print('box:'+ str(len(boxes)))
    print('class_ids:'+ str(len(class_ids)))
    draw_labels(boxes, confs, colors, class_ids, classes, image)
    obj_class = list()
    for obj in class_ids:
        obj_class.append(classes[obj])

    return obj_class