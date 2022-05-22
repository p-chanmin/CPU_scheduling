# HRRN 알고리즘 구현


# R값을 구하고, R으로 정렬 후 반환하는 함수
# 입력 파라미터 ( 준비큐, 현재 시간 )
def sort_ready(ready : list, now_time : int):
    # 준비큐를 돌면서 R값 갱신
    for i in ready:
        # R값 계산하여 저장
        i[6] = ((now_time - i[5]) + i[3])/i[3]
    # R값이 큰 순서로 정렬, R값이 같은 경우 도착한 시간이 빠른 순서로 정렬
    ready.sort(key=lambda x : (-x[6], x[5]))
    # 준비큐 반환
    return ready

# 프로세스 종료 시 해당 프로세스 정보를 출력하고
# turn_around_time, normalized_turnaround_time 반환하는 함수
# 입력 파라미터 ( 종료 된 프로세스, 현재 시간 )
def end_process(p : list, now_time : int):
    # process_id, priority, computiong_time, turn_around_time, normalized_turnaround_time 출력
    print(f"{p[1]:^11}|{p[2]:^10}|{p[3]:^17}|{now_time-p[5]:^18}|{p[6]:^28}|")
    return now_time-p[5], p[6] # turn_around_time, normalized_turnaround_time 반환

# 스케줄링 함수
# 입력 파라미터 ( 준비큐, 스케줄링 할 시간, 현재 시간, turn_around_time을 저장할 리스트, normalized_turnaround_time을 저장할 리스트 )
def scheduling(ready : list, t : int, now_time : int, turn_around_time : list, normalized_turnaround_time : list):
    # 준비큐가 비어있으면 스케줄링 하지 않고 그대로 반환
    if len(ready)==0:
        return ready, now_time
    # 스케줄링 시간이 0이 될 때까지 스케줄링 반복
    while(t != 0):
        # 스케줄링 시간 t가 남은 시간보다 작다면
        # 프로세스가 끝나지 않고 시간 종료
        if (ready[0][4] > t):
            ready[0][4] -= t    # 프로세스의 남은 시간에서 t를 빼서 갱신
            now_time += t       # 현재 시간을 t만큼 증가
            t = 0               # t는 모두 작업 했으므로 0
        # 스케줄링 시간 t가 남은 시간보다 크다면
        # 최소 한 개 이상의 프로세스가 종료 됨을 의미
        else:
            t -= ready[0][4]    # t에서 프로세스의 남은 시간을 빼서 갱신
            now_time += ready[0][4] # 남은 시간만큼 현재시간이 증가 했으므로 갱신
            ready[0][4] = 0     # 남은 시간은 모두 소모되어 0
            # 출력
            # 준비큐의 맨 앞에 있는 종료된 프로세스 제거 후 출력
            # 이때 turn_around_time, normalized_turnaround_time을 반환
            tat, ntat = end_process(ready.pop(0), now_time)
            # 각각 list에 저장
            turn_around_time.append(tat)
            normalized_turnaround_time.append(ntat)
            # 프로세스가 종료되었기 때문에 다음 우선순위의 프로세스를 찾기 위해
            # R값을 갱신하면서 준비큐를 정렬하는 sort_ready 함수 실행
            ready = sort_ready(ready, now_time)
            # 준비큐가 비어 있다면 그대로 반환 t가 남아 있더라도 그대로 반환
            if len(ready) == 0:
                return ready, now_time
    # 스케줄링이 완료되면 반환
    return ready, now_time


#### 프로그램 시작 ####
# input Data 읽기
path = input("input data의 절대경로 입력 : ")
f = open(path, mode='r')
# 한 줄 씩 읽으면서 int형으로 변환하여 input_data에 삽입
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

# 프로그램 동작 시간 초기값 0
now_time = 0

# 프로그램 동작
ready = []  # 프로세스 준비큐
turn_around_time = []   # turn_around_time을 저장할 리스트
normalized_turn_around_time = [] # normalized_turnaround_time을 저장할 리스트

# 출력 형태
print("HRRN 알고리즘 출력 결과")
print("process_id | priority | computiong_time | turn_around_time | normalized_turnaround_time |")

# input_data 하나씩 읽어들이면서 프로그램 동작
for data in input_data:
    # data의 type 확인 후 진행
    if data[0] == 0:    # data의 type이 0일 경우 프로세스 입력
        # left_time, arrival_time, R(응답 비율) 3개의 필드를 추가
        data.append(data[3])      # 초기 left_time 삽입은 computing_time
        data.append(now_time)     # 초기 arrival_time은 현재 진행시간 t
        data.append(1.0)          # 초기 R(응답 비율)은 1.0
        ready.append(data)        # 준비큐에 삽입

    elif data[0] == 1:  # type이 1일 경우 20의 시간이 흐름, 20만큼 스케줄링
        ready, now_time = scheduling(ready, 20, now_time, turn_around_time, normalized_turn_around_time)

    else:   # type이 -1, 혹은 그 외 값이 들어올 경우, 입력 종료를 의미
        # 준비큐에 남은 프로세스가 없을 때 까지 스케줄링
        # 이때 HRRN은 비선점 모드이므로 준비큐에서 우선순위가 제일 높은 프로세스의
        # 남은 시간만큼 스케줄링 시작
        while (len(ready) != 0):
            ready, now_time = scheduling(ready, ready[0][4], now_time, turn_around_time, normalized_turn_around_time)

# 스케줄링 완료
print("----------------------------------------------------------------------------------------")
print("프로세스 스케줄링 종료")
print(f"average_turn_around_time : {sum(turn_around_time)/len(turn_around_time)}")
print(f"normalized_average_turn_around_time : {sum(normalized_turn_around_time)/len(normalized_turn_around_time)}")






