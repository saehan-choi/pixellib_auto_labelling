from pixellib.torchbackend.instance import instanceSegmentation
import pyscreenshot as ImageGrab
from collections import deque
from math import sqrt
import pyautogui
import time



# 화면 좌표 보고나서 이 변수만 변경해주면 됨
x1 = 76
y1 = 186
x2 = 2211
y2 = 1378

length_diffrence_limit = 80

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

arr = deque()
arr_num = deque()
position_x1_y1 = deque()

for j in range(540):
    results = image_process(x1,y1,x2,y2)
    boxes = results["boxes"]
    arr_num.append(len(boxes))

    for _ in range(len(boxes)):
        # 이게현재박스
        x1_2nd, y1_2nd, x2_2nd, y2_2nd = boxes[_][:]
        arr.extend([x1_2nd,y1_2nd,x2_2nd,y2_2nd])
        pyautogui.moveTo(x1+x1_2nd, y1+y1_2nd)
        pyautogui.press('n')
        time.sleep(0.1)
        pyautogui.click()
        time.sleep(0.1)
        pyautogui.move(x2_2nd-x1_2nd, y2_2nd-y1_2nd)
        time.sleep(0.1)
        pyautogui.click()
        # time.sleep(0.5)

#  박스가 내부에 들어오면 작동하지않음. . .
#  다수의 사람이 모여있을때 잘 동작하지 않음. . .
##################################################################
#       여기위론 x_position_1, y_position_1 이거없음  
        x_position_2, y_position_2 = x_y_center_position(x1_2nd, y1_2nd, x2_2nd, y2_2nd)
        if j == 0:
            pass
        else:
            position_x1_y1.extend([x_position_2, y_position_2])

    if j == 0:
        pass
    else:
        
        for k in range(arr_num[1]):
            x_position_2, y_position_2 = position_x1_y1.popleft(), position_x1_y1.popleft()
            for i in range(arr_num[0]):
                # 실제로는 이게 첫번째 박스네
                # print(arr)
                # print(f'arr_num : {arr_num}')
                x1_1st, y1_1st, x2_1st, y2_1st = arr[4*i+0], arr[4*i+1], arr[4*i+2], arr[4*i+3]
                # 이렇게하면 4번씩 돌아옴 0 1 2 3- 4 5 6 7 - ....
                x_position_1, y_position_1 = x_y_center_position(x1_1st, y1_1st, x2_1st, y2_1st)

                position_diffrence = sqrt((x_position_2-x_position_1)**2 + (y_position_2-y_position_1)**2)

                if position_diffrence > length_diffrence_limit:
                    pass
                else:
                    pyautogui.press('d')
                    time.sleep(0.05)
                    pyautogui.press('m')
                    # time.sleep(0.1)
                    pyautogui.moveTo(x1+x_position_1, y1+y_position_1)
                    pyautogui.click()
                    # 바운딩박스의 중앙점을 클릭
                    
                    time.sleep(0.1)
                    pyautogui.press('f')
                    time.sleep(0.1)
                    print(f'y_position_1:{y_position_1}')
                    print(f'y_position_2:{y_position_2}')
                    if y_position_2 < y_position_1:
                        pyautogui.moveTo(x1+x_position_1, y1+y1_1st - 1)
                        pyautogui.click()
                        # x -> 픽셀의 중앙점 y -> 이전박스의 경계선 +1 픽셀 클릭
                        # time.sleep(0.1)
                        pyautogui.press('m')
                        time.sleep(0.05)
                        # 1픽셀 바깥쪽의 이미지를 클릭
                    else:
                        pyautogui.moveTo(x1+x_position_1, y1+y2_1st + 1)
                        pyautogui.click()
                        # x -> 픽셀의 중앙점 y -> 이전박스의 경계선 -1 픽셀 클릭
                        # time.sleep(0.1)
                        pyautogui.press('m')
                        time.sleep(0.05)
            pyautogui.moveTo(x1, y1)    
        for z in range(4*arr_num[0]):
            del arr[0]
        del arr_num[0]
    pyautogui.press('f')