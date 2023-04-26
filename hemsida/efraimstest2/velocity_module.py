import numpy as np

def velocity(x_side, y_side, x_floor, y_floor, ball_radius_side, ball_radius_floor, frame_rate):

        throw_ok = True
        # Skapar en lista för hastigheten
        velocity = []

        converter_side = 17.78/(2*ball_radius_side)
        converter_floor = 17.78/(2*ball_radius_floor)
        
        # Tar bort alla värden för bilder då en boll ej var detekterad, 
        # fram tills första detekterade bollen
        for element in x_floor[:]:
            if int(element) == 0:
                x_floor.remove(element) 
            else:
                break
        for element in y_floor[:]:
            if int(element) == 0:
                y_floor.remove(element) 
            else:
                break
        for element in x_side[:]:
            if int(element) == 0:
                x_side.remove(element) 
            else:
                break
        for element in y_side[:]:
            if int(element) == 0:
                y_side.remove(element)
            else:
                break
        # print(x_floor)
        # print(y_floor)
        # print(x_side)
        # print(y_side)
        
        num_nodet_frames = 0
        steps = 1
        for element in range(0, len(x_floor)):
            if x_floor[element] == 0:
                num_nodet_frames += 1
            else:
                if num_nodet_frames/len(x_floor) > 0.5:
                    throw_ok = False
                    print('Kastet kunde ej detekterades väl nog')
                else:
                    while steps <= num_nodet_frames:
                        x_floor[element-steps] = x_floor[element-num_nodet_frames-1] + ((x_floor[element] - x_floor[element-num_nodet_frames-1])*(num_nodet_frames+1-steps))/(num_nodet_frames+1)
                        steps += 1
                    num_nodet_frames = 0
                    steps = 1
        num_nodet_frames = 0
        steps = 1
        for element in range(0, len(y_floor)):
            if y_floor[element] == 0:
                num_nodet_frames += 1
            else:
                if num_nodet_frames/len(y_floor) > 0.5:
                    throw_ok = False
                    print('Kastet kunde ej detekterades väl nog')
                else:
                    while steps <= num_nodet_frames:
                        y_floor[element-steps] = y_floor[element-num_nodet_frames-1] + ((y_floor[element] - y_floor[element-num_nodet_frames-1])*(num_nodet_frames+1-steps))/(num_nodet_frames+1)
                        steps += 1
                    num_nodet_frames = 0
                    steps = 1
        num_nodet_frames = 0
        steps = 1
        for element in range(0, len(x_side)):
            if x_side[element] == 0:
                num_nodet_frames += 1
            else:
                if num_nodet_frames/len(x_side) > 0.5:
                    throw_ok = False
                    print('Kastet kunde ej detekterades väl nog')
                else:
                    while steps <= num_nodet_frames:
                        x_side[element-steps] = x_side[element-num_nodet_frames-1] + ((x_side[element] - x_side[element-num_nodet_frames-1])*(num_nodet_frames+1-steps))/(num_nodet_frames+1)
                        steps += 1
                    num_nodet_frames = 0
                    steps = 1
        num_nodet_frames = 0
        steps = 1
        for element in range(0, len(y_side)):
            if y_side[element] == 0:
                num_nodet_frames += 1
            else:
                if num_nodet_frames/len(y_side) > 0.5:
                    throw_ok = False
                    print('Kastet kunde ej detekterades väl nog')
                else:
                    while steps <= num_nodet_frames:
                        y_side[element-steps] = y_side[element-num_nodet_frames-1] + ((y_side[element] - y_side[element-num_nodet_frames-1])*(num_nodet_frames+1-steps))/(num_nodet_frames+1)
                        steps += 1
                    num_nodet_frames = 0
                    steps = 1
        # print(x_floor)
        # print(y_floor)
        # print(x_side)
        # print(y_side)
        diff = len(x_side) - len(y_floor)

        if diff < 0:
            del x_floor[0:-diff]
            del y_floor[0:-diff]
            del x_floor[-2:]
            del y_floor[-2:]
            del x_side[-2:]
            del y_side[-2:]
        elif diff > 0:
            del x_side[0:diff]
            del y_side[0:diff]
            del x_floor[-2:]
            del y_floor[-2:]
            del x_side[-2:]
            del y_side[-2:]
        
        for k in range(1,len(y_floor)):     
            distance_between_frames = np.sqrt((converter_side*(x_side[k]-x_side[k-1]))**2+(converter_floor*(y_floor[k]-y_floor[k-1]))**2+(converter_side*(y_side[k]-y_side[k-1]))**2)
            velocity.append(3.6 / 100 * distance_between_frames * frame_rate) 
        if len(velocity) > 0:
            #print(velocity)
            mean_velocity = sum(velocity) / len(velocity)
            print('Hasitgheten för bollen var: ' + str(mean_velocity) + ' km/h')
            return round(mean_velocity, 1), throw_ok
        else:
            # Handle the case when the velocity list is empty
            print("No throw detected")
            mean_velocity = None 
            return mean_velocity, throw_ok
        
        