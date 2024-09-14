import matplotlib.pyplot as plt
import matplotlib.ticker as tck
import numpy as np
import pickle

font = {'size'   : 14}
plt.rc('font', **font)

a_rm = 2.952*10**(-4)
a_mLambda = 0.7729

a_mLambda_w1 = 0.7911
a_mLambda_w2 = 0.8068
a_mLambda_w1_H0 = 0.7911

def getDataFromFile(filename):
    with open(filename, "rb") as handle:
        return pickle.load(handle)
    
def getTimeForScaleFactor(a, listOfT, listOfA):
    for pos, value in enumerate(listOfA):
        if value > a:
            ALarger = value
            if pos != 0:
                ASmaller = listOfA[pos-1]
            else: 
                return listOfT[pos]
            if np.abs(ALarger-a) < np.abs(ASmaller-a):
                return listOfT[pos]
            else:
                return listOfT[pos-1]
    return None

def ticks(value, pos):
    if value == 1 or value == 10:
        return f'{value:.0f}'
    else:
        return f'$10^{{{int(np.log10(value))}}}$'

# ------ data from the numeric approximation:
benchmark_t = getDataFromFile("benchmark_data_t.txt")
benchmark_a = getDataFromFile("benchmark_data_a.txt")
# change_w1_t = getDataFromFile("change_w-1.1_data_t.txt")
# change_w1_a = getDataFromFile("change_w-1.1_data_a.txt")
# change_w2_t = getDataFromFile("change_w-1.2_data_t.txt")
# change_w2_a = getDataFromFile("change_w-1.2_data_a.txt")
# change_w1_H0_t = getDataFromFile("change_w-1.1_H0-69.54_data_t.txt")
# change_w1_H0_a = getDataFromFile("change_w-1.1_H0-69.54_data_a.txt")
# ------------


# ------ times for equilibria:
t_0 = 13.79 # From Planck
t_rm = getTimeForScaleFactor(a_rm, benchmark_t, benchmark_a)
t_mLambda = getTimeForScaleFactor(a_mLambda, benchmark_t, benchmark_a)
# t_mLambda_w1 = getTimeForScaleFactor(a_mLambda_w1, change_w1_t, change_w1_a)
# t_mLambda_w2 = getTimeForScaleFactor(a_mLambda_w2, change_w2_t, change_w2_a)
# t_mLambda_w1_H0 = getTimeForScaleFactor(a_mLambda_w1_H0, change_w1_H0_t, change_w1_H0_a)
# ------------

# ------- plot graphs, including settings:
fig, axs = plt.subplots()
axs.loglog(benchmark_t, benchmark_a, label="Benchmark model", color="red")
# axs.loglog(change_w1_t, change_w1_a, label="$w_{\Lambda}^{(1)} = -1.1$", color="#ffc31f", zorder=4)
# axs.loglog(change_w2_t, change_w2_a, label="$w_{\Lambda}^{(2)} = -1.2$", color="#b51f92", zorder=4)
# axs.loglog(change_w1_H0_t, change_w1_H0_a, label="$H_0 = 69.54$\n$w_{\Lambda}^{(1)} = -1.1$", color="#4a0134", zorder=5)

axs.set_xscale("log", base=10)
axs.set_yscale("log", base=10)
axs.xaxis.set_major_formatter(tck.FuncFormatter(ticks))
axs.yaxis.set_major_formatter(tck.FuncFormatter(ticks))

# --- set dashed lines for equilibria:
axs.vlines(x=t_0*10**9, ymin=10**(-6), ymax=1, color="black", linewidth=1, linestyle="dashed")
axs.text(t_0*10**9+10**9.5, 10**(-3), r"$t_0$", color="black")
axs.hlines(y=1, xmin=10**(-10), xmax=t_0*10**9, color="black", linewidth=1, linestyle="dashed")

axs.vlines(x=t_rm, ymin=10**(-6), ymax=a_rm, color="black", linewidth=1, linestyle="dashed")
axs.text(t_rm+10000, 10**(-5), r"$t_{rm}$", color="black")
axs.hlines(y=a_rm, xmin=10**(-10), xmax=t_rm, color="black", linewidth=1, linestyle="dashed")

axs.vlines(x=t_mLambda, ymin=10**(-6), ymax=a_mLambda, color="black", linewidth=1, linestyle="dashed")
axs.text(t_mLambda-10.09**9.9, 10**(-3), r"$t_{m\Lambda}$", color="black")
axs.hlines(y=a_mLambda, xmin=10**(-10), xmax=t_mLambda, color="black", linewidth=1, linestyle="dashed")


# axs.vlines(x=t_mLambda_w1, ymin=10**(-6), ymax=a_mLambda_w1, color="#ffc31f", linewidth=1, linestyle="dashed")
# axs.text(t_mLambda_w1-10**9.9, 10**(-2), r"$t_{m\Lambda}^{(1)}$", color="#ffc31f")
# axs.hlines(y=a_mLambda_w1, xmin=10**(-10), xmax=t_mLambda_w1, color="#ffc31f", linewidth=1, linestyle="dashed")

# axs.vlines(x=t_mLambda_w2, ymin=10**(-6), ymax=a_mLambda_w2, color="#b51f92", linewidth=1, linestyle="dashed")
# axs.text(t_mLambda_w2-10**9.9, 10**(-4), r"$t_{m\Lambda}^{(2)}$", color="#b51f92")
# axs.hlines(y=a_mLambda_w2, xmin=10**(-10), xmax=t_mLambda_w2, color="#b51f92", linewidth=1, linestyle="dashed")

# axs.vlines(x=t_mLambda_w1_H0, ymin=10**(-6), ymax=a_mLambda_w1_H0, color="#4a0134", linewidth=1, linestyle="dashed")
# axs.text(t_mLambda_w1_H0-10**9.9, 10**(-4), r"$t_{m\Lambda}^{(2)}$", color="#4a0134")
# axs.hlines(y=a_mLambda_w1_H0, xmin=10**(-10), xmax=t_mLambda_w1_H0, color="#4a0134", linewidth=1, linestyle="dashed")
# ------

axs.margins(x=0)
axs.yaxis.minorticks_off()
axs.xaxis.minorticks_on()
axs.tick_params(which="minor", axis="both")
axs.set_ylim([10**(-6), 10**(3)])
axs.set_xlim([1, None])
axs.set_ylabel("a")
axs.set_xlabel("t [yr]")
plt.legend(loc="upper left")
plt.grid()
plt.savefig("saved_images/[filename].pdf", bbox_inches="tight")
plt.show()
# ------------
