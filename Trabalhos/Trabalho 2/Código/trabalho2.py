import cv2
import sys,getopt
import time
import numpy as np

# ------------  Halftones methods  ------------
# Floyd and Steinberg method
def method_FloydSteinberg(img,error,i,j,k,sweep):
	if(sweep=='2'):
		img[i,j-1,k] = img[i,j-1,k] + (7/16) * error
		img[i+1,j-1,k] = img[i+1,j-1,k] + (1/16) * error
		img[i+1,j,k] = img[i+1,j,k] + (5/16) * error
		img[i+1,j+1,k] = img[i+1,j+1,k] + (3/16) * error
	else:
		img[i,j+1,k] = img[i,j+1,k] + (7/16) * error
		img[i+1,j-1,k] = img[i+1,j-1,k] + (3/16) * error
		img[i+1,j,k] = img[i+1,j,k] + (5/16) * error
		img[i+1,j+1,k] = img[i+1,j+1,k] + (1/16 )* error
	return img

# Stevenson and Arce method
def method_StevensonArce(img,error,i,j,k,sweep):
	if(sweep == '2'):
		img[i,j-2,k] = img[i,j-2,k] + (32/200) * error 
		img[i+1,j-3,k] = img[i+1,j-3,k] + (16/200) * error
		img[i+1,j-1,k] = img[i+1,j-1,k] + (30/200) * error
		img[i+1,j+1,k] = img[i+1,j+1,k] + (26/200) * error
		img[i+1,j+3,k] = img[i+1,j+3,k] + (12/200) * error
	else:
		img[i,j+2,k] = img[i,j+2,k] + (32/200) * error 
		img[i+1,j-3,k] = img[i+1,j-3,k] + (12/200) * error
		img[i+1,j-1,k] = img[i+1,j-1,k] + (26/200) * error
		img[i+1,j+1,k] = img[i+1,j+1,k] + (30/200) * error
		img[i+1,j+3,k] = img[i+1,j+3,k] + (16/200) * error

	img[i+2,j-2,k] = img[i+2,j-2,k] + (12/200) * error
	img[i+2,j,k] = img[i+2,j,k] + (26/200) * error
	img[i+2,j+2,k] = img[i+2,j+2,k] + (12/200) * error
	img[i+3,j-3,k] = img[i+3,j-3,k] + (5/200) * error
	img[i+3,j-1,k] = img[i+3,j-1,k] + (12/200) * error
	img[i+3,j+1,k] = img[i+3,j+1,k] + (12/200) * error
	img[i+3,j+3,k] = img[i+3,j+3,k] + (5/200) * error
	return img

# Burkes method
def method_Burkes(img,error,i,j,k,sweep):	
	if(sweep=='2'):
		img[i,j-1,k] = img[i,j-1,k] + (8/32) * error
		img[i,j-2,k] = img[i,j-2,k] + (4/32) * error
	else:
		img[i,j+1,k] = img[i,j+1,k] + (8/32) * error
		img[i,j+2,k] = img[i,j+2,k] + (4/32) * error
	img[i+1,j-2,k] = img[i+1,j-2,k] + (2/32) * error
	img[i+1,j-1,k] = img[i+1,j-1,k] + (4/32) * error
	img[i+1,j,k] = img[i+1,j,k] + (8/32) * error
	img[i+1,j+1,k] = img[i+1,j+1,k] + (4/32) * error
	img[i+1,j+2,k] = img[i+1,j+2,k] + (2/32) * error
	return img

# Sierra method
def method_Sierra(img,error,i,j,k,sweep):
	if(sweep=='2'):
		img[i,j-1,k] = img[i,j-1,k] + (5/32) * error
		img[i,j-2,k] = img[i,j-2,k] + (3/32) * error
	else:
		img[i,j+1,k] = img[i,j+1,k] + (5/32) * error
		img[i,j+2,k] = img[i,j+2,k] + (3/32) * error
	img[i+1,j-2,k] = img[i+1,j-2,k] + (2/32) * error
	img[i+1,j-1,k] = img[i+1,j-1,k] + (4/32) * error
	img[i+1,j,k] = img[i+1,j,k] + (5/32) * error
	img[i+1,j+1,k] = img[i+1,j+1,k] + (4/32) * error
	img[i+1,j+2,k] = img[i+1,j+2,k] + (2/32) * error
	img[i+2,j-1,k] = img[i+2,j-1,k] + (2/32) * error
	img[i+2,j,k] = img[i+2,j,k] + (3/32) * error
	img[i+2,j+1,k] = img[i+2,j+1,k] + (2/32) * error
	return img

