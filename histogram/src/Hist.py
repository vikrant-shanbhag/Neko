import os
import cv2
class Hist(object):

    def __init__(self, img):
        """Default constructor. Must be overloaded in order to properly handle the histogramming methodology used.
        The size and dimensionality of the class member 'hist' will vary based on the histogram method employed in your
        implementation of this class."""
        if len(img.shape) > 2:
            self._img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        else:
            self._img = img
        self._hist = None

    def _calculate(self):
        """Calculates the histogram value on the given input image. This value is stored in the class member 'hist'"""
        return None

    def compare(self, otherHist, dist):
        """return True is the other histogram is within some distance metric of this histogram.
        INPUTS:
            otherHist       the histogram to be compared to
            dist            the distance metric to define what is 'near' this histogram. Choose default value.
        OUTPUTS:
            True if other histogram is within the given dist of similarity, False otherwise."""
        return None

    def __str__(self):
        """return a formatted output string for this histogram"""
        return " Overload me. "


import numpy as np
class RadAngleHist(Hist):


    def __init__(self, img, orientation,yCentroid,xCentroid,blurVal):
        super(RadAngleHist, self).__init__(img)
        self._MAX_VAL = 255

        #Centroid calculation. Assumes passed image window is centered on centroid of blob.
        #w, h = self._img.shape
        h, w = self._img.shape
        self._rmin=2
        self._rmax=0
        if w%2:
            x = int(np.ceil(w/float(2)))
            self._rmax=int(np.ceil(w/float(2)))
        else:
            x = w/2
            self._rmax = w/2

        if h%2:
            y = int(np.ceil(h/float(2)))
        else:
            y = h/2

        #self._centroid = (x, y)
        self._centroid = (y, x)
        self._orientation = orientation
        self._origCentroidX = xCentroid
        self._origCentroidY = yCentroid
        self._blurVal = blurVal
        self._calculate()

    def _calculate(self):
        """X is rows, Y is columns here."""
        # Canny edge detection
        #blurImg = cv2.blur(self._img, (3,3))
        blurImg = cv2.blur(self._img, self._blurVal)
        edge = cv2.Canny(blurImg, 90, 250)

#        # Rotate image
#        M = cv2.getRotationMatrix2D(self._centroid, 360 - self._orientation, 1)
#        img = cv2.warpAffine(edge, M, edge.shape)
#        M = cv2.getRotationMatrix2D(self._centroid, 90, 1)
#        img = cv2.warpAffine(img, M, img.shape)
#        margin = int(img.shape[1]*0.2)
#        
#        #img[:,0:10] = 0
#        #img[:,img.shape[1] - 10:img.shape[1]] = 0
#        img[:,0:margin] = 0
#        img[:,img.shape[1] - margin:img.shape[1]] = 0

        img = edge
        
        dirName = "windowTiles"
        filename = "win_%d_%d_edge_o_%d.jpg" % (self._origCentroidY, self._origCentroidX,self._orientation)
        cv2.imwrite(os.path.join(dirName, filename), img)

        # Radiometric histogram calculation begins
        # Measure from centroid outward to edge of blob
        rVals = []
        thetaVals = []

        xarr = np.arange(-self._centroid[1], self._centroid[1] + 1, 1)
        yarr = np.arange(self._centroid[0], -self._centroid[0] - 1, -1)

        xg, yg = np.meshgrid(xarr, yarr)

        for x in range(img.shape[1]):
            for y in range(img.shape[0]):
                #import pdb; pdb.set_trace()
                #xCoordinate = xg[x][y]
                #yCoordinate = yg[x][y]
                xCoordinate = xg[y][x]
                yCoordinate = yg[y][x]
                #pixel = img[x][y]
                pixel = img[y][x]
                #if not((xCoordinate == 0) and (yCoordinate == 0)) and pixel == self._MAX_VAL:
                if not((xCoordinate == 0) and (yCoordinate == 0)) and pixel > 10:
                    # Calculate distance and angle from centroid
                    rad = np.sqrt(np.square(xCoordinate) + np.square(yCoordinate))
                    #theta = np.arctan2(xCoordinate, yCoordinate)
                    theta = np.arctan2(yCoordinate, xCoordinate)
                   # print "(%d,%d)  px: %d  rad: %d  theta: %f" %(xCoordinate,yCoordinate,pixel,rad,theta)
                    if theta < 0:
                        theta = theta + 2*np.pi
                    rVals.append(rad)
                    thetaVals.append(theta)

        radiusBins = np.logspace(np.log10(self._rmin),np.log10(self._rmax * np.sqrt(2)),6)
        thetaBins = np.arange(0,2*np.pi+0.001, np.pi/6)
        H, xe, ye = np.histogram2d(rVals, thetaVals, bins=[radiusBins, thetaBins],normed=True)
        self._hist = H
        self._xe = xe
        self._ye = ye

        rot = int(self._orientation/30)
        self._hist = np.roll(self._hist,-rot)

        eigVals, eigVec = np.linalg.eig(self._img)
        self._eigVals = eigVals
        self._eigVec = eigVec
        self._idx = eigVals.argsort()[::-1]

        #print "Histogram:\n" + str(self._hist) + "\nxEdges: " + str(xe) + "\nyEdges: " + str(ye) + "\nCentroid: " \
        #+ str(self._centroid) + "\nrVals: " + str(rVals) + "\nthetaVals:" + str(thetaVals)+ "\nori: " + str(self._orientation)+"\n\n"


