from scipy import optimize
from scipy.interpolate import UnivariateSpline
import cv2
import math
import random


def piecewise_linear_2line(x, x0, y0, k1, k2):
	# x<x0 ⇒ lambda x: k1*x + y0 - k1*x0
	# x>=x0 ⇒ lambda x: k2*x + y0 - k2*x0
    return np.piecewise(x, [x < x0, x >= x0], [lambda x:k1*x + y0-k1*x0, lambda x:k2*x + y0-k2*x0])


def piecewise_linear_4line(x, x0, y0, x1, y1, x2, y2, k1, k2):
	# x<x0 ⇒ lambda x: k1*x + y0 - k1*x0
	# x>=x0 ⇒ lambda x: k2*x + y0 - k2*x0
    return np.piecewise(x, [x < x0, (x >= x0) & (x < x1), (x >= x1) & (x < x2), x >= x2], [lambda x:k1*(x-x0) + y0, lambda x:(y1-y0)/(x1-x0)*(x-x0) + y0, lambda x:(y2-y1)/(x2-x1)*(x-x1) + y1, lambda x:k2*(x-x2) + y2])


def piecewise_linear_3line(x, x0, y0, x1, y1, k1, k2):
	# x<x0 ⇒ lambda x: k1*x + y0 - k1*x0
	# x>=x0 ⇒ lambda x: k2*x + y0 - k2*x0
    return np.piecewise(x, [x < x0, (x >= x0) & (x < x1), x >= x1], [lambda x:k1*(x-x0) + y0, lambda x:(y1-y0)/(x1-x0)*(x-x0) + y0, lambda x:k2*(x-x1) + y1])

#放弃detectMulLine，效果不好


