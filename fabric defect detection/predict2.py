import copy

from tensorflow.keras.models import load_model
from pyimagesearch import config
from collections import deque
import numpy as np
import argparse
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", required=True,
	help="path to our input image")
args=vars(ap.parse_args())

# load the trained model from disk
print("[INFO] loading model and label binarizer...")
model = load_model(config.MODEL_PATH)

print("[INFO] processing image...")
image = cv2.imread(args["input"])
writer = None
(W, H) =  image.shape[:2]
Q = deque(maxlen=128)
output = copy.deepcopy(image)

image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
image = cv2.resize(image, (224,224))
image = image.astype('float32')
# make predictions on the frame and then update the predictions
    # queue
preds = model.predict(np.expand_dims(image, axis=0))[0]
print('prediction array', preds)
# Q.append(preds)
# perform prediction averaging over the current history of
# previous predictions
# results = np.array(Q).mean(axis=0)
i = np.argmax(preds)
label = config.CLASSES[i]
print('index', i)
print('label', label)

# draw the activity on the output frame
text = "prediction :{}".format(label)
cv2.putText(output, text, (35, 50), cv2.FONT_HERSHEY_SIMPLEX,
            1.25, (0, 255, 0), 5)

# check if the video writer is None
cv2.imwrite('predict_'+args["input"], output)
print('predict_'+args["input"])

# check to see if we should display the output frame to our
# screen
# if args["display"] > 0:
#     # show the output image
#     cv2.imshow("Output", output)
#     key = cv2.waitKey(1) & 0xFF

