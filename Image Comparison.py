# USAGE
# python image_diff.py --first images/original_01.png --second images/modified_01.png

# import the necessary packages
from skimage.measure import compare_ssim
import argparse
import imutils
import cv2
import os     # libbers for create and delete folder

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-f", "--first", required=False, help="Path first Image Master", default=r"C:\Users\Inpeco\Desktop\Compare\Tip Image.JPG")
ap.add_argument("-s", "--second", required=False, help="Path Image to compare2", default=r"C:\Users\Inpeco\Desktop\Compare\Tip Image1.JPG")
ap.add_argument("-c", "--folder", required=False, help="Path Folder Image", default=r"C:\Users\Inpeco\Desktop\LOG Image Comparison")
ap.add_argument("-n", "--number", required=False, help="Number of file", default= 9)
ap.add_argument("-r", "--resize", required=False, help="Cutter", default= True)
ap.add_argument("-t", "--target", required=False, help="Target Scale", default= 0.999)
args = vars(ap.parse_args())

#---------------------SPLIT PATH---------------------------------------------------------------
PathImageMaster = os.path.dirname(args["first"])
NameFile_Image = os.path.basename(args["first"])
NameFile_ImageP = os.path.splitext(NameFile_Image)[0]
extantionFile = os.path.splitext(NameFile_Image)[1]
Resize = (args["resize"])
#-----------------------VAR TO BLOCK---------------------------------------------------------
block = 0;
bufferFileNotFound = 10
targetscore = (args["target"])

#----------------------CREATE A FILE TXT LOG--------------------------------------------------
path_folder = (args["folder"])
if os.path.exists(path_folder):
    print("Old folder present")
else:
    os.mkdir(path_folder)
    pathLog = os.path.join(path_folder, "Log Compare.txt")
    LogFile = open(pathLog,"a")
    LogFile.write("FILE LOG START")
    LogFile.write("\n")
    LogFile.close()
    print(pathLog)

#print(PathImageMaster)
#print(NameFile_Image)

#----------------------------------------------------------------------------------------------
#-------------------FOR NUMBER PHOTO-----------------------------------------------------------
ActualPhoto = 0
NumberPhoto = (args["number"])
#print(ActualPhoto)
#print(NumberPhoto)

