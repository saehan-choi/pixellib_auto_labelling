import pixellib
from pixellib.torchbackend.instance import instanceSegmentation
import pyautogui
import time
import pyscreenshot as ImageGrab
from collections import deque

# 화면 좌표 보고나서 이 변수만 변경해주면 됨
x1 = 76
y1 = 186
x2 = 1137
y2 = 1015

img=ImageGrab.grab(bbox=(x1, y1, x2, y2))
img.save('my_region.jpg')

ins = instanceSegmentation()
ins.load_model("pointrend_resnet50.pkl")
# ins.load_model("pointrend_resnet50.pkl", confidence = 0.3)
# 감지 잘안될경우 confidence 줄이기
target_classes = ins.select_target_classes(person = True, car = True)
results, output = ins.segmentImage("my_region.jpg", segment_target_classes = target_classes, show_bboxes=True, output_image_name="result.jpg")

boxes = results["boxes"]
print(boxes)
print(results["class_ids"])
print(results["class_names"])

# im2 = pyautogui.screenshot('my_screenshot.png')
# im3 = pyautogui.screenshot('my_region.png', region=(76, 186, 1137, 850))
# 이건 pyscreen에서 에러나면 이거쓸것

# 커서만 바꾸자
empty = []
dq = deque([])

# for j in range(540):   540까지 하는거니깐!
for i in range(len(boxes)):
    x1_, y1_, x2_, y2_ = boxes[i][:]
    empty.extend([x1+x1_, y1+y1_, x2+x2_, y2+y2_])
    pyautogui.moveTo(x1+x1_, y1+y1_)
    pyautogui.press('n')
    time.sleep(1)
    pyautogui.click()
    time.sleep(0.5)
    pyautogui.move(x2_-x1_, y2_-y1_)
    pyautogui.click()

pyautogui.press('d')
# x1 = 
