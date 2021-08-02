from controller import Robot
from controller import LED

robot = Robot()
    

timestep = int(robot.getBasicTimeStep())

motor_list = ["front_right_motor", "front_left_motor", "rear_right_motor", "rear_left_motor"]

sensor_list = ["st_right","st_left","rod_center_ir", "rod_right_ir", "rod_left_ir",
                "rod_ext_right_ir", "rod_ext_left_ir",
                "ir_wall_right_up", "ir_wall_left_up",
                "ir_wall_right_down", "ir_wall_left_down","ir_cam_box"]
led_list = ["led_1","led_2","led_3"]

motor = dict()
sensor = dict()
led = dict()

for m in motor_list:
    motor[m] = robot.getDevice(m)
    motor[m].setPosition(float('inf'))
    motor[m].setVelocity(0.0)

for s in sensor_list:
    sensor[s] = robot.getDevice(s)
    sensor[s].enable(timestep)

for l in led_list:
    led[l] = robot.getDevice(l)
    led[l].set(0)
flag1= 0
flag2= 0
flag3= 0
count=0
last_error = intg = diff = prop = waitCounter = 0
kp = 0.005
ki = 0
kd = 0.15
def pid(error):
    global last_error, intg, diff, prop, kp, ki, kd
    prop = error
    intg = error + intg
    diff = error - last_error
    balance = (kp*prop) + (ki*intg) + (kd*diff)
    last_error = error
    return balance    
            
def SetMotorSpeed(main, balance):
    motor['front_right_motor'].setVelocity(main + balance)
    motor['rear_right_motor'].setVelocity(main + balance)
    motor['front_left_motor'].setVelocity(main - balance)
    motor['rear_left_motor'].setVelocity(main - balance)
    
