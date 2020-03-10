from pypylon import pylon
import os
import cv2

os.environ["PYLON_CAMEMU"] = "1"

camera = pylon.InstantCamera(pylon.TlFactory_GetInstance().CreateFirstDevice())
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
import pprint

pprint.pprint(img)
# cv2.imshow("", img)
# cv2.waitKey(0)
