# HRRN 알고리즘 구현

# input Data 읽기
f = open("input.txt", mode='r')

input_data = []
for i in f.readlines():
    input_data.append(list(map(int, i.split())))


# 프로그램이 돌면서 left_time, arrival_time, R(응답 비율) 3개의 필드를 추가
# index
# 0 : type
# 1 : process_id
# 2 : priority
# 3 : computing_time
# 4 : left_time
# 5 : arrival_time
# 6 : R

# 프로그램 동작 시간
time = 0

# 프로그램 동작

ready = []  # 프로세스 준비 큐

# R값을 구하고, R으로 정렬 후 반환하는 함수
def sort_ready(ready : list, now_time : int):
    for i in ready:
        i[6] = ((now_time - i[5]) + i[3])/i[3]
    ready.sort(key=lambda x : -x[6])
    return ready

# 스케줄링 함수
def scheduling(ready : list, t : int, now_time : int):
    if len(ready)==0:
        return ready, now_time
    while(t != 0):
        if (ready[0][4] > t):
            ready[0][4] -= t
            now_time += t
            t = 0
        else:
            t -= ready[0][4]
            now_time += ready[0][4]
            ready[0][4] = 0
            print(ready.pop(0))
            ready = sort_ready(ready, now_time)
            if len(ready) == 0:
                return ready, now_time
    return ready, now_time



for data in input_data:
    # data의 type 확인 후 진행
    if data[0] == 0:
        data.append(data[3])    # 초기 left_time 삽입은 computing_time
        data.append(time)          # 초기 arrival_time은 현재 진행시간 t
        data.append(1)          # 초기 R(응답 비율)은 1
        ready.append(data)
    elif data[0] == 1:
        ready, time = scheduling(ready, 20, time)
    else:
        # 입력 종료
        print("입력 종료")
        while (len(ready) != 0):
            ready, time = scheduling(ready, ready[0][4], time)





