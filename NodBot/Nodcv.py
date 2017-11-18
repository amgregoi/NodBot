import numpy as np
import cv2
import mss
from matplotlib import pyplot as plt
import Output as NodLog

# Dictionary of Screen Shot template files 
SSQueries = {
    "exit": "NodBot/images/exit.png",
    "confirm": "NodBot/images/confirm.png",
    "chest1": "NodBot/images/chest_1.png",
    "chest2": "NodBot/images/chest_2.png",
    "chest3": "NodBot/images/chest_3.png",
    "ooc": "NodBot/images/setup/map.jpg", #out of combat
    }

# CONSTANTS
MIN_MATCH_COUNT = 5

#Var
mScreen = mss.mss()

"""
" 
"
" Parent: None
"""
def takeSetupSS(aPath):
    monitor = {'top': 200, 'left': 100, 'width': 127, 'height': 127}
    lOutput = aPath.format(**monitor)
    lScreenShot = mScreen.grab(monitor)
    mss.tools.to_png(lScreenShot.rgb, lScreenShot.size, lOutput)

"""
" This function takes a screenshot and keypoint matches to specified query template
"
" Parent: None
"""
def doScreenMatch (aQueryTemplate):
    monitor = {'top': 200, 'left': 100, 'width': 815, 'height': 815}
    lOutput = 'current.png'.format(**monitor)
    lScreenShot = mScreen.grab(monitor)
    mss.tools.to_png(lScreenShot.rgb, lScreenShot.size, lOutput)
    
    coords = matchImage("current.png", aQueryTemplate, False)
    return coords


"""
" This function uses SIFT & BruteForce-Hamming matcher to scan for chests.
"
" Parent: None
"""
def chestMatch(query):
    monitor = {'top': 0, 'left': 0, 'width': 815, 'height': 815}
    lOutput = 'current.png'.format(**monitor)
    lScreenShot = mScreen.grab(monitor)
    mss.tools.to_png(lScreenShot.rgb, lScreenShot.size, lOutput)

    img1 = cv2.imread(query, 0)          # queryImage
    img2 = cv2.imread('current.png',0) # trainImage

    # Initiate SIFT detector
    sift = cv2.xfeatures2d.SIFT_create()

    # find the keypoints and descriptors with SIFT
    kp1, des1 = sift.detectAndCompute(img1,None)
    kp2, des2 = sift.detectAndCompute(img2,None)

    # BFMatcher with default params
    bf = cv2.BFMatcher()
    matches = bf.knnMatch(des1,des2, k=2)

    # Apply ratio test
    good = []
    for m,n in matches:
        if m.distance < .65*n.distance:
            good.append([m])

    NodLog.logDebug("Good points: %d" %len(good), 1)
    

    del img1
    del img2

    # cv2.drawMatchesKnn expects list of lists as matches.
    # img3 = cv2.drawMatchesKnn(img1,kp1,img2,kp2,good,None,flags=2)
    # plt.imshow(img3),plt.show()

    #Average the coordinates of the 'good' matches
    x = 0; y = 0; count = 0
    for key in good:
        x += kp2[key[0].trainIdx].pt[0]
        y += kp2[key[0].trainIdx].pt[1]
        count += 1

    if count > 0:
        return ((x/count)/2, (y/count)/2)

    return None

"""
" OpenCV private keypoint template match
"
" Parent: None
"""
def matchImage(screenshot, query, output):
    lQueryImage = cv2.imread(query, 0) #1
    lScreenImage = cv2.imread(screenshot, 0) #2

    # Initiate SIFT detector
    sift = cv2.xfeatures2d.SIFT_create()

    # find the keypoints and descriptors with SIFT
    kp1, des1 = sift.detectAndCompute(lQueryImage,None)
    kp2, des2 = sift.detectAndCompute(lScreenImage,None)

    FLANN_INDEX_KDTREE = 0
    index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
    search_params = dict(checks = 50)

    flann = cv2.FlannBasedMatcher(index_params, search_params)

    matches = flann.knnMatch(des1,des2,k=2)

    # store all the good matches as per Lowe's ratio test.
    good = []
    for m,n in matches:
        if m.distance < 0.7 * n.distance:
            good.append(m)

    if len(good)>MIN_MATCH_COUNT:
        src_pts = np.float32([ kp1[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
        dst_pts = np.float32([ kp2[m.trainIdx].pt for m in good ]).reshape(-1,1,2)
        
        M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
        matchesMask = mask.ravel().tolist()

        h,w = lQueryImage.shape
        pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
        dst = cv2.perspectiveTransform(pts,M)
        lScreenImage = cv2.polylines(lScreenImage,[np.int32(dst)],True,0,3, cv2.LINE_AA) 

        # If output is requested, an image is shown
        if output:
            draw_params = dict(matchColor = (0,255,0), # draw matches in green color
                       singlePointColor = None,
                       matchesMask = matchesMask, # draw only inliers
                       flags = 2)
           
            img3 = cv2.drawMatches(lQueryImage,kp1,lScreenImage,kp2,good,None,**draw_params)
            plt.imshow(img3, 'gray'),plt.show()

    del lQueryImage
    del lScreenImage

    x = 0; y = 0; count = 0
    for key in good:
        x += kp2[key.trainIdx].pt[0]
        y += kp2[key.trainIdx].pt[1]
        count += 1

    if count > MIN_MATCH_COUNT:
        NodLog.logDebug("(" + query + ") Minimum match count achieved - %d/%d" % (len(good),MIN_MATCH_COUNT)) #Log
        return ((x/count)/2, (y/count)/2)

    else:
        NodLog.logDebug("(" + query + ") Not enough matches are found - %d/%d" % (len(good),MIN_MATCH_COUNT)) #Log

    return None






