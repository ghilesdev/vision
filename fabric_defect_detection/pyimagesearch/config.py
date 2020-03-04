# import the necessary packages
import os

# initialize the path to the input directory containing our dataset
# of images
DATASET_PATH = "dataset"
# initialize the class labels in the dataset
CLASSES = ["defect", "noDefect"]

TRAIN_SPLIT = 0.75
VAL_SPLIT = 0.1
TEST_SPLIT = 0.25

# define the minimum learning rate, maximum learning rate, batch size,
# step size, CLR method, and number of epochs
MIN_LR = 1e-6
MAX_LR = 1e-4
BATCH_SIZE = 32
# BATCH_SIZE = 96
STEP_SIZE = 8
CLR_METHOD = "triangular"
NUM_EPOCHS = 24

# set the path to the serialized model after training
MODEL_PATH = os.path.sep.join(["fabric_defect_detection", "output", "fabric.model"])
# define the path to the output learning rate finder plot, training
# history plot and cyclical learning rate plot
LRFIND_PLOT_PATH = os.path.sep.join(["output", "lrfind_plot.png"])
TRAINING_PLOT_PATH = os.path.sep.join(["output", "training_plot.png"])
CLR_PLOT_PATH = os.path.sep.join(["output", "clr_plot.png"])