while robot.step(timestep) != -1:
    st_left_value = sensor['st_left'].getValue()
    st_right_value = sensor['st_right'].getValue()
    center_value = sensor['rod_center_ir'].getValue()
    right_value = sensor['rod_right_ir'].getValue()
    left_value = sensor['rod_left_ir'].getValue()
    right_ext_value = sensor['rod_ext_right_ir'].getValue()
    left_ext_value = sensor['rod_ext_left_ir'].getValue()
    wall_right_up_value = sensor['ir_wall_right_up'].getValue()
    wall_left_up_value = sensor['ir_wall_left_up'].getValue()
    wall_right_down_value = sensor['ir_wall_right_down'].getValue()
    wall_left_down_value = sensor['ir_wall_left_down'].getValue()
    cam_value = sensor['ir_cam_box'].getValue()
    
    print(" st_left_value\n", st_left_value)
    print("st_right_value \n", st_right_value)
    print("center_value \n", center_value)
    print("right_value \n", right_value)
    print("left_value \n", left_value)
    print("right_ext_value \n", right_ext_value)
    print("left_ext_value \n", left_ext_value)
    print("wall_right_up_value \n", wall_right_up_value)
    print("wall_left_up_value \n", wall_left_up_value)
    print("wall_right_down_value \n", wall_right_down_value)
    print("wall_left_down_value \n", wall_left_down_value)
    print("cam_value \n", cam_value)
    print("count \n", count)
    
    if center_value< 450 and right_ext_value>950 and left_ext_value<950:
        SetMotorSpeed(1,-1)
    elif center_value< 450 and right_ext_value<950 and left_ext_value>950:
        SetMotorSpeed(1,1)
    elif center_value<450 and right_value<450 and left_value<450:
        SetMotorSpeed(3,0)
    elif center_value<450:
        if right_value>950 and left_value>950:
            SetMotorSpeed(8,0)
        elif right_value<950:
            SetMotorSpeed(0,-2.5)
        elif left_value<950:
            SetMotorSpeed(0,2.5)
            
        if wall_left_up_value!=1000:
            led["led_1"].set(1)
            led["led_2"].set(0)
            led["led_3"].set(0)
            
            if flag1==0:
                flag1=1
                count+=1
                
        else:
            led["led_1"].set(0)
            led["led_2"].set(0)
            led["led_3"].set(0)
            
            flag1=0
        if wall_right_up_value!=1000:
            led["led_3"].set(1)
            led["led_2"].set(0)
            led["led_1"].set(0)
           
            if flag2==0:
                flag2=1
                count+=1
        else:
            led["led_3"].set(0)
            led["led_2"].set(0)
            led["led_1"].set(0)
            
            flag2=0
        
                
        
        if st_right_value<450 and right_ext_value<450 and left_ext_value<450 :
            led["led_1"].set(1)
            led["led_2"].set(1)
            led["led_3"].set(1)
            if flag3==0:
                flag3=1
                count+=1
        else:
            led["led_3"].set(0)
            led["led_2"].set(0)
            led["led_1"].set(0)
            flag3=0
        if wall_right_down_value!=1000:
            led["led_3"].set(1)
                
            
        if wall_left_down_value!=1000:
            led["led_1"].set(1)
            
    elif center_value>950:
        if right_ext_value>950 and left_ext_value>950:
            if right_value<950:
                SetMotorSpeed(0,-3.5)
            elif left_value<950:
                SetMotorSpeed(0,3.5)
            elif right_value>950 and left_value>950:
                if st_left_value<950 and st_right_value==1000:
                    led["led_3"].set(1)
                    led["led_2"].set(1)
                    led["led_1"].set(1)
                    SetMotorSpeed(0,0)
                
                elif st_left_value==1000 and st_right_value==1000:
                    SetMotorSpeed(2,0)
                    if count==0:
                        led['led_1'].set(0)
                        led['led_2'].set(0)
                        led['led_3'].set(0)
                    elif count==1:
                        led['led_1'].set(0)
                        led['led_2'].set(0)
                        led['led_3'].set(1)
                    elif count==2:
                        led['led_1'].set(0)
                        led['led_2'].set(1)
                        led['led_3'].set(0)
                    elif count==3:
                        led['led_1'].set(0)
                        led['led_2'].set(1)
                        led['led_3'].set(1)
                    elif count==4:
                        led['led_1'].set(1)
                        led['led_2'].set(0)
                        led['led_3'].set(0)
                    elif count==5:
                        led['led_1'].set(1)
                        led['led_2'].set(0)
                        led['led_3'].set(1)
                    elif count==6:
                        led['led_1'].set(1)
                        led['led_2'].set(1)
                        led['led_3'].set(0)
                    elif count==7:
                        led['led_1'].set(1)
                        led['led_2'].set(1)
                        led['led_3'].set(1)
  
             
                    
        elif right_value>950 and left_value>950:
            SetMotorSpeed(3,0)
            if wall_right_down_value!=1000:
                led["led_3"].set(1)
                led["led_2"].set(0)
                led["led_1"].set(0)
                if flag2==0:
                    flag2=1
                    count+=1
            else:
                led["led_3"].set(0)
                led["led_2"].set(0)
                led["led_1"].set(0)
                flag2=0
            if wall_left_down_value!=1000:
                led["led_1"].set(1)
                led["led_2"].set(0)
                led["led_3"].set(0)
                if flag1==0:
                    flag1=1
                    count+=1
            else:
                led["led_1"].set(0)
                led["led_2"].set(0)
                led["led_3"].set(0)
                flag1=0
        elif right_value<950:
            SetMotorSpeed(0,2)
        elif left_value<950:
            SetMotorSpeed(0,-2)
            
    
                
             

    if center_value>450:
        if cam_value>900:
            if wall_right_up_value<1000:
                error = ( 600 - wall_right_up_value )
                rectify = pid(error) 
                SetMotorSpeed(3, rectify)
            elif wall_left_up_value<1000:
                error = (wall_left_up_value - 600)
                rectify = pid(error)
                SetMotorSpeed(3, rectify)    
            elif wall_right_up_value==1000:
                if wall_right_down_value<1000:
                    error = ( 600 - wall_right_down_value )
                    rectify = pid(error)
                    SetMotorSpeed(3, rectify)
                
            else:
                if wall_left_down_value<1000:
                    error = (wall_left_down_value -600 )
                    rectify = pid(error)
                    SetMotorSpeed(3, rectify)
            
                    
        else:
            if wall_right_up_value<1000 :
                SetMotorSpeed(0,3 )
            elif wall_left_up_value<1000:
                SetMotorSpeed(0, -3)
            elif cam_value>300:
                SetMotorSpeed(3, 0)
            else:
                SetMotorSpeed(0, 0)
       
            
            
    pass
    
  
