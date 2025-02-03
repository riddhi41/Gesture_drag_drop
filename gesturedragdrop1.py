
from cvzone.HandTrackingModule import HandDetector
import cv2

cap = cv2.VideoCapture(0)
cap.set(3, 1288)
cap.set(4, 720)
detector = HandDetector(staticMode=False, maxHands=2, modelComplexity=1, detectionCon=0.8)

cap = cv2.VideoCapture(0)
cap.set(3, 1288)
cap.set(4, 720)
detector = HandDetector(detectionCon=0.8)
coloR = (255,0,255)

cx, cy, w, h = 100, 100, 200, 200

class DragRect():
    def __init__(self, posCenter, size=[200,200]):
        self.posCenter = posCenter
        self.size = size

    def update(self, cursor):
        cx,cy = self.posCenter
        w, h = self.size

        #index tip in region
        if cx - w // 2 < cursor[0] < cx + w // 2 and cy - h // 2 < cursor[1] < cy + h // 2:
            coloR = (0, 255, 0)
            self.posCenter = cursor[0], cursor[1]

rectList = []
for x in range(5):
    rectList.append(DragRect([x*250+150,150]))

while True:
   success, img = cap.read()
   img = cv2.flip(img, 1)
   hands, img = detector.findHands(img, draw=True, flipType=False)
   if hands:
       #  hand detected
       hand1 = hands[0]  # hand detected
       lmList1 = hand1["lmList"]  # 21 landmarks
       bbox1 = hand1["bbox"]  # Bounding box around the  hand (x,y,w,h coordinates)
       center1 = hand1['center'] # Center coordinates of the hand
       handType1 = hand1["type"] # Type of the  hand ("Left" or "Right")

       # calculate distance between specific landmarks on the  hand
       length, info, img = detector.findDistance(lmList1[8][0:2], lmList1[12][0:2], img, color=(255, 0, 255),
                                                 scale=10)

       if lmList1:
           x1, y1 = lmList1[8][0:2]
           x2, y2 = lmList1[12][0:2]

           l, _, _ = detector.findDistance((x1, y1), (x2, y2), img)
           print(l)

           if l<60:
               cursor = lmList1[8]

               #call the update
               for rect in rectList:
                    rect.update(cursor)
   #draw
   for rect in rectList:
       cx, cy = rect.posCenter
       w, h = rect.size
       cv2.rectangle(img, (cx - w // 2, cy - h // 2), (cx + w // 2, cy + h // 2), coloR, cv2.FILLED)


   cv2.imshow("image", img)
   cv2.waitKey(1)

