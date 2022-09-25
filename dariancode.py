#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 11 19:10:55 2022

@author: darian
"""

# Make sure to have the server side running in CoppeliaSim: 
# in a child script of a CoppeliaSim scene, add following command
# to be executed just once, at simulation start:
#
# simRemoteApi.start(19999)
#
# then start simulation, and run this program.
#
# IMPORTANT: for each successful call to simxStart, there
# should be a corresponding call to simxFinish at the end!

try:
    import sim
except:
    print ('--------------------------------------------------------------')
    print ('"sim.py" could not be imported. This means very probably that')
    print ('either "sim.py" or the remoteApi library could not be found.')
    print ('Make sure both are in the same folder as this file,')
    print ('or appropriately adjust the file "sim.py"')
    print ('--------------------------------------------------------------')
    print ('')

import time
import math
import numpy
print ('Program started')
sim.simxFinish(-1) # just in case, close all opened connections
clientID=sim.simxStart('127.0.0.1',19999,True,True,5000,5) # Connect to CoppeliaSim
if clientID!=-1:
    print ('Connected to remote API server')

    # Now try to retrieve data in a blocking fashion (i.e. a service call):
    res,objs=sim.simxGetObjects(clientID,sim.sim_handle_all,sim.simx_opmode_blocking)
    res,_endEffector =sim.simxGetObjectHandle( clientID, 'Franka_connection', sim.simx_opmode_blocking)
    #res,_base =sim.simxGetObjectHandle( clientID, 'Franka_joint1', sim.simx_opmode_blocking)

    if res==sim.simx_return_ok:
        print ('Number of objects in the scene: ',len(objs))
# Darian's code starts here
        X = 0.7250*1000 ; 
        Y = 0.3750*1000 ; 
        r = 70; 
        
        X = 0;
        Y = 0;
        
        x_boundary = [];
        y_boundary = []; 
        z_boundary = [];
        x = [] ; y= [];
        k = 50
        for j in range(100): 
            theta =  numpy.linspace(0,math.pi/200,100)
            print (theta[j])
            x = k * math.cos(j) + X; # x trajectory 
            y = k * math.sin(j) + Y; # y trajectory 

            x_boundary_tmp = -0.22+(x*0.0008);
            x_boundary.append(x_boundary_tmp)
            
            y_boundary_tmp = -0.1+(y*0.0008);
            y_boundary.append(y_boundary_tmp)
            
            z_boundary_tmp  = 0.495
            z_boundary.append(z_boundary_tmp)    
        
        
        x_boundary = numpy.array(x_boundary)
        y_boundary = numpy.array(y_boundary)
        z_boundary = numpy.array(z_boundary)
        
        for j in range(100): 
            print(j)
            #returnCode=sim.simxSetObjectPosition(clientID,sim.sim_handle_all,-1,(x_boundary[j],y_boundary[j],z_boundary[j]),sim.simx_opmode_blocking)
            returnCode=sim.simxSetObjectPosition(clientID,_endEffector,-1,(x_boundary[j],y_boundary[j],z_boundary[j]),sim.simx_opmode_blocking)

    # Darian's code ends here
    else:
        print ('Remote API function call returned with error code: ',res)

    time.sleep(2)

    # Now retrieve streaming data (i.e. in a non-blocking fashion):
    startTime=time.time()
    sim.simxGetIntegerParameter(clientID,sim.sim_intparam_mouse_x,sim.simx_opmode_streaming) # Initialize streaming
    while time.time()-startTime < 5:
        returnCode,data=sim.simxGetIntegerParameter(clientID,sim.sim_intparam_mouse_x,sim.simx_opmode_buffer) # Try to retrieve the streamed data
        if returnCode==sim.simx_return_ok: # After initialization of streaming, it will take a few ms before the first value arrives, so check the return code
            print ('Mouse position x: ',data) # Mouse position x is actualized when the cursor is over CoppeliaSim's window
        time.sleep(0.005)

    # Now send some data to CoppeliaSim in a non-blocking fashion:
    sim.simxAddStatusbarMessage(clientID,'Hello CoppeliaSim!',sim.simx_opmode_oneshot)

    # Before closing the connection to CoppeliaSim, make sure that the last command sent out had time to arrive. You can guarantee this with (for example):
    sim.simxGetPingTime(clientID)

    # Now close the connection to CoppeliaSim:
    sim.simxFinish(clientID)
else:
    print ('Failed connecting to remote API server')
print ('Program ended')