def detectMulLines(lanePosX, lanePosY):
      #基于hough
    lanePosX = lanePosX
    lanePosY = lanePosY
    width = round(max(lanePosX)-min(lanePosX))+10
    height = round(max(lanePosY)-min(lanePosY))+10
    gray = np.zeros((height, width), np.uint8)
    imgBlack = np.zeros((height, width, 3), np.uint8)

    lanePosX = lanePosX.round().astype(int)
    lanePosY = lanePosY.round().astype(int)
    gray.fill(0)
    print(lanePosY)
    tmpX = np.round(lanePosX - min(lanePosX))
    tmpY = np.round(lanePosY - min(lanePosY))

    gray[tmpY, tmpX] = 255

    cv2.imshow(curLaneID, gray)

    lines = cv2.HoughLinesP(gray, 2, 0.1*np.pi/180, 30,
                            minLineLength=20, maxLineGap=5)

    for line in lines:
        for x1, y1, x2, y2 in line:
            c = (random.randint(0, 255), random.randint(
                0, 255), random.randint(0, 255))
            cv2.line(imgBlack, (x1, y1), (x2, y2), c)
            k = math.atan((y2-y1)/(x2-x1))*180/np.pi
            dist = abs(x1-x2)+abs(y2-y1)
            print(k, dist)
            print(x1, y1, x2, y2)

    #lines = cv2.HoughLines(gray,10,5*np.pi/180, 50)

    #thetas = []
    #for line in lines:
    #        for rho, theta in line:
    #            print(rho, theta*180/np.pi)
    #            a = np.cos(theta)
    #            b = np.sin(theta)
    #            x0 = a * rho
    #            y0 = b * rho
    #            x1 = int(x0 + 1000 * (-b))
    #            y1 = int(y0 + 1000 * (a))
    #            x2 = int(x0 - 1000 * (-b))
    #            y2 = int(y0 - 1000 * (a))

    #            cv2.line(gray, (x1, y1), (x2, y2), 255, 3)

    cv2.imshow(curLaneID+str(1), imgBlack)
    #plt.show()

    input()
    #cv2.destroyAllWindows()
    #continue
    #lines = cv2.HoughLinesP(result, 1, 1 * np.pi/180, 10, minLineLength=10, maxLineGap=5)

    #样条拟合,不能用
    #vehInOneLaneTmp = vehInOneLane.sort_values(by='vehicle_x', ascending=True)
    #lanePosXTmp = vehInOneLaneTmp.vehicle_x.to_numpy()
    #lanePosYTmp = vehInOneLaneTmp.vehicle_y.to_numpy()
    #spline = UnivariateSpline(lanePosXTmp, lanePosYTmp, s=1)
    #ySpline = spline(lanePosXTmp)
    #errorMax = max(abs(ySpline - lanePosYTmp))
    #errorAvg = np.mean(abs( ySpline - lanePosYTmp))
    #print("spline", errorAvg, errorMax)

    #plt.plot(lanePosX, lanePosY, '.', lanePosXTmp, lanePosYTmp, 'r.')
    #plt.show()
    #continue

    #高阶曲线拟合
    #pc= np.polyfit(lanePosX, lanePosY, 40)
    #poly = np.poly1d(pc)

    #Ypoly = poly(lanePosX)
    #errorMax = max(abs(Ypoly - lanePosY))
    #errorAvg = np.mean(abs(Ypoly - lanePosY))
    #print("ploy20", errorAvg,errorMax)
    #plt.plot(lanePosX, lanePosY, '.', lanePosX, Ypoly, 'r.')
    #plt.show()
    #continue
    #分段曲线拟合

    errors = []
    #checkErros
    min1 = [min(lanePosX), min(lanePosY),  -10, -10]
    max1 = [max(lanePosX), max(lanePosY),   10, 10]
    p2, e = optimize.curve_fit(
        piecewise_linear_2line, lanePosX, lanePosY,  bounds=(min1, max1))
    Y2 = piecewise_linear_2line(lanePosX, *p2)
    errorMax = max(abs(Y2 - lanePosY))
    errorAvg = np.mean(abs(Y2 - lanePosY))
    print("2line", errorAvg, errorMax)
    errors.append(errorAvg)
    x0, y0, k1, k2 = p2

    min1 = [min(lanePosX), min(lanePosY), min(
        lanePosX), min(lanePosY), -10, -10]
    max1 = [max(lanePosX), max(lanePosY), max(
        lanePosX), max(lanePosY),  10, 10]
    p30 = [x0, y0, max(lanePosX), max(lanePosY), k1, k2]
    p3, e = optimize.curve_fit(
        piecewise_linear_3line, lanePosX, lanePosY,  bounds=(min1, max1))
    Y3 = piecewise_linear_3line(lanePosX, *p3)
    errorMax = max(abs(Y3 - lanePosY))
    errorAvg = np.mean(abs(Y3 - lanePosY))
    print("3line", errorAvg, errorMax)
    errors.append(errorAvg)
    x0, y0, x1, y1, k1, k2 = p3

    min1 = [min(lanePosX), min(lanePosY), min(lanePosX), min(
        lanePosY), min(lanePosX), min(lanePosY), -10, -10]
    max1 = [max(lanePosX), max(lanePosY), max(lanePosX), max(
        lanePosY), max(lanePosX), max(lanePosY), 10, 10]
    p40 = [x0, y0, x1, y1, max(lanePosX), max(lanePosY), k1, k2]
    p4, e = optimize.curve_fit(
        piecewise_linear_4line, lanePosX, lanePosY,  bounds=(min1, max1))
    p4, e = optimize.curve_fit(
        piecewise_linear_4line, lanePosX, lanePosY,  bounds=(min1, max1), p0=p4)
    Y4 = piecewise_linear_4line(lanePosX, *p4)
    errorMax = max(abs(Y4 - lanePosY))
    errorAvg = np.mean(abs(Y4 - lanePosY))
    print("4line", errorAvg, errorMax)
    errors.append(errorAvg)

    #
    minIndex = np.argmin(errors)
    if minIndex == 2:
        min1 = [min(lanePosX), min(lanePosY), min(lanePosX), min(
            lanePosY), min(lanePosX), min(lanePosY), -10, -10]
        max1 = [max(lanePosX), max(lanePosY), max(lanePosX), max(
            lanePosY), max(lanePosX), max(lanePosY), 10, 10]
        p4, e = optimize.curve_fit(
            piecewise_linear_4line, lanePosX, lanePosY,  bounds=(min1, max1), p0=p4)
        X = np.linspace(min(lanePosX), max(lanePosX), 100)
        plt.plot(lanePosX, lanePosY, '.', X,
                 piecewise_linear_4line(X, *p4), 'r.')
        #plt.show()

    if minIndex == 1:
        min1 = [min(lanePosX), min(lanePosY), min(
            lanePosX), min(lanePosY), -10, -10]
        max1 = [max(lanePosX), max(lanePosY), max(
            lanePosX), max(lanePosY),  10, 10]
        p3, e = optimize.curve_fit(
            piecewise_linear_3line, lanePosX, lanePosY,  bounds=(min1, max1), p0=p3)
        X = np.linspace(min(lanePosX), max(lanePosX), 100)
        plt.plot(lanePosX, lanePosY, '.', X,
                 piecewise_linear_3line(X, *p3), 'r.')
        #plt.show()

    if minIndex == 0:
        X = np.linspace(min(lanePosX), max(lanePosX), 100)
        plt.plot(lanePosX, lanePosY, '.', X,
                 piecewise_linear_2line(X, *p2), 'r.')
        #plt.show()
