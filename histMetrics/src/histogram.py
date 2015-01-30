import sys, os
#from phasesym import *
from PhaseSymmetry.src.phasesym import *
import cv2, optparse
import numpy as np
import pymeanshift as pms
from Hist import RadAngleHist
from scipy import spatial
from sklearn.cluster import DBSCAN
from matplotlib import pyplot as plt
from collections import defaultdict
import colorsys
import logging
import phasesymLogger
np.set_printoptions(precision=3)
np.set_printoptions(linewidth=200)


DEBUG = False
logger = None


def drawBox(img, contour):
    """
    INPUTS:
        img      = image to be drawn on
        contours = contour objects
    OUTPUTS:
        None 
    """
    rect = cv2.minAreaRect(contour)
    box = cv2.cv.BoxPoints(rect)
    box = np.int0(box)
    cv2.drawContours(img, [box], 0, (255, 0, 0), 2)
    

def getCentroids(contours):
    """
    INPUTS:
        contours = list of contour objects
    OUTPUTS:
        centroids = list of centroids corresponding to the input contours
    """
    centroids = []
    for cnt in contours:
        moments = cv2.moments(cnt)
        centroid_x = int(moments['m10']/moments['m00'])
        centroid_y = int(moments['m01']/moments['m00'])
        centroid = (centroid_y, centroid_x)
        centroids.append(centroid)

    return centroids

def getContours(thresh_img, AMIN, AMAX, WMIN, WMAX, HMIN, HMAX, ARATIO):
    """
    INPUTS:
        thresh_img = thresholded image (black and white)
        AMIN       = blob minimum area
        AMAX       = blob maximum area
        WMIN       = minimum contour bounding rectangle width
        WMAX       = maximum contour bounding rectangle width
        HMIN       = minimum contour bounding rectangle height
        HMAX       = maximum contour bounding rectangle height
        ARATIO     = minimum contour bounding rectangle aspect ratio
    OUTPUTS:
        filteredContours = list of contours filtered according to input params
    """
    contours, hierarchy = cv2.findContours(thresh_img, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    filteredContours = []
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area >= AMIN and area <= AMAX:
            x,y,w,h = cv2.boundingRect(cnt)
            if w < WMAX and h < HMAX and w > WMIN and h > HMIN:
                aspectRatio = 0
                if w == min(w, h):
                    aspectRatio = float(w)/h
                else:
                    aspectRatio = float(h)/w

                if aspectRatio > ARATIO:
                    filteredContours.append(cnt)

    return filteredContours


def drawCentroids(img, centroids):
    for cen in centroids:
        cv2.circle(img,(cen[1],cen[0]),1,(0,0,255),-1)



def getImageWindow(img,y,x,h,w):
    """
    INPUTS:
        img = input image
        x,y = point in image to be the center of the returned window
        w,h = height and width of the windo
    OUTPUTS:
        window = a wxh size window containing a slice of the image
                 centered on x,y. The window will be padded with 
                 zeros for border cases
    """
    imgY,imgX,imgZ = img.shape 
    window = np.zeros((h,w,imgZ))

    winCenterX = -1
    winCenterY = -1

    #account for even/odd window sizes
    if w%2:
        winCenterX = int(np.ceil(w/float(2)))
    else:
        winCenterX = w/2

    if h%2:
        winCenterY = int(np.ceil(h/float(2)))
    else:
        winCenterY = h/2

    #get the upper and lower bounds of the image slice
    lowX = max(x-winCenterX,0)
    highX = min(imgX,x+winCenterX)
    lowY = max(y-winCenterY,0)
    highY = min(imgY,y+winCenterY)

    #get the offset X and Y distances between the centroid (x,y) and the 
    #edge of the image slice
    offsetLowX = x - lowX
    offsetLowY = y - lowY
    offsetHighX = highX - x
    offsetHighY = highY - y


    #get the window upper and lower bounds where the image
    #slice is to be placed
    XwinLow = winCenterX - offsetLowX
    YwinLow = winCenterY - offsetLowY
    XwinHigh = winCenterX + offsetHighX
    YwinHigh = winCenterY + offsetHighY

    try:
        window[YwinLow:YwinHigh-1,XwinLow:XwinHigh-1,:] = img[lowY:highY-1,lowX:highX-1,:]
    except:
        import pdb; pdb.set_trace()

    return np.uint8(window)

def scanBlobs(centroids, inputImage, eps, min_samples):
    """
    INPUT:
        centroids:      A list of centroids obtained from the image being processed
        inputImage:     A copy of the original input image
    OUTPUT:
        clusters:       The clusters found in the centroids dataset using DBSCAN.
                        Ideally, this is representative of each car in the image.
    """

    #Get physical spatial differences
    physical_distances = spatial.distance.pdist(centroids, 'euclidean')
    physical_distances = spatial.distance.squareform(physical_distances)

    #Get pixel intensities at centroids
    grayImg = cv2.cvtColor(inputImage, cv2.COLOR_RGB2GRAY)
    colorPoints = []
    for curcen in centroids:
        colorPoints.append((grayImg[curcen], 0))

    #Get color space distances
    #color_distances = spatial.distance.pdist(colorPoints, 'euclidean')
    #color_distances = spatial.distance.squareform(color_distances)

    #Create summed distance metric
    #sum_distances = np.add(physical_distances, color_distances)

    #use DBSCAN
    #dbResult = DBSCAN(eps=25, min_samples=1, metric='precomputed').fit(sum_distances)
    #dbResult = DBSCAN(eps=25, min_samples=1, metric='precomputed').fit(physical_distances)

    #dbResult = DBSCAN(eps=15, min_samples=1, metric='precomputed').fit(physical_distances)
    dbResult = DBSCAN(eps=eps, min_samples=min_samples, metric='precomputed').fit(physical_distances)

    #plotClusters(dbResult, physical_distances)
    return dbResult

def plotClusters(dbResult, data):
    # Plot result
    # Black removed and is used for noise instead.

    labels = dbResult.labels_
    core_samples_mask = np.zeros_like(dbResult.labels_, dtype=bool)
    core_samples_mask[dbResult.core_sample_indices_] = True
    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
    unique_labels = set(labels)
    colors = getClusterColors(len(unique_labels))
    for k, col in zip(unique_labels, colors):
        if k == -1:
            # Black used for noise.
            col = 'k'

        class_member_mask = (labels == k)

        #xy = sum_distances[class_member_mask & core_samples_mask]
        xy = data[class_member_mask & core_samples_mask]
        plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=col, markeredgecolor='k', markersize=14)

        #xy = sum_distances[class_member_mask & ~core_samples_mask]
        xy = data[class_member_mask & ~core_samples_mask]
        plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=col, markeredgecolor='k', markersize=6)

    plt.title('Estimated number of clusters: %d' % n_clusters_)
    plt.show()


