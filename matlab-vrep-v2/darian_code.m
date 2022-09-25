function darian_code()
    disp('Program started');
    sim=remApi('remoteApi'); % using the prototype file (remoteApiProto.m)
    sim.simxFinish(-1); % just in case, close all opened connections
    clientID=sim.simxStart('127.0.0.1',19999,true,true,5000,5);

    if (clientID > -1)
        disp('Connected to remote API server');
        % Now send some data to CoppeliaSim in a non-blocking fashion:
        sim.simxAddStatusbarMessage(clientID,'Hello CoppeliaSim! from matlab',sim.simx_opmode_oneshot);
        sim.simxGetPingTime(clientID);
        
        % Darian's code starts here:
        % Now try to retrieve data in a blocking fashion (i.e. a service call):
        [~,dum]=sim.simxGetObjectHandle(clientID,'target',sim.simx_opmode_blocking);

        [returnCode,pose] = sim.simxGetObjectPosition(clientID,dum,-1,sim.simx_opmode_blocking);
        disp(pose);
        X = 0.7250*1000 ; Y = 0.3750*1000 ; r = [70]; 
        theta = 0: pi/200 : (2*pi); 
        x = [] ; y= [];
        for k = 1 : length(r) 
        for j = 1 : length(theta) 
        x(k,j) = r(k) * cos(theta(j)) + X; % x trajectory 
        y(k,j) = r(k) * sin(theta(j)) + Y; % y trajectory 
        end
        end
        z = zeros(4 , length(x)) ; % 2_D circulation 
        
        x_boundary = [];
        y_boundary = [] ; 
        z_boundary = [];
        
        x_boundary = -0.22+(x.*0.0008);
        y_boundary = -0.1+(y.*0.0008);
        z_boundary = (z.*0.000+0.495);

        for k = 1 : length(r)
        for j = 1:length(theta)
        [returnCode]=sim.simxSetObjectPosition(clientID,dum,-1,[x_boundary(k,j),y_boundary(k,j),z_boundary(k,j)],sim.simx_opmode_blocking)
        end
        end
        
        % Darian's code ends here.
        % Now close the connection to CoppeliaSim:    
        sim.simxFinish(clientID);
    else
        disp('Failed connecting to remote API server');
    end
    sim.delete(); % calling the destructor
    disp('Program ended');
end