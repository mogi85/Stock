from pandas_datareader import data
import matplotlib.pyplot as plt
import pandas as pd
import datetime
import numpy as np


def MLE(dateS,S):
    X     = np.log(S)
    plt.plot(dateS,S)
    plt.grid()
    plt.xlabel('days')
    plt.ylabel('Stock Value')

    # Maximum Likelihood Estimation of mu

    dt = 1
    m  = len(dateS)
    mu = 1/(m * dt) * (X[-1]-X[0])

    # Maximum Likelihood Estimation of sigma

    s = 0;
    for i in range(0,len(X)-1):
        s = np.power(X[i+1]-X[i]-mu*dt,2)
    sigma = np.sqrt(s/(m*dt))
    print('Estimated parameters are: mu = {0} and sigma = {1}'.format(mu,sigma))

    # Monte Carlo simulation -- Forecasting

    NoOfPaths    = 10; # plot 10 paths
    NoOfSteps    = 160; # for about 0.5 year
    Z            =  np.random.normal(0.0,1.0,[NoOfPaths,NoOfSteps])
    Xsim         =  np.zeros([NoOfPaths,NoOfSteps])
    Xsim[:,0]    =  np.log(S[-1])

    for i in range(0,NoOfSteps-1):
        Z[:,i]         = (Z[:,i]-np.mean(Z[:,i]))/np.std(Z[:,i])
        Xsim[:,i+1]    = Xsim[:,i] + mu*dt + sigma*np.sqrt(dt)*Z[:,i]
    plt.plot(range(dateS[-1],dateS[-1]+NoOfSteps),np.exp(np.transpose(Xsim)),'-r')

ticker=input("Ingresa el ticker:")
print(ticker)
end_date=input("Ingresa Fecha formato AAAA-MM-DD:")
print(end_date)

year, month, day = map(int, end_date.split('-'))
date1 = datetime.date(year, month, day)
start_date=str(date1- datetime.timedelta(30))

#Lee de Yahoo el ticker ingresado de las fechas ingresadas
panel_data = data.DataReader(ticker, 'yahoo', start_date, end_date)

modified = panel_data.reset_index()
#list=modified['Date'].to_list()
dateS=modified['Date'].dt.strftime("%Y%m%d").to_list()
for i in range(0, len(dateS)):
    dateS[i] = int(dateS[i])

#Aqui se le puede cambiar en vez del precio al cierre
data=panel_data['Close'].to_list()


MLE(dateS,data)
