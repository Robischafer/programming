### Programming
### Take Home Exam 1

import numpy
import matplotlib.pyplot as plt
import pandas
import random
from tabulate import tabulate


## Q1

# european call option payoff: max(0, S(T) - K),
# T=maturity, S(T)=price at given date, K=strike price

def OptionEval(S, K):
    """
    return the payoff of a
    European call option
    max(0, S(T) - K)
    given values of S(T) = value underlying at t = T
    and K = strike price
    """
    if (S - K) > 0:
        payoff = S - K
    else:
        payoff = 0
    return payoff


LK = [8000, 8500, 9000]
LS = [8200, 9700, 10000, 12100]


def ListOptionEval(LS, LK):
    """
    return the payoff of a
    European call option
    max(0, S(T) - K)
    given lists of S(T) and K
    """
    Payoff = []
    for i in range(0, len(LK)):
        p = []
        for j in range(0, len(LS)):
            p.append(OptionEval(LS[j], LK[i]))
        Payoff.append(p)
    # transform in dataframe for easier usage
    Payoff = pandas.DataFrame(Payoff, index=LK, columns=LS)
    return Payoff


print(OptionEval(8000, 9000))
print(ListOptionEval(LS, LK))

P = ListOptionEval(LS=range(7000, 9000, 10), LK=[8000])
plt.plot(P.loc[8000, :])
plt.title("inner value for European call option", x=-0.1, y=0.1, rotation=90)
plt.grid([True, "major", "x"], color='grey', linestyle='dotted', linewidth=1)
plt.xlim(7000, 9000)
plt.xticks(range(7000, 9500, 500))
plt.ylim(0, 1000)
plt.yticks(range(0, 1200, 200))
plt.show()

##Q2

# PV = E[(e^-rT)*max(S(T) - K, 0)]
# dS(t)/S(t) = r*dt + sigma*dW(t)

# with W ~ brownian motion
# S(T) = S(0)*exp((r-(1/2)*sigma^2)*T + sigma*W(T))
# W(T) ~ N(0, T)
# sqrt(T)*Z ~ N(0, T), Z ~ N(0, 1)

# S(T) = S(0)*exp((r-(1/2)*sigma^2)*T + sigma*sqrt(T)*Z)
# The logarithm of the stock price is thus normally distributed,
# and the stock price itself has a log-normal distribution.

# estimate expectation using Monte Carlo integration

random.seed(a=1234)


# sigma is the variance of the underlying stock,
# here i choose to explicitly ask for it in the parameter


def OptionPrice(S0, K, T, r, sigma):
    """
    give option price given parameters
    using Monte Carlo integration
    S0 = underlying asset price at t = 0,
    K = strike price, T = maturity,
    actualization rate r,
    sigma = BS assumed constant volatility
    of the underlying asset
    """
    n = 1000
    # generate list for normal variable
    Z = []
    for i in range(0, n):
        Z.append(random.gauss(0, 1))
    C = []
    # generating ST given parameter
    for i in range(0, n):
        ST = S0 * numpy.exp((r - (1 / 2) * numpy.power(sigma, 2)) * T + sigma * numpy.sqrt(T) * Z[i])
        C.append(numpy.exp(-r * T) * OptionEval(ST, K))
    # averaging to minimize approximation error
    Cn = sum(C) / n
    return Cn


LK = [6000, 6500, 7000]
LS0 = [8000, 8200, 9000]
LT = [1, 2, 4]
Lr = [0.01, 0.02, 0.03]


def ListOptionPrice(LS0, LK, LT, Lr, sigma):
    """
    give option price given parameters
    using Monte Carlo integration
    and output the results to a text
    file in the form of a table with
    associated parameters
    S0 = underlying asset price at t = 0,
    K = strike price, T = maturity,
    actualization rate r,
    sigma = BS assumed constant volatility
    of the underlying asset
    """
    b = open("Q2_output.txt", "w+")
    temp1 = []
    for i in range(0, len(LS0)):
        for j in range(0, len(LK)):
            for k in range(0, len(LT)):
                for m in range(0, len(Lr)):
                    table = [LS0[i], LK[j], LT[k], Lr[m], OptionPrice(LS0[i], LK[j], LT[k], Lr[m], sigma)]
                    temp1.append(table)
    # transform in dataframe for easier usage
    b.write(tabulate(temp1, headers=["S0", "K", "T", "r", "Cn"], tablefmt="github"))
    b.close()
    return "done!"


# here i choose sigma = 0.2
ListOptionPrice(LS0, LK, LT, Lr, sigma=0.2)



