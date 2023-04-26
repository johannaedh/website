from phone_camera import Phone_Camera
from math import sqrt
from scipy.special import lambertw
from math import tan

OnePlus8 = Phone_Camera("https://en.wikipedia.org/wiki/OnePlus_8")
<<<<<<< HEAD
i= 0.0357143*lambertw(16.0604*sqrt(OnePlus8.megaPixels))
o = i*tan(1)/(0.000000560*OnePlus8.apperature*i-tan(1))

print(OnePlus8.apperature)
print(OnePlus8.megaPixels)
print(abs(o.real))
=======
print(OnePlus8.general_distance)
>>>>>>> a7fc2bd10f82ee998b79c2c4072b86211158164a
