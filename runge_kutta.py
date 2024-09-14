import pickle
import scipy.integrate as integrate

# parameters:
Omega_r0 = 9.240*10**(-5)
Omega_m0 = 0.3158
Omega_Lambda0 = 0.6841
Omega_k0 = 1
H_0 = 67.32*((3600*24*365)/((3.1*10**10)*10**9)) # [1/years]

"""When performing the calculations for the Runge Kutta methods, the time value of approximately t*H_0 is used.
Otherwise, the program creates an OverflowError.
When writing the value for the final list self.t, the value for the time t [yr] is calculated by dividing by H_0."""

class RungeKutta():
    def __init__(self, f, N0, Nmax, steprange, stepIncreaseFactor) -> None:
        self.f = f
        self.stepIncreaseFactor = stepIncreaseFactor # increases the steprange by this factor
        self.Nmax = Nmax
        self.N0 = N0
        if steprange < 0:
            self.t = [Nmax/H_0]
        else:
            self.t = [N0/H_0]
        self.a = []
        self.h = steprange
    
    def approx(self, a_0, reverse):
        self.a.append(a_0)
        if reverse:
            n = self.Nmax
            whileCondition = lambda x: x >= self.N0
        else:
            n = self.N0
            whileCondition = lambda x: x <= self.Nmax
        while whileCondition(n):
            try:
                k1 = self.f(self.a[-1])
                k2 = self.f(self.a[-1]+(1/2)*self.h*k1)
                k3 = self.f(self.a[-1]+(1/2)*self.h*k2)
                k4 = self.f(self.a[-1] + self.h*k3)
                newA = self.a[-1] + (self.h/6)*(k1 + 2*k2 + 2*k3 + k4)
            except OverflowError:
                break
            if n/abs(self.h) < 100:
                self.h *= self.stepIncreaseFactor
                print("HIer", self.t[-1], self.a[-1])
                continue
            n += self.h
            self.t.append(n/H_0)
            self.a.append(newA)
        if reverse:
            self.a.reverse() # sorts the list for increasing time
            self.t.reverse() # sorts the list for increasing time

def safeInFile(filename, data_t, data_a):
    handle = open(filename+"_t.txt", "wb")
    pickle.dump(data_t, handle)
    handle.close()
    handle = open(filename+"_a.txt", "wb")
    pickle.dump(data_a, handle)
    handle.close()

def f(a):
    return (Omega_r0/(a**2) + Omega_m0/a + Omega_Lambda0*(a**2) + (1-Omega_k0))**(1/2)
def f_change_w1(a):
    return (Omega_r0/(a**2) + Omega_m0/a + Omega_Lambda0*(a**(2.3)) + (1-Omega_k0))**(1/2)
def f_change_w2(a):
    return (Omega_r0/(a**2) + Omega_m0/a + Omega_Lambda0*(a**(2.6)) + (1-Omega_k0))**(1/2)

def getCurrentTime(p):
    def integrand(a):
        return 1/((Omega_r0/(a**2) + Omega_m0/a + Omega_Lambda0*(a**(2+p)) + (1-Omega_k0))**(1/2))
    result = integrate.quad(integrand, 0, 1)
    return result[0]


benchmark1 = RungeKutta(f, 10**(-11), getCurrentTime(0), -10**(-2), 0.1)
benchmark2 = RungeKutta(f, getCurrentTime(0), 10, 10**(-4), 10)
benchmark1.approx(1, True)
benchmark2.approx(1, False)
safeInFile("benchmark_data", benchmark1.t + benchmark2.t, benchmark1.a + benchmark2.a)

# change_w1 = RungeKutta(f_change_w1, getCurrentTime(0), 10, 10**(-4), 10)
# change_w1.approx(1, False)
# safeInFile("change_w-1.1_data", benchmark1.t + change_w1.t, benchmark1.a + change_w1.a)

# change_w2 = RungeKutta(f_change_w2, getCurrentTime(0), 10, 10**(-4), 10)
# change_w2.approx(1, False)
# safeInFile("change_w-1.2_data", benchmark1.t + change_w2.t, benchmark1.a + change_w2.a)

# H_0 = 69.54*((3600*24*365)/((3.1*10**10)*10**9)) # [1/years]
# change_w1_H0 = RungeKutta(f_change_w1, getCurrentTime(0), 10, 10**(-4), 10)
# change_w1_H0.approx(1, False)
# safeInFile("change_w-1.1_H0-69.54_data", benchmark1.t + change_w1_H0.t, benchmark1.a + change_w1_H0.a)
