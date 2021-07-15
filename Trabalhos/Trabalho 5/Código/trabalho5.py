import cv2
import numpy as np
from math import floor, ceil, cos, sin
import sys,getopt 
import time

def floor_or_ceil(x):
	if(x-floor(x)>0.5):
		return ceil(x)
	else:
		return floor(x)

def nearestNeighborInterpolation(newX,newY,dx,dy,img):
	imgHeight, imgWidth = img.shape
	newImg = 0
	if(floor(newX)+1 < 0 or floor(newX)+1 > imgWidth-1) or (floor(newY)+1 < 0 or floor(newY)+1 > imgHeight-1):
		return 0
	elif((dx) < 0.5 and (dy) < 0.5 ):
		newImg = img[floor(newX)][floor(newY)]
	elif((dx) >= 0.5 and (dy) < 0.5 ):
		newImg = img[floor(newX)+1][floor(newY)]
	elif((dx) < 0.5 and (dy) >= 0.5 ):
		newImg = img[floor(newX)][floor(newY+1)]
	elif((dx) >= 0.5 and (dy) >= 0.5 ):
		newImg = img[floor(newX)+1][floor(newY)+1]
	return newImg

def nearestNeighborScale(newImg,img,scale):
	height, width = newImg.shape
	for i in range(height):
		for j in range(width):
			newX = (i/float(scale)-1)
			newY = (j/float(scale)-1)
			dx = newX%1
			dy = newY%1
			newImg[i][j] = nearestNeighborInterpolation(newX,newY,dx,dy,img)
	return newImg

def nearestNeighborRotation(newImg,img,angle):
	height, width = newImg.shape
	for i in range(height):
		for j in range(width):
			newX = (i - (width/2)) * cos(np.deg2rad(angle)) - (j - (height/2)) * sin(np.deg2rad(angle)) + (width/2)
			newY = (i - (width/2)) * sin(np.deg2rad(angle)) + (j - (height/2)) * cos(np.deg2rad(angle)) + (height/2)
			dx = newX%1
			dy = newY%1
			newImg[i][j] = nearestNeighborInterpolation(newX,newY,dx,dy,img)
	return newImg

def bilinearInterpolation(newX,newY,dx,dy,img):
	imgHeight, imgWidth = img.shape
	if(floor(newX)+1 < 0 or floor(newX)+1 > imgWidth-1) or (floor(newY)+1 < 0 or floor(newY)+1 > imgHeight-1):
		return 0
	return (1 - dx) * (1 - dy) * img[floor(newX)][floor(newY)] + dx * (1 - dy) * img[floor(newX)+1][floor(newY)] + (1 - dx) * dy * img[floor(newX)][floor(newY)+1] + dx * dy * img[floor(newX)+1][floor(newY)+1]

def bilinearScale(newImg,img,scale):
	height, width = newImg.shape
	for i in range(height-1):
		for j in range(width-1):
			newX = (i/float(scale)-1)
			newY = (j/float(scale)-1)
			dx = newX%1
			dy = newY%1
			newImg[i][j] = bilinearInterpolation(newX,newY,dx,dy,img)
	return newImg

def bilinearRotation(newImg,img,angle):
	height, width = newImg.shape
	for i in range(height-1):
		for j in range(width-1):
			newX = (i - (width/2)) * cos(np.deg2rad(angle)) - (j - (height/2)) * sin(np.deg2rad(angle)) + (width/2)
			newY = (i - (width/2)) * sin(np.deg2rad(angle)) + (j - (height/2)) * cos(np.deg2rad(angle)) + (height/2)
			dx = newX%1
			dy = newY%1
			newImg[i][j] = bilinearInterpolation(newX,newY,dx,dy,img)
	return newImg

def pFunction(t):
	if(t > 0):
		return t
	else:
		return 0

def rFunction(s):
	return ((1/6) * ((pFunction(s + 2)**3) - 4 * (pFunction(s + 1)**3) + 6 * pFunction(s)**3 - 4 * pFunction(s - 1)**3))

def cubicInterpolation(newX,newY,dx,dy,img):
	newImg = 0
	imgHeight, imgWidth = img.shape
	if(floor(newX)+2 < 0 or floor(newX)+2 > imgWidth-2) or (floor(newY)+2 < 0 or floor(newY)+2 > imgHeight-2):
		return 0
	for m in range(-1, 3):
		for n in range(-1, 3):
			newImg += img[floor(newX)+m][floor(newY)+n] * rFunction(m-dx) * rFunction(dy - n)
	return newImg

