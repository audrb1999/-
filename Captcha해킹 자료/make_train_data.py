import os
import cv2
import utils
#training_data 폴더 생성 및 그 내부에 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12 폴더 생성

image = cv2.imread('4.png')
chars = utils.extract_chars(image)# 색깔별 숫자 추출


for char in chars:
    cv2.imshow('Image', char[1])# 이미지 보여주고
    input = cv2.waitKey(0)
    resized = cv2.resize(char[1], (20, 20))# 크기 변경

# 사용자의 입력으로 라벨링함!
    if input >= 48 and input <=57:
        name = str(input - 48)
        file_count = len(os.listdir('./training_data/' + name + '/'))# 파일 이름이 안 겹치게 만드는 것 1 2 3 4 이렇게
        #사용자가 만들어준 디렉토리로 해당 데이터가 이동
        #확장자 지정 꼭 하자!
        cv2.imwrite('./training_data/' + str(input - 48) + '/' + str(file_count + 1) + '.png', resized)
        print('./training_data/' + str(input - 48) + '/' + str(file_count + 1) + '.png')
# 대문자 소문자 구분해서 누르기!
    elif input == ord('a') or input == ord('b') or input == ord('c'):#+ - * 경우는 (+,a), (-, b), (*, c)로 구분해서 만듬
        name = str(input - ord('a') + 10)
        file_count = len(os.listdir('./training_data/' + name + '/'))
        cv2.imwrite('./training_data/' + name + '/'+ str(file_count + 1) + '.png', resized)