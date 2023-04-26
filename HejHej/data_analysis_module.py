import numpy as np

class DataAnalyzis:

    def __init__(self, x_floor, y_floor, x_side, y_side, frame_rate, ball_radius_floor, ball_radius_side):

        self.frame_rate=frame_rate
        self.converter_side = 17.78/(2*ball_radius_side)
        self.converter_floor = 17.78/(2*ball_radius_floor)
        self.x_floor = x_floor
        self.y_floor = y_floor
        self.x_side = x_side
        self.y_side = y_side

    def velocity(self):

        # Skapar en lista för hastigheten
        velocity = []
        
        # Tar bort alla värden för bilder då en boll ej var detekterad, 
        # fram tills första detekterade bollen
        for element in self.x_floor[:]:
            if int(element) == 0:
                self.x_floor.remove(element) 
            else:
                break
        for element in self.y_floor[:]:
            if int(element) == 0:
                self.y_floor.remove(element) 
            else:
                break
        for element in self.x_side[:]:
            if int(element) == 0:
                self.x_side.remove(element) 
            else:
                break
        for element in self.y_side[:]:
            if int(element) == 0:
                self.y_side.remove(element)
            else:
                break

        count = 0
        for element in range(0, len(self.x_floor)):
            if self.x_floor[element] == 0:
                count += 1
                continue
            if count == 1:
                self.x_floor[element-count] = self.x_floor[element-count-1] - (self.x_floor[element-count-1] - self.x_floor[element])/(count+1)
                count = 0
            elif count == 2:
                self.x_floor[element-count] = self.x_floor[element-count-1] - (self.x_floor[element-count-1] - self.x_floor[element])/(count+1)
                self.x_floor[element-count+1] = self.x_floor[element-count] - (self.x_floor[element-count-1] - self.x_floor[element])/(count+1)
                count = 0
            elif count > 2:
                print('Kastet kunde ej detekterades väl nog')
        count = 0
        for element in range(0, len(self.y_floor)):
            if self.y_floor[element] == 0:
                count += 1
                continue
            if count == 1:
                self.y_floor[element-count] = self.y_floor[element-count-1] - (self.y_floor[element-count-1] - self.y_floor[element])/(count+1)
                count = 0
            elif count == 2:
                self.y_floor[element-count] = self.y_floor[element-count-1] - (self.y_floor[element-count-1] - self.y_floor[element])/(count+1)
                self.y_floor[element-count+1] = self.y_floor[element-count] - (self.y_floor[element-count-1] - self.y_floor[element])/(count+1)
                count = 0
            elif count > 2:
                print('Kastet kunde ej detekterades väl nog')
        count = 0
        for element in range(0, len(self.x_side)):
            if self.x_side[element] == 0:
                count += 1
                continue
            if count == 1:
                self.x_side[element-count] = self.x_side[element-count-1] + (self.x_side[element] - self.x_side[element-count-1])/(count+1)
                count = 0
            elif count == 2:
                self.x_side[element-count] = self.x_side[element-count-1] + (self.x_side[element] - self.x_side[element-count-1])/(count+1)
                self.x_side[element-count+1] = self.x_side[element-count] + (self.x_side[element] - self.x_side[element-count-1])/(count+1)
                count = 0
            elif count > 2:
                print('Kastet kunde ej detekterades väl nog')
        count = 0
        for element in range(0, len(self.y_side)):
            if self.y_side[element] == 0:
                count += 1
                continue
            if count == 1:
                self.y_side[element-count] = self.y_side[element-count-1] - (self.y_side[element-count-1] - self.y_side[element])/(count+1)
                count = 0
            elif count == 2:
                self.y_side[element-count] = self.y_side[element-count-1] - (self.y_side[element-count-1] - self.y_side[element])/(count+1)
                self.y_side[element-count+1] = self.y_side[element-count] - (self.y_side[element-count-1] - self.y_side[element])/(count+1)
                count = 0
            elif count > 2:
                print('Kastet kunde ej detekterades väl nog')

        diff = len(self.x_side) - len(self.y_floor)

        if diff < 0:
            del self.x_floor[0:-diff]
            del self.y_floor[0:-diff]
            del self.x_floor[-2:]
            del self.y_floor[-2:]
            del self.x_side[-2:]
            del self.y_side[-2:]
        elif diff > 0:
            del self.x_side[0:diff]
            del self.y_side[0:diff]
            del self.x_floor[-2:]
            del self.y_floor[-2:]
            del self.x_side[-2:]
            del self.y_side[-2:]
        
        for k in range(1,len(self.y_floor)):     
            distance_between_frames = np.sqrt((self.converter_side*(self.x_side[k]-self.x_side[k-1]))**2+(self.converter_floor*(self.y_floor[k]-self.y_floor[k-1]))**2+(self.converter_side*(self.y_side[k]-self.y_side[k-1]))**2)
            velocity.append(3.6 / 100 * distance_between_frames * self.frame_rate)  
        mean_velocity = sum(velocity)/len(velocity)
        print('Hasitgheten för bollen var: ' + str(mean_velocity) + ' km/h')
        return mean_velocity

    def accuracy(self, cross_position_floor_x, cross_position_floor_y, cross_position_side_x, cross_position_side_y):
    
        cross_coord_x = cross_position_floor_y
        cross_coord_y = cross_position_side_y
        x_coord = self.x_floor[-1]
        y_coord = self.y_side[-1]
        diff_x = self.converter_floor * (cross_coord_x-x_coord)
        diff_y = self.converter_side * (cross_coord_y-y_coord)
        diff_tot = np.sqrt(diff_x**2 + diff_y**2)
        print('Bollens avstånd från målet i x-led: ' + str(diff_x) + ' cm')
        print('Bollens avstånd från målet i y_led: ' + str(diff_y) + ' cm')
        print('Bollens totala avstånd från målet: ' + str(diff_tot) + ' cm')
        return diff_x, diff_y, diff_tot