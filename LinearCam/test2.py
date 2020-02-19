from pypylon import pylon, genicam
import cv2
import numpy

camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())

camera.Open()

print("DeviceClass: ", camera.GetDeviceInfo().GetDeviceClass())
print("DeviceFactory: ", camera.GetDeviceInfo().GetDeviceFactory())
print("ModelName: ", camera.GetDeviceInfo().GetModelName())

Hardware_Trigger = True

if Hardware_Trigger:
    # reset registration
    camera.RegisterConfiguration(
        pylon.ConfigurationEventHandler(),
        pylon.RegistrationMode_ReplaceAll,
        pylon.Cleanup_Delete,
    )

# The parameter MaxNumBuffer can be used to control the count of buffers
# allocated for grabbing. The default value of this parameter is 10.
camera.MaxNumBuffer = 5

# set exposure time
camera.ExposureTimeRaw.SetValue(100)

# Select the Frame Start trigger
camera.TriggerSelector.SetValue("FrameStart")
# Acquisition mode
camera.AcquisitionMode.SetValue("SingleFrame")
# Enable triggered image acquisition for the Frame Start trigger
camera.TriggerMode.SetValue("On")
# Set the trigger source to Line 1
camera.TriggerSource.SetValue("Line1")
# Set the trigger activation mode to rising edge
camera.TriggerActivation.SetValue("RisingEdge")
# Set the delay for the frame start trigger to 300 µs
camera.TriggerDelayAbs.SetValue(300.0)
# Pixel format
camera.PixelFormat.SetValue("Mono8")

camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)
converter = pylon.ImageFormatConverter()

converter.OutputPixelFormat = pylon.PixelType_BGR8packed
converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned

count = 1
while camera.IsGrabbing():
    grabResult = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)

    if grabResult.GrabSucceeded():
        # Access the image data
        image = converter.Convert(grabResult)
        img = image.GetArray()
        print("yes, an image is grabbed successfully")

        cv2.imwrite("save_images/%06d.png" % count, img)
        print("image/%06d.png saved" % count)
        count += 1
        k = cv2.waitKey(1)
        if k == 27:
            break
    grabResult.Release()
    camera.StopGrabbing()
