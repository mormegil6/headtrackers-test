from matplotlib import pyplot as plt
import numpy as np
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)
import rpp
from scipy.interpolate import interp1d

np.set_printoptions(precision=5, suppress=True)

if __name__ == '__main__':

    ##########################
    ### 01. rotations test ###
    ##########################

    # read Reaper file for recorded automation tracks
    f = open('.\\HeadtrackersTest-rotation.rpp', 'r')
    rf = f.read()
    f.close()
    r = rpp.loads(rf)

    # scale for automation values from 0/1 to -180/180 
    scale01to180 = interp1d([0, 1], [-180, 180])

    # Supperware headtracker YPR recorded data
    lstY = np.array(r[62][23][11][6:])[:, 1:3]
    lstP = np.array(r[62][23][8][6:])[:, 1:3]
    lstR = np.array(r[62][23][9][6:])[:, 1:3]
    supp_Y = lstY.astype(np.float)
    supp_P = lstP.astype(np.float)
    supp_R = lstR.astype(np.float)
    supp_Y[:, 1] = scale01to180(supp_Y[:, 1])
    supp_P[:, 1] = scale01to180(supp_P[:, 1])
    supp_R[:, 1] = scale01to180(supp_R[:, 1])

    # IEM MrHeadTracker YPR recorded data
    lstY = np.array(r[63][23][8][6:])[:, 1:3]
    lstP = np.array(r[63][23][9][6:])[:, 1:3]
    lstR = np.array(r[63][23][10][6:])[:, 1:3]
    mrht_Y = lstY.astype(np.float)
    mrht_P = lstP.astype(np.float)
    mrht_R = lstR.astype(np.float)
    mrht_Y[:, 1] = scale01to180(mrht_Y[:, 1])
    mrht_P[:, 1] = scale01to180(mrht_P[:, 1])
    mrht_R[:, 1] = scale01to180(mrht_R[:, 1])

    # WavesNX headtracker YPR recorded data
    lstY = np.array(r[64][23][7][6:])[:, 1:3]
    lstP = np.array(r[64][23][8][6:])[:, 1:3]
    lstR = np.array(r[64][23][9][6:])[:, 1:3]
    wvnx_Y = lstY.astype(np.float)
    wvnx_P = lstP.astype(np.float)
    wvnx_R = lstR.astype(np.float)
    wvnx_Y[:, 1] = scale01to180(wvnx_Y[:, 1]) * (-1)
    wvnx_P[:, 1] = scale01to180(wvnx_P[:, 1])
    wvnx_R[:, 1] = scale01to180(wvnx_R[:, 1])
    
    # plot results
    fg, ax = plt.subplots()
    titleStr = 'Headtrackers test - latency\nRotating headtrackers, saving IEM SceneRotator output'
    fg.canvas.manager.set_window_title(titleStr)
    fg.suptitle(titleStr)
    legendStr = ['Supperware Y', 'Supperware P', 'Supperware R', 'IEM MrHeadTracker Y', 'IEM MrHeadTracker P',
                 'IEM MrHeadTracker R', 'WavesNX Y', 'WavesNX P', 'WavesNX R']
    # results for Supperware
    lineSupp_Y, = ax.plot(supp_Y[:, 0], supp_Y[:, 1], '-', color='red', label=legendStr[0])
    lineSupp_P, = ax.plot(supp_P[:, 0], supp_P[:, 1], '-', color='orangered', label=legendStr[1])
    lineSupp_R, = ax.plot(supp_R[:, 0], supp_R[:, 1], '-', color='orange', label=legendStr[2])
    # results for MrHeadTracker
    lineMrht_Y, = ax.plot(mrht_Y[:, 0], mrht_Y[:, 1], '-', color='lime', label=legendStr[3])
    lineMrht_P, = ax.plot(mrht_P[:, 0], mrht_P[:, 1], '-', color='forestgreen', label=legendStr[4])
    lineMrht_R, = ax.plot(mrht_R[:, 0], mrht_R[:, 1], '-', color='mediumspringgreen', label=legendStr[5])
    # results for WavesNX
    lineWvnx_Y, = ax.plot(wvnx_Y[:, 0], wvnx_Y[:, 1], '-', color='aqua', label=legendStr[6])
    lineWvnx_P, = ax.plot(wvnx_P[:, 0], wvnx_P[:, 1], '-', color='deepskyblue', label=legendStr[7])
    lineWvnx_R, = ax.plot(wvnx_R[:, 0], wvnx_R[:, 1], '-', color='royalblue', label=legendStr[8])

    # remove lines, so the plot shows only Yaw coordinates - comment to plot Pitch and Roll
    # lineSupp_P.remove()
    # lineSupp_R.remove()
    # lineMrht_P.remove()
    # lineMrht_R.remove()
    # lineWvnx_P.remove()
    # lineWvnx_R.remove()

    ax.legend()

    ax.set_ylim([-190, 190])
    ax.yaxis.set_major_locator(MultipleLocator(30))
    ax.yaxis.set_minor_locator(MultipleLocator(10))
    ax.tick_params(axis='y', which='minor', bottom=False)
    ax.grid(which='major', linestyle='--', axis='both')
    ax.grid(which='minor', linestyle=':', axis='y')
    ax.set_xlabel('time [s]')
    ax.set_ylabel('angle [deg]')

    extraticks = [14, 26, 38, 48, 56, 62]
    ax2 = ax.twiny()
    ax2.set_xlim(ax.get_xlim())
    ax2.set_xticks(extraticks, minor=True)
    ax2.tick_params(axis='x', length=0, which='minor')
    ax2.tick_params(axis='x', which='major', bottom=False, top=False, labelbottom=False, labeltop=False)
    ax2.set_xticklabels(["rotating 360° clockwise\nand back on yaw axis", "rotating 360° clockwise\nand back on yaw axis",
                        "rotating 360° clockwise\nand back on yaw axis", "90° left/right\nyaw axis",
                         "90° down/up\npitch axis", "90° left/right\nroll axis"], minor=True, color='b', rotation=0)

    plt.show()


    ######################
    ### 02. drift test ###
    ######################

    # read Reaper file for recorded automation tracks
    f = open('.\\HeadtrackersTest-drift.rpp', 'r')
    rf = f.read()
    f.close()
    r = rpp.loads(rf)

    # scale for automation values from 0/1 to -180/180
    scale01to180 = interp1d([0, 1], [-180, 180])

    # Supperware headtracker YPR recorded data
    lstY = np.array(r[62][23][11][6:])[:, 1:3]
    lstP = np.array(r[62][23][8][6:])[:, 1:3]
    lstR = np.array(r[62][23][9][6:])[:, 1:3]
    supp_Y = lstY.astype(np.float)
    supp_P = lstP.astype(np.float)
    supp_R = lstR.astype(np.float)
    supp_Y[:, 1] = scale01to180(supp_Y[:, 1])
    supp_P[:, 1] = scale01to180(supp_P[:, 1])
    supp_R[:, 1] = scale01to180(supp_R[:, 1])

    # IEM MrHeadTracker YPR recorded data
    lstY = np.array(r[63][23][8][6:])[:, 1:3]
    lstP = np.array(r[63][23][9][6:])[:, 1:3]
    lstR = np.array(r[63][23][10][6:])[:, 1:3]
    mrht_Y = lstY.astype(np.float)
    mrht_P = lstP.astype(np.float)
    mrht_R = lstR.astype(np.float)
    mrht_Y[:, 1] = scale01to180(mrht_Y[:, 1])
    mrht_P[:, 1] = scale01to180(mrht_P[:, 1])
    mrht_R[:, 1] = scale01to180(mrht_R[:, 1])

    # WavesNX headtracker YPR recorded data
    lstY = np.array(r[64][23][7][6:])[:, 1:3]
    lstP = np.array(r[64][23][8][6:])[:, 1:3]
    lstR = np.array(r[64][23][9][6:])[:, 1:3]
    wvnx_Y = lstY.astype(np.float)
    wvnx_P = lstP.astype(np.float)
    wvnx_R = lstR.astype(np.float)
    wvnx_Y[:, 1] = scale01to180(wvnx_Y[:, 1]) * (-1)
    wvnx_P[:, 1] = scale01to180(wvnx_P[:, 1])
    wvnx_R[:, 1] = scale01to180(wvnx_R[:, 1])

    # plot results
    fg, ax = plt.subplots()
    titleStr = 'Headtrackers test - drift\nLeaving headtrackers on a dummy head for 10 mins, saving IEM SceneRotator output'
    fg.canvas.manager.set_window_title(titleStr)
    fg.suptitle(titleStr)
    legendStr = ['Supperware Y', 'Supperware P', 'Supperware R', 'IEM MrHeadTracker Y', 'IEM MrHeadTracker P',
                 'IEM MrHeadTracker R', 'WavesNX Y', 'WavesNX P', 'WavesNX R']
    # results for Supperware
    lineSupp_Y, = ax.plot(supp_Y[:, 0], supp_Y[:, 1], '-', color='red', label=legendStr[0])
    lineSupp_P, = ax.plot(supp_P[:, 0], supp_P[:, 1], '-', color='orangered', label=legendStr[1])
    lineSupp_R, = ax.plot(supp_R[:, 0], supp_R[:, 1], '-', color='orange', label=legendStr[2])
    # results for MrHeadTracker
    lineMrht_Y, = ax.plot(mrht_Y[:, 0], mrht_Y[:, 1], '-', color='lime', label=legendStr[3])
    lineMrht_P, = ax.plot(mrht_P[:, 0], mrht_P[:, 1], '-', color='forestgreen', label=legendStr[4])
    lineMrht_R, = ax.plot(mrht_R[:, 0], mrht_R[:, 1], '-', color='mediumspringgreen', label=legendStr[5])
    # results for WavesNX
    lineWvnx_Y, = ax.plot(wvnx_Y[:, 0], wvnx_Y[:, 1], '-', color='aqua', label=legendStr[6])
    lineWvnx_P, = ax.plot(wvnx_P[:, 0], wvnx_P[:, 1], '-', color='deepskyblue', label=legendStr[7])
    lineWvnx_R, = ax.plot(wvnx_R[:, 0], wvnx_R[:, 1], '-', color='royalblue', label=legendStr[8])

    # remove lines, so the plot shows only Yaw coordinates - comment to plot Pitch and Roll
    # lineSupp_P.remove()
    # lineSupp_R.remove()
    # lineMrht_P.remove()
    # lineMrht_R.remove()
    # lineWvnx_P.remove()
    # lineWvnx_R.remove()

    ax.legend()

    ax.set_ylim([-10, 10])
    ax.yaxis.set_major_locator(MultipleLocator(2))
    ax.yaxis.set_minor_locator(MultipleLocator(0.5))
    ax.tick_params(axis='y', which='minor', bottom=False)
    ax.grid(which='major', linestyle='--', axis='both')
    ax.grid(which='minor', linestyle=':', axis='y')
    ax.set_xlabel('time [s]')
    ax.set_ylabel('angle [deg]')

    plt.show()

    print("end.")
