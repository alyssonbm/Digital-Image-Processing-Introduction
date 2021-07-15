import cv2
import sys,getopt
import time
import numpy as np


def globalBinarization(img,threshold,invert):
	imgModified = np.copy(img)
	threshold = float(threshold)
	if(invert == '0'):
		imgModified[img<=threshold] = 0
		imgModified[img>threshold] = 255
	else:
		imgModified[img<=threshold] = 255
		imgModified[img>threshold] = 0
	return imgModified

def otsuBinarization(img,invert):
	img = img.astype('uint8')
	if(invert == '0'):
		otsu_threshold, img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
	else:
		otsu_threshold, img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)	
	return img

def parcialBinarization(img,method,invert,threshold,neighborhoodSize,k,R,p,q):
	width,height = img.shape
	neighborhoodSizeMean = int(neighborhoodSize/2)	
	imgModified = np.copy(img)
	for i in range(width):
		for j in range(height):
			neighborhood = img[i-neighborhoodSizeMean:i+neighborhoodSizeMean+1,j-neighborhoodSizeMean:j+neighborhoodSizeMean+1]
			if(neighborhood.size != 0):

				if(method=='3'):
					threshold = bernsenBinarization(neighborhood)
				elif(method=='4'):
					threshold = niblackBinarization(neighborhood,k)
				elif(method=='5'):
					threshold = sauvolaPietaksinenBinarization(neighborhood,k,R)
				elif(method=='6'):
					threshold = phansalskarMoreSabaleBinarization(neighborhood,k,R,p,q)
				elif(method=='8'):
					threshold = meanBinarization(neighborhood)
				elif(method=='9'):
					threshold = medianBinarization(neighborhood)
				
				if(img[i,j]>=threshold):
					if(invert == '0'):
						imgModified[i,j] = 255
					else:
						imgModified[i,j] = 0
				else:
					if(invert == '0'):
						imgModified[i,j] = 0
					else:
						imgModified[i,j] = 255
	return imgModified

def bernsenBinarization(neighborhood):
	threshold = (np.max(neighborhood) + np.min(neighborhood))/2
	return threshold

def niblackBinarization(neighborhood,k):
	mean = np.mean(neighborhood)
	standard_deviation = np.std(neighborhood)
	threshold = mean + (float(k) * standard_deviation)
	return threshold

def sauvolaPietaksinenBinarization(neighborhood,k,R):
	mean = np.mean(neighborhood)
	standard_deviation = np.std(neighborhood)
	threshold = mean * (1 + (float(k) * ((standard_deviation/float(R))-1)))
	return threshold

def phansalskarMoreSabaleBinarization(neighborhood,k,R,p,q):
	p = float(p)
	q = float(q)
	mean = np.mean(neighborhood)
	standard_deviation = np.std(neighborhood)
	threshold = mean * (1 + p * np.exp(-1*q*mean) + (float(k) * ((standard_deviation/float(R))-1)))
	return threshold

def contrastBinarization(img,neighborhoodSize,invert):
	width,height = img.shape
	neighborhoodSizeMean = int(neighborhoodSize/2)	
	imgModified = np.copy(img)
	for i in range(width):
		for j in range(height):
			neighborhood = img[i-neighborhoodSizeMean:i+neighborhoodSizeMean+1,j-neighborhoodSizeMean:j+neighborhoodSizeMean+1]
			if(neighborhood.size != 0):
				areaMinValue = np.min(neighborhood)
				areaMaxValue = np.max(neighborhood)
				if( (abs(img[i,j]-areaMinValue)) >= (abs(img[i,j]-areaMaxValue)) ):
					if(invert == '0'):
						imgModified[i,j] = 255
					else:
						imgModified[i,j] = 0
				else:
					if(invert == '0'):
						imgModified[i,j] = 0
					else:
						imgModified[i,j] = 255
	return imgModified

def meanBinarization(neighborhood):
	mean = np.mean(neighborhood)
	return mean

def medianBinarization(neighborhood):
	median = np.median(neighborhood)	
	return median