# Stucki method
def method_Stucki(img,error,i,j,k,sweep):
	if(sweep=='2'):
		img[i,j-1,k] = img[i,j-1,k] + (8/42) * error
		img[i,j-2,k] = img[i,j-2,k] + (4/42) * error
	else:
		img[i,j+1,k] = img[i,j+1,k] + (8/42) * error
		img[i,j+2,k] = img[i,j+2,k] + (4/42) * error
	img[i+1,j-2,k] = img[i+1,j-2,k] + (2/42) * error
	img[i+1,j-1,k] = img[i+1,j-1,k] + (4/42) * error
	img[i+1,j,k] = img[i+1,j,k] + (8/42) * error
	img[i+1,j+1,k] = img[i+1,j+1,k] + (4/42) * error
	img[i+1,j+2,k] = img[i+1,j+2,k] + (2/42) * error
	img[i+2,j-2,k] = img[i+2,j-2,k] + (1/42) * error
	img[i+2,j-1,k] = img[i+2,j-1,k] + (2/42) * error
	img[i+2,j,k] = img[i+2,j,k] + (4/42) * error
	img[i+2,j+1,k] = img[i+2,j+1,k] + (2/42) * error
	img[i+2,j+2,k] = img[i+2,j+2,k] + (1/42) * error
	return img

# Jarvis, Judice and Ninke method
def method_JarvisJudiceNinke(img,error,i,j,k,sweep):
	if(sweep):
		img[i,j-1,k] = img[i,j-1,k] + (7/48) * error
		img[i,j-2,k] = img[i,j-2,k] + (5/48) * error
	else:
		img[i,j+1,k] = img[i,j+1,k] + (7/48) * error
		img[i,j+2,k] = img[i,j+2,k] + (5/48) * error
	img[i+1,j-2,k] = img[i+1,j-2,k] + (3/48) * error
	img[i+1,j-1,k] = img[i+1,j-1,k] + (5/48) * error
	img[i+1,j,k] = img[i+1,j,k] + (7/48) * error
	img[i+1,j+1,k] = img[i+1,j+1,k] + (5/48) * error
	img[i+1,j+2,k] = img[i+1,j+2,k] + (3/48) * error
	img[i+2,j-2,k] = img[i+2,j-2,k] + (1/48) * error
	img[i+2,j-2,k] = img[i+2,j-2,k] + (3/48) * error
	img[i+2,j,k] = img[i+2,j,k] + (5/48) * error
	img[i+2,j+1,k] = img[i+2,j+1,k] + (3/48) * error
	img[i+2,j+2,k] = img[i+2,j+2,k] + (1/48) * error
	return img

# Function to select method used 
def methodChoose(img, error,i,j,k,method,sweep):
	if(method in ['1','FloydSteinberg','floydsteinberg','Floydsteinberg']):
		img = method_FloydSteinberg(img, error,i,j,k,sweep)
	elif(method in ['2','StevensonArce','stevensonarce','Stevensonarce']):
		img = method_StevensonArce(img, error,i,j,k,sweep)
	elif(method in ['3','Burkes','burkes']):
		img = method_Burkes(img, error,i,j,k,sweep)
	elif(method in ['4','Sierra','sierra']):
		img = method_Sierra(img, error,i,j,k,sweep)
	elif(method in ['5','Stucki','stucki']):
		img = method_Stucki(img, error,i,j,k,sweep)
	elif(method in ['6','JarvisJudiceNinke','jarvisjudiceninke','Jarvisjudiceninke']):
		img = method_JarvisJudiceNinke(img, error,i,j,k,sweep)
	else:
		print('Método selecionado não disponível.')
		sys.exit()
	return img

# ------------  Matrix Path mode  ------------
# Left Right mode of matrix path
def sweepLeftRight(img,gImage,borderSize,method,sweep):
	width,height,channel = img.shape
	for i in range(width-borderSize):
		for j in range(height-borderSize):
			for k in range(channel):
				if img[i,j,k] < 128:
					gImage[i,j,k] = 0
				else:
					gImage[i,j,k] = 255
				error = img[i,j,k] - gImage[i,j,k]
				img = methodChoose(img, error,i,j,k,method,sweep)
	return gImage