def cubicScale(newImg,img,scale):
	height, width = newImg.shape
	for i in range(height-2):
		for j in range(width-2):
			newX = (i/float(scale)-1)
			newY = (j/float(scale)-1)
			dx = newX%1
			dy = newY%1
			newImg[i][j] = cubicInterpolation(newX,newY,dx,dy,img)
	return newImg

def cubicRotation(newImg,img,angle):
	height, width = newImg.shape
	for i in range(height-2):
		for j in range(width-2):
			newX = (i - (width/2)) * cos(np.deg2rad(angle)) - (j - (height/2)) * sin(np.deg2rad(angle)) + (width/2)
			newY = (i - (width/2)) * sin(np.deg2rad(angle)) + (j - (height/2)) * cos(np.deg2rad(angle)) + (height/2)
			dx = newX%1
			dy = newY%1
			newImg[i][j] = cubicInterpolation(newX,newY,dx,dy,img)
	return newImg

def lFunction(n,img,newX,newY,dx):
	return ((-dx*(dx-1)*(dx-2)*img[floor(newX)-1][floor(newY)+n-2])/6) + (((dx+1)*(dx-1)*(dx-2)*img[floor(newX)][floor(newY)+n-2])/2) + ((-dx*(dx+1)*(dx-2)*img[floor(newX)+1][floor(newY)+n-2])/2) + ((dx*(dx+1)*(dx-1)*img[floor(newX)+2][floor(newY)+n-2])/6)

def lagrangeInterpolation(newX,newY,dx,dy,img):
	imgHeight, imgWidth = img.shape
	if(floor(newX)+2 < 0 or floor(newX)+2 > imgWidth-2) or (floor(newY)+2 < 0 or floor(newY)+2 > imgHeight-2):
		return 0
	return ((-dy*(dy-1)*(dy-2)*lFunction(1,img,newX,newY,dx))/6) + (((dy+1)*(dy-1)*(dy-2)*lFunction(2,img,newX,newY,dx))/2) + ((-dy*(dy+1)*(dy-2)*lFunction(3,img,newX,newY,dx))/2) + ((dy*(dy+1)*(dy-1)*lFunction(4,img,newX,newY,dx))/6)


def lagrangeScale(newImg,img,scale):
	height, width = newImg.shape
	for i in range(height-2):
		for j in range(width-2):
			newX = (i/float(scale)-1)
			newY = (j/float(scale)-1)
			dx = newX%1
			dy = newY%1
			newImg[i][j] = lagrangeInterpolation(newX,newY,dx,dy,img)
	return newImg

def lagrangeRotation(newImg,img,angle):
	height, width = newImg.shape
	for i in range(height-2):
		for j in range(width-2):
			newX = (i - (width/2)) * cos(np.deg2rad(angle)) - (j - (height/2)) * sin(np.deg2rad(angle)) + (width/2)
			newY = (i - (width/2)) * sin(np.deg2rad(angle)) + (j - (height/2)) * cos(np.deg2rad(angle)) + (height/2)
			dx = newX%1
			dy = newY%1
			newImg[i][j] = lagrangeInterpolation(newX,newY,dx,dy,img)
	return newImg

def scaleTransform(inputfile,outputfile,scale,dimentionH,dimentionW,method):
	img = cv2.imread('../Images/' + inputfile, cv2.IMREAD_GRAYSCALE)
	if(img is None):
		print('Imagem indisponível, escolha uma imagem no diretório Images.')
		exit(0)
	height, width = img.shape
	if(scale!=''):
		scaledHeight = height * round(float(scale),3)
		scaledWidth = width * round(float(scale),3)
	elif(dimentionH!='' and dimentionW!=''):
		scaledHeight = round(float(dimentionH)/height,3) * height
		scaledWidth = round(float(dimentionW)/width,3) * width
	newImg = np.zeros((floor_or_ceil(scaledWidth),floor_or_ceil(scaledHeight)),dtype=np.uint8)
	tic = time.time()
	if(method == '1'):
		newImg = nearestNeighborScale(newImg,img,scale)
	elif(method == '2'):
		newImg = bilinearScale(newImg,img,scale)
	elif(method == '3'):
		newImg = cubicScale(newImg,img,scale)
	elif(method == '4'):
		newImg = lagrangeScale(newImg,img,scale)
	tac = time.time()
	print("Tempo decorrido: " + str("{0:.2}".format(tac-tic)) + 's')
	#savaImage
	if(outputfile == ''):
		if(scale!=''):
			cv2.imwrite('Imagem Escalada: '+ inputfile + ' Fator de Escala: ' + scale + ' Método: '+ method + '.png',newImg)
		else:
			cv2.imwrite('Imagem Escalada: '+ inputfile + ' Dimensões Fornecidas: ' + dimensaoH + ',' + dimensaoW + ' Método: '+ method + '.png',newImg)
	else:
		cv2.imwrite(outputfile,newImg)
	cv2.imshow('Imagem Escalada', newImg)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

