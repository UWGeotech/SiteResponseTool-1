import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as sg
from scipy.interpolate import interp1d

def plot_motionData():

    PlotResults('FA1-5','1_Clay1.acc','x')
    PlotResults('FA1-5','1_Clay1.acc','y')
    PlotResults('FA1-5','1_Clay1.acc','z')

    PlotResults('DHB6','6_Clay6.acc','x')
    PlotResults('DHB6','6_Clay6.acc','y')
    PlotResults('DHB6','6_Clay6.acc','z')

    PlotResults('DHB11','11_Clay11.acc','x')
    PlotResults('DHB11','11_Clay11.acc','y')
    PlotResults('DHB11','11_Clay11.acc','z')

    PlotResults('DHB17','17_Clay17.acc','x')
    PlotResults('DHB17','17_Clay17.acc','y')
    PlotResults('DHB17','17_Clay17.acc','z')

    accUP = np.loadtxt(open("", 'r').readlines()[:-1], skiprows=skip)

def PlotResults (RecFName, SimFName, Dir):

    if Dir == 'X' or Dir == 'x':
        bID = 'N'
        rID = '7N'
        sID = 1
    elif Dir == 'Y' or Dir == 'y':
        bID = 'U'
        rID = '7U'
        sID = 2
    elif Dir == 'Z' or Dir == 'z':
        bID = 'E'
        rID = '7E'
        sID = 3
    else:
        print("Wrong Dir")

    # Read Recorded Data
    dT = 0.005
    DS = 4
    skip = 9
    RecData, time = readLotung(RecFName+"."+rID, dT, DS, skip)

    # Read Simulated data
    SimData = np.loadtxt(open(SimFName, 'r'))
    SimTime = SimData[:,0]
    Sim = SimData[:,sID]

    baseTimeData = np.loadtxt("DHB47" + bID + ".time")
    baseAccData = np.loadtxt("DHB47" + bID + ".acc")

    # interpolate base acceleraion with recorded time
    baseTimeInterp = interp1d(baseTimeData, baseAccData, kind='linear', fill_value='extrapolate')
    #baseAcc = Sim[:,0] + 9.81 * baseTimeInterp(SimTime).reshape(len(SimTime), 1)
    TotalAcc = Sim + 9.81 * baseTimeInterp(SimTime)

    # Create Plot comparing recorded and simulated data
    fig1 = plt.figure()
    ax1 = fig1.add_subplot(111)
    ax1.plot(time, RecData/980)
    #ax1.plot(SimTime, Sim/9.81, 'r')
    ax1.plot(SimTime, TotalAcc/9.81, 'r')
    ax1.set_ylabel('acc (g)')
    ax1.set_xlabel('time $(s)$')
    ax1.set_xlim(5, 20)
    ax1.set_ylim(-0.2, 0.2)
    plt.grid(color='k', linestyle='--', linewidth=0.5)
    plt.legend(('Recorded', 'Simulation'), loc = 0 )
    plt.savefig(RecFName+"-"+rID+".png")
    plt.show(block = False)

    # Plots for checking accel components
    #fig2 = plt.figure()
    #ax2 = fig2.add_subplot(111)
    #ax2.plot(baseTimeData, baseAccData)
    #ax2.plot(SimTime, Sim)
    #ax2.plot(SimTime, TotalAcc)
    #plt.show()



def readLotung(filename, dT, DS, skip):
    motionDT = dT*DS
    mdata = np.loadtxt(open(filename, 'r').readlines()[:-1], skiprows=skip)
    aa = mdata.reshape(-1)
    aa_resample = sg.decimate(aa,DS)
    motionSteps = np.size(aa_resample)
    motionTotalTime = motionSteps * motionDT
    time = np.linspace(0.0, motionTotalTime, motionSteps)

    return aa_resample, time

if __name__ == "__main__":
    plot_motionData()
