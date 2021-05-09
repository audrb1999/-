import cv2
import numpy as np
import re


BLUE = 0  # bgr 순서
GREEN = 1
RED = 2


# 특정한 색상의 모든 단어가 포함된 이미지를 추출합니다.
# 어떠한 색상이 들어왔다하면
# blue(0)가 들어왔다하면 그것과 다른 두 가지 색을 고름
def get_chars(image, color):
    other1 = (color + 1) % 3  # 이것을 통해 다른 두 가지를 고름 Green
    other2 = (color + 2) % 3  # red

    c = image[:, :, other1] == 255  # (FF) = 255 다른 색깔들은 제거 순수 green 제거
    image[c] = [0, 0, 0]  # 000으로 만듬

    c = image[:, :, other2] == 255  # 순수 red 제거
    image[c] = [0, 0, 0]

    # 그리고 색깔 두 개가 겹치는 곳을 따로 제거해줌
    c = image[:, :, color] < 170  # 파란색 값이 부족하면 없앰 파란색과 섞이면 괜찮지만 red green이 섞인 것들은 제거
    image[c] = [0, 0, 0]

    c = image[:, :, color] != 0  # 파란색이 0이 아닌것들은 흰색으로 바꿈
    image[c] = [255, 255, 255]

    return image

def extract_chars(image):
    chars = []
    colors = [BLUE, GREEN, RED]# 색깔별로 모든 이미지를 추출할 수 있게함!
    for color in colors:
        image_from_one_color = get_chars(image.copy(), color)# 색상별로 숫자 이미지 추출 추출된 넘파이 객체 저장
        image_gray = cv2.cvtColor(image_from_one_color, cv2.COLOR_BGR2GRAY)#그레이로 적용
        ret, thresh = cv2.threshold(image_gray, 127, 255, 0)# 그 다음 threshold로 바이너리 처리 > 컨투어를 쓰기위한 준비
        # RETR_EXTERNAL; 옵션으로 숫자의 외각을 기준으로 분리
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:# 추출 후 약간 의미없는 하얀 픽셀들이 생기는데 그걸 제거
            # 추출된 이미지 크기가 50이상인 경우만 실제 문자 데이터인 것으로 파악 작은 픽셀 지우기
            area = cv2.contourArea(contour)#픽셀 크기 측정
            if area > 50:
                x, y, w, h = cv2.boundingRect(contour)
                roi = image_gray[y:y + h, x:x + w]#숫자에 해당하는 부분만 뽑기 위해서 roi를 이용!
                chars.append((x, roi))

    chars = sorted(chars, key = lambda char:char[0])# 추출 이미지를 x축으로 정렬
    return chars

# 특정 이미지를 (20x20)크기로 Scaling 합니다.
def resize20(image):
    resized = cv2.resize(image, (20, 20))
    return resized.reshape(-1, 400).astype(np.float32)

# 문자열 형태로 계산 = eval()함수
# 007 + 1 이런 경우, 00+7 이런경우에는 오류가 발생한다.
# 양 쪽에 있는 0을 지워주는 작업을 실행 > 7 + 1, 0 + 7
def remove_first_0(string):
    temp = []
    for i in string:
        if i == "+" or i == "-" or i =="*":
            temp.append(i)
    split = re.split('\*|\+|-', string)# 수식을 기준으로 값을 나눔 003 + 74면 [003, 74] 이렇게 정규식
    i = 0
    temp_count = 0
    result = ""
    for a in split: # 밑에껄 진행하다 연산자가 나오면 다시 붙임
        a = a.lstrip('0')# 왼쪽 0을 지움  left stirp
        if a == " ": # 만약 원래 0만 존재해서 0을 지웠을 때 빈 문자열이 남으면
            a = '0'# 0을 다시 넣음
        result += a# 0이 아닌건 다시 붙어넣음
        if i < len(split) - 1:
            result += temp[temp_count]
            temp_count = temp_count + 1
        i = i+1
    return result
