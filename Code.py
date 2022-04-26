import math
import random
import cvzone
import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector


cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
detector = HandDetector(detectionCon=0.8)

class snakegameclass:
    def __init__(self,pathfood):
        self.points=[]
        self.lengths=[]
        self.currentlength= 0
        self.allowedlength= 250
        self.previoushead = 0,0

        self.imgfood = cv2.imread(pathfood, cv2.IMREAD_UNCHANGED)
        self.hfood, self.wfood,_ = self.imgfood.shape
        self.foodpoint = 0, 0

        self.randomFoodLocation()

        self.score = 0
        self.gameover = False

    def randomFoodLocation(self):
        self.foodpoint=random.randint(100,1000),random.randint(100,600)


    def update(self , imgmain , currenthead):

        if self.gameover:
            cvzone.putTextRect(imgmain,"Game Over",[300,400],scale=7,thickness=5,offset=20)
            cvzone.putTextRect(imgmain, f"your Score is :{self.score}", [300, 550], scale=7, thickness=5, offset=20)

        else:


            px, py = self.previoushead
            cx, cy= currenthead

            self.points.append([cx, cy])
            distance=math.hypot(cx-px ,cy-py)

            self.lengths.append(distance)
            self.currentlength += distance
            self.previoushead = cx, cy




            # reducing legnth
            if self.currentlength>self.allowedlength:
                for i , length in enumerate(self.lengths):
                    self.currentlength -= length
                    self.lengths.pop(i)
                    self.points.pop(i)

                    if self.currentlength < self.allowedlength:
                        break

            rx, ry = self.foodpoint
            if rx-self.wfood//2 <cx< rx+self.wfood//2 and ry-self.wfood//2<cy< ry+self.wfood//2:
                self.randomFoodLocation()
                self.allowedlength += 50
                self.score += 1
                print(self.score)



            # drwa snake
            if self.points:
                for i , point in enumerate(self.points):
                    if i !=0:
                        cv2.line(imgmain,self.points[i - 1],self.points[i],(0,0,255),20)
                cv2.circle(imgmain,self.points[-1],20,(200,0,200),cv2.FILLED)

            #Draw food
            imgmain= cvzone.overlayPNG(imgmain,self.imgfood,(rx-self.wfood//2,ry-self.hfood//2))

            cvzone.putTextRect(imgmain, f"Game Score :{self.score}", [50 , 80], scale=3, thickness=3, offset=10)

            # check for Collisions
            pts = np.array(self.points[:2], np.int32)
            pts = pts.reshape((-1, 1, 2))
            cv2.polylines(imgmain, [pts], False, (0, 200, 0), 3)
            minDist=cv2.pointPolygonTest(pts,(cx,cy),True)

            #print(minDist)
            if 2 <= minDist <= -2:
                print("hit")
                self.gameover = True
                self.points = []
                self.lengths = []
                self.currentlength = 0
                self.allowedlength = 250
                self.previoushead = 0, 0

                self.randomFoodLocation()

        return imgmain


game = snakegameclass("stc1.png")



while True:
    success, img = cap.read()
    img=cv2.flip(img,1)
    hands,img = detector.findHands(img,flipType=False)

    if hands:
        # Find distance between fingers
        lmList = hands[0]['lmList']
        imgpointer = lmList[8][0:2]
        img = game.update(img,imgpointer)



    cv2.imshow("Snake Game by Asif", img)
    key=cv2.waitKey(1)
    if key==ord("r"):
        game.gameover=False
cap.release()
cv2.destryAllWindows()
