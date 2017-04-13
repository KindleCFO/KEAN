from scipy.stats import norm
import math

#S = underlying
#K = strike
#r = riskless rate
#T = time
#v = volatility

s = 42
k = 40
r = 0.1
t = 0.5
vol = 0.2

#Black-Scholes-Merton option model
d1 = (math.log(s/k) + (r+vol**2/2)*t)/(vol*t**0.5)

d2 = d1 - vol*t**.5

call = s*norm.cdf(d1) - k*math.exp(-r*t)*norm.cdf(d2)

put = k*math.exp(-r*t)*norm.cdf(-d2) - s*norm.cdf(-d1)

print(call, put)

#use this as test
