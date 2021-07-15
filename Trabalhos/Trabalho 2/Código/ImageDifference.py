import cv2
import sys,getopt

def difference(inputfile_i,inputfile_j,outputfile):
	img1 = cv2.imread(inputfile_i, cv2.IMREAD_COLOR)
	img2 = cv2.imread(inputfile_j, cv2.IMREAD_COLOR)
	
	if (img1 is None):
		print('Imagem 1 indisponível, escolha uma imagem no diretório.')
	elif (img2 is None):
		print('Imagem 2 indisponível, escolha uma imagem no diretório.')
	else:
		img = img1 - img2

		cv2.imshow('halftone Image', img)
		cv2.waitKey(0)
		cv2.destroyAllWindows()
		#savaImage
		if(outputfile == ''):
			cv2.imwrite('Imagem 1: '+ inputfile_i + 'Imagem 2: '+ inputfile_j +'.png',img)			
		else:
			cv2.imwrite(outputfile,img)
			
 #----------------------------------------------- MAIN -----------------------------------------------
def main(argv):
	inputfile_i = ''
	inputfile_j = ''
	outputfile = ''
	
	try:
		opts, args = getopt.getopt(argv, 'hi:j:o:', ['ifile=','jfile=','ofile='])
	except getopt.GetoptError:
		print('ImageDifference.py -i <inputfile_i> -j <inputfile_j> -o <outputfile>')
		sys.exit(2)

	for opt, arg in opts:
		if opt == 'h':
			print('ImageDifference.py -i <inputfile_i> -j <inputfile_j> -o <outputfile>')
			sys.exit()
		elif opt in ('-i','--inputfile_i'):
			inputfile_i = arg
		elif opt in ('-j','--inputfile_j'):
			inputfile_j = arg
		elif opt in ('-o','--outputfile'):
			outputfile = arg

	img = difference(inputfile_i,inputfile_j,outputfile)


if __name__ == '__main__':
	main(sys.argv[1:])