def getClusterColors(numClusters):
    """
    INPUT:
        numClusters     The number of clusters to define unique colors for
    OUTPUT:
        RGB_tuples      A list of distinct colors for each cluster in RGB color space
    """
    HSV_tuples = [(x * 1.0/numClusters, 0.5, 0.5) for x in range(numClusters)]
    RGB_tuples = map(lambda x: colorsys.hsv_to_rgb(*x), HSV_tuples)
    RGB_tuples = [(e[0] * 256, e[1] * 256, e[2] * 256) for e in RGB_tuples]
    RGB_tuples = [(np.floor(e[0]), np.floor(e[1]), np.floor(e[2])) for e in RGB_tuples]

    return RGB_tuples

def drawClusterColors(dbResult, inputImg, data):
    """
    INPUT:
        dbResult        Resulting clusters from DBSCAN
        inputImg        A copy of the original input image
    OUTPUT:
        <Image Name>_BoxedClusters      A mutated version of the input image with a bounding box around each cluster
    """
    outputImg = inputImg.copy()

    #set up a dictionary for cluster member collection
    dict = defaultdict(list)

    labels = dbResult.labels_
    core_samples_mask = np.zeros_like(dbResult.labels_, dtype=bool)
    core_samples_mask[dbResult.core_sample_indices_] = True
    unique_labels = set(labels)
    colors = getClusterColors(len(unique_labels))

    for k in unique_labels:
        class_member_mask = (labels == k)
        for i in range(len(class_member_mask)):
            member = class_member_mask[i]
            if member:
                dict[k].append(data[i])
    logger.info("Num Clusters: " + str(len(labels)))
    logger.info(dict)

    for i, color in zip(dict, colors):
        entry = dict[i]
        for j in entry:
            tempCentroid = (j[1], j[0])
            cv2.circle(outputImg, tempCentroid, 4, color, thickness=2)

    cv2.imwrite("clusterColors.jpg", outputImg)
    logger.info( "Number of unique clusters: " + str(len(unique_labels)))

