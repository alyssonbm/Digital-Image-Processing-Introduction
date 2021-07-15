import cv2 
import numpy as np
import sys,getopt
import random

def imageGenerate(img,pieces,pieceSizei,pieceSizej,rand):
	if(rand == '1'):
		spaceValues = list(range(16))
		random.shuffle(spaceValues)
	else:
		spaceValues = [5,10,12,2,7,15,0,8,11,13,1,6,3,14,9,4]
	count = 0
	for i in range(4):
		for j in range(4):
			img[pieceSizei*i:pieceSizei*(i+1),pieceSizej*j:pieceSizej*(j+1)] = pieces[spaceValues[count]]
			count +=1
	return img

def mosaic(img,outputfile,rand):
	pieces = []
	pieceSizei = int(img.shape[0]/4)
	pieceSizej = int(img.shape[1]/4)

	for i in range(4):
		for j in range(4):
			pieces = np.append( pieces, img[pieceSizei*i:pieceSizei*(i+1),pieceSizej*j:pieceSizej*(j+1)])
	
	pieces = pieces.reshape(16,pieceSizei,pieceSizej)

	img = imageGenerate(img,pieces,pieceSizei,pieceSizej,rand)

	cv2.imshow('Slices',img)
	if(outputfile == ''):
		cv2.imwrite('Q4 - Slices.png',img)
	else:
		cv2.imwrite(outputfile,img)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

def main(argv):
	inputfile = ''
	outputfile = ''
	rand = ''

	try:
		opts, args = getopt.getopt(argv,'hi:o:r:',['ifile=','ofile=','rand='])
	except:
		print('t2.py -i <inputfile> -o <outputfile> -r <rand>')
	for opt, arg in opts:
		if opt == 'h':
			print('T1.py -i <inputfile> -o <outputfile> -r <rand>')
		elif opt in ('-i','--ifile'):
			inputfile = arg
		elif opt in ('-o','--ofile'):
			outputfile = arg
		elif opt in ('-r','--rand'):
			rand = arg

	img =  cv2.imread('../Images/' + inputfile, cv2.IMREAD_GRAYSCALE)
	if(img is None):
		print('Imagem indisponível, escolha uma imagem no diretório Images.')
	else:
		mosaic(img,outputfile,rand)


if __name__=='__main__':
	main(sys.argv[1:])