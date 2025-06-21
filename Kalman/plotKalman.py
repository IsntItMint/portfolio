from numpy import array, sqrt
import matplotlib.pyplot as plt


def plotKalman(t, z_true, z, z_hat, sigma, plotname):
    plt.figure(figsize=(6, 6))

    zvalue95 = 1.960  # Z value for 95% confidence
    n = len(t)
    confi = array([zvalue95*sigma/sqrt(i) for i in range(1, n+1)])  # 95% confidence range

    # fig = plt.figure()
    ax = plt.subplot(111)

    ax.plot(t, z_true, linestyle='-', marker='o', markersize=2, label='true')
    ax.plot(t, z, linestyle='-', marker='o', markersize=2, label='measured')
    ax.plot(t, z_hat, linestyle='-', marker='o', markersize=2, color='g', label='estimated')
    ax.fill_between(t, (z_hat-confi), (z_hat+confi), color='g', alpha=.33, label='95% confidence')

    ax.set_xlabel(r"$t_i$")
    ax.set_ylabel(r"$z_i$")
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.1), ncol=2)

    plt.tight_layout()
    plt.savefig(plotname)
    plt.show()

    return


def plotSim(t, z, plotname):
    # fig = plt.figure()
    ax = plt.subplot(111)

    ax.plot(t, z, linestyle='-', marker='o', markersize=2, label='measured')

    ax.set_xlabel("r$t_i$")
    ax.set_ylabel(r"$z_i$")
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.1), ncol=2)

    plt.tight_layout()
    plt.show()
    plt.savefig(plotname)

    return
