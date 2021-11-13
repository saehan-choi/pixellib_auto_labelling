import pixellib
from pixellib.torchbackend.instance import instanceSegmentation
import pyautogui
from math import sqrt
import time
import pyscreenshot as ImageGrab
from collections import deque

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
    target_classes = ins.select_target_classes(person = True, car = True)
    results, output = ins.segmentImage("my_region.jpg", segment_target_classes = target_classes, show_bboxes=True, output_image_name="result.jpg")
    return results

def x_y_center_position(x1,y1,x2,y2):
    diffrence_x = (x2-x1)/2
    x_position = x1+diffrence_x
    diffrence_y = (y2-y1)/2
    y_position = y1+diffrence_y
    return x_position, y_position

results = image_process(x1,y1,x2,y2)
boxes = results["boxes"]
# print(boxes)
# print(results["class_ids"])
# print(results["class_names"])

screen_position_1 = []

for j in range(100):   
    # 540까지 하는거니까 540 으로 고쳐야함
    print(boxes)
    for i in range(len(boxes)):
        x1_, y1_, x2_, y2_ = boxes[i][:]
        screen_position_1.extend([x1+x1_, y1+y1_, x2+x2_, y2+y2_])
        pyautogui.moveTo(x1+x1_, y1+y1_)
        pyautogui.press('n')
        time.sleep(0.5)
        pyautogui.click()
        time.sleep(0.5)
        pyautogui.move(x2_-x1_, y2_-y1_)
        pyautogui.click()

    ################################################
    # 다음작업
    ################################################
    pyautogui.press('f')
    screen_position_2 = []

    results = image_process(x1,y1,x2,y2)
    boxes = results["boxes"]
    print(boxes)
    for i in range(len(boxes)):
        x1_, y1_, x2_, y2_ = boxes[i][:]
        screen_position_2.extend([x1+x1_, y1+y1_, x2+x2_, y2+y2_])
        pyautogui.moveTo(x1+x1_, y1+y1_)
        pyautogui.press('n')
        time.sleep(0.5)
        pyautogui.click()
        time.sleep(0.5)
        pyautogui.move(x2_-x1_, y2_-y1_)
        pyautogui.click()

        # print(screen_position_1)
        # print(len(screen_position_1)/4)
        # print(type(len(screen_position_1)/4))

    for i in range(int(len(screen_position_1)/4)):
    # 나누기 4 하는 이유는 pop 을 4번하기 때문
        
        # print(f'screen_position1: {screen_position_1}')
        y2_pop_1 = screen_position_1.pop()
        x2_pop_1 = screen_position_1.pop()
        y1_pop_1 = screen_position_1.pop()
        x1_pop_1 = screen_position_1.pop()

        # print(f'x1_pop1: {x1_pop_1}')
        # print(f'y1_pop1: {y1_pop_1}')
        # print(f'x2_pop1: {x2_pop_1}')
        # print(f'y2_pop2: {y2_pop_1}')

        x_position_1, y_position_1 = x_y_center_position(x1_pop_1, y1_pop_1, x2_pop_1, y2_pop_1)


        for j in range(int(len(screen_position_2)/4)):
            y2_pop_2 = screen_position_2.pop()
            x2_pop_2 = screen_position_2.pop()
            y1_pop_2 = screen_position_2.pop()
            x1_pop_2 = screen_position_2.pop()


            x_position_2, y_position_2 = x_y_center_position(x1_pop_2, y1_pop_2, x2_pop_2, y2_pop_2)

            
            position_diffrence = sqrt((x_position_2-x_position_1)**2 + (y_position_2-y_position_1)**2)
            # 피타고라스 법칙 점사이의 거리

            if position_diffrence > length_diffrence_limit:
                pass
            
            else:
                pyautogui.press('d')
                time.sleep(0.3)
                pyautogui.press('m')
                time.sleep(0.3)
                pyautogui.moveTo(x_position_1, y_position_1)
                pyautogui.click()
                # 바운딩박스의 중앙점을 클릭
                
                time.sleep(0.3)
                pyautogui.press('f')
                time.sleep(0.3)
                if y_position_1 < y_position_2:
                    pyautogui.moveTo(x_position_1, y2_pop_1 + 1)
                    pyautogui.click()
                    # x -> 픽셀의 중앙점 y -> 이전박스의 경계선 +1 픽셀 클릭
                    time.sleep(0.3)
                    pyautogui.press('m')
                    time.sleep(0.1)
                    # 1픽셀 바깥쪽의 이미지를 클릭
                else:
                    pyautogui.moveTo(x_position_1, y1_pop_1 - 1)
                    pyautogui.click()
                    # x -> 픽셀의 중앙점 y -> 이전박스의 경계선 -1 픽셀 클릭
                    time.sleep(0.3)
                    pyautogui.press('m')
                    time.sleep(0.1)