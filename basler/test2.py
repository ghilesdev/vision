from pypylon import pylon
import time

"""
* creates an instance of the camera 
  sets the parameters to Framestart, Trigger on, 
  line 3, 
  wait for a trigger within the timeout value, if a trigger is detetcted, 
  it saves the image 
"""
info = pylon.DeviceInfo()
info.SetDeviceClass("BaslerGigE")
camera = pylon.InstantCamera(pylon.TlFactory_GetInstance().CreateFirstDevice(info))
print("Using device ", camera.GetDeviceInfo().GetModelName())
# print("settings: ", camera.GetNodeMap())
if camera.IsGigE():  # if a real camera is attached
    camera.Open()
    # configure camera parameter
    # heightMax = camera.Height.GetMax()
    # heightInc = camera.Height.GetInc()
    # camera.Height.SetValue(heightMax)
    # print("height", heightInc)
    camera.ExposureTimeAbs.SetValue(100.0)
    camera.OffsetX.SetValue(0)
    width = camera.Width.GetMax()
    camera.Width = width
    camera.TriggerSelector.SetValue("FrameStart")
    camera.TriggerMode.SetValue("On")
    camera.TriggerSource.SetValue("Line1")
    camera.TriggerSelector.SetValue("LineStart")
    camera.TriggerMode.SetValue("On")
    camera.TriggerSource.SetValue("Line2")
    # camera.ExposureMode.SetValue("Timed")
    # Analog gain is applied before the signal from the camera sensor is converted into digital values.
    # Digital gain is applied after the conversion, i.e., it is basically a multiplication of the digitized values.
    # camera.GainSelector.SetValue("DigitalAll") or AnalogAll
    print("camera.TriggerMode: ", camera.TriggerMode.GetValue())
    print("camera.TriggerSelector: ", camera.TriggerSelector.GetValue())
    print("camera.TriggerSource: ", camera.TriggerSource.GetValue())
    camera.StartGrabbingMax(1)
    img = pylon.PylonImage()
    tlf = pylon.TlFactory.GetInstance()
    print("waiting for grab")
    while camera.IsGrabbing():
        grabResult = camera.RetrieveResult(10000, pylon.TimeoutHandling_ThrowException)
        img.AttachGrabResultBuffer(grabResult)

        # pylon.DisplayImage(1, grabResult)
        # The JPEG format that is used here supports adjusting the image
        # quality (100 -> best quality, 0 -> poor quality).
        ipo = pylon.ImagePersistenceOptions()
        quality = 100
        ipo.SetQuality(quality)

        filename = f"saved_pypylon_img{time.time()}.jpeg"
        img.Save(pylon.ImageFileFormat_Jpeg, filename, ipo)

        # In order to make it possible to reuse the grab result for grabbing
        # again, we have to release the image (effectively emptying the
        # image object).
        img.Release()

    camera.StopGrabbing()
    camera.Close()

else:  # use emulated camera
    camera.Open()
    camera.Width = 4096
    camera.Height = 4096
    camera.TestImageSelector = "Testimage1"
    # camera.TriggerMode.SetValue("On")

    print("camera.TriggerMode: ", camera.TriggerMode.GetValue())
    print("camera.TriggerSelector: ", camera.TriggerSelector.GetValue())
    print("camera.TriggerSource: ", camera.TriggerSource.GetValue())
    camera.StartGrabbingMax(10)
    img = pylon.PylonImage()

    while camera.IsGrabbing():
        res = camera.RetrieveResult(10000)
        img.AttachGrabResultBuffer(res)

        # print(res.Array[0, :])
        ipo = pylon.ImagePersistenceOptions()
        quality = 100
        ipo.SetQuality(quality)

        filename = "saved_pypylon_img.jpeg"
        img.Save(pylon.ImageFileFormat_Jpeg, filename, ipo)
        res.Release()
    camera.StopGrabbing()
    camera.Close()
