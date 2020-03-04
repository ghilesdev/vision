from image_tools.image_preprocess import absoluteFilePaths
from fabric_defect_detection.pyimagesearch import config
from tensorflow.keras.models import load_model

import os
import copy

import numpy as np
import cv2
import time

OUTPUT_PATH = "image_tools\\output\\"
prediction_path = "image_tools\\prediction\\"
if not os.path.exists(prediction_path):
    os.makedirs(prediction_path)


def predict(image, neural_model, count):
    """
        predict if in image of fabric presents a defect, then anotates it and saves it to the
        prediction folder
    Args:
        image: path to the image to be predicted
        neural_model: the trained neural network model to be used
        count: used to name the image to be saved (only temporary until a good naming method)

    Returns:

    """
    model = neural_model
    image = cv2.imread(image)
    output = copy.deepcopy(image)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, (224, 224))
    image = image.astype("float32")

    # make predictions on the image
    preds = model.predict(np.expand_dims(image, axis=0))[0]
    i = np.argmax(preds)
    label = config.CLASSES[i]

    # draw the label on the image
    text = "prediction :{}".format(label)
    cv2.putText(output, text, (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.imwrite(prediction_path + "predict_" + str(count) + ".bmp", output)


def main():
    model = load_model(config.MODEL_PATH)
    output_files = list(absoluteFilePaths(OUTPUT_PATH))
    count = 0
    start_time = time.perf_counter()
    for image in output_files:
        predict(image, model, count)
        count += 1
    end_time = time.perf_counter()
    runing_time = end_time - start_time
    print(f"process took {runing_time} s")


if __name__ == "__main__":
    main()