def binarizationMethodVerification(img,method,invert,threshold,neighborhoodSize,k,R,p,q):
	if(invert in ['0','falso','Falso','false','False','f','F']):
		invert = '0'
	elif(invert in ['1','verdadeiro','Verdadeiro','true','True','t','T','v','V']):
		invert = '1'
	else:
		print('Método de inversão selecionado não reconhecido')
		sys.exit()

	if(method in ['1','global','Global','g']):
		method = '1'
		if(threshold!=''):
			img = globalBinarization(img,threshold,invert)
		else:
			print('É necessário descrever um threshold para este método')
			sys.exit()
	elif(method in ['2','otsu','Otsu','o']):
		method = '2'
		img = otsuBinarization(img,invert)
	elif(method in ['7','contrast','Contrast','c']):
		method = '7'
		if(neighborhoodSize == ''):
			print('É ncessário declarar a área da vizinhança, n, onde a vizinhança será n x n')
			sys.exit()
		else:
			img = contrastBinarization(img,int(neighborhoodSize),invert)
	else:
		if(method in ['3','bernsen','Bernsen','b']):
			method = '3'
			if(neighborhoodSize == ''):
				print('É ncessário declarar a área da vizinhança, n, onde a vizinhança será n x n')
				sys.exit()
		if(method in ['4','niblack','Niblack','n']):
			method = '4'
			if(neighborhoodSize == ''):
				print('É ncessário declarar a área da vizinhança, n, onde a vizinhança será n x n')
				sys.exit()
			if(k == ''):
				print('É ncessário declarar a constante k')
				sys.exit()
		if(method in ['5','sauvolapietaksinen','SauvolaPietaksinen','s']):
			method = '5'
			if(neighborhoodSize == ''):
				print('É ncessário declarar a área da vizinhança, n, onde a vizinhança será n x n')
				sys.exit()
			if(k == ''):
				print('É ncessário declarar a constante k')
				sys.exit()
			if(R == ''):
				print('É ncessário declarar a constante r') 
				sys.exit()
		if(method in ['6','phansalskarmoreSabale','PhansalskarMoreSabale','p']):
			method = '6'
			if(neighborhoodSize == ''):
				print('É ncessário declarar a área da vizinhança, n, onde a vizinhança será n x n')
				sys.exit()
			if(k == ''):
				print('É ncessário declarar a constante k')
				sys.exit()
			if(R == ''):
				print('É ncessário declarar a constante r')
				sys.exit()
			if(p == ''):
				print('É ncessário declarar a constante p')
				sys.exit()
			if(q == ''):
				print('É ncessário declarar a constante q')
				sys.exit()
		if(method in ['8','mean','Mean','mea','media','Media']):
			method = '8'
			if(neighborhoodSize == ''):
				print('É ncessário declarar a área da vizinhança, n, onde a vizinhança será n x n')
				sys.exit()
		if(method in ['9','median','Median','med','mediana','Mediana']):
			method = '9'
			if(neighborhoodSize == ''):
				print('É ncessário declarar a área da vizinhança, n, onde a vizinhança será n x n')
				sys.exit()
		
		img = parcialBinarization(img,method,invert,threshold,int(neighborhoodSize),k,R,p,q)

	return img,method

