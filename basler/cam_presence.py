from pypylon import pylon

camera = pylon.InstantCamera(pylon.TlFactory_GetInstance().CreateFirstDevice())
print("Using device ", camera.GetDeviceInfo().GetModelName())
# print("settings: ", camera.GetNodeMap())
