from pixellib.torchbackend.instance import instanceSegmentation
import pyscreenshot as ImageGrab
from collections import deque
from math import sqrt
import pyautogui
import pixellib
import time

# 화면 좌표 보고나서 이 변수만 변경해주면 됨
x1 = 76
y1 = 186
x2 = 1137
y2 = 1015

length_diffrence_limit = 20

def image_process(x1,y1,x2,y2):
    img=ImageGrab.grab(bbox=(x1, y1, x2, y2))
    img.save('my_region.jpg')
    ins = instanceSegmentation()
    ins.load_model("pointrend_resnet50.pkl")
    # ins.load_model("pointrend_resnet50.pkl", confidence = 0.3)
    # 감지 잘안될경우 confidence 줄이기
    target_classes = ins.select_target_classes(person = True)
    # target_classes = ins.select_target_classes(person = True, car = True)
    results, output = ins.segmentImage("my_region.jpg", segment_target_classes = target_classes, show_bboxes=True, output_image_name="result.jpg")
    return results

def x_y_center_position(x1,y1,x2,y2):
    diffrence_x = (x2-x1)/2
    x_position = x1+diffrence_x
    diffrence_y = (y2-y1)/2
    y_position = y1+diffrence_y
    return x_position, y_position

x1 = 76
y1 = 186
x2 = 1137
y2 = 1015

arr = deque()
arr_num = deque()

for j in range(540):
    results = image_process(x1,y1,x2,y2)
    boxes = results["boxes"]
    arr_num.append(len(boxes))

    for _ in range(len(boxes)):
        # 이게현재박스
        x1_, y1_, x2_, y2_ = boxes[i][:]
        arr.extend([x1_,y1_,x2_,y2_])
        pyautogui.moveTo(x1+x1_, y1+y1_)
        pyautogui.press('n')
        time.sleep(0.5)
        pyautogui.click()
        time.sleep(0.5)
        pyautogui.move(x2_-x1_, y2_-y1_)
        pyautogui.click()

        x_position_1, y_position_1 = x_y_center_position(x1_, y1_, x2_, y2_)

        if j == 0:
            pass
        else:
            for i in range(arr_num[0]):
                # 실제로는 이게 첫번째 박스네

                x1__, y1__, x2__, y2__ = arr[arr_num[0]+4*i], arr[arr_num[0]+4*i+1], arr[arr_num[0]+4*i+2], arr[arr_num[0]+4*i+3]
                # 이렇게하면 4번씩 돌아옴 0 1 2 3- 4 5 6 7 - ....
                x_position_2, y_position_2 = x_y_center_position(x1__, y1__, x2__, y2__)
                position_diffrence = sqrt((x_position_2-x_position_1)**2 + (y_position_2-y_position_1)**2)

                if position_diffrence > length_diffrence_limit:
                    pass
                else:
                    pyautogui.press('d')
                    time.sleep(1)
                    pyautogui.press('m')
                    time.sleep(1)
                    pyautogui.moveTo(x1+x_position_1, y1+y_position_1)
                    pyautogui.click()
                    # 바운딩박스의 중앙점을 클릭
                    
                    time.sleep(1)
                    pyautogui.press('f')
                    time.sleep(1)
                    if y_position_1 < y_position_2:
                        pyautogui.moveTo(x1+x_position_1, y1+y2_ + 1)
                        pyautogui.click()
                        # x -> 픽셀의 중앙점 y -> 이전박스의 경계선 +1 픽셀 클릭
                        time.sleep(1)
                        pyautogui.press('m')
                        time.sleep(1)
                        # 1픽셀 바깥쪽의 이미지를 클릭
                    else:
                        pyautogui.moveTo(x1+x_position_1, y1+y1_ - 1)
                        pyautogui.click()
                        # x -> 픽셀의 중앙점 y -> 이전박스의 경계선 -1 픽셀 클릭
                        time.sleep(1)
                        pyautogui.press('m')
                        time.sleep(1)                

    for m in range(4*arr_num[0]):
        del arr[0]
    del arr_num[0]
    pyautogui.press('f')
