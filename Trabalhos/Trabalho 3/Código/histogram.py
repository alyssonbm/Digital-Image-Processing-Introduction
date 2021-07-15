import cv2
import sys,getopt
import numpy as np
import matplotlib.pyplot as plt

def histogram(inputfile,outputfile,num_bins):

	img = cv2.imread('../imagens_pgm/' + inputfile, cv2.IMREAD_GRAYSCALE)

	blackPixels = img[img==0]
	blackPixelsFraction = (len(blackPixels) * 100)/img.size

	plt.hist(img.ravel(), bins=range(int(num_bins)), edgecolor='none', color="#3F5D7D")
	plt.xlim([-1, int(num_bins)+1])
	plt.title(inputfile + ' - Fracao de Pixels Pretos: ' + str(blackPixelsFraction) + ' %')

	if(outputfile != ''):
		plt.savefig(outputfile+'.png', bbox_inches='tight')
	else:
		plt.savefig(inputfile+' - histogram.png', bbox_inches='tight')

 #----------------------------------------------- MAIN -----------------------------------------------
def main(argv):
	inputfile = ''
	outputfile = ''
	num_bins = 256

	try:
		opts, args = getopt.getopt(argv, 'hi:o:b:', ['ifile=','ofile=','num_bins'])
	except getopt.GetoptError:
		print('trabalho2.py -i <inputfile> -o <outputfile> -b <num_bins>')
		sys.exit(2)

	for opt, arg in opts:
		if opt == 'h':
			print('trabalho2.py -i <inputfile> -o <outputfile> -b <num_bins>')
			sys.exit()
		elif opt in ('-i','--inputfile'):
			inputfile = arg
		elif opt in ('-o','--outputfile'):
			outputfile = arg
		elif opt in ('-b','--num_bins'):
			num_bins = arg

	
	histogram(inputfile,outputfile,num_bins)


if __name__ == '__main__':
	main(sys.argv[1:])
