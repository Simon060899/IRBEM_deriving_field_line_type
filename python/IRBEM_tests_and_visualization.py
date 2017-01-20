# -*- coding: utf-8 -*-
"""
Created on Fri Jan  6 19:26:04 2017

@author: mike
"""

# IRBEM test and visualization functions.
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pylab as plt
import numpy as np

from IRBEM import IRBEM

# A few test and visualization scripts.
def testLStarOutput():
    """
    This test function will test is the make_lstar1() function works correctly.
    If you run this, the output should be the follwing. 
    
    {'MLT': [8.34044753112316], 'xj': [9.898414822276834], 'lstar': [-1e+31],
    'Lm': [4.631806704496794], 'bmin': [268.5087756309121], 
    'blocal': [39730.828875776126]}
    """
    model = IRBEM(options = [0,0,0,0,0])
    LLA = {}
    LLA['x1'] = 651
    LLA['x2'] = 63
    LLA['x3'] = 15.9
    LLA['dateTime'] = '2015-02-02T06:12:43'
    maginput = {'Kp':40.0}
    model.make_lstar(LLA, maginput, STATUS_FLAG = False)
    print(model.lstar1_output)

def footPointTest():
    """
    Test script to find the same hemisphere footprint for some arbitary 
    loccation.
    
    {'XFOOT': [99.15918384268508, 65.18720406063792, 16.115261431962285], 
    'BFOOT': [-30667.04604376155, -7651.837684485317, -39138.97550317413],
    'BFOOTMAG': [50307.82977269011, -9999.0, -9999.0]}
    """
    model = IRBEM(options = [0,0,0,0,0])
    LLA = {}
    LLA['x1'] = 651
    LLA['x2'] = 63.97
    LLA['x3'] = 15.9
    LLA['dateTime'] = '2015-02-02T06:12:43'
    maginput = {'Kp':40.0} 
    stopAlt = 100
    hemiFlag = 0
    model.find_foot_point(LLA, maginput, stopAlt, hemiFlag, STATUS_FLAG = False)
    print(model.foot_point_output)
    
