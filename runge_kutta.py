import pickle

# parameters:
Omega_r0 = 9.240*10**(-5)
Omega_m0 = 0.3158
Omega_Lambda0 = 0.6841
Omega_k0 = 1
H_0 = 67.32*((3600*24*365)/((3.1*10**10)*10**9)) # [1/years]
# H_0 = 69.54*((3600*24*365)/((3.1*10**10)*10**9)) # [1/years]

class RungeKutta():
    def __init__(self, f, N0, Nmax, steprange, stepIncreaseFactor, stepsBeforeIncrease, stepCountIncrease) -> None:
        self.f = f
        # the next three parameters change the interval of the steprange
        self.stepIncreaseFactor = stepIncreaseFactor # increases the steprange by this factor
        self.stepsBeforeIncrease = stepsBeforeIncrease # number of steps until increase
        self.stepCountIncrease = stepCountIncrease # factor by which stepsBeforeIncrease is increased at each increase of stepIncreaseFactor
        self.Nmax = Nmax
        self.N0 = N0
        if steprange < 0:
            self.t = [Nmax/H_0]
        else:
            self.t = [N0/H_0]
        self.a = []
        self.h = steprange
    
    def variableApprox(self, a_0):
        self.a.append(a_0)
        n = self.N0
        iterationCounter = 0
        totalIncreases = 0
        while n <= self.Nmax:
            iterationCounter += 1
            try:
                k1 = self.f(self.a[-1])
                k2 = self.f(self.a[-1]+(1/2)*self.h*k1)
                k3 = self.f(self.a[-1]+(1/2)*self.h*k2)
                k4 = self.f(self.a[-1] + self.h*k3)
                self.a.append(self.a[-1] + (self.h/6)*(k1 + 2*k2 + 2*k3 + k4))
            except OverflowError:
                break
            n += self.h
            self.t.append(n/H_0)
            if iterationCounter == self.stepsBeforeIncrease:
                iterationCounter = 0
                totalIncreases += 1
                self.h *= self.stepIncreaseFactor
                self.stepsBeforeIncrease *= self.stepCountIncrease
    def safeInFile(self, filename):
        handle = open(filename+"_t.txt", "wb")
        pickle.dump(self.t, handle)
        handle.close()
        handle = open(filename+"_a.txt", "wb")
        pickle.dump(self.a, handle)
        handle.close()

def f(a):
    return (Omega_r0/(a**2) + Omega_m0/a + Omega_Lambda0*(a**2) + (1-Omega_k0))**(1/2)
def f_change_w1(a):
    return (Omega_r0/(a**2) + Omega_m0/a + Omega_Lambda0*(a**(2.3)) + (1-Omega_k0))**(1/2)
def f_change_w2(a):
    return (Omega_r0/(a**2) + Omega_m0/a + Omega_Lambda0*(a**(2.6)) + (1-Omega_k0))**(1/2)

benchmark = RungeKutta(f_change_w1, 10**(-11), 10, 10**(-12), 10, 10, 10)
benchmark.variableApprox((10**(-6.2)))
benchmark.safeInFile("benchmark_data_t.txt", benchmark.t)
benchmark.safeInFile("benchmark_data_a.txt", benchmark.a)

change_w1 = RungeKutta(f_change_w1, 10**(-11), 10, 10**(-12), 10, 10, 10)
change_w1.variableApprox((10**(-6.2)))
change_w1.safeInFile("change_w-1.1_data_t.txt", change_w1.t)
change_w1.safeInFile("change_w-1.1_data_t.txt", change_w1.a)

change_w2 = RungeKutta(f_change_w2, 10**(-11), 10, 10**(-12), 10, 10, 10)
change_w2.variableApprox((10**(-6.2)))
change_w2.safeInFile("change_w-1.2_data_t.txt", change_w2.t)
change_w2.safeInFile("change_w-1.2_data_t.txt", change_w2.a)

change_w1_H0 = RungeKutta(f_change_w2, 10**(-11), 10, 10**(-12), 10, 10, 10)
change_w1_H0.variableApprox((10**(-6.2)))
change_w1_H0.safeInFile("change_w-1.1_H0-69.54_data_t.txt", change_w1_H0.t)
change_w1_H0.safeInFile("change_w-1.1_H0-69.54_data_t.txt", change_w1_H0.a)
