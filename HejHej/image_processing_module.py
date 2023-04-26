import cv2
import os
from roboflow import Roboflow
import shutil
from data_analysis_module import DataAnalyzis 
import numpy as np

class ImageProcessing:

    def __init__(self, directory_path):
        self.directory_path = directory_path
        self.folder_name = "dodge"  

    
    # Denna funktion kalibrerar kryssets position. Som input skickas en path 
    # till en video där användaren håller bollen mot krysset samt vilken av kamerorna videon 
    # är tagen från
    def calibrate_cross(self, video_path, camera_angle):

        # Skapar den tomma mappen 'dodge' på plats vald av användaren
        os.mkdir(os.path.join(self.directory_path, self.folder_name))
        print(f"Created folder {self.folder_name} in directory {self.directory_path}")

        # Öppnar kalibreringsvideon
        video = cv2.VideoCapture(video_path)

        # Delar upp videon i frames som placeras i mappen 'dodge'
        i=0
        path = self.directory_path + "/" + self.folder_name
        while(video.isOpened()):
            ret, frame = video.read()
            if ret == False:
                break
            cv2.imwrite(os.path.join(path,'dodge'+str(i)+'.jpg'),frame)
            i+=1
        frame_rate = int(video.get(cv2.CAP_PROP_FPS))

        # Stänger ner videon
        video.release()
        cv2.destroyAllWindows()

        # Tillkallar en i Roboflow tränad modell för att detektera fotbollar
        rf = Roboflow(api_key="HEfNlI5lkTBazBknN8jz")
        project = rf.workspace().project("footballs-1trlz")
        model = project.version(3).model

        # Gör en lista över de frames där detektering av dodgeball är aktuell för kalibrering
        list_of_images_numbers = list(range(1, i, frame_rate))

        # Skapar listor för bildens x- & y-koordinat och bollens bredd och höjd
        x = []
        y = []
        w = []
        h = []

        # Detekterar bollen för de aktuella framesen och stoppar kalibreringen då 
        # bollen varit relativt stilla mellan två aktuella frames (1 sekund)
        for k in list_of_images_numbers:
            prediction = model.predict(self.directory_path + "/" + self.folder_name + "/dodge" + str(k) + '.jpg')
            for result in prediction.json()['predictions']:
                x.append(result['x'])
                y.append(result['y'])
                w.append(result['width'])
                h.append(result['height'])
            if len(x) < 2:
                continue
            if len(y) < 2:
                continue
            if max(abs(x[-2] - x[-1]), abs(y[-2] - y[-1])) < 3:
                print('Calibration for ' + camera_angle + ' camera done successfully')
                break
        
        # Sparar kryssets x- & y-koordinat i två variabler samt bollens radie
        cross_position_x = x[-1]
        cross_position_y = y[-1]
        self.ball_radius = (w[-1] + h[-1])/4

        # Raderar mappen 'dodge' innehållandes alla frames
        shutil.rmtree(self.directory_path + '/' + self.folder_name)  

        # Skriver ut kryssets koordinater samt returnerar dem + bollens radie
        print('x: ' + str(cross_position_x), 'y: ' + str(cross_position_y))  
        print('Bollens radie för ' + camera_angle + ' camera: ' + str(self.ball_radius))
        return cross_position_x, cross_position_y, self.ball_radius


    # Denna funktion spottar ut en lista med x- & y-koordinater för bollens position
    # under flera frames för ett kast. 
    # Som input skickas en path till en video av kastet, den minsta arean som kan detekteras,
    # samt vilken av de två kamerorna videon kommer ifrån
    def measure_throw(self, video_path, min_ball_area, camera_angle):

        # Öppnar kastvideon
        video = cv2.VideoCapture(video_path)

        landscape = False
        portrait = False

        # Ger bredden och höjden för videon i pixlar
        width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        # Checkar om video är i formatet landscape eller portrait
        if width > height:
            landscape = True
        else:
            portrait = True

        # Tar ut den första bilden och anger den som bakgrundsbild
        _, bg = video.read()
        bg_gray = cv2.cvtColor(bg, cv2.COLOR_BGR2GRAY)

        # Definierar minsta skillnad mellan bakgrund och bild
        threshold = 35

        # Skapar listor för bildens x- & y-koordinat samt höjd och bredd
        x_list = []
        y_list = []
        w_list = []
        h_list = []

        count = 0

        # Loopar igenom alla frames i videon tills bollen studsar mot väggen
        while(video.isOpened()):

            # Delar upp videon i frames
            ret, frame = video.read()

            # Checkar om det lyckades
            if ret == False:
                break

            # Konvertera nuvarande frame till gråskala (underlättar detektion)
            count += 1
            frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Subtraherar nuvarande frame från bakgrundsbilden
            diff = cv2.absdiff(bg_gray, frame_gray)
            _, thresh = cv2.threshold(diff, threshold, 255, cv2.THRESH_BINARY)
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
            thresh = cv2.erode(thresh, kernel, iterations=2)
            thresh = cv2.dilate(thresh, kernel, iterations=2)

            # Hittar sjok av pixelförändringar för att urskilja bollen
            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # Loopar igenom sjoken
            for contour in contours:
                # Beräknar arean av sjoket
                area = cv2.contourArea(contour)

                # Checkar om sjoket är en boll
                if area > min_ball_area:
                    # Ritar en box runt bollen
                    x, y, w, h = cv2.boundingRect(contour)
                    center_x = x + w/2
                    center_y = y + h/2
                    x_list.append(center_x)
                    y_list.append(center_y)
                    w_list.append(w)
                    h_list.append(h)
                    box_left_corner_x = int(center_x - self.ball_radius)
                    box_left_corner_y = int(center_y + self.ball_radius)
                    box_right_corner_x = int(center_x + self.ball_radius)
                    box_right_corner_y = int(center_y - self.ball_radius)
                    cv2.rectangle(frame, (box_left_corner_x, box_left_corner_y), (box_right_corner_x, box_right_corner_y), (0, 0, 255), 2)
                    break
            
            # Spelar upp nuvarande frame
            cv2.imshow('frame', frame)

            # Villkor för när bollen har träffat väggen och videon ska sluta spelas upp
            # Om videon kommer från sidokameran:
            if camera_angle == 'side':
                # om videon är i formatet landscape:
                if landscape == True:
                    # Lägger till en 0:a i listan om bollen inte kunde detekteras
                    if len(x_list) < count:
                        x_list.append(0)
                        y_list.append(0)
                        w_list.append(0)
                        h_list.append(0)

                    if len(x_list) < 2:
                        continue

                    # Stannar loopen om bollen har börjat studsa tillbaka
                    if x_list[-1] < x_list[-2]:
                        if x_list[-1] == 0:
                            continue
                        else:
                            del x_list[-1:]
                            del y_list[-1:]
                            del w_list[-1:]
                            del h_list[-1:]
                            break

                # om videon är i formatet portrait:
                elif portrait == True:
                    # Lägger till en 0:a i listan om bollen inte kunde detekteras
                    if len(y_list) < count:
                        x_list.append(0)
                        y_list.append(0)
                        w_list.append(0)
                        h_list.append(0)

                    if len(y_list) < 2:
                        continue
                    
                    # Stannar loopen om bollen har börjat studsa tillbaka
                    if y_list[-1] < y_list[-2]:
                        if y_list[-1] == 0:
                            continue
                        else:
                            del x_list[-1:]
                            del y_list[-1:]
                            del w_list[-1:]
                            del h_list[-1:]
                            break

            # Om videon kommer från golvkameran:
            if camera_angle == 'floor':
                # om videon är i formatet landscape:
                if landscape == True:
                    # Lägger till en 0:a i listan om bollen inte kunde detekteras
                    if len(y_list) < count:
                        x_list.append(0)
                        y_list.append(0)
                        w_list.append(0)
                        h_list.append(0)

                    if len(y_list) < 2:
                        continue

                    # Stannar loopen om bollen har börjat studsa tillbaka
                    if y_list[-1] < y_list[-2]:
                        if y_list[-1] == 0:
                            continue
                        else:
                            del x_list[-1:]
                            del y_list[-1:]
                            del w_list[-1:]
                            del h_list[-1:]
                            break

                # om videon är i formatet portrait:
                elif portrait == True:
                    # Lägger till en 0:a i listan om bollen inte kunde detekteras
                    if len(x_list) < count:
                        x_list.append(0)
                        y_list.append(0)
                        w_list.append(0)
                        h_list.append(0)

                    if len(x_list) < 2:
                        continue

                    # Stannar loopen om bollen har börjat studsa tillbaka
                    if x_list[-1] > x_list[-2]:
                        if x_list[-2] == 0:
                            continue
                        else:
                            del x_list[-1:]
                            del y_list[-1:]
                            del w_list[-1:]
                            del h_list[-1:]
                            break


            # Videon slutar också spelas upp om användaren trycker på tangenten 'q'
            key = cv2.waitKey(1)
            if key == ord('q'):
                break

        # Stänger ner videon
        video.release()
        cv2.destroyAllWindows() 

        # Returnerar en lista vardera över x- % y-koordinater för de frames då bollen är i bild
        return x_list, y_list