def genReferenceCar(sz,aspectRatio=0.5):
    """
    INPUTS:
        sz          = size of the image patch to be generated
        aspectRatio = ratio of the width to height of the rectangle
    OUTPUTS:
        ref         =  a sz by sz image patch containing a centered rectangle
                       of the given aspect ratio whose height is 2
                       pixels shorter than the image size (to leave
                       a 1 pixel boarder around the longest rectangle
                       dimension aka height)
        winCenterRow = centroid of image patch
        winCenterCol
    """
    winCenterRow = -1
    winCenterCol = -1
    border = 2

    ref = np.zeros((sz,sz))

    #account for even/odd window sizes
    if sz%2:
        winCenterRow = int(np.ceil(sz/float(2)))
    else:
        winCenterRow = sz/2

    winCenterCol = winCenterRow

    rectHeight = sz-border
    rectWidth = int(np.ceil(rectHeight*aspectRatio))


    rectRowStart = winCenterRow - int(np.ceil(rectWidth/2))-1
    rectColStart = border


    rectRowEnd = winCenterRow + int(np.ceil(rectWidth/2))-1
    rectColEnd = rectHeight-1   #account for zero indexing

    cv2.rectangle(ref,(rectRowStart, rectColStart), (rectRowEnd,rectColEnd),255, thickness=-1)
    ref = np.uint8(ref)
    return ref, (winCenterRow,winCenterCol)