def binarization(inputfile,outputfile,method,invert,threshold,neighborhoodSize,k,R,p,q):
	img = cv2.imread('../imagens_pgm/' + inputfile, cv2.IMREAD_GRAYSCALE)
	if(img is None):
		print('Imagem indisponível, escolha uma imagem no diretório Images.')
	else:
		blackPixels = img[img==0]
		preBlackPixels = (len(blackPixels) * 100)/img.size
		img = np.float64(img)
		ini = time.time()
		img,method = binarizationMethodVerification(img,method,invert,threshold,neighborhoodSize,k,R,p,q)
		fim = time.time()
		print ("Tempo de Execução: ", fim-ini)
		img = np.uint8(img)
		blackPixels = img[img==0]
		posBlackPixelsFraction = (len(blackPixels) * 100)/img.size
		cv2.imshow('Imagem Binarizada - Fracao de Pixels Pretos Pre-Processamento: ' + str(preBlackPixels) + ' % - Fracao de Pixels Pretos Pos-Processamento: ' + str(posBlackPixelsFraction) + ' %', img)
		cv2.waitKey(0)
		cv2.destroyAllWindows()
		#savaImage
		if(outputfile == ''):
			if(method in ['1']):
				cv2.imwrite('Imagem: '+ inputfile + ' - Técnica: ' + method + ' - Invertida: ' + invert + ' - Threshold: ' + threshold + ' Fracao de Pixels Pretos Pré-Processamento: '+ str(preBlackPixels) +' % - Fracao de Pixels Pretos Pós-Processamento: ' + str(posBlackPixelsFraction) + '%.pgm',img)
			if(method in ['2']):
				cv2.imwrite('Imagem: '+ inputfile + ' - Técnica: ' + method + ' - Invretida: ' + invert + ' Fracao de Pixels Pretos Pré-Processamento: '+ str(preBlackPixels) +' % - Fracao de Pixels Pretos Pós-Processamento: ' + str(posBlackPixelsFraction) + '%.pgm',img)		
			if(method in ['3','7','8','9']):
				cv2.imwrite('Imagem: '+ inputfile + ' - Técnica: ' + method + ' - Invertida: ' + invert  + ' - NeighborhoodSize: ' + neighborhoodSize + ' Fracao de Pixels Pretos Pré-Processamento: '+ str(preBlackPixels) +' % - Fracao de Pixels Pretos Pós-Processamento: ' + str(posBlackPixelsFraction) + '%.pgm',img)		
			if(method in ['4']):
				cv2.imwrite('Imagem: '+ inputfile + ' - Técnica: ' + method + ' - Invertida: ' + invert  + ' - NeighborhoodSize: ' + neighborhoodSize + ' - K: ' + k + ' Fracao de Pixels Pretos Pré-Processamento: '+ str(preBlackPixels) +' % - Fracao de Pixels Pretos Pós-Processamento: ' + str(posBlackPixelsFraction) + '%.pgm',img)	
			if(method in ['5']):
				cv2.imwrite('Imagem: '+ inputfile + ' - Técnica: ' + method + ' - Invertida: ' + invert + ' - NeighborhoodSize: ' + neighborhoodSize + ' - K: ' + k + ' - R: ' + R + ' Fracao de Pixels Pretos Pré-Processamento: '+ str(preBlackPixels) +' % - Fracao de Pixels Pretos Pós-Processamento: ' + str(posBlackPixelsFraction) + '%.pgm',img)
			if(method in ['6']):
				cv2.imwrite('Imagem: '+ inputfile + ' - Técnica: ' + method + ' - Invertida: ' + invert + ' - NeighborhoodSize: ' + neighborhoodSize + ' - K: ' + k + ' - R: ' + R +' - P: ' + p +' - Q: ' + q + ' Fracao de Pixels Pretos Pré-Processamento: '+ str(preBlackPixels) +' % - Fracao de Pixels Pretos Pós-Processamento: ' + str(posBlackPixelsFraction) + '%.pgm',img)
		else:
			cv2.imwrite(outputfile,img)
		
 #----------------------------------------------- MAIN -----------------------------------------------
def main(argv):
	inputfile = ''
	outputfile = ''
	method = '1'
	threshold = '128'
	neighborhoodSize = '15'
	k = '-0.2'
	R = '3'
	p = '2'
	q = '10'
	invert = '0'

	try:
		opts, args = getopt.getopt(argv, 'hi:o:m:t:n:k:r:p:q:v:', ['ifile=','ofile=','method=','threshold=','neighborhoodSize=','kValue=','rValue=','pValue=','qValue=','invert='])
	except getopt.GetoptError:
		print('trabalho2.py -i <inputfile> -o <outputfile> -m <method> -v <invert> -t <threshold> -n <neighborhoodSize> -k <kValue> -r <rValue> -p <pValue> -q <qValue>')
		sys.exit(2)

	for opt, arg in opts:
		if opt == 'h':
			print('trabalho2.py -i <inputfile> -o <outputfile> -m <method> -v <invert> -t <threshold> -n <neighborhoodSize> -k <kValue> -r <rValue> -p <pValue> -q <qValue>')
			sys.exit()
		elif opt in ('-i','--inputfile'):
			inputfile = arg
		elif opt in ('-o','--outputfile'):
			outputfile = arg
		elif opt in ('-m','--method'):
			method = arg
		elif opt in ('-t','--threshold'):
			threshold = arg
		elif opt in ('-n','--neighborhoodSize'):
			neighborhoodSize = arg
		elif opt in ('-k','--kValue'):
			k = arg
		elif opt in ('-r','--rValue'):
			R = arg
		elif opt in ('-p','--pValue'):
			p = arg
		elif opt in ('-q','--qValue'):
			q = arg
		elif opt in ('-v','--invert'):
			invert = arg

	if(inputfile!=''):	
		binarization(inputfile,outputfile,method,invert,threshold,neighborhoodSize,k,R,p,q)
	else:
		print('É necessário declarar a imagem de entrada')

if __name__ == '__main__':
	main(sys.argv[1:])







	#FILTO 2 é igual ao de contraste?
	#Porcentagem de preto.