from pixellib.torchbackend.instance import instanceSegmentation
import pyscreenshot as ImageGrab
from collections import deque
from math import sqrt
import pyautogui
import time

###################### 주의 ############################
############사람이 나타나는 시점에서는 잘 동작하지않음 ㅠㅠ
########################################################

# 화면 좌표 보고나서 이 변수만 변경해주면 됨
x1 = 76
y1 = 186
x2 = 1145
y2 = 1028

# length_diffrence_limit = 80

# 여기는 merge안되서 옮겨놓을 오른쪽 위 좌표 ( 상가있는쪽에 놔두면 편하겠다 )
# 
x3 = 1289
y3 = 515

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
num_box = deque()
for j in range(540):
    results = image_process(x1,y1,x2,y2)
    boxes = results["boxes"]
    num_box.append(len(boxes))
    center_xy_2nd = deque()

    for _ in range(num_box[-1]):
        # 이게현재박스
        x1_2nd, y1_2nd, x2_2nd, y2_2nd = boxes[_][:]
        arr.extend([x1_2nd,y1_2nd,x2_2nd,y2_2nd])
        if j == 0:
            pass
        else:
            center_xy_2nd.extend([(x_y_center_position(x1_2nd, y1_2nd, x2_2nd, y2_2nd))])
        pyautogui.moveTo(x1+x1_2nd, y1+y1_2nd)
        pyautogui.press('n')
        time.sleep(0.1)
        pyautogui.click()
        time.sleep(0.1)
        pyautogui.move(x2_2nd-x1_2nd, y2_2nd-y1_2nd)
        time.sleep(0.1)
        pyautogui.click()
        # time.sleep(0.5)
    pyautogui.hotkey('t', 'h')
    time.sleep(0.1)
    if j == 0:
        pass
    else:
        pyautogui.hotkey('t', 'h')
        num_b = num_box.popleft()
        for _ in range(num_b):
            pyautogui.press('d')
            
            x1_1st, y1_1st, x2_1st, y2_1st = arr.popleft(), arr.popleft(), arr.popleft(), arr.popleft()
            center_x, center_y = x_y_center_position(x1_1st, y1_1st, x2_1st, y2_1st)
            pyautogui.moveTo(x1+center_x, y1+center_y)
            pyautogui.dragTo(x1+x3,y1+y3)
            # merge가 제대로 안되니깐 처음박스를 오른쪽위에다 옮기고 머지한다음 다시 재위치에 갖다놓자

            pyautogui.press('m')
            time.sleep(0.1)
            pyautogui.click()
            time.sleep(0.1)
            pyautogui.press('f')
            time.sleep(0.1)
            minimum_diffrence = []
            print(f'center_xy_2nd: {center_xy_2nd}')
            print(f'len(center_xy_2nd): {len(center_xy_2nd)}')
            for a in range(len(center_xy_2nd)):
                position_diffrence = sqrt((center_xy_2nd[a][0]-center_x)**2 + (center_xy_2nd[a][1]-center_y)**2)
                minimum_diffrence.append(position_diffrence)
            minumun_idx = minimum_diffrence.index(min(minimum_diffrence))

            pyautogui.moveTo(x1+center_xy_2nd[minumun_idx][0], y1+center_xy_2nd[minumun_idx][1])
            # 여기서는 최소 거리를 가지는 좌표로 이동해야함
            time.sleep(0.1)
            pyautogui.click()
            time.sleep(0.1)
            pyautogui.press('m')
            time.sleep(0.1)

            pyautogui.press('d')
            pyautogui.moveTo(x1+x3, y1+y3)
            pyautogui.dragTo(x1+center_x, y1+center_y)
            pyautogui.press('f')

        pyautogui.hotkey('t', 'h')
    pyautogui.press('f')
    time.sleep(0.1)
    
    
# -------------------------
# 이거 이렇게 하려다가 더 좋은방식 생각남 마우스커서로 처음위치를 옮기자
# 위치를 옮기는 이유는 중앙에 클릭시 그다음박스가 같은곳에 겹쳐질때 적용이 안되서 그럼.
# 아 근데 맨처음에 내가하려는 방식이 옳은듯 그대로가자
# 왜냐면 이렇게하니깐 다른사람들이랑 겹쳐짐...


    # for _ in range(len(boxes)):
    #     arr.popleft