while (ActualPhoto != (NumberPhoto + bufferFileNotFound)):

    print("START")
    #print(NameFile_ImageP)
    incrementPhoto = (ActualPhoto + 1)
    NameFile_Image = str(NameFile_ImageP) + str(incrementPhoto) + str(extantionFile)
    # ---------------------------------------------------------------------------------------------
    PhotoAnalysis = os.path.join(PathImageMaster, NameFile_Image)
    #print(incrementPhoto)
    if os.path.exists(PhotoAnalysis):
        #print(NameFile_Image)
        # print(PhotoAnalysis)
        # ----------------------------------------------------------------------------------------------
        # find folder and create
        # detect the current working directory and print it

        path_folder = (args["folder"])
        # path_folder = os.getcwd()  Check folder in directory project
        print("The current working directory is %s" % path_folder)

        # Create a folder
        try:
            os.mkdir(path_folder)
        except OSError:
            print("Creation of the directory %s failed" % path_folder)
        else:
            print("Successfully created the directory %s" % path_folder)
        # ----------------------------------------------------------------------------------------------
        if Resize == True and block == 0:
            print("RESIZE")

            #----------------------------INT CLASS RESIZE------------------------------------------------
            # initialize the list of reference points and boolean indicating
            # whether cropping is being performed or not
            refPt = []
            cropping = False


            def click_and_crop(event, x, y, flags, param):
                # grab references to the global variables
                global refPt, cropping

                # if the left mouse button was clicked, record the starting
                # (x, y) coordinates and indicate that cropping is being
                # performed
                if event == cv2.EVENT_LBUTTONDOWN:
                    refPt = [(x, y)]
                    cropping = True

                # check to see if the left mouse button was released
                elif event == cv2.EVENT_LBUTTONUP:
                    # record the ending (x, y) coordinates and indicate that
                    # the cropping operation is finished
                    refPt.append((x, y))
                    cropping = False

                    # draw a rectangle around the region of interest
                    cv2.rectangle(image, refPt[0], refPt[1], (0, 255, 0), 2)
                    cv2.imshow("image", image)



            # load the image, clone it, and setup the mouse callback function
            image = cv2.imread(args["first"])
            clone = image.copy()
            cv2.namedWindow("image")
            cv2.setMouseCallback("image", click_and_crop)
            #------------------------------------------------------------------------
            #-------------------------RESIZE IMAGE WAIT PRESS BUTTON------------------
            # keep looping until the 'q' key is pressed
            while True:
                # display the image and wait for a keypress
                cv2.imshow("image", image)
                key = cv2.waitKey(1) & 0xFF

                # if the 'r' key is pressed, reset the cropping region
                if key == ord("r"):
                    image = clone.copy()

                # if the 'c' key is pressed, break from the loop
                elif key == ord("c"):
                    break

            # if there are two reference points, then crop the region of interest
            # from teh image and display it
            if len(refPt):
                imageCheck = cv2.imread(args["first"])
                cloneCheck = imageCheck.copy()
                roi = cloneCheck[refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]]
                #roi2 = cloneCheck[refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]]
                cv2.imshow("ROI", roi)
                #cv2.imshow("ROI", roi2)
                cv2.waitKey(0)
                block = 1
                print("CUT")

            # close all open windows
            cv2.destroyAllWindows()
        else:
            print("NOT RESIZE")
            # load the two input images
            imageA = cv2.imread(args["first"])
            imageB = cv2.imread(PhotoAnalysis)
            # print(PhotoAnalysis)
        print("GO PHOTO")
        if Resize == True:
            PhotoAnalysis = cv2.imread(PhotoAnalysis)
            #cv2.imshow("Original", roi)
            #cv2.waitKey(0)
            imageA = roi
            roiMaster = roi.copy()
            imageA = roiMaster
            imageB = PhotoAnalysis[refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]]

        # convert the images to grayscale
        grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
        grayB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)
        #print(Resize)

        # compute the Structural Similarity Index (SSIM) between the two
        # images, ensuring that the difference image is returned
        (score, diff) = compare_ssim(grayA, grayB, full=True)
        diff = (diff * 255).astype("uint8")
        print("SSIM: {}".format(score))

        # threshold the difference image, followed by finding contours to
        # obtain the regions of the two input images that differ
        thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)

        # loop over the contours
        for c in cnts:
            # compute the bounding box of the contour and then draw the
            # bounding box on both input images to represent where the two
            # images differ
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(imageA, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.rectangle(imageB, (x, y), (x + w, y + h), (0, 0, 255), 2)
        # --------------------------------------------------------------------

        # ----------------Condition matching scale -1 to 1---------------------
        if score >= targetscore:
            print("matching image")
            # -----------LOG------------------------------------------------
            LogFile = open(pathLog, "a", )
            #print("\n", NameFile_Image, ":  matching image"+";"+"0")
            LogFile.write("\n")
            LogFile.write(NameFile_Image + ":  matching image"+";"+"0")
            LogFile.close()
            print("LOG", NameFile_Image)
            # ----------END LOG---------------------------------------------

        else:

            print("not matching image")
            pathFile_Image = os.path.basename(args["second"])
            #print(pathFile_Image)
            path_Image = os.path.join(path_folder, NameFile_Image)
            print(NameFile_Image)

            try:
                os.mkdir(path_Image)
            except OSError:
                print("Creation of the directory %s failed" % path_Image)

            else:
                print("Successfully created the directory %s" % path_Image)
                cv2.imwrite(os.path.join(path_Image, NameFile_Image), imageB)
                # -----------LOG------------------------------------------------
                LogFile = open(pathLog, "a",)
                #print( "\n", NameFile_Image, ":  not matching image"+";"+"1")
                LogFile.write("\n")
                LogFile.write(NameFile_Image + ":  not matching image"+";"+"1")
                LogFile.close()
                print("LOG",NameFile_Image)
                # ----------END LOG---------------------------------------------

        # --------------------------------------------------------------------
        ActualPhoto = ActualPhoto + 1

        # show the output images
        #cv2.imshow("Original", imageA)
        #cv2.imshow("Modified", imageB)
        # cv2.imshow("Diff", diff)
        # cv2.imshow("Thresh", thresh)
        cv2.waitKey(0)

    else:
        ActualPhoto = ActualPhoto + 1
        print("FILE NOT FOUND")

else:
    print("IMAGES CHECK COMPLETE")

