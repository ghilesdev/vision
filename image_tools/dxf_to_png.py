from tekyntools.tools.browse_tools import select_file_path
import pickle as pkl
from tekyntools.dxfTools import dxfParser
import numpy as np
import cv2
import os

OUTPUT_PATH = "output_image_similarity\\"
SOURCE_PATH = OUTPUT_PATH + "source\\"
PROD_PATH = OUTPUT_PATH + "prod\\"

for path in [SOURCE_PATH, PROD_PATH]:
    if not os.path.exists(path):
        os.makedirs(path)


def shape_writer(f):
    """
        takes a dxf files and saves each shape in a separate file
        reminder change the output path between prod and source
    """

    # extract the file extension
    _, ext = os.path.splitext(f)

    # if the file is a dxf then parse it otherwise
    # loads it as a pickle
    if ext.lower() == ".dxf":
        dxf = dxfParser.parse(f)
        shapes = []
        rects = []
        for s in dxf:
            bounding_rect = s.cutPolyline.getBoundsRectanglePolyline()
            rects.append(bounding_rect)
            bounds = s.cutPolyline.getBounds()
            tx = -bounds["left"]
            ty = -bounds["bottom"]
            s.cutPolyline.translatePoly(tx, ty)
            shapes.append(s.cutPolyline.polylineToTuple())

    else:  # if it's a pickle file
        with open(f, "rb") as file:
            dxf = pkl.load(file)
        dxf = dxf[0]
        shapes = []
        rects = []
        for s in dxf:
            # same flow but shapes has no cutPolyline()
            bounding_rect = s.getBoundsRectanglePolyline()
            rects.append(bounding_rect)
            bounds = s.getBounds()
            tx = -bounds["left"]
            ty = -bounds["bottom"]
            s.translatePoly(tx, ty)
            shapes.append(s.polylineToTuple())

    for i, shape in enumerate(shapes):
        h = int(rects[i].coords[3][1] - rects[i].coords[1][1])
        w = int(rects[i].coords[2][0] - rects[i].coords[0][0])
        # create a blank image
        img = np.zeros((h + 10, w + 10), dtype=np.uint8)
        img.fill(255)

        polyx = []
        polyy = []

        for coords in shape:
            polyx.append(coords[0] + 5)
            polyy.append(coords[1] + 5)

        pts = np.vstack((polyx, polyy)).astype(np.int32).T

        cv2.polylines(img, [pts], 0, 0, thickness=1)
        if ext.lower() == ".dxf":
            cv2.imwrite(f"{SOURCE_PATH}shape_{i}.png", img)
        else:
            cv2.imwrite(f"{PROD_PATH}\\shape_{i}.png", img)


def main():

    file_path = select_file_path()
    shape_writer(file_path)


if __name__ == "__main__":
    main()
