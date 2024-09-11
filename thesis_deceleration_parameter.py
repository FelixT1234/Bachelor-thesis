import matplotlib.pyplot as plt
import matplotlib.ticker as tck
import pickle
import numpy as np
from thesis_scale_factor import t_0, t_mLambda, t_rm

font = {'size'   : 14}
plt.rc('font', **font)

# parameters:
Omega_r0 = 9.240*10**(-5)
Omega_m0 = 0.3158
Omega_Lambda0 = 0.6841

def getDataFromFile(filename):
    with open(filename, "rb") as handle:
        return pickle.load(handle)

# ------- functions for the deceleration parameter:
def f(a):
    return (Omega_r0/(a**4) + Omega_m0/(2*a**3) - Omega_Lambda0)

def f_change_w1(a):
    try:
        return (Omega_r0/(a**4) + Omega_m0/(2*a**3) - Omega_Lambda0*a**(0.3))
    except OverflowError:
        return None

def f_change_w2(a):
    try:
        return (Omega_r0/(a**4) + Omega_m0/(2*a**3) - Omega_Lambda0*a**(0.6))
    except OverflowError:
        return None
# ------------

# ------ get deceleration parameter value or time value:
def getParameterForTime(t, listOfT, listOfQ):
    for pos, value in enumerate(listOfT):
        if value > t:
            tLarger = value
            tSmaller = listOfT[pos-1]
            if np.abs(tLarger-t) < np.abs(tSmaller-t):
                return listOfQ[pos]
            else:
                return listOfQ[pos-1]
    return None

def getTimeForParameter(q, listOfT, listOfQ):
    for pos, value in enumerate(listOfQ):
        if value < q:
            QLarger = value
            QSmaller = listOfQ[pos-1]
            if np.abs(QLarger-q) < np.abs(QSmaller-q):
                return listOfT[pos]
            else:
                return listOfT[pos-1]
    return None
# ------------

# ------ functions to set axis ticks:
def ticksY(value, pos):
    if np.abs(value) == 1 or value == 0:
        return f'{value:.0f}'
    elif value > 0 and int(np.log10(np.abs(value))) % 2 == 0:
        return f'$10^{{{int(np.log10(value))}}}$'
    elif value < 0 and int(np.log10(np.abs(value))) % 2 == 0:
        return f'$-10^{{{int(np.log10(-value))}}}$'
    else:
        return None

def ticksX(value, pos):
    if value == 1 or value == 10:
        return f'{value:.0f}'
    else:
        return f'$10^{{{int(np.log10(value))}}}$'
# ------------

# ------- values for the graphs:
benchmark_t = getDataFromFile("benchmark_data_t.txt")
benchmark_q = [f(a) for a in getDataFromFile("benchmark_data_a.txt")]

change_w1_t = getDataFromFile("change_w-1.1_data_t.txt")
change_w1_q = [f_change_w1(a) for a in getDataFromFile("change_w-1.1_data_a.txt")]

change_w2_t = getDataFromFile("change_w-1.2_data_t.txt")
change_w2_q = [f_change_w2(a) for a in getDataFromFile("change_w-1.2_data_a.txt")]

change_w1_H0_t = getDataFromFile("change_w-1.1_H0-69.54_data_t.txt")
change_w1_H0_q = [f_change_w1(a) for a in getDataFromFile("change_w-1.1_H0-69.54_data_a.txt")]
# ------------

fig, axs = plt.subplots()
axs.plot(benchmark_t, benchmark_q, label="Benchmark model", color="g", zorder=3)
# axs.plot(change_w1_t, change_w1_q, label="$w_\Lambda^{(1)} = -1.1$", color="#ffc31f", zorder=4)
# axs.plot(change_w2_t, change_w2_q, label="$w_\Lambda^{(2)} = -1.2$", color="#b51f92", zorder=4)
# axs.plot(change_w1_H0_t, change_w1_H0_q, label="$H_0 = 69.54$\n$w_{\Lambda}^{(1)} = -1.1$", color="#4a0134", zorder=5)

# ------ settings:
axs.set_yscale('symlog', linthresh=1)
axs.set_xscale("log", base=10)
axs.margins(x=0)

axs.yaxis.set_major_formatter(tck.FuncFormatter(ticksY))
axs.xaxis.set_major_formatter(tck.FuncFormatter(ticksX))

axs.set_xlabel("t [yr]")
axs.set_ylabel("q")
axs.set_xlim([1, None])
axs.set_ylim(bottom=-1.01)
# axs.set_ylim(bottom=-100.01)
for tick in axs.yaxis.get_major_ticks()[5::2]:
    tick.set_visible(False) # hide every second tick
axs.yaxis.get_major_ticks()[1].set_visible(False) # hide one specific tick

# --- plot vertical dashed lines:
axs.vlines(x=t_0, ymin=-100, ymax=getParameterForTime(t_0, benchmark_t, benchmark_q), color="black", linewidth=1, linestyle="dashed")
axs.text(t_0+10**9.5, -0.2, r"$t_0$", color="black")

axs.vlines(x=t_mLambda, ymin=-100, ymax=getParameterForTime(t_mLambda, benchmark_t, benchmark_q), color="black", linewidth=1, linestyle="dashed")
axs.text(t_mLambda-10**9.95, -0.7, r"$t_{m\Lambda}$", color="black")

axs.vlines(x=t_rm, ymin=-100, ymax=getParameterForTime(t_rm, benchmark_t, benchmark_q), color="black", linewidth=1, linestyle="dashed")
axs.text(t_rm+10000, 10**4, r"$t_{rm}$", color="black")

axs.hlines(y=1, xmin=1, xmax=axs.get_xlim()[1], color="black", linewidth=1, label="Change of scale", zorder=2)
axs.hlines(y=-1, xmin=1, xmax=getTimeForParameter(-1, change_w1_t, change_w1_q), color="black", linewidth=1, zorder=2)
# ------

axs.legend(loc="upper right")
axs.grid(True, which="major", axis="both")
plt.savefig("saved_images/[filename].pdf", format="pdf", bbox_inches="tight")
plt.show()
# ------------