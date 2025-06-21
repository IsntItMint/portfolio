# Bézier Curve Fitting

본 프로젝트는 비선형 최적화 기법인 Levenberg–Marquardt (LM) Method 의 구현 예시로,  
Bézier 곡선을 2차원 데이터에 피팅하는 Python 기반 시뮬레이션입니다.  
모델 복잡도에 따른 AIC (Akaike Information Criterion)를 계산하여  
최적 제어점 개수를 자동 선택할 수 있도록 설계되었습니다.

---

## 구성 파일

- `LM.py`:  
  Bézier 곡선과 LM 최적화 구현.  
  `if __name__ == "__main__"` 블록에서 최적화를 수행하고 제어점을 `result/ctrl_n{n}.csv`에 저장합니다.

- `plot.py`:  
  `points.csv`와 최적화된 제어점으로 Bézier 곡선과 제어점을 시각화합니다.  
  `fig/plot_n{n}.png` 이미지로 저장됩니다.

- `plotAIC.py`:  
  제어점 수에 따른 AIC 값을 시각화한 그래프를 출력합니다 (`fig/AIC.png`).

---

## 사용 방법

```bash
# 1.최적화 실행
$ python LM.py

# 2. Bézier 곡선 시각화
$ python plot.py

# 3. AIC 곡선 시각화
$ python plotAIC.py
```

---

## 사용된 Python 라이브러리

    - numpy
    - pandas
    - matplotlib
