import cv2
import numpy as np
import sys,getopt
from scipy.linalg import sqrtm

h1 = np.array((
		[0,0,-1,0,0],
		[0,-1,-2,-1,0],
		[-1,-2,16,-2,-1],
		[0,-1,-2,-1,0],
		[0,0,-1,0,0]),dtype='int')

h2 = (1/256)* np.array((
	[1,4,6,4,1],
	[4,16,24,16,4],
	[6,24,36,24,6],
	[4,16,24,16,4],
	[1,4,6,4,1]),dtype='int')

h3 = np.array((
	[-1,0,1],
	[-2,0,2],
	[-1,0,1]),dtype='int')

h4 = np.array((
	[-1,-2,-1],
	[0,0,0],
	[1,2,1]),dtype='int')

h5 = np.array((
	[-1,-1,-1],
	[-1,8,-1],
	[-1,-1,-1]),dtype='int')

h6 = (1/9) * np.array((
	[1,1,1],
	[1,1,1],
	[1,1,1]),dtype='int')

h7 = np.array((
	[-1,-1,2],
	[-1,2,-1],
	[2,-1,-1]),dtype='int')

h8 = np.array((
	[2,-1,-1],
	[-1,2,-1],
	[-1,-1,2]),dtype='int')

h9 = (1/9) * np.array((
	[1,0,0,0,0,0,0,0,0],
	[0,1,0,0,0,0,0,0,0],
	[0,0,1,0,0,0,0,0,0],
	[0,0,0,1,0,0,0,0,0],
	[0,0,0,0,1,0,0,0,0],
	[0,0,0,0,0,1,0,0,0],
	[0,0,0,0,0,0,1,0,0],
	[0,0,0,0,0,0,0,1,0],
	[0,0,0,0,0,0,0,0,1]),dtype='int')

h10 = (1/8) * np.array((
	[-1,-1,-1,-1,-1],
	[-1,2,2,2,-1],
	[-1,2,8,2,-1],
	[-1,2,2,2,-1],
	[-1,-1,-1,-1,-1]),dtype='int')

h11 = np.array((
	[-1,-1,0],
	[-1,0,1],
	[0,1,1]),dtype='int')

h3h4 = sqrtm((h3**2)+(h4**2))


def borderChoosed(borderTypeReceived):
	borderType = cv2.BORDER_DEFAULT
	if((borderTypeReceived == 'constant') or borderTypeReceived == '1'): 
		borderType = cv2.BORDER_CONSTANT
	elif((borderTypeReceived == 'replicate') or borderTypeReceived == '2'): 
		borderType = cv2.BORDER_REPLICATE
	elif((borderTypeReceived == 'reflect') or borderTypeReceived == '3'): 
		borderType = cv2.BORDER_REFLECT
	elif((borderTypeReceived == 'reflect101') or borderTypeReceived == '4'): 
		borderType = cv2.BORDER_REFLECT_101
	elif((borderTypeReceived == 'isolated') or borderTypeReceived == '5'): 
		borderType = cv2.BORDER_ISOLATED
	return borderType

def kernelC(kernelChoosed):
	if(kernelChoosed == 'h1'):
		kernel = h1
	elif(kernelChoosed == 'h2'):
		kernel = h2
	elif(kernelChoosed == 'h3'):
		kernel = h3
	elif(kernelChoosed == 'h4'):
		kernel = h4
	elif(kernelChoosed == 'h5'):
		kernel = h5
	elif(kernelChoosed == 'h6'):
		kernel = h6
	elif(kernelChoosed == 'h7'):
		kernel = h7
	elif(kernelChoosed == 'h8'):
		kernel = h8
	elif(kernelChoosed == 'h9'):
		kernel = h9
	elif(kernelChoosed == 'h10'):
		kernel = h10
	elif(kernelChoosed == 'h11'):
		kernel = h11
	elif(kernelChoosed == 'h3h4'):
		kernel = 'h3h4'
	else:
		kernel = h1
	return kernel

def convolution(inputfile, outputfile, kernelChoosed,borderTypeReceived):
	img = cv2.imread('../Images/' + inputfile, cv2.IMREAD_GRAYSCALE)
	if (img is None):
		print('Imagem indisponível, escolha uma imagem no diretório Images.')
	else:
		borderType = borderChoosed(borderTypeReceived)
		kernel = kernelC(kernelChoosed)
		if(str(kernel)!='h3h4'):
			kernel = cv2.flip(kernel, -1)
			img = cv2.filter2D(img,-1,kernel,borderType=borderType)
		else:
			img = np.float32(img)

			img = cv2.filter2D(img,-1,cv2.flip(h3, -1),borderType=borderType)
			img2 = cv2.filter2D(img,-1,cv2.flip(h4, -1),borderType=borderType)
			img = np.uint8(np.sqrt(img**2+img2**2))

		cv2.imshow('Transformed Image', img)
		cv2.waitKey(0)
		cv2.destroyAllWindows()
		#Save Image
		if(outputfile == ''):
			cv2.imwrite('Imagem: '+ inputfile + 'Filtro: ' + kernelChoosed +', Borda: ' + str(borderTypeReceived) +'.png',img)
		else:
			cv2.imwrite(outputfile,img)

def main(argv):
	kernel = 'h1'
	inputfile = ''
	outputfile = ''
	borderTypeReceived = 'default'

	try:
		opts, args = getopt.getopt(argv, 'hi:o:k:b:',['ifile=','ofile=', 'kernel=','borderType='])
	except getopt.GetoptError:
		print('T1.py -i <inputfile> -o <outputfile> -k <kernel> -b <borderType>')
		sys.exit(2)
	for opt, arg in opts:
		if opt == 'h':
			print('T1.py -i <inputfile> -o <outputfile> -k <kernel> -b <borderType>')
			sys.exit()
		elif opt in ('-i','--ifile'):
			inputfile = arg
		elif opt in ('-o','--ofile'):
			outputfile = arg
		elif opt in ('-k','--kernel'):
			kernel = arg
		elif opt in ('-b','--borderType'):
			borderTypeReceived = arg

	convolution(inputfile, outputfile, kernel,borderTypeReceived)

if __name__ == "__main__":
	main(sys.argv[1:])