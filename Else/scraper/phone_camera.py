from webscraped import func
from scipy.special import lambertw
from math import sqrt, tan

class Phone_Camera:
    list = []
    megaPixels = 0.0
    apperature = 0.0
    image_center_size_ = 0.0
    pixel_size_ = 0.0
    general_distance = 0.0

    def __init__(self, URL):
        self.list = func(URL)
        self.megaPixels = self.list[0]
        self.apperature = self.list[1]
        try:
            self.image_center_size_ = self.list[2]
            self.pixel_size_ = self.list[3]
        except IndexError:
            self.image_center_size_ = None
            self.pixel_size_ = None
        i= 0.0357143*lambertw(16.0604*sqrt(self.megaPixels))
        o = i*tan(1)/(0.000000560*self.apperature*i-tan(1)).real
        self.general_distance = abs(o)
