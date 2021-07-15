#!/usr/bin/python
import cv2
import numpy as np
import sys, getopt

def bright(img,outputfile,gamma):
	if(gamma != ''):
		gamma = float(gamma)
	else:
		gamma = 1

	A = img/255
	if gamma != 0:
		B = A**(1/gamma)
	else:
		B = A**(1/0.1)

	img = B*255
	img = np.uint8(img)

	cv2.imshow('Ajuste de Brilho',img)
	if(outputfile == ''):
		cv2.imwrite('Q2 - '+ str(gamma)+ ' - Bright.png',img)
	else:
		cv2.imwrite(outputfile,img)
	cv2.waitKey(0)
	cv2.destroyAllWindows()
	

def main(argv):
	inputfile = ''
	outputfile = ''
	gamma = ''
	try:
		opts, args = getopt.getopt(argv,"hi:o:g:",["ifile=","ofile=","gamma="])
	except getopt.GetoptError:
		print('T1.py -i <inputfile> -o <outputfile> -g <-gamma>')
		sys.exit(2)
	for opt, arg in opts:
		if opt == 'h':
			print('T1.py -i <inputfile> -o <outputfile> -g <-gamma>')
			sys.exit()
		elif opt in ("-i","--ifile"):
			inputfile = arg
		elif opt in ("-o","--ofile"):
			outputfile = arg
		elif opt in ("-g","--gamma"):
			gamma = arg

	img =  cv2.imread('../Images/' + inputfile, cv2.IMREAD_GRAYSCALE)
	if(img is None):
		print('Imagem indisponível, escolha uma imagem no diretório Images.')
	else:
		bright(img,outputfile,gamma)

if __name__=="__main__":
	main(sys.argv[1:])