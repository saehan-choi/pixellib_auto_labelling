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
    target_classes = ins.select_target_classes(person = True, car = True)
    results, output = ins.segmentImage("my_region.jpg", segment_target_classes = target_classes, show_bboxes=True, output_image_name="result.jpg")
    return results

def x_y_center_position(x1,y1,x2,y2):
    diffrence_x = (x2-x1)/2
    x_position = x1+diffrence_x
    diffrence_y = (y2-y1)/2
    y_position = y1+diffrence_y
    return x_position, y_position

# 맨처음은 그냥 박스침
# print(f'box_position_1 original:{box_position_1}')

box_position = deque()
box_repeat = deque()
for j in range(100):
    # 540까지 하는거니까 540 으로 고쳐야함
    ################################################
    # 다음작업
    ################################################

    results = image_process(x1,y1,x2,y2)
    boxes = results["boxes"]

    for i in range(len(boxes)):
        x1_, y1_, x2_, y2_ = boxes[i][:]
        box_position.extend([x1_, y1_, x2_, y2_])
        pyautogui.moveTo(x1+x1_, y1+y1_)
        pyautogui.press('n')
        time.sleep(0.5)
        pyautogui.click()
        time.sleep(0.5)
        pyautogui.move(x2_-x1_, y2_-y1_)
        pyautogui.click()

    box_repeat.append(len(boxes))
    pyautogui.press('f')
    time.sleep(0.3)

    if j == 0:
        pass
    else:
        # 배열값들이 영향을 받지않기 위해서 이렇게 함
        # box_position2가 변경될때 box_postion1이 변경되면 안됨

        box_repeat_1 = box_repeat.popleft()
        # 제일 첫번째 box_num을 popleft
        box_repeat_2 = box_repeat[-1]
        # 제일 마지막 box_num을 가져옴
        box_repeat_1_copy = box_repeat.popleft()

        for _ in range(box_repeat_1):
            x1_pop_1 = box_position.popleft()
            y1_pop_1 = box_position.popleft()
            x2_pop_1 = box_position.popleft()
            y2_pop_1 = box_position.popleft()

            x_position_1, y_position_1 = x_y_center_position(x1_pop_1, y1_pop_1, x2_pop_1, y2_pop_1)

            for _ in range(box_repeat_2):
                x1_pop_2 = box_position[box_repeat_1_copy*4+0]
                y1_pop_2 = box_position[box_repeat_1_copy*4+1]
                x2_pop_2 = box_position[box_repeat_1_copy*4+2]
                y2_pop_2 = box_position[box_repeat_1_copy*4+3]

                x_position_2, y_position_2 = x_y_center_position(x1_pop_2, y1_pop_2, x2_pop_2, y2_pop_2)

                position_diffrence = sqrt((x_position_2-x_position_1)**2 + (y_position_2-y_position_1)**2)
                # 피타고라스 법칙 점사이의 거리
                # print('피타고라스 법칙 점사이의 거리')
                # print(position_diffrence)

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
                        pyautogui.moveTo(x1+x_position_1, y1+y2_pop_1 + 1)
                        pyautogui.click()
                        # x -> 픽셀의 중앙점 y -> 이전박스의 경계선 +1 픽셀 클릭
                        time.sleep(1)
                        pyautogui.press('m')
                        time.sleep(1)
                        # 1픽셀 바깥쪽의 이미지를 클릭
                    else:
                        pyautogui.moveTo(x1+x_position_1, y1+y1_pop_1 - 1)
                        pyautogui.click()
                        # x -> 픽셀의 중앙점 y -> 이전박스의 경계선 -1 픽셀 클릭
                        time.sleep(1)
                        pyautogui.press('m')
                        time.sleep(1)
            
            box_repeat_1_copy -= 1