#    def compare(self, otherHist, dist=0):
#        """
#        Compares this histogram to the passed histogram using a Euclidian distance metric.
#        Euclidian distance is also known as 'ordinary ' distance. In general, n-dimensional
#        Euclidian distance is defined as follows:
#
#                    d(p, q) = sqrt((p1 - q1)^2 + (p2 - q2)^2 + (p3 - q3)^2 + ... + (pn - qn)^2)
#
#        Each point in this histogram is defined as a bin value. In this case, our histogram is 5 by 12
#        bins in size
#        :param:
#            otherHist:  the other histogram to compare 'this' histogram against.
#            dist:       the distance tolerance to allow. Default is no tolerance. If a tolerance is provided,
#                        the return value will be 0 if the distance lies within the tolerance. Any value outside
#                        the tolerance will return dist - <calcuated distance>.
#
#        :return: Returns the 'distance' the histograms are from each other. Positive value if valid, negative value
#                 if the histograms do not match in size, and 'None' if the provided argument is not a histogram.
#        """
#        thisList = []
#        otherList = []
#        try:
#            thisList = self._hist.tolist()
#            otherList = otherHist.tolist()
#
#        except Exception as e:
#            #Something is wrong with the provided histogram. Stop.
#            print e
#            return None
#
#        if len(thisList) != len(otherList) or len(thisList) == 0 or len(otherList) == 0:
#            #Histogram size mismatch or empty lists. Stop.
#            return -1
#
#        #Calculate histogram distance.
#
#        currentSquareDiff = 0
#        for thisRow, otherRow in zip(thisList, otherList):
#            for thisElement, otherElement in zip(thisRow, otherRow):
#                currentSquareDiff = currentSquareDiff + np.square(thisElement - otherElement)
#
#        totalDistance = np.sqrt(currentSquareDiff)
#        
#        if (totalDistance - dist) <= 0:
#            return 0
#        else:
#            return totalDistance - dist


    def compare(self, otherHist, dist=0):
        """
        Compares this histogram to the passed histogram using a Euclidian distance metric.
        Euclidian distance is also known as 'ordinary ' distance. In general, n-dimensional
        Euclidian distance is defined as follows:

                    d(p, q) = sqrt((p1 - q1)^2 + (p2 - q2)^2 + (p3 - q3)^2 + ... + (pn - qn)^2)

        Each point in this histogram is defined as a bin value. In this case, our histogram is 5 by 12
        bins in size
        :param:
            otherHist:  the other histogram to compare 'this' histogram against.
            dist:       the distance tolerance to allow. Default is no tolerance. If a tolerance is provided,
                        the return value will be 0 if the distance lies within the tolerance. Any value outside
                        the tolerance will return dist - <calcuated distance>.

        :return: Returns the 'distance' the histograms are from each other. Positive value if valid, negative value
                 if the histograms do not match in size, and 'None' if the provided argument is not a histogram.
        """

        dist = 0
        histDist = np.linalg.norm(self._hist-otherHist._hist)
        
        #eigDotProd = np.abs(self._eigVec[:,0].dot(self._eigVec[:,1]))
        #eigDotProd = self._eigVec[:,0].dot(self._eigVec[:,1])
        #angle = np.arccos(np.clip(np.dot(self._eigVec[:,0], self._eigVec[:,1]),-1,1))
        angle = np.angle(np.arccos(np.clip(np.vdot(self._eigVec[:,0], self._eigVec[:,1]),-1,1)))


        #eigDotProdOtherHist = np.abs(otherHist._eigVec[:,0].dot(otherHist._eigVec[:,1]))
        #eigDotProdOtherHist = otherHist._eigVec[:,0].dot(otherHist._eigVec[:,1])
        #angleOtherHist = np.arccos(np.clip(np.dot(otherHist._eigVec[:,0], otherHist._eigVec[:,1]),-1,1))
        angleOtherHist = np.angle(np.arccos(np.clip(np.vdot(otherHist._eigVec[:,0], otherHist._eigVec[:,1]),-1,1)))

        #eigDist = np.sqrt(np.square(eigDotProd - eigDotProdOtherHist))
        #eigDist = np.sqrt(np.square(angle-angleOtherHist))
        eigDist = np.linalg.norm(angle-angleOtherHist)
        print angle, angleOtherHist
         
        #dist = histDist + eigDist
        dist = histDist
        return dist

    def getHist(self):
        """
        :return: Returns a copy of this histogram
        """
        return self._hist.copy()

    def getHistSum(self):
        histSum = self._hist.sum()
        return histSum

    def tolist(self):

        return self._hist.tolist()


    def __str__(self):

        histStr = str(self._hist) + "\n" + str(self._xe) + "\n" + str(self._ye)
        return str(histStr)


