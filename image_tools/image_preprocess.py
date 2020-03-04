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

    Args:
        source_file:

    Returns:
        preprocessed image
    """
    image = cv2.imread(source_file)
    # taking only one channel because the three channels are already in gray
    image = image[:, :, 0]
    equalized = cv2.equalizeHist(image)
    return equalized


def segment(processed):
    """
        cuts the image into 512*512 batch
    Args:
        processed:

    Returns:
        list of cropped images
        list of labels of images
    """
    w, h = processed.shape[1], processed.shape[0]
    nb_of_hsegment = round((w / 512) + 0.5)
    nb_of_vsegment = round((h / 512) + 0.5)
    print("nb of h seg", nb_of_hsegment)
    print("nb of v seg", nb_of_vsegment)
    segmented = []
    labels = []
    for i in range(nb_of_vsegment):
        for j in range(nb_of_hsegment):
            img = processed[i * 512 : (i + 1) * 512, j * 512 : (j + 1) * 512]
            labels.append((i, j))
            segmented.append(img)
    return segmented, labels


def anotate(segmented):
    """

    Args:
        segmented:

    Returns:

    """
    return segmented


def save(segmented, labels):
    """
    
    Args:
        segmented: 

    Returns:
        nothing
    """
    for i, seg in enumerate(segmented):
        cv2.imwrite(f"{OUTPUT_PATH}{labels[i]}.bmp", seg)


def main():
    source_files = list(absoluteFilePaths(INPUT_PATH))
    print(source_files)
    segmented_images = []
    count = 0
    for source_file in source_files:
        processed = process(source_file)
        segmented, labels = segment(processed)
        annotated = anotate(segmented)
        segmented_images.append(annotated)
        save(segmented, labels)
        count += 1


if __name__ == "__main__":
    main()
