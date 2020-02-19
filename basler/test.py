from pypylon import pylon, genicam
import sys
import cv2
import numpy

try:
    # connecting to the first available camera
    camera = pylon.InstantCamera(pylon.TlFactory_GetInstance().CreateFirstDevice())
    # open the camera
    camera.Open()
    # load the config file saved from pylon viewer
    # loads the hardware trigger
    file = "raL8192-12gm_working_settings.pfs"
    pylon.FeaturePersistence_Load(file, camera.GetNodeMap(), True)
    camera.RegisterConfiguration(
        pylon.SoftwareTriggerConfiguration(),
        pylon.RegistrationMode_ReplaceAll,
        pylon.Cleanup_Delete,
    )
    # camera.TriggerSelector.SetValue("FrameStart")
    # camera.TriggerMode.SetValue("On")
    # camera.TriggerSource.SetValue("Line3")
    # # camera.properties["TriggerMode"] = "On"
    # # camera.properties["TriggerSource"] = "Line3"
    # # camera.properties["TriggerSelector"] = "FrameStart"
    # camera.GetNodeMap()
    # camera.RegisterConfiguration(
    #     pylon.ConfigurationEventHandler(),
    #     pylon.RegistrationMode_Append,
    #     pylon.Cleanup_Delete,
    # )
    # # Print the model name of the camera.
    print("Using device ", camera.GetDeviceInfo().GetModelName())

    # Start the grabbing using the grab loop thread, by setting the grabLoopType parameter
    # to GrabLoop_ProvidedByInstantCamera. The grab results are delivered to the image event handlers.
    # The GrabStrategy_OneByOne default grab strategy is used.
    camera.StartGrabbing(
        pylon.GrabStrategy_OneByOne, pylon.GrabLoop_ProvidedByInstantCamera
    )
    converter = pylon.ImageFormatConverter()

    # converting to opencv bgr format
    converter.OutputPixelFormat = pylon.PixelType_BGR8packed
    converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned

    images = []
    numberOfImages = 10
    while camera.IsGrabbing():
        grabResult = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
        print("grabbing: ", grabResult)
        # if grabResult.GrabSucceeded():
        print("Picture number ")
        img = grabResult.Array
        print("Max Intensity:", numpy.amax(img))
        images.append(img)
        image = converter.Convert(grabResult)
        img = image.GetArray()
        cv2.namedWindow("title", cv2.WINDOW_NORMAL)
        cv2.imshow("title", img)
        k = cv2.waitKey(1)
        if k == 27:
            break
    grabResult.Release()
    # else:
    #     print("Error: ", grabResult.ErrorCode, grabResult.ErrorDescription)
    #     grabResult.Release()

    print("Acquisition process completed")
    print("Images meant to be taken: ", numberOfImages)
    print("Images succesfully taken: ", len(images))

except genicam.GenericException as e:
    print("an error occurred")
