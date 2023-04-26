from data_analysis_module_2 import DataAnalyzis
from HejHej.image_processing_module import ImageProcessing
# Exempel

# object = ImageProcessing('/Users/efraimzetterqvist/Documents')

# cal_side_x, cal_side_y, ball_radius_side = object.calibrate_cross('/Users/efraimzetterqvist/Documents/kal_side2.mov', 'side')
# cal_floor_x, cal_floor_y, ball_radius_floor = object.calibrate_cross('/Users/efraimzetterqvist/Documents/kal_floor3.mov', 'floor')

# throw_floor_Axel_x, throw_floor_Axel_y, fps_floor = object.measure_throw('/Users/efraimzetterqvist/Documents/Axel_floor.mov', 1/3*(ball_radius_floor*2)**2, 'floor')
# throw_side_Axel_x, throw_side_Axel_y, fps_side = object.measure_throw('/Users/efraimzetterqvist/Documents/Axel_side.mov', 1/3*(ball_radius_side*2)**2, 'side')
# throw = DataAnalyzis(throw_floor_Axel_x, throw_floor_Axel_y, throw_side_Axel_x, throw_side_Axel_y, 240, ball_radius_floor, ball_radius_side)
# print('Axels kast:')
# throw_velocity = throw.velocity()
# throw_accuracy = throw.accuracy(cal_floor_x, cal_floor_y, cal_side_x, cal_side_y)