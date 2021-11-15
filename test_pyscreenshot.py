# import pyscreenshot as ImageGrab
# img=ImageGrab.grab(bbox=(76, 186, 1137, 1015))
# img.save('my_region.jpg')

a = [1, 2, 3, 4, 5, 6, 7, 8, 4, 2]
b = [8, 4, 2]

del a[-len(b):]
print(a)
# [1, 3, 4, 5, 6, 7]