def segment_image(img):
    gray = img.copy()
    if len(gray.shape) == 3:
        gray = cv2.cvtColor(gray, cv2.COLOR_BGR2GRAY)


    ret, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

    #cv2.imwrite("thresh.jpg",thresh)
    kernel = np.ones((3,3),np.uint8)
    thresh = cv2.morphologyEx(thresh,cv2.MORPH_CLOSE,kernel, iterations = 10)

    #cv2.imwrite("close.jpg",thresh)
    fg = cv2.erode(thresh,None,iterations = 7)
    bgt = cv2.dilate(thresh,None,iterations = 8)
    ret,bg = cv2.threshold(bgt,1,128,1)
    #cv2.imwrite("fg.jpg", fg)
    #cv2.imwrite("bg.jpg", bg)
    marker = cv2.add(fg,bg)
    #cv2.imwrite("marker.jpg", marker)
    marker32 = np.int32(marker)
    cv2.watershed(img,marker32)
    m = cv2.convertScaleAbs(marker32)
    #cv2.imwrite("after_watershed.jpg", m)
    ret,thresh = cv2.threshold(m,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    res = cv2.bitwise_and(img,img,mask = thresh)
    #cv2.imwrite("segment_2.jpg", res)
    return res, thresh



def checkopts(parser, opts):
    if not opts.WINSZ%2 and opts.WINSZ >= 3:
        logger.debug("Invalid user specified window size. --win=%d"%(opts.WINSZ))
        parser.error("option --win must be an odd integer greater than or equal to 3")

    if opts.BLUR == -1:
        if opts.WINSZ >= 35:
            opts.BLUR = 3
        else:
            opts.BLUR = 1
    else:
        if not opts.BLUR%2 and opts.BLUR >= 1:
            logger.debug("Invalid user specified blur size. --blur=%d"%(opts.BLUR))
            parser.error("option --blur must be an odd integer greater than or equal to 1")

    if opts.SRAD == -1:
        opts.SRAD = int(np.maximum(3,np.floor(np.sqrt(opts.WINSZ))))
    if opts.DEN == -1:
        opts.DEN = int(np.maximum(2,np.floor(np.sqrt(opts.WINSZ))))

    if opts.TRAD == -1:
        opts.TRAD = int(np.maximum(3,opts.WINSZ/2))

        # must be odd
        if opts.TRAD % 2 == 0:
            opts.TRAD = opts.TRAD+1

    if opts.WMIN == -1:
        opts.WMIN = int(np.maximum(3,np.floor((opts.WINSZ*0.65*0.06))))
    if opts.HMIN == -1:
        opts.HMIN = int(np.maximum(3,np.floor(opts.WINSZ *0.06)))
    if opts.WMAX == -1:
        opts.WMAX = int(np.maximum(opts.WMIN,np.floor(opts.WINSZ*0.65)))
    if opts.HMAX == -1:
        opts.HMAX = opts.WINSZ
    if opts.AMIN == -1:
        opts.AMIN = opts.WMIN*opts.HMIN
    if opts.AMAX == -1:
        opts.AMAX = opts.WMAX*opts.HMAX
    if opts.EPS == -1:
        opts.EPS = int(np.maximum(3,np.floor(opts.WINSZ*0.3)))
    return    







def main(argv=None):
    if argv is None:
        argv = sys.argv

    desc = """%prog is a tool performs mean shift clustering and a phase symmetry transfromation\n
     on a given input image, in that order."""

    parser = optparse.OptionParser(description=desc, usage='Usage: ex) %prog imageFile.png')
    parser.add_option('--scale', help='specify number of phasesym scales', dest='NSCALE', default=4, type="int")
    parser.add_option('--ori', help='specify number of phasesym orientations', dest='NORIENT', default=6, type="int")
    parser.add_option('--mult', help='specify multiplier for phasesym', dest='MULT', default=3.0, type="float")
    parser.add_option('--sig', help='specify sigma on frequncy for phasesym', dest='SIGMAONF', default=0.55, type="float")
    parser.add_option('--k', help='specify k value for phasesym', dest='K', default=1, type="int")
    parser.add_option('--blur', help='specify blur width value N for NxN blur operation', dest='BLUR', default=-1, type="int")          # default=3
    parser.add_option('--srad', help='specify spatial radius for mean shift', dest='SRAD', default=-1, type="int")                      # default=5
    parser.add_option('--rrad', help='specify radiometric radius for mean shift', dest='RRAD', default=6, type="int")
    parser.add_option('--den', help='specify pixel density value for mean shift', dest='DEN', default=-1, type="int")                   # default=10  
    parser.add_option('--trad', help='specify the pixel neighborhood for thresholding', dest='TRAD', default=-1, type="int")            # default=7
    parser.add_option('--amin', help='specify blob minimum area for boxing', dest='AMIN', default=-1, type="int")                       # default=5
    parser.add_option('--amax', help='specify blob maximum area for boxing', dest='AMAX', default=-1, type="int")                       # default=400
    parser.add_option('--wmin', help='specify box minimum width acceptance', dest='WMIN', default=-1, type="int")                       # default=3
    parser.add_option('--wmax', help='specify box maximum width acceptance', dest='WMAX', default=-1, type="int")                       # default=35
    parser.add_option('--hmin', help='specify box minimum height acceptance', dest='HMIN', default=-1, type="int")                      # default=2
    parser.add_option('--hmax', help='specify box maximum height acceptance', dest='HMAX', default=-1, type="int")                      # default=55
    parser.add_option('--arat', help='specify minimum box aspect ratio for acceptance', dest='ARATIO', default=0.25, type="float")
    parser.add_option('--edgeMin', help='specify minimum hysteresis value for edge detection', dest='EDGEMIN', default=100, type="int")
    parser.add_option('--edgeMax', help='specify maximum hysteresis value for edge detection', dest='EDGEMAX', default=200, type="int")
    parser.add_option('--ref', help='specify reference car image', dest='MASTERIMG', default="")
    parser.add_option('--win', help='specify search window size, default matches reference image size', dest='WINSZ', default=-1, type="int")
    parser.add_option('--tol', help='specify shape description tolerance ex) --tol=0.07', dest='TOL', default=0.07, type="float")
    parser.add_option('--eps', help='specify maximum epsilon value for DBSCAN clustering algorithm', dest='EPS', default=-1, type="int")    #default=15
    parser.add_option('--min_samples', help='specify the numer fo minimum samples that constitute a cluster during DBSCAN', dest='MINSAMPLES', default=1, type="int")
    parser.add_option('--bestFit', help='specify best fit Euclidian distance for shape description', action='store_true' ,dest='BESTFIT', default=False)


    (opts, args) = parser.parse_args(argv)
    args = args[1:]

    # Check to see if the user provided an input image
    if len(args) == 0:
        parser.print_help()
        parser.error("No input file provided")

    # Check to see if the file system image is provided
    if len(args) > 1:
        parser.print_help()
        parser.error("More than one image input argument provided")

    # At the moment you can't have both
    # TODO: perhaps auto-downsampling feature?
    if len(opts.MASTERIMG) != 0 and opts.WINSZ != -1:
        parser.error("options --ref and --win are mutually exclusive")


    masterImg = None
    masterHist = None
    masterCentroid = None


    filename = args[0]
    basename = os.path.splitext(filename)[0]

    global logger
    logger = phasesymLogger.setupLogger("LOCAL_PHASE_SYM","%s.log"%(basename))
    logger.debug(" ".join(sys.argv))


    # Auto-setting the other parameters hinges on getting the window size
    # Must handle this first
    if len(opts.MASTERIMG) > 0:
        masterImg = cv2.imread(opts.MASTERIMG)

        if len(masterImg.shape) == 2:
            h, w = masterImg.shape
        else:
            h, w, z = masterImg.shape

        if w%2:
            x = int(np.ceil(w/float(2)))
        else:
            x = w/2
        if h%2:
            y = int(np.ceil(h/float(2)))
        else:
            y = h/2

        masterCentroid = (y,x)
        logger.debug("User provided reference image")

    if opts.WINSZ == -1:
        opts.WINSZ = masterImg.shape[0]

    checkopts(parser,opts)

    
    NSCALE = opts.NSCALE
    NORIENT = opts.NORIENT
    MULT = opts.MULT
    SIGMAONF = opts.SIGMAONF
    K = opts.K
    BLUR = (opts.BLUR, opts.BLUR)
    SRAD = opts.SRAD
    RRAD = opts.RRAD
    DEN = opts.DEN
    TRAD = opts.TRAD
    AMIN = opts.AMIN
    AMAX = opts.AMAX
    WMAX = opts.WMAX
    WMIN = opts.WMIN
    HMAX = opts.HMAX
    HMIN = opts.HMIN
    ARATIO = opts.ARATIO
    EDGEMIN = opts.EDGEMIN
    EDGEMAX = opts.EDGEMAX
    WINSZ = opts.WINSZ 
    TOL = opts.TOL
    EPS = opts.EPS
    MINSAMPLES = opts.MINSAMPLES
    BESTFIT = opts.BESTFIT

    logger.debug("NSCALE=%d"%(NSCALE))
    logger.debug("NORIENT=%d"%(NORIENT))
    logger.debug("MULT=%.2f"%(MULT))
    logger.debug("SIGMAONF=%.2f"%(SIGMAONF))
    logger.debug("K=%d"%(K))
    logger.debug("BLUR=%s"%(str(BLUR)))
    logger.debug("SRAD=%d"%(SRAD))
    logger.debug("RRAD=%d"%(RRAD))
    logger.debug("DEN=%d"%(DEN))
    logger.debug("TRAD=%d"%(TRAD))
    logger.debug("AMIN=%d"%(AMIN))
    logger.debug("AMAX=%d"%(AMAX))
    logger.debug("WMAX=%d"%(WMAX))
    logger.debug("WMIN=%d"%(WMIN))
    logger.debug("HMAX=%d"%(HMAX))
    logger.debug("HMIN=%d"%(HMIN))
    logger.debug("ARATIO=%.2f"%(ARATIO))
    logger.debug("EDGEMIN=%d"%(EDGEMIN))
    logger.debug("EDGEMAX=%d"%(EDGEMAX))
    logger.debug("WINSZ=%d"%(WINSZ))
    logger.debug("TOL=%.2f"%(TOL))
    logger.debug("EPS=%d"%(EPS))
    logger.debug("MINSAMPLES=%d"%(MINSAMPLES))
    logger.debug("BESTFIT=%d"%(BESTFIT))




    #create subdirectory if it does not already exist
    dirName = basename + '_windowTiles'
    if not (os.path.isdir(dirName)):
        os.mkdir(dirName)

    carDir = os.path.join(dirName, "cars")
    if not (os.path.isdir(carDir)):
        os.mkdir(carDir)

    notCarDir = os.path.join(dirName, "notCars")
    if not (os.path.isdir(notCarDir)):
        os.mkdir(notCarDir)

    edgeDir = os.path.join(dirName, "edge")
    if not (os.path.isdir(edgeDir)):
        os.mkdir(edgeDir)



    # If the user did not provide a reference image
    if masterImg is None:
        masterImg, masterCentroid = genReferenceCar(WINSZ)
        logger.debug("Autogenerated reference image")


    cv2.imwrite(os.path.join(dirName, "genCar.png"), masterImg)

    logger.debug("\nReference Hist Centroid (Y,X): %d, %d" %(masterCentroid))
    #masterHist = RadAngleHist(masterImg, 0, masterCentroid[0], masterCentroid[1],BLUR,outDir=dirName)
    masterHist = RadAngleHist(masterImg, 0, masterCentroid[0], masterCentroid[1],(1,1),55,200,outDir=dirName)
    logger.debug(str(masterHist)+"\n")



    #img = cv2.imread(filename)
    img_orig = cv2.imread(filename)
    img = img_orig.copy()
    #img, threshMask = segment_image(img)
    grayImg = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    cv2.imwrite(basename+"_gray.png", grayImg)


    # calculate Phase Symmetry
    logger.info("Stage 1: Phase Symmetry")
    pha, ori, tot, T = phasesym(grayImg, nscale=NSCALE, norient=NORIENT, minWaveLength=3, mult=MULT, sigmaOnf=SIGMAONF, k=K, polarity=0)
    pha = cv2.normalize(pha, pha, 0, 255, cv2.NORM_MINMAX, cv2.CV_8UC1)
    pha = np.uint8(pha)
    cv2.imwrite(basename + "_PS" + "_%d_%d_%.2f_%.2f_%d.png" % (NSCALE, NORIENT, MULT, SIGMAONF, K), pha)
    cv2.imwrite(basename + "_PS" + "_%d_%d_%.2f_%.2f_%d_ori.png" % (NSCALE, NORIENT, MULT, SIGMAONF, K), ori)
    np.savetxt('python_ori.txt',ori)


    # blurring the image helps disperse the energy enough for mean-shift to pick up hotspots
    pha = cv2.blur(pha, BLUR)
    cv2.imwrite(basename + "_PS" + "_%d_%d_%.2f_%.2f_%d_B_%d_%d.png" % (NSCALE, NORIENT, MULT, SIGMAONF, K, BLUR[0], BLUR[1]), pha)
    pha = cv2.cvtColor(pha, cv2.COLOR_GRAY2RGB)
    pha = cv2.cvtColor(pha, cv2.COLOR_RGB2LUV)
    logger.info("Stage 1: Phase Symmetry -- Complete")

    # calculate mean-shift in LUV colorspace and convert back to RBB
    logger.info("Stage 2: Mean-Shift")
    (segmented_image, labels_image, number_regions) = pms.segment(pha, spatial_radius=SRAD, range_radius=RRAD, min_density=DEN)
    segmented_image=cv2.normalize(segmented_image, segmented_image, 0, 255, cv2.NORM_MINMAX, cv2.CV_8UC1)
    segmented_image = np.uint8(segmented_image)
    segmented_image = cv2.cvtColor(segmented_image, cv2.COLOR_LUV2RGB)
    segmented_image = cv2.cvtColor(segmented_image, cv2.COLOR_RGB2GRAY)
    cv2.imwrite(basename + "_PS" + "_%d_%d_%.2f_%.2f_%d_B_%d_%d_MS_%d_%d_%d.png" % (NSCALE, NORIENT, MULT, SIGMAONF, K, BLUR[0], BLUR[1], SRAD, RRAD, DEN), segmented_image)

    # threshold to obtain symmetry blobs
    #thresh_img = cv2.adaptiveThreshold(segmented_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 7, 0)
    #thresh_img = cv2.adaptiveThreshold(segmented_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, TRAD, 1)
    thresh_img = cv2.adaptiveThreshold(segmented_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, WINSZ, 4)
    cv2.imwrite(basename + "_PS" + "_%d_%d_%.2f_%.2f_%d_B_%d_%d_MS_%d_%d_%d_T.png" % (NSCALE, NORIENT, MULT, SIGMAONF, K, BLUR[0], BLUR[1], SRAD, RRAD, DEN), thresh_img)
    logger.info("Stage 2: Mean-Shift -- Complete")

    #get centroids
    contours = getContours(thresh_img, AMIN, AMAX, WMIN, WMAX, HMIN, HMAX, ARATIO)
    centroids = getCentroids(contours)
    

    histograms = []



    #outputImg = img.copy()
    outputImg = img_orig
    centroidsImg = img.copy()
    drawCentroids(centroidsImg,centroids)

    logger.info("Stage 3: Histogram Comparison")
    shapedCentroids = []
    shapeDistances = [] 
    for cen,cnt in zip(centroids,contours):
        win = getImageWindow(img, cen[0],cen[1],WINSZ,WINSZ)   #correct
        filename = "win_%d_%d.jpg" % (cen[0], cen[1])

        histogram = RadAngleHist(win, 90+ori[cen[0], cen[1]],cen[0],cen[1],BLUR,outDir=edgeDir)

        logger.debug(str(histogram)+"\n")

        #if histogram.getShapeHistSum() < 0.1:
        #    continue
        #if histogram.getShapeHistSum() < masterHist.getShapeHistSum():
        #    continue
        if histogram.getShapeHistSum() < masterHist.getShapeHistSum() or histogram.getShapeHistSum() > masterHist.getShapeHistSum()*2.5:
            continue

        #if masterHist.compare(histogram, tol=TOL, bestFit=BESTFIT, distMetric="DIST_EMD"):
        compare =  masterHist.compare(histogram, tol=TOL, bestFit=BESTFIT, distMetric="DIST_EMD")
        #compare =  masterHist.compare(histogram, tol=TOL, bestFit=BESTFIT, distMetric="DIST_EUCLIDIAN")
        shapeDistances.append(compare.shapeDist)
        if compare.result:
            cv2.imwrite(os.path.join(carDir, filename), win)
            drawBox(outputImg, cnt)
            shapedCentroids.append(cen)
        else:
            cv2.imwrite(os.path.join(notCarDir, filename), win)


    logger.info("Stage 3: Histogram Comparison -- Complete")


    dirName = ""
    cv2.imwrite(os.path.join(dirName, "Boxes_Centroids.jpg"), outputImg)
    cv2.imwrite(basename + "_PS" + "_%d_%d_%.2f_%.2f_%d_B_%d_%d_MS_%d_%d_%d_A_%d_%d_W_%d_%d_H_%d_%d_R_%.2f_E_%d_%d_W_%d_T_%.2f.png" % (NSCALE, NORIENT, MULT, SIGMAONF, K, BLUR[0], BLUR[1], SRAD, RRAD, DEN, AMIN, AMAX, WMIN, WMAX, HMIN, HMAX, ARATIO,EDGEMIN,EDGEMAX,WINSZ,TOL), outputImg) 
    cv2.imwrite(os.path.join(dirName, "Centroids.jpg"), centroidsImg) 


    logger.info("Stage 4: Blob Merge")
    if len(shapedCentroids) > 0:
        dbResult = scanBlobs(shapedCentroids, img.copy(), EPS, MINSAMPLES)
        drawClusterColors(dbResult, img.copy(), shapedCentroids)
    else:
        logger.info("No clusters found")
        logger.info("Try adjusting the matching tolerance (ex. python histogram.py --tol=0.65 input.jpg)")

    logger.info("Stage 4: Blob Merge -- Complete")

    f = open("centroids.txt","w")
    for cen in shapedCentroids:
        f.write("%d, %d\n"%(cen[0],cen[1]))
    f.close()

    shapeDistances = np.array(shapeDistances)
    logger.debug("\nHistogram Shape Distance Stats")
    logger.debug("Mean = %f"%(shapeDistances.mean()))
    logger.debug("Var  = %f"%(shapeDistances.var()))
    logger.debug("Std  = %f"%(shapeDistances.std()))
    logger.debug("Min  = %f"%(shapeDistances.min()))
    logger.debug("Max  = %f"%(shapeDistances.max()))
    

    logging.shutdown()


if __name__ == "__main__":
    sys.exit(main())
