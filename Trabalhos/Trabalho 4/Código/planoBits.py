import cv2 
import numpy as np
import sys,getopt

def bitPlane(inputfile,img,outputfile,atualbBit):
	img = np.unpackbits(img).reshape(img.shape[0],img.shape[1],img.shape[2],8)
	for k in range(img.shape[2]):
		for i in range(img.shape[0]):
			for j in range(img.shape[1]):
				if(img[i][j][k][7-atualbBit] == 0):
					img[i][j][k] = 00000000
				else:
					img[i][j][k] = 11111111

	img = np.packbits(img).reshape(img.shape[0],img.shape[1],img.shape[2])

	cv2.imshow('Slices',img)
	if(outputfile == ''):
		cv2.imwrite(inputfile+'BitPlane'+str(atualbBit)+'.png',img)
	else:
		cv2.imwrite(outputfile,img)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

def bitPlaneOneChannel(inputfile,img,outputfile,atualbBit,channel):
	if (channel==0):
		img[:,:,1] = 0
		img[:,:,2] = 0
	if (channel==1):
		img[:,:,0] = 0
		img[:,:,2] = 0
	if (channel==2):
		img[:,:,0] = 0
		img[:,:,1] = 0

	img = np.unpackbits(img).reshape(img.shape[0],img.shape[1],img.shape[2],8)
	for k in range(img.shape[2]):
		for i in range(img.shape[0]):
			for j in range(img.shape[1]):
				if(img[i][j][k][7-atualbBit] == 0):
					img[i][j][k] = 00000000
				else:
					img[i][j][k] = 11111111

	img = np.packbits(img).reshape(img.shape[0],img.shape[1],img.shape[2])

	cv2.imshow('Slices',img)
	if(outputfile == ''):
		cv2.imwrite(inputfile+'BitPlane'+str(atualbBit)+'Channel'+str(channel)+'.png',img)
	else:
		cv2.imwrite(outputfile,img)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

def main(argv):
	inputfile = ''
	outputfile = ''
	atualbBit = ''
	channel = ''

	try:
		opts, args = getopt.getopt(argv,'hi:o:b:c:',['ifile=','ofile=','bitPlane=','channel=='])
	except:
		print('t2.py -i <inputfile> -o <outputfile> -b <bitPlane>')
	for opt, arg in opts:
		if opt == 'h':
			print('T1.py -i <inputfile> -o <outputfile> -b <bitPlane>')
		elif opt in ('-i','--ifile'):
			inputfile = arg
		elif opt in ('-o','--ofile'):
			outputfile = arg
		elif opt in ('-b','--bitPlane'):
			atualbBit = int(arg)
		elif opt in ('-c','--channel'):
			channel = int(arg)

	img =  cv2.imread(inputfile, cv2.IMREAD_COLOR)
	if(atualbBit == ''):
		atualbBit = 7
	if(img is None):
		print('Imagem indisponível, escolha uma imagem no diretório Images.')
	elif ((atualbBit > 7) or (atualbBit < 0)):
		print('Imagens contém apenas 8 planos de bits, de 0 a 7')
	else:
		if(channel==''):
			bitPlane(inputfile,img,outputfile,atualbBit)
		else:
			bitPlaneOneChannel(inputfile,img,outputfile,atualbBit,channel)

if __name__=="__main__":
	main(sys.argv[1:])