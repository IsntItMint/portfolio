# Kalman Filter Simulation Portfolio

본 프로젝트는 Kalman 필터의 기초 개념부터 비선형 시스템에 대한 확장까지 다양한 예제를 포함한 시뮬레이션 입니다.  

## 구현 예제

    - 정상 상태 추정 (Constant Model)  
    센서 노이즈 하의 상수 값을 추정하는 1차 Kalman 필터 구현.

    - **등가속도 운동 (Accelerated Motion)  
    등가속도 운동을 따르는 시스템의 위치를 Kalman 필터로 추정.

    - 진자의 비선형 운동 (Pendulum / EKF)  
    비선형 진자 운동에 대해 Extended Kalman Filter 기법을 적용하여 상태 추정.

---

## 사용 방법

```bash
# 정적 위치 추정 예제 실행
$ python Kalman_constant.py

# 등가속도 운동 추정 예제 실행
$ python Kalman_accel.py

# 진자 운동 (비선형 시스템) 추정 예제 실행
$ python Kalman_pendulum.py
```

실행 결과는 fig/ 디렉토리에 그래프로 저장되며, data/ 디렉토리에 시뮬레이션 데이터가 생성됩니다.

## 사용된 Python 라이브러리

    - numpy
    - scipy
    - matplotlib
