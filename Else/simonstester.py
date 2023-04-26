import cv2

# Load the image
img = cv2.imread("C:/Users/Joakim/Documents/3an/Kandidatarbete/Egen programmering/dodgeball_red1.jpg")

# Display the image and wait for a mouse click
cv2.imshow("Image", img)
#cv2.waitKey(0)

# Define a callback function to handle mouse events
def onMouse(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        # Print the pixel value at the clicked location
        print("Pixel value at ({}, {}): {}".format(x, y, img[y, x]))
        cv2.destroyAllWindows()

cv2.setMouseCallback("Image", onMouse)
# Set the callback function for mouse events
cv2.waitKey(0)
print('hej')


# Wait for a key press to exit
#cv2.waitKey(0)
#cv2.destroyAllWindows()
