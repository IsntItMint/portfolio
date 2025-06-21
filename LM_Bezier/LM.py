import math
import numpy as np
import pandas as pd


# Bernstein basis polynomial
def basis(t, n, i):
    return math.comb(n-1, i) * ((1-t) ** (n-1-i)) * (t ** i)


# Bézier curve
# Bx(t, P), By(t, P) 출력
# 파라미터 t (0 <= t <= 1)
# P(Px, Py) 는 control point
# n 은 control point 의 갯수
def bezier(t, Px, Py, n):
    b = [basis(t, n, i) for i in range(n)]
    Bx = np.dot(b, Px)
    By = np.dot(b, Py)

    return Bx, By


# Bézier curve 의 Jacobian 출력
def bezierJacobian(t, Px, Py, n):
    # dBx/dPx 와 dBy/dPy 는 같은 값이기 떄문에 dBdP로 통일
    dBdP = np.array([basis(t, n, i) for i in range(n)])

    deltaPx = Px[1:] - Px[0:(n-1)]
    deltaPy = Py[1:] - Py[0:(n-1)]
    deltaBx, deltaBy = bezier(t, deltaPx, deltaPy, n-1)

    dBxdt = n*deltaBx
    dBydt = n*deltaBy

    return dBdP, dBxdt, dBydt


weight1 = 1000  # 페널티 함수의 weight. 아무 양수 지정. 숫자 커질 수록 더 큰 페널티
weight2 = 1000


# 페널티 함수 (t < 0 or t > 1 일 경우 페널티 부여)
# ti 가 단조증가가 아닐 때에도 페널티 부여
def penalty(t):
    N = len(t)
    g = np.zeros(N)

    for i in range(N):
        if t[i] > 1:
            g[i] += weight1*(t[i]-1.0)*(t[i]-1.0)
        elif t[i] < 0:
            g[i] += weight1*t[i]*t[i]
    for i in range(1, N):
        if t[i-1] > t[i]:
            g[i] += weight2*(t[i-1]-t[i])*(t[i-1]-t[i])

    return g


# 페널티 함수의 Jacobian
def penaltyJacobian(t):
    N = len(t)
    dgdt = np.zeros((N, N))

    for i in range(N):
        if t[i] > 1:
            dgdt[i, i] = 2*weight1*(t[i]-1.0)
        elif t[i] < 0:
            dgdt[i, i] = 2*weight1*t[i]
    for i in range(1, N):
        if t[i-1] > t[i]:
            deltag = 2*weight2*(t[i-1]-t[i])
            dgdt[i, i] -= deltag
            dgdt[i, i-1] += deltag

    return dgdt


# 목적함수 (페널티함수, Bx, By로 구성)
def LMProblem(theta, N, n):
    t = theta[:N]
    Px = theta[N:(N+n)]
    Py = theta[(N+n):]
    f = np.zeros(3*N)

    f[:N] = penalty(t)
    for i, ti in enumerate(t):
        Bx, By = bezier(ti, Px, Py, n)
        f[N+i] = Bx
        f[2*N+i] = By
    return f


# 목적함수의 Jacobian
def LMJacobian(theta, N, n):
    t = theta[:N]
    Px = theta[N:(N+n)]
    Py = theta[(N+n):]
    J = np.zeros((3*N, N + 2*n))

    J[:N, :N] = penaltyJacobian(t)
    for i, ti in enumerate(t):
        dBdP, dBxdt, dBydt = bezierJacobian(ti, Px, Py, n)

        J[N+i, i] = dBxdt
        J[2*N+i, i] = dBydt
        J[N+i, N:(N+n)] = dBdP
        J[2*N+i, (N+n):(N+2*n)] = dBdP

    return J


# 파라미터의 초기 guess
# 파라미터는 t, Px, Py로 구성 (0 <= t <= 1)
def LMInitialGuess(f0, N, n):
    theta = np.zeros(N + 2*n)
    theta[:N] = np.linspace(0, 1.0, N)

    idx = np.linspace(0, N-1, n, dtype=int)
    x = f0[N:2*N]
    y = f0[2*N:]

    theta[N:(N+n)] = x[idx]
    theta[(N+n):] = y[idx]

    return theta


if __name__ == "__main__":
    df = pd.read_csv("data/points.csv")  # 피팅 시키고자 하는 모의실험 데이터
    N = df.shape[0]
    f0 = np.zeros(3*N)
    f0[N:2*N] = df.iloc[:, 0].values
    f0[2*N:] = df.iloc[:, 1].values

    AIC = [None]*(21 - 3)

    lmd = 1.0  # damping parameter lamdba
    maxitr = 100
    for n in range(3, 21):
        # initial guess
        theta = LMInitialGuess(f0, N, n)

        # initial state
        f = LMProblem(theta, N, n)
        r = f0 - f
        sqsum = np.dot(r, r)
        J = LMJacobian(theta, N, n)

        itr = 0
        while itr < maxitr:
            # LM update step
            K = J.T@J + lmd * np.eye(N+2*n)
            dtheta = np.linalg.solve(K, J.T@r)

            # new state
            thetanew = theta + dtheta
            fnew = LMProblem(thetanew, N, n)
            rnew = f0 - fnew
            sqsumnew = np.dot(rnew, rnew)

            # 수렴 여부 판단, damping parameter 조정
            if sqsumnew < sqsum:
                theta = thetanew
                f = fnew
                r = rnew
                sqsum = sqsumnew
                J = LMJacobian(theta, N, n)
                lmd *= 0.5
            else:
                lmd *= 2.0

            itr += 1

        # AIC 계산
        AIC[n-3] = 2*n + sqsum

        # control point 저장
        Px = theta[N:(N+n)]
        Py = theta[(N+n):]
        df_ctrl = pd.DataFrame({'Px': Px, 'Py': Py})
        df_ctrl.to_csv(f"result/ctrl_n{n}.csv", index=False)

        print(f"n = {n}, AIC = {AIC[n-3]}")

    # AIC 저장
    df_AIC = pd.DataFrame(AIC, columns=["AIC"], index=range(3, 21))
    df_AIC.to_csv("result/AIC.csv")
