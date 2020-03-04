import cv2
import os

OUTPUT_PATH = "output\\"
INPUT_PATH = "input\\"

for path in [INPUT_PATH, OUTPUT_PATH]:
    if not os.path.exists(path):
        os.makedirs(path)


def absoluteFilePaths(directory):
    """
        returns filenames with absolute path
    Args:
        relative path to the file:
    Returns:
        absolute path of the file
    """
    for dirpath, _, filenames in os.walk(directory):
        for f in filenames:
            yield os.path.abspath(os.path.join(dirpath, f))


def process(source_file):
    """
        apply bgr to grayscale conversion
        apply histogram equalisation
    Args:
        source_file: path to the image to be processed

    Returns:
        preprocessed image
    """
    image = cv2.imread(source_file)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # taking only one channel because the three channels are already in gray
    # image = image[:, :, 0]
    equalized = cv2.equalizeHist(image)
    return equalized


def segment(processed, name):
    """
        cuts the image into 512*512 batch
    Args:
        processed:

    Returns:
        list of cropped images
        list of labels of images
    """
    width, height = processed.shape[1], processed.shape[0]
    if width > 512 and height > 512:
        nb_of_hsegment = round((width / 512) + 0.5)
        nb_of_vsegment = round((height / 512) + 0.5)
        segmented = []
        labels = []
        for i in range(nb_of_vsegment):
            for j in range(nb_of_hsegment):
                img = processed[i * 512 : (i + 1) * 512, j * 512 : (j + 1) * 512]
                labels.append((i, j))
                segmented.append(img)
                cv2.imwrite(f"{OUTPUT_PATH}{(i, j)}{name}", img)

    elif width == 512 and height == 512:
        segmented = processed
        labels = (1, 1)
        cv2.imwrite(f"{OUTPUT_PATH}{labels}{name}", segmented)

    return segmented, labels


def main():
    source_files = list(absoluteFilePaths(INPUT_PATH))
    segmented_images = []
    labels_list = []
    count = 0
    for source_file in source_files:
        file_name = os.path.basename(source_file)
        processed = process(source_file)
        segmented, labels = segment(processed, file_name)
        segmented_images.append(segmented)
        labels_list.append(labels)
        count += 1


if __name__ == "__main__":
    main()
