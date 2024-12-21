import os 
import argparse
import numpy as np
from PIL import Image, ImageDraw

parser = argparse.ArgumentParser(description="Provide following parameters")

parser.add_argument("-p", '--path', dest="input_label", required=True, type=str,
                    help="input directory")

args = parser.parse_args()
if not os.path.exists(args.input_label):
    raise FileNotFoundError(f"The input path '{args.input_path}' does not exist.")

with open(args.input_label, "r") as file:
    annotation_list = file.read().split("\n")[:-1]
    annotation_list = [x.split(" ") for x in annotation_list]
    annotation_list = [[float(y) for y in x ] for x in annotation_list]

class_id_to_name_mapping = {0:"rose",1:"lotus",2:"hibiscuss",3:"marigold",4:"sunflower"}

def plot_bounding_box(image, annotation_list):
    annotations = np.array(annotation_list)
    w, h = image.size
    
    plotted_image = ImageDraw.Draw(image)

    transformed_annotations = np.copy(annotations)
    transformed_annotations[:,[1,3]] = annotations[:,[1,3]] * w
    transformed_annotations[:,[2,4]] = annotations[:,[2,4]] * h 
    
    transformed_annotations[:,1] = transformed_annotations[:,1] - (transformed_annotations[:,3] / 2)
    transformed_annotations[:,2] = transformed_annotations[:,2] - (transformed_annotations[:,4] / 2)
    transformed_annotations[:,3] = transformed_annotations[:,1] + transformed_annotations[:,3]
    transformed_annotations[:,4] = transformed_annotations[:,2] + transformed_annotations[:,4]
    
    for ann in transformed_annotations:
        obj_cls, x0, y0, x1, y1 = ann
        plotted_image.rectangle(((x0,y0), (x1,y1)))
        
        plotted_image.text((x0, y0 - 10), class_id_to_name_mapping[(int(obj_cls))])
    image.save("/media/asim/home/asim/Documents/flowers/YOLOv1/image.jpg")

image_file = args.input_label.replace("labels", "images").replace("txt", "jpg")
assert os.path.exists(image_file)

#Load the image
image = Image.open(image_file)
#Plot the Bounding Box
plot_bounding_box(image, annotation_list)