def rotationTransform(inputfile,outputfile,angle,method):
	angle = float(angle)
	img = cv2.imread('../Images/' + inputfile, cv2.IMREAD_GRAYSCALE)
	if(img is None):
		print('Imagem indisponível, escolha uma imagem no diretório Images.')
		exit(0)
	height, width = img.shape
	
	newImg = np.zeros((height,width),dtype=np.uint8)
	tic = time.time()
	if(method == '1'):
		newImg = nearestNeighborRotation(newImg,img,angle)
	elif(method == '2'):
		newImg = bilinearRotation(newImg,img,angle)
	elif(method == '3'):
		newImg = cubicRotation(newImg,img,angle)
	elif(method == '4'):
		newImg = lagrangeRotation(newImg,img,angle)
	tac = time.time()
	print("Tempo decorrido: " + str("{0:.2}".format(tac-tic)) + 's')
	#savaImage
	if(outputfile == ''):
		cv2.imwrite('Imagem Rotacionada: '+ inputfile + ' Angulo: ' + str(angle) + ' Método: '+ method +'.png',newImg)
	else:
		cv2.imwrite(outputfile,newImg)
	cv2.imshow('Imagem Escalada', newImg)
	cv2.waitKey(0)
	cv2.destroyAllWindows()
	
 #----------------------------------------------- MAIN -----------------------------------------------
def main(argv):
	inputfile = ''
	outputfile = ''
	angulo = ''
	escala = ''
	dimensaoH = ''
	dimensaoW = ''
	metodo = ''

	try:
		opts, args = getopt.getopt(argv, 'hi:o:a:e:dh:dw:m:', ['ifile=','ofile=','angulo=','escala=','dimensaoH=','dimensaoW=','metodo='])
	except getopt.GetoptError:
		print('trabalho4.py -i <inputfile> -o <outputfile> -a <angulo> -e <escala> -dh <dimensaoH> -dw <dimensaoW> -m <metodo>')
		sys.exit(2)

	for opt, arg in opts:
		if opt == 'h':
			print('trabalho4.py -i <inputfile> -o <outputfile> -a <angulo> -e <escala> -dh <dimensaoH> -dw <dimensaoW> -m <metodo>')
			sys.exit()
		elif opt in ('-i','--inputfile'):
			inputfile = arg
		elif opt in ('-o','--outputfile'):
			outputfile = arg
		elif opt in ('-a','--angulo'):
			angulo = arg
		elif opt in ('-e','--escala'):
			escala = arg
		elif opt in ('-d','--dimensaoH'):
			dimensaoH = arg
		elif opt in ('-d','--dimensaoW'):
			dimensaoW = arg
		elif opt in ('-m','--metodo'):
			metodo = arg

	if(metodo==''):
		metodo = '1'
	if(escala!='' or (dimensaoH!='' and dimensaoW!='')):	
		scaleTransform(inputfile,outputfile,escala,dimensaoH,dimensaoW,metodo)
	elif(angulo!=''):
		rotationTransform(inputfile,outputfile,angulo,metodo)
	else:
		if(inputfile==''):
			print('É necessário declarar uma imagem de entrada')
		if(escala=='' or (dimensaoH!='' and dimensaoW!='') or angulo==''):
			print('É necessário definir a escala ou dimensão para métodos de escala e o ângulo para métodos de rotação. São informações obrigatórias para cada um destes métodos.')

if __name__ == '__main__':
	main(sys.argv[1:])