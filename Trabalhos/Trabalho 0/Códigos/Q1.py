#!/usr/bin/python
import cv2
import numpy as np
import sys,getopt

def normalImage(img,outputfile):
	cv2.imshow('Natural Image',img)
	cv2.waitKey(0)
	cv2.destroyAllWindows()
	#Save Image
	if(outputfile == ''):
		cv2.imwrite('(b)Natural Image.png',img)
	else:
		cv2.imwrite(outputfile,img)

def negativeImage(img, outputfile):
	#Negative Image Construction
	img = 255 - img
	#Show Image
	cv2.imshow('Negative',img)
	cv2.waitKey(0)
	cv2.destroyAllWindows()
	#Save Image
	if(outputfile == ''):
		cv2.imwrite('(b)Negative.png',img)
	else:
		cv2.imwrite(outputfile,img)

def flipImage(img, outputfile):
	#Flip Image around y-axis = 1
	#0, for flipping the image around the x-axis (vertical flipping);
	# > 0 for flipping around the y-axis (horizontal flipping);
	# < 0 for flipping around both axes.
	img = cv2.flip(img, 0)
	cv2.imshow('Flipped - Eixo y',img)
	cv2.waitKey(0)
	cv2.destroyAllWindows()
	#Save Image
	if(outputfile == ''):
		cv2.imwrite('(c)Flipped.png',img)
	else:
		cv2.imwrite(outputfile,img)

def contrastImage(img, outputfile):
	imgSuport = img/255
	img = (100*imgSuport) + 100 
	img = np.uint8(img)

	cv2.imshow('Contrast: 100 - 200',img)
	cv2.waitKey(0)
	cv2.destroyAllWindows()
	#Save Image
	if(outputfile == ''):
		cv2.imwrite('(d)Contrast.png',img)
	else:
		cv2.imwrite(outputfile,img)

def invertedLineImage(img, outputfile):
	cont = 0
	for i in img:
		if(cont%2 == 0):
			img[cont] = np.flip(img[cont])
		cont = cont + 1

	cv2.imshow('Inverted Lines',img)
	cv2.waitKey(0)
	cv2.destroyAllWindows()
	#Save Image
	if(outputfile == ''):
		cv2.imwrite('(e)InvertedLines.png',img)
	else:
		cv2.imwrite(outputfile,img)

def reflexeImage(img, outputfile):
	size = img.shape[0]
	sub_img = img[0:int(size/2)]
	sub_img = cv2.flip(sub_img,0)
	
	if((img.shape[0] % 2) == 0):
		img[int(size/2):size-1] = sub_img[0:int(size/2)-1]
	else:
		img[int(size/2):size-1] = sub_img[0:int(size/2)]

	cv2.imshow('Reflexion',img)
	cv2.waitKey(0)
	cv2.destroyAllWindows()
	#save Image
	if(outputfile == ''):
		cv2.imwrite('(f)Reflexion.png',img)
	else:
		cv2.imwrite(outputfile,img)

def main(argv):
	inputfile = ''
	outputfile = ''
	method = ''
	try:
		opts, args = getopt.getopt(argv,"hi:o:m:",["ifile=","ofile=","method="])
	except getopt.GetoptError:
		print('T0.py -i <inputfile> -o <outputfile> -m <method>')
		sys.exit(2)
	for opt,arg in opts:
		if opt == 'h':
			print('T0.py -i <inputfile> -o <outputfile> -m <method>')
			sys.exit()
		elif opt in ('-i','--ifile'):
			inputfile = arg
		elif opt in ('-o','--outputfile'):
			outputfile = arg
		elif opt in ('-m','--method'):
			method = arg

	#Image Import
	img =  cv2.imread('../Images/' + inputfile, cv2.IMREAD_GRAYSCALE)
	if(img is None):
		print('Imagem indisponível, escolha uma imagem no diretório Images.')
	else:
		itens = ['a','b','c','d','e','f','']
		#Call methods
		if (method not in itens):
			print('Apenas itens a, b, c, d, e ,f são disponíveis para a entrada -m ou --method')
		elif method == 'a' or method == '':
			normalImage(img,outputfile)
		elif method == 'b':
			negativeImage(img,outputfile)		
		elif method == 'c':
			flipImage(img,outputfile)
		elif method == 'd':
			contrastImage(img,outputfile)
		elif method == 'e':
			invertedLineImage(img,outputfile)
		elif method == 'f':
			reflexeImage(img,outputfile)

if __name__=="__main__":
	main(sys.argv[1:])