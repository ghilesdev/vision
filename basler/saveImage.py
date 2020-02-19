from pypylon import pylon
import cv2

camera = pylon.InstantCamera(pylon.TlFactory_GetInstance().CreateFirstDevice())
print("Using device ", camera.GetDeviceInfo().GetModelName())
camera.Open()
file = "raL8192-12gm_working_settings.pfs"
pylon.FeaturePersistence_Load(file, camera.GetNodeMap())
camera.RegisterConfiguration(
    pylon.SoftwareTriggerConfiguration(),
    pylon.RegistrationMode_ReplaceAll,
    pylon.Cleanup_Delete,
)
# converter = pylon.ImageFormatConverter()
#
# # converting to opencv bgr format
# converter.OutputPixelFormat = pylon.PixelType_BGR8packed
# converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned


camera.StartGrabbing()
# camera.StartGrabbing()
num_img_to_save = 10
img = pylon.PylonImage()
tlf = pylon.TlFactory.GetInstance()

for i in range(num_img_to_save):
    with camera.RetrieveResult(100000) as result:  # 20 seconds timeout

        # Calling AttachGrabResultBuffer creates another reference to the
        # grab result buffer. This prevents the buffer's reuse for grabbing.
        img.AttachGrabResultBuffer(result)

        # The JPEG format that is used here supports adjusting the image
        # quality (100 -> best quality, 0 -> poor quality).
        ipo = pylon.ImagePersistenceOptions()
        quality = 100
        ipo.SetQuality(quality)

        filename = "saved_pypylon_img_%d.jpeg" % i
        img.Save(pylon.ImageFileFormat_Jpeg, filename, ipo)

        # In order to make it possible to reuse the grab result for grabbing
        # again, we have to release the image (effectively emptying the
        # image object).
        img.Release()

camera.StopGrabbing()
camera.Close()
