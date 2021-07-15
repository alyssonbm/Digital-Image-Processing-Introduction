#!/usr/bin/python
import cv2
import numpy as np
import sys, getopt

def weightedAverage(img1,img2,outputfile,weight):
	img = img1
	if(weight != ''):
		weight = float(weight)
	else:
		weight = 0.5
	img = ((img1*weight)+(img2*(1-weight)))
	#cv2.addWeighted( img1, weight, img2, 1-weight, 0.0, img);

	img = np.uint8(img)

	cv2.imshow('Weighted Image',img)
	if(outputfile == ''):
		cv2.imwrite('Q5 - '+str(weight)+'*A'+ ' + '+ str(1-weight) + '*B ' +'- Weighted.png',img)
	else:
		cv2.imwrite(outputfile,img)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

def main(argv):
	inputfilei = ''
	inputfilej = ''
	outputfile = ''
	weight = ''
	try:
		opts, args = getopt.getopt(argv,"hi:j:o:w:",["ifilei=","jfilej=","ofile=","weight="])
	except getopt.GetoptError:
		print('T1.py -i <inputfile i> -j <inputfile j> -o <outputfile> -w <weight>')
		sys.exit(2)
	for opt, arg in opts:
		if opt == 'h':
			print('T1.py -i <inputfile i> -j <inputfile j> -o <outputfile> -w <weight>')
			sys.exit()
		elif opt in ("-i","--ifilei"):
			inputfilei = arg
		elif opt in ("-j","--ifilej"):
			inputfilej = arg
		elif opt in ("-o","--ofile"):
			outputfile = arg
		elif opt in ("-w","--weight"):
			weight = arg

	img1 = cv2.imread('../Images/' + inputfilei,cv2.IMREAD_GRAYSCALE)
	img2 = cv2.imread('../Images/' + inputfilej,cv2.IMREAD_GRAYSCALE)
	if((img1 is None) or (img2 is None)):
		print('Imagem indisponível, escolha uma imagem no diretório Images.')
	elif (img1.shape != img2.shape):
		print('As imagens devem conter as mesmas dimensões.')
	else:
		weightedAverage(img1,img2,outputfile,weight)

if __name__=="__main__":
	main(sys.argv[1:])