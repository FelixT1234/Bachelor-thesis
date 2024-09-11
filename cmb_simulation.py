import matplotlib.pyplot as plt
import numpy as np

font = {'size'   : 12}
plt.rc('font', **font)

# simulated values
planck_sim = np.loadtxt("class-output/base-planck00_cl_lensed.dat")
# change_w1 = np.loadtxt("class-output/planck_w-fld--1.100_cl_lensed.dat")
# change_w2 = np.loadtxt("class-output/planck_w-fld--1.200_cl_lensed.dat")
# change_w1_H0 = np.loadtxt("class-output/planck_w-fld--1.1_H0-69.5400_cl_lensed.dat")

# measured values
planckValuesTT = np.loadtxt("planck-data/values_Planck_TT.txt")
planckValuesTE = np.loadtxt("planck-data/values_Planck_TE.txt")
planckValuesEE = np.loadtxt("planck-data/values_Planck_EE.txt")

spectrum = input("specify power spectrum (TT, TE, EE): ")
if spectrum == "TE":
    index = 1 # index specifies the column for the required data
    maxRange = 1994 # maxRange is the amount of values in that column
elif spectrum == "EE":
    index = 2
    maxRange = 1994
else:
    spectrum = "TT"
    index = 0
    maxRange = 2499

l = planck_sim[:, 0]
C_planck_sim = [planck_sim[:, 1], planck_sim[:, 4], planck_sim[:, 2]]

C_planck = [planckValuesTT[:2499, 1], planckValuesTE[:, 1], planckValuesEE[:, 1]]
l_planck = [planckValuesTT[:2499, 0], planckValuesTE[:, 0], planckValuesEE[:, 0]]
ERROR_Planck_pos = [planckValuesTT[:2499, 3], planckValuesTE[:, 3], planckValuesEE[:, 3]]
ERROR_Planck_neg = [planckValuesTT[:2499, 2], planckValuesTE[:, 2], planckValuesEE[:, 2]]

# C_change_w1 = [change_w1[:, 1], change_w1[:, 4], change_w1[:, 2]]
# C_change_w2 = [change_w2[:, 1], change_w2[:, 4], change_w2[:, 2]]
# C_change_w1_H0 = [change_w1_H0[:, 1], change_w1_H0[:, 4], change_w1_H0[:, 2]]

fig, (ax0, ax1) = plt.subplots(2, 1, gridspec_kw={'height_ratios': [3, 1]})

ax0.errorbar(l_planck[index], C_planck[index], yerr = [ERROR_Planck_neg[index], ERROR_Planck_pos[index]], color="#025fa1", label="Planck measurement", fmt=".", markersize="3", ecolor="#78bf7d", alpha=0.7, capsize=2, zorder=2)
ax0.plot(l, C_planck_sim[index], color="red", label="Simulated CMB", linewidth="2", zorder=3)
# ax0.plot(l, C_change_w1[index], color="#ffc31f", label=r"$w_{\Lambda}^{(1)} = -1.1$", linewidth="2", zorder=5)
# ax0.plot(l, C_change_w2[index], color="#b51f92", label=r"$w_{\Lambda}^{(2)} = -1.2$", linewidth="2", zorder=4)
# ax0.plot(l, C_change_w1_H0[index], color="#4a0134", label="$H_0 = 69.54$\n$w_{\Lambda}^{(1)} = -1.1$", linewidth="2", zorder=5)


difference_Planck = [C_planck[index][pos] - value for pos, value in enumerate(C_planck_sim[index][:maxRange])]
# difference_change_w1 = [C_change_w1[index][pos] - value for pos, value in enumerate(C_planck_sim[index])]
# difference_change_w2 = [C_change_w2[index][pos] - value for pos, value in enumerate(C_planck_sim[index])]
# difference_change_w1_H0 = [C_change_w1_H0[index][pos] - value for pos, value in enumerate(C_planck_sim[index])]

ax1.errorbar(l_planck[index][:maxRange], difference_Planck, yerr= [ERROR_Planck_neg[index][:maxRange], ERROR_Planck_pos[index][:maxRange]], color="#025fa1", fmt=".", ecolor="#78bf7d", alpha=0.7, capsize=2, markersize="3", zorder=2)
# ax1.plot(l, difference_change_w1, color="#ffc31f", zorder=4, linewidth="2")
# ax1.plot(l, difference_change_w2, color="#b51f92", zorder=4, linewidth="2")
# ax1.plot(l, difference_change_w1_H0, color="#4a0134", zorder=5, linewidth="2")
ax1.hlines(0, xmin=1, xmax=2500, color="red", zorder=3)

ax1.set_xlabel(r"$\ell$")
ax0.set_ylabel(f'$\mathcal{{D}}^{{{spectrum}}}_\ell$ [$\mu $K$^2$]')
ax1.set_ylabel(f'$\Delta \mathcal{{D}}^{{{spectrum}}}_\ell$ [$\mu $K$^2$]')
yabs_max = abs(max(difference_Planck, key=abs)) # difference_Planck has to be interchanged with the most drastic parameter change to accurately show the difference
yabs_max *= 1.3
ax1.set_ylim(ymin=-yabs_max, ymax=yabs_max)

ax0.set_xlim(xmin=0, xmax=2500)
ax1.set_xlim(xmin=0, xmax=2500)
ax0.minorticks_on()
ax1.minorticks_on()
ax0.grid(which="both")
ax1.grid(which="minor", axis="x")
ax1.grid(which="major", axis="both")
if spectrum == "TT":
    ax0.legend(loc="upper right")

plt.savefig(f"[filename]_{spectrum}.pdf", bbox_inches="tight")
plt.show()
