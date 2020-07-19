            #each frame conversion to gray scale and Gaussian blur filter applying
            gray = cv2.cvtColor(frames, cv2.COLOR_BGR2GRAY)

            # Detects cars of different sizes in the input image 
            cars = car_cascade.detectMultiScale(gray, 1.3, 3) 
              
            # To draw a rectangle in each cars 
            for (x,y,w,h) in cars: 
                cv2.rectangle(frames,(x,y),(x+w, y+h),(0,0,255),2) 



            #save every 10th frame in the video
            #each frame must be resized to 340 x 20 pixels 
            if c <= 680:
                if c % 20 == 0:
                    cv2.imshow('highway_vehicles_detected', frames)
                    success, image = self.video.read()
                    resize = cv2.resize(frames, (340, 220), interpolation=cv2.INTER_LINEAR)
                    cv2.imwrite("%03ddection.jpg" % c, resize)

                c += 1

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    print("Video detection halted.")
                    break

                else:
                    print ("Video is completed.")
                    break

        # cleanup the camera and close any open windows
        cv2.destroyAllWindows()
            
            gray = cv2.GaussianBlur(gray, (21,21), 0)

            if ReferenceFrame is None:
                ReferenceFrame = gray
                continue                 

            
            #Background subtraction and image binarization
            FrameDelta = cv2.absdiff(ReferenceFrame, gray)
            FrameThresh = cv2.threshold(FrameDelta, 
                VideoCamera.BinarizationThreshold, 255, cv2.THRESH_BINARY )[1]


            #Dilate image and find all the contours
            FrameThresh = cv2.dilate(FrameThresh, None, iterations=2)
            _, cnts, _ = 
                cv2.findContours(FrameThresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            QttyOfContours = 0

            #plot reference lines (entrance and exit lines)
            CoorYEntranceLine = (VideoCamera.height / 2) - VideoCamera.OffsetRefLines
            CoorYExitLine = (VideoCamera.height / 2) + VideoCamera.OffsetRefLines

            cv2.line(frame, (0, CoorYEntranceLine), (VideoCamera.width,CoorYEntranceLine),
                (255, 0, 0), 2)
            cv2.line(frame, (0, CoorYExitLine), (VideoCamera.width,CoorYExitLine),
                (0, 0, 255), 2)

            
            #check all found countours
            for c in cnts:
                #if a contour has small area, it'll be ignored
                if cv2.contourArea(c) < VideoCamera.MinCountourArea:
                    continue

                QttyOfContours = QttyOfContours + 1

                #draw an rectangle "around" the object
                (x, y, w, h) = cv2.boundingRect(c)
                cv2.rectangle(frames, (x,y), (x + w, y + h), (0, 0, 255), 2)

                #find object's centroid
                CoordXCentroid = (x+x+w) / 2
                CoordYCentroid = (y+y+h) / 2
                ObjectCentroid = (CoordXCentroid, CoordYCentroid)
                cv2.circle(frames, ObjectCentroid, 1, (0,0,0), 5)


            if (CheckEntranceLineCrossing(
                CoordYCentroid,CoorYEntranceLine, CoorYExitLine)):
                VideoCamera.EntranceCounter += 1


            if (CheckExitLineCrossing(
                CoordYCentroid,CoorYEntranceLine, CoorYExitLine)):
                VideoCamera.ExitCounter += 1

            print ("Total rectangle found: "+str(QttyOfRectangle))
            print ("Total countours found: "+str(QttyOfContours))

            #Write entrance and exit counter values on frame and shows it
            cv2.putText(frames, "Entrances: {}" .format(str(VideoCamera.EntranceCounter)), 
                (10,50), cv2.FONT_HERSEY_SIMPLEX, 0.5, (250, 0, 1), 2)

            cv2.putText(frames, "Exits: {}" .format(str(VideoCamera.ExitCounter)), 
                (10,50), cv2.FONT_HERSEY_SIMPLEX, 0.5, (250, 0, 1), 2)
