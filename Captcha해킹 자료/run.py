import numpy as np
import cv2
import utils
import requests # 웹사이트와 손쉽게 연결할 수 있게 해줌
import shutil
import time

FILE_NAME = 'train.npz'# 데이터 셋 가져와서

#각 글자의 (1 x 400) 데이터와 정답 (0~9, +-*)
with np.load(FILE_NAME) as data:# 그 데이터 셋을 data라는 변수에 넣고
    train = data['train']# 옮겨 담음
    train_labels = data['train_labels']

knn = cv2.ml.KNearest_create()#knn 선언
knn.train(train, cv2.ml.ROW_SAMPLE, train_labels)#knn 학습

def check(test, train, train_labes):
    # test 이미지와 가장 가까운 레이블을 출력 k = 1인 이유는 모든 이미지가 동일한 크기, 동일한 모양이라서 가장 가까운거 하나 찾아도 됨!
    #가장 가까운 k개의 글자를 찾아, 어떤 숫자에 해당하는지 찾습니다. 테스트 데이터 갯수에 따라 조절
    ret, result, neighbours, dist = knn.findNearest(test, k=1)
    return result

def get_result(file_name):# 파일이 들어오면
    image = cv2.imread(file_name)
    chars = utils.extract_chars(image)# 각각의 이미지를 왼쪽부터 담고
    result_string = ""
    for char in chars:
        # 이미지를 400으로 쭉 늘어트리고 매치되는 데이터를 담음
        matched = check(utils.resize20(char[1]), train, train_labels)
        if matched < 10:
            # 숫자를 왼쪽부터 차례로 붙일 수 있게
            result_string += str(int(matched))
            continue
            
        if matched == 10:
            matched = "+"

        elif matched == 11:
            matched = "-"

        elif matched == 12:
            matched = "*"

        result_string += matched
    return result_string

# 최종적으로 이미지를 문자열로 반환
#print(get_result("3.png"))

#8:30

import requests # 웹사이트와 손쉽게 연결할 수 있게 해줌
import shutil
import time

host = 'http://localhost:10000'# 문제나오는 주소
url = '/start'# start(문제 풀기를 시작하면 나오는 링크)로 접속하기 위해서 설정

host = 'http://localhost:10000'# 문제나오는 주소
url = '/start'# start(문제 풀기를 시작하면 나오는 링크)로 접속하기 위해서 설정

# target_images라는 폴더 생성
with requests.Session() as s:# 해당 웹사이트에 접속
    answer = '' # 첫 번째에는 정답에 빈칸을 둠 > 문제를 스타트를 눌렀을 때는 정답을 보낼 필요가 없어
    for i in range(0, 100):# 실제에서는 문제를 100번 풀어야 됬기에 100으로 설정
        start_time = time.time()# 문제를 풀고 전송하는 시간을 알아보기위해 시간 설정
        params = {'ans':answer}# ans파라미터에 answer값을 넣어서 전송함

        # 정답을 피라미터에 달아서 전송하여, 이미지 경로를 받아옵니다.
        response = s.post(host + url, params)# 해당 url에 포스트 방식으로 접속을 함
        print('Server Return:' + response.text)# 서버로부터 리턴값을 받아옴
        if i ==0:# 첫번째에는 바로 이미지 url이 나와서
            returned = response.text
            image_url = host+ returned# 그걸 바로 받아옴 이후 연산
            url = '/check'# 그 후 url값을 check으로 바꿔줌 > 정답코드를 제출할 url이 check이기 때문

        else:
            returned = response.json()# 1번째가 아닌 경우 json형태로 서버로부터 데이터가 들어오고
            image_url = host + returned['url']# 이미지 url 정보

        print('Problem' + str(i)+ ':' + image_url)

        # 특정한 폴더에 이미지 파일을 다운로드 받습니다.
        response = s.get(image_url, stream = True)# 이미지 파일 다운
        target_image = './target_images/'+str(i)+'.png' # 이미지를 타겟 디렉토리에 저장
        with open(target_image, 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
        del response

        # 다운로드 받은 이밎 파일을 분석하여 답을 도출합니다.
        answer_string = get_result(target_image)#이미지에 대한 string 값을 구하고
        print('String:' + answer_string) # 2 + 0 인경우 2+ 이렇게 되버림
        answer_string = utils.remove_first_0(answer_string)# 수를 정제
        answer = str(eval(answer_string))# 계산 > 이게 다음번 호출 때 전달 됨!
        print('Answer:' + answer) # 결과 출력!
        print(f'---{time.time()-start_time} seconds---')
