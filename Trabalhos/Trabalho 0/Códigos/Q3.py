import cv2 
import numpy as np
import sys,getopt

def bitPlane(img,outputfile,atualbBit):
	img = np.unpackbits(img).reshape(img.shape[0],img.shape[1],8)

	for i in range(img.shape[0]):
		for j in range(img.shape[1]):
			if(img[i][j][7-atualbBit] == 0):
				img[i][j] = 00000000
			else:
				img[i][j] = 11111111

	img = np.packbits(img).reshape(img.shape[0],img.shape[1])

	cv2.imshow('Slices',img)
	if(outputfile == ''):
		cv2.imwrite('Q3 - Bit Plane '+str(atualbBit)+'.png',img)
	else:
		cv2.imwrite(outputfile,img)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

def main(argv):
	inputfile = ''
	outputfile = ''
	atualbBit = ''

	try:
		opts, args = getopt.getopt(argv,'hi:o:b:',['ifile=','ofile=','bit='])
	except:
		print('t2.py -i <inputfile> -o <outputfile> -b <bit>')
	for opt, arg in opts:
		if opt == 'h':
			print('T1.py -i <inputfile> -o <outputfile> -b <bit>')
		elif opt in ('-i','--ifile'):
			inputfile = arg
		elif opt in ('-o','--ofile'):
			outputfile = arg
		elif opt in ('-b','--bit'):
			atualbBit = int(arg)

	img =  cv2.imread('../Images/' + inputfile, cv2.IMREAD_GRAYSCALE)
	if(atualbBit == ''):
		atualbBit = 7
	if(img is None):
		print('Imagem indisponível, escolha uma imagem no diretório Images.')
	elif ((atualbBit > 7) or (atualbBit < 0)):
		print('Imagens contém apenas 8 planos de bits, de 0 a 7')
	else:
		bitPlane(img,outputfile,atualbBit)


if __name__=="__main__":
	main(sys.argv[1:])