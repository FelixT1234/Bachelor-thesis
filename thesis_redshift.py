import scipy.integrate as integrate
import scipy.special as special
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import numpy as np

font = {'size'   : 12}
plt.rc('font', **font)

# parameters
Omega_r0 = 9.322*10**(-5)
Omega_m0 = 0.3158
Omega_Lambda0 = 0.6841
Omega_k0 = 1
H0_1 = 67.32*((3600*24*365)/((3.1*10**19)))
H0_2 = 69.54*((3600*24*365)/((3.1*10**19)))

#benchmark max-min
m_Omega_r0 = [9.142*10**(-5), 9.502*10**(-5)]
m_Omega_m0 = [0.308, 0.3226]
m_Omega_Lambda0 = [0.6774, 0.692]
m_H_0 = [66.82*((3600*24*365)/((3.1*10**19))), 67.9*((3600*24*365)/((3.1*10**19)))]

# constants
t_0 = 13.79
c0 = 299792458*((1.057*10**(-16))/(3.17098*10**(-8)))

def f_magnitude(d, M):
    magnitude = M + 5*np.log10(d)+25
    return magnitude

def getDistance(z, p, H_0):
    # calculates the luminosity distance
    def distance_integrand(a):
        return 1/((Omega_r0 + Omega_m0*a + Omega_Lambda0*(a**(4+p)))**(1/2))
    scale_factor = 1/(1+z)
    resultDistance1 = integrate.quad(distance_integrand, 1/(1+z), 1)[0]
    return (c0/(H_0*scale_factor*3.26156))*resultDistance1

# -------- measured data:
data = np.loadtxt("data_redshift.txt")
z_data = data[:, 0]
m_data = data[:, 2]
m_error = data[:, 3]
d_data = [getDistance(z, 0, H0_1) for z in z_data]
# -----------

# ------- curve fit:
parameters, covariance = curve_fit(f_magnitude, d_data, m_data, sigma=m_error, absolute_sigma=True)
fit_M = parameters[0]
error_M = np.sqrt(covariance[0][0])
print(fit_M, error_M)
fit = f_magnitude(z_data, fit_M)
z_th = np.arange(0.1, 0.9, 0.0001)
d_th = [getDistance(val_z, 0, H0_1) for val_z in z_th]
d_th2 = [getDistance(val_z, 0.3, H0_1) for val_z in z_th]
d_th3 = [getDistance(val_z, 0.3, H0_2) for val_z in z_th]
m = [f_magnitude(d_L, fit_M) for d_L in d_th]
m2 = [f_magnitude(d_L, fit_M) for d_L in d_th2]
m2 = [f_magnitude(d_L, fit_M) for d_L in d_th3]
# ----------

# ------ plot and settings:
fig, axs = plt.subplots()
axs.plot(z_th, m, label="Benchmark model", color="green", zorder=2)
axs.plot(z_th, m2, label="$w_\Lambda^{(1)} = -1.1$", color="#ffc31f", zorder=3)
axs.plot(z_th, m2, label="$H_0 = 69.54$\n$w_{\Lambda}^{(1)} = -1.1$", color="#4a0134", zorder=4)
axs.errorbar(z_data, m_data, yerr=m_error, label="SCP measurement", fmt=".", ecolor="grey", markersize="5", color="red", capsize=2, zorder=5)

axs.margins(x=0)
axs.set_xlabel(r"$z_{\text{em}}$")
axs.set_ylabel(r"$m_\text{peak}$")
axs.grid(which="both", axis="both")
axs.legend(loc="lower right")

plt.savefig("saved_images/[filename].pdf", format="pdf", bbox_inches="tight")
plt.show()
# ----------