from pypylon import pylon
import time

"""
* creates an instance of the camera 
  sets the parameters to Framestart, Trigger on, 
  line 3, 
  wait for a trigger within the timeout value, if a trigger is detetcted, 
  it saves the image 
"""
camera = pylon.InstantCamera(pylon.TlFactory_GetInstance().CreateFirstDevice())
print("Using device ", camera.GetDeviceInfo().GetModelName())
# print("settings: ", camera.GetNodeMap())
camera.Open()
camera.TriggerSelector.SetValue("FrameStart")
camera.TriggerMode.SetValue("On")
camera.TriggerSource.SetValue("Line3")
# camera.ExposureMode.SetValue("Timed")
# Analog gain is applied before the signal from the camera sensor is converted into digital values.
# Digital gain is applied after the conversion, i.e., it is basically a multiplication of the digitized values.
# camera.GainSelector.SetValue("DigitalAll") or AnalogAll
print(camera.TriggerMode.GetValue())
print(camera.TriggerSelector.GetValue())
print(camera.TriggerSource.GetValue())
camera.StartGrabbing(1)
img = pylon.PylonImage()
tlf = pylon.TlFactory.GetInstance()
print("waiting for grab")
while camera.IsGrabbing():
    grabResult = camera.RetrieveResult(50000, pylon.TimeoutHandling_ThrowException)
    img.AttachGrabResultBuffer(grabResult)

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
