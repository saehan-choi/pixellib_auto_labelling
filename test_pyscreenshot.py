import pyscreenshot as ImageGrab
img=ImageGrab.grab(bbox=(76, 186, 1137, 1015))
img.save('my_region.jpg')
