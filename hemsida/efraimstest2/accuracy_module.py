import numpy as np

def accuracy(x_floor, y_side, ball_radius_side, ball_radius_floor, cross_position_floor_x, cross_position_floor_y, cross_position_side_x, cross_position_side_y):
    
        converter_side = 17.78/(2*ball_radius_side)
        converter_floor = 17.78/(2*ball_radius_floor)

        cross_coord_x = cross_position_floor_y
        cross_coord_y = cross_position_side_y
        x_coord = x_floor[-1]
        y_coord = y_side[-1]
        diff_x = converter_floor * (cross_coord_x-x_coord)
        diff_y = converter_side * (cross_coord_y-y_coord)
        diff_tot = np.sqrt(diff_x**2 + diff_y**2)
        print('Bollens avstånd från målet i x-led: ' + str(diff_x) + ' cm')
        print('Bollens avstånd från målet i y-led: ' + str(diff_y) + ' cm')
        print('Bollens totala avstånd från målet: ' + str(diff_tot) + ' cm')
        return diff_x, diff_y, round(diff_tot, 1)