def testDriftShell(pltDensity = 10):
    """
    Test script to generate a drift shell for electrons mirroring at the
    input location. 
    
    You may get a PEP 3118 buffer warning.
    """
    print('Under construction')
    model = IRBEM(options = [0,0,0,0,0])
    LLA = {}
    LLA['x1'] = 651
    LLA['x2'] = 34
    LLA['x3'] = 90
    LLA['dateTime'] = '2015-02-02T06:12:43'
    maginput = {'Kp':0.0}
    output = model.drift_shell(LLA, maginput)
    
    # Now plot the drift shell   
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    n = 10
    xGEO = -9999*np.ones(n*1000//pltDensity)
    yGEO = -9999*np.ones(n*1000//pltDensity)
    zGEO = -9999*np.ones(n*1000//pltDensity)
    
    for i in range(n):
        xGEO[i*1000//pltDensity:(i+1)*1000//pltDensity] = output['POSIT'][i,::pltDensity,0]
        yGEO[i*1000//pltDensity:(i+1)*1000//pltDensity] = output['POSIT'][i,::pltDensity,1]
        zGEO[i*1000//pltDensity:(i+1)*1000//pltDensity] = output['POSIT'][i,::pltDensity,2]

    ax.scatter(xGEO, yGEO, zGEO)
    
    # Now draw a sphere
    u, v = np.mgrid[0:2*np.pi:40j, 0:np.pi:20j]
    x=np.cos(u)*np.sin(v)
    y=np.sin(u)*np.sin(v)
    z=np.cos(v)
    ax.plot_wireframe(x, y, z, color="k")
    ax.set_ylim([-5, 5])
    ax.set_xlim([-5, 5])
    ax.set_zlim([-5, 5])
    ax.set_xlabel('x GEO')
    ax.set_ylabel('y GEO')
    ax.set_zlabel('z GEO')
    
def test_find_mirror_point():
    """
    Test function to calculate the mirror point. Output should be
    
    {'blocal': 39730.828875776126, 'POSIT': [0.4828763104086329, 
    0.13755093538265498, 0.9794110012635103], 'bmin': 39730.828875776126}
    """
    model = IRBEM(options = [0,0,0,0,0])
    LLA = {}
    LLA['x1'] = 651
    LLA['x2'] = 63
    LLA['x3'] = 15.9
    LLA['dateTime'] = '2015-02-02T06:12:43'
    maginput = {'Kp':40.0}
    alpha = 90 # Locally mirroring at input location.
    print(model.find_mirror_point(LLA, maginput, alpha, STATUS_FLAG = False))
    
def testTraceFieldLine(pltDensity = 10):
    """
    Test function to plot a fieldline and a sphere.
    """
    model = IRBEM(options = [0,0,0,0,0])
    LLA = {}
    LLA['x1'] = 651
    LLA['x2'] = 63
    LLA['x3'] = 15.9
    LLA['dateTime'] = '2015-02-02T06:12:43'
    maginput = {'Kp':40.0}
    out = model.trace_field_line(LLA, maginput, STATUS_FLAG = False)
    
    # Now plot the field lines
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    xGEO = out['POSIT'][::pltDensity, 0] 
    yGEO = out['POSIT'][::pltDensity, 1] 
    zGEO = out['POSIT'][::pltDensity, 2] 

    ax.scatter(xGEO, yGEO, zGEO)
    
    # Draw sphere    
    u, v = np.mgrid[0:2*np.pi:40j, 0:np.pi:20j]
    x=np.cos(u)*np.sin(v)
    y=np.sin(u)*np.sin(v)
    z=np.cos(v)
    ax.plot_wireframe(x, y, z, color="k")
    ax.set_ylim([-5, 5])
    ax.set_xlim([-5, 5])
    ax.set_zlim([-5, 5])
    ax.set_xlabel('x GEO')
    ax.set_ylabel('y GEO')
    ax.set_zlabel('z GEO')
    
def azimuthalFieldLineVisualization(lat = 55, dLon = 20, pltDensity = 10):
    """
    This function draws the megnetic field lines defined by the lat argument,
    at different longitudes from 0 to 360, in dLon angle steps. pltDensity 
    defines at what inerval to plot the field lines, since it is very 
    computationaly expensive to plot. 
    """
    model = IRBEM(options = [0,0,0,0,0])
    startLon = 0
    endLon = 360
    
    N = (endLon - startLon)//dLon
    # We will have to append since we can't tell how big the output will be
    xGEO = np.array([])
    yGEO = np.array([])
    zGEO = np.array([])
    
    for i in range(N):#np.arange(startLon, endLon, dLon):
        LLA = {}
        LLA['x1'] = 651
        LLA['x2'] = lat
        LLA['x3'] = i*dLon
        LLA['dateTime'] = '2015-02-02T06:12:43'
        maginput = {'Kp':40.0}
        out = model.trace_field_line(LLA, maginput, STATUS_FLAG = False)
        # pltDensity is to plot every pltDensity location of the field line,
        # to ease the graphical visualization. 
        xGEO = np.append(xGEO, out['POSIT'][::pltDensity, 0])
        yGEO = np.append(yGEO, out['POSIT'][::pltDensity, 1])
        zGEO = np.append(zGEO, out['POSIT'][::pltDensity, 2])
    
    # Now plot the field line
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(xGEO, yGEO, zGEO)
    
    # Draw sphere    
    u, v = np.mgrid[0:2*np.pi:40j, 0:np.pi:20j]
    x=np.cos(u)*np.sin(v)
    y=np.sin(u)*np.sin(v)
    z=np.cos(v)
    ax.plot_wireframe(x, y, z, color="k")
    ax.set_ylim([-5, 5])
    ax.set_xlim([-5, 5])
    ax.set_zlim([-5, 5])
    ax.set_xlabel('x GEO')
    ax.set_ylabel('y GEO')
    ax.set_zlabel('z GEO')
    return