# Alternet Line, Left and Right mode of matrix path
def sweepAlternate(img,gImage,borderSize,method,sweep):
	width,height,channel = img.shape
	for i in range(width-borderSize):
		if(i % 2):
			for j in range(0,height-borderSize):
				for k in range(channel):
					if img[i,j,k] < 128:
						gImage[i,j,k] = 0
					else:
						gImage[i,j,k] = 255
					error = img[i,j,k] - gImage[i,j,k]
					img = methodChoose(img, error,i,j,k,method,sweep)
		else:
			for j in range(height-borderSize,0,-1):
				for k in range(channel):
					if img[i,j,k] < 128:
						gImage[i,j,k] = 0
					else:
						gImage[i,j,k] = 255
					error = img[i,j,k] - gImage[i,j,k]
					img = methodChoose(img, error,i,j,k,method,sweep)
	return gImage

# # Function to select matrix path method 
def sweepMethod(img,gImage,borderSize,method,sweep):
	if(sweep in ['1','LeftRight','Leftright','leftright']):
		img = sweepLeftRight(img,gImage,borderSize,method,sweep)
	elif(sweep in ['2','Alternate','alternate']):
		img = sweepAlternate(img,gImage,borderSize,method,sweep)
	else:
		print('Modo de Varredura não disponível.')
		sys.exit()
	return img

# ------------  Halftone method, select of features to use  ------------
def halftone(inputfile,outputfile,method,sweep,color):
	if(method==''):
		method = '1'
	if(sweep==''):
		sweep = '1'
	if(color==''):
		color = '1'
	if(color=='1'):
		img = cv2.imread('../Imagens Coloridas/' + inputfile, cv2.IMREAD_COLOR)
	else:
		img = cv2.imread('../Imagens Coloridas/' + inputfile, cv2.IMREAD_GRAYSCALE)
	img = np.float64(img)
	if (img is None):
		print('Imagem indisponível, escolha uma imagem no diretório Images.')
	else:
		borderSize = 4
		if(len(img.shape)<3):
			img = np.expand_dims(img, axis=2)
		gImage = np.zeros(img.shape) 
		img = sweepMethod(img,gImage,borderSize,method,sweep)
		img = np.uint8(img)
		cv2.imshow('halftone Image', img)
		cv2.waitKey(0)
		cv2.destroyAllWindows()
		#savaImage
		if(outputfile == ''):
			cv2.imwrite('Imagem: '+ inputfile + ' - Técnica: ' + method +' - Caminho: ' + sweep +' - Color: ' + color +'.png',img)			
		else:
			cv2.imwrite(outputfile,img)
			
 #----------------------------------------------- MAIN -----------------------------------------------
def main(argv):
	inputfile = ''
	outputfile = ''
	method = ''
	sweep = ''
	color = ''

	try:
		opts, args = getopt.getopt(argv, 'hi:o:m:s:c:', ['ifile=','ofile=','method=','sweep=','color='])
	except getopt.GetoptError:
		print('trabalho2.py -i <inputfile> -o <outputfile -m <method> -s <sweep> -c <color>')
		sys.exit(2)

	for opt, arg in opts:
		if opt == 'h':
			print('trabalho2.py -i <inputfile> -o <outputfile -m <method> -s <sweep> -c <color>')
			sys.exit()
		elif opt in ('-i','--inputfile'):
			inputfile = arg
		elif opt in ('-o','--outputfile'):
			outputfile = arg
		elif opt in ('-m','--method'):
			method = arg
		elif opt in ('-s','--sweep'):
			sweep = arg
		elif opt in ('-c','--color'):
			color = arg

	ini = time.time()
	halftone(inputfile,outputfile,method,sweep,color)
	fim = time.time()
	print ("Tempo de Execução: ", fim-ini)
if __name__ == '__main__':
	main(sys.argv[1:])

# Paulo Júnio Reis Rodrigues
# 19:05
# Sim a minha tb ficou mais clara 
# Gustavo de Jesus Merli
# 19:05
# Esse problema de brilho eu também tive. Não sei se é o mesmo caso que o seu mas no meu o problema era que eu tava pegando a saida como a imagem de entrada mas na verdade era a variável g
# Lucas Martins Veras Pereira
# 19:06
# a minha está bem clara comparada com a do .pdf
# Matheus Santos Almeida
# 19:07
# o problema que eu tive era que a opencv lia a imagem em BGR, ai eu tive que converter pra RGB
# Lucas Ribeiro de Oliveira
# 19:09
# é bom testar um método por vez tbm. Eu estava testando duas abordagens seguidas e tinha um bug que a segunda imagem as vezes ficava mais clara.
