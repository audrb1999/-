import os
import cv2
import numpy as np

file_names = list(range(0, 13))
train = []
train_labels = []# 데이터 라벨 설정

for file_name in file_names:
    path = 'training_data/' + str(file_name) + '/'
    file_count = len(os.listdir('training_data/' + str(file_name) + '/'))# 총 이미지 갯수를 읽어롬
    for i in range(1, file_count + 1):# 그 이미지 갯수만큼 반복
        img = cv2.imread(path + str(i) + '.png')


        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)# 읽은 파일을 흑백으로 바꿈
        train.append(gray)#
        train_labels.append(file_name)


x = np.array(train)
train = x[:, :].reshape(-1, 400).astype(np.float32)# 20x20 을 1차원으로 변경
train_labels = np.array(train_labels)[:, np.newaxis]# 2차원으로 변형

print(train.shape)# 우리가 수집한 데이터, 24개에 길이 400
print(train_labels.shape)

np.savez('train.npz', train = train, train_labels = train_labels)#데이터 셋 저장!

