from scipy.optimize import curve_fit
from scipy import asarray as ar,exp
import numpy as np

# Input x and y
# Here we have 10 set
x = ar(range(10))
y = ar([0,0,0,0,0,0,0,0,0,0])

# gaussian curve fitting
def gaussian(x, *param):
    return param[0]*np.exp(-np.power(x - param[2], 2.) / (2 * np.power(param[4], 2.)))+ param[1]*np.exp(-np.power(x - param[3], 2.) / (2 * np.power(param[5], 2.)))

def poly(x, *param):
	return param[0]* np.power(x, 3.) + param[1]* np.power(x, 2.) + param[2]*np.power(x, 1.)+ param[3]

def get_angle(x,y):
	y_min = min(y)
	y2 = y - y_min
	popt,pcov = curve_fit(gaussian,x,y2,p0=[3,4,3,6,1,1])
	#popt,pcov = curve_fit(poly,x,y,p0=[1,1,1,1]) p0=[3,4,3,6,1,1]		# tan_theta = (f-f')/dx
	dx = 0.0000001
	tan_theta = (gaussian(x+dx,*popt)-gaussian(x,*popt))/dx
	# theta in [-180,180]
	theta = np.arctan(tan_theta)/3.14*180
	return theta
	#else :
	#	return ar([0,0,0,0,0,0,0,0,0,0])


# popt: Optimal values for the parameters
# so that the sum of the squared error of f(xdata, *popt) - ydata is minimized


theta = get_angle(x,y)
print theta