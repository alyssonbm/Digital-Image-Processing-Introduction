import cv2
import sys,getopt

def bitstring_to_bytes(s):
    v = int(s, 2)
    b = bytearray()
    while v:
        b.append(v & 0xff)
        v >>= 8
    return bytes(b[::-1])

def testeSizeCapacite(img,bits):
	h,w,c = img.shape
	#Dado 30 como margem de segurança e futuras expanções
	imgBits = (h*w*3)
	if(imgBits < (len(bits)+30)):
		print('Este conteúdo é muito grande para a imagem selecionada, por favor selecione uma imagem com uma escala maior ou um novo conteúdo')
		exit(1)

def encodeBinary(img,binaryMessage,bitPlane):
	messageSizeBinary = "{0:b}".format(len(binaryMessage))
	zerosComplement = '0'* (60-len(messageSizeBinary))
	messageSizeBinary = zerosComplement + messageSizeBinary
	binaryMessage = messageSizeBinary + binaryMessage

	bitPlane = int(bitPlane)
	h,w,c = img.shape
	sizeMessage=0
	controller = 0
	mask = (1 << bitPlane)
	invertMask = ~mask & 0xff
	while sizeMessage < len(binaryMessage):
		for dimension in range(c):
			if(sizeMessage < len(binaryMessage)):
				messageToInput= (int(binaryMessage[sizeMessage])<<bitPlane)
				img[controller//w][controller%w][dimension] = (img[controller//w][controller%w][dimension] & invertMask | messageToInput)
				# print('Posição : [' + str(controller//w) + '][' + str(controller%w) + '][' + str(dimension) + ']' )
				sizeMessage += 1
		controller += 1 
	return img

def decodeBinary(img,bitPlane):
	bitPlane = int(bitPlane)+1
	h,w,c = img.shape
	catchSizeMessage = 0
	size = ''
	controller = 0
	while catchSizeMessage < 60:
		for dimension in range(c):
			if(catchSizeMessage < 60):
				bits = "{0:b}".format(img[controller//w][controller%w][dimension])
				bitSize = len(bits)
				size += bits[bitSize - bitPlane]
				catchSizeMessage+=1
				# print('Posição : [' + str(controller//w) + '][' + str(controller%w) + '][' + str(dimension) + ']' )
		controller += 1
	size = int(size,2)

	message = ''
	while catchSizeMessage < size+60:
		for dimension in range(c):
			if(catchSizeMessage < size+60):
				bit = "{0:b}".format(img[controller//w][controller%w][dimension])
				bitSize = len(bit)
				message += bit[bitSize - bitPlane]
				catchSizeMessage+=1
		controller += 1
	return message

def encodeMessage(img,message,bitPlane):
	binaryMessage = ''.join(format(ord(i), '08b') for i in message) 
	testeSizeCapacite(img,binaryMessage)
	img = encodeBinary(img,binaryMessage,bitPlane)
	return img

def decodeMessage(img,bitPlane):
	message = decodeBinary(img,bitPlane)
	messageFinal = ''
	for i in range(0,len(message),8):
		messageFinal += (chr(int(message[i:i+8], 2)))
	print(messageFinal)

def encodeFile(img,file,bitPlane):
	#Verifica o tipo de arquivo e transforma em binário, complementando com 0 caso tenha menos que 4 caracteres, 32 bits
	typeFile = file.split('.')
	typeFile = '.'+typeFile[-1]
	typeFile = ''.join(format(ord(i), '08b') for i in typeFile) 
	zerosComplement = '0'* (32-len(typeFile))
	typeFile = zerosComplement + typeFile

	bitFile = ''
	with open(file, "rb") as file:
		f = file.read()
		for my_byte in f:
			bitFile += f'{my_byte:0>8b}'
	
	bytes_as_bits = typeFile + bitFile
	testeSizeCapacite(img,bytes_as_bits)
	img = encodeBinary(img,bytes_as_bits,bitPlane)
	return img

def decodeFile(img,bitPlane,outputfile):
	typeFile=''
	objectBit = decodeBinary(img,bitPlane)
	typeFileBit = objectBit[0:32]
	for i in range(0,len(typeFileBit),8):
		typeFile += chr(int(typeFileBit[i:i+8], 2))
	
	objectByte = bitstring_to_bytes(objectBit[32:])
	objectByte = bytearray(objectByte)
	if(outputfile==''):
		f=open('arquivo' + typeFile,"wb")
	else:
		f=open(outputfile + typeFile,"wb")
	f.write(objectByte)

def steganography(inputfile,outputfile,message,bitPlane,encode,textFile):
	if(textFile!='' and message!=''):
		print('Escolha apenas uma fonte para anexar a imagem')
	if(encode=='1'):
		img = cv2.imread('../Imagens Coloridas/' + inputfile, cv2.IMREAD_COLOR)
		if(img is None):
			print('Imagem indisponível, escolha uma imagem no diretório Images.')
			exit(0)
		if(message!=''):
			img = encodeMessage(img,message,bitPlane)
		else:
			img = encodeFile(img,textFile,bitPlane)

		cv2.imshow('Secret Image', img)
		cv2.waitKey(0)
		cv2.destroyAllWindows()
		#savaImage
		if(outputfile == ''):
			cv2.imwrite('Secret-Image:'+ inputfile + '.png',img)
		else:
			cv2.imwrite(outputfile,img)
	
	else:
		img = cv2.imread(inputfile, cv2.IMREAD_COLOR)
		if(img is None):
			print('Imagem indisponível, escolha uma imagem no diretório Images.')
			exit(0)
		if(message=='1'):
			decodeMessage(img,bitPlane)
		if(textFile=='1'):
			decodeFile(img,bitPlane,outputfile)

 #----------------------------------------------- MAIN -----------------------------------------------
def main(argv):
	inputfile = ''
	outputfile = ''
	message = ''
	bitPlane = ''
	encode = ''
	textFile = ''

	try:
		opts, args = getopt.getopt(argv, 'hi:o:m:b:e:f:', ['ifile=','ofile=','message=','bitPlane=','encode=','file='])
	except getopt.GetoptError:
		print('trabalho4.py -i <inputfile> -o <outputfile> -e <encode> -b <bitPlane> -m <message> -f <file>')
		sys.exit(2)

	for opt, arg in opts:
		if opt == 'h':
			print('trabalho2.py -i <inputfile> -o <outputfile> -e <encode> -b <bitPlane> -m <message> -f <file>')
			sys.exit()
		elif opt in ('-i','--inputfile'):
			inputfile = arg
		elif opt in ('-o','--outputfile'):
			outputfile = arg
		elif opt in ('-m','--message'):
			message = arg
		elif opt in ('-b','--bitplane'):
			bitPlane = arg
		elif opt in ('-e','--encode'):
			encode = arg
		elif opt in ('-f','--file'):
			textFile = arg

	if (bitPlane == ''):
		bitPlane = 0

	if(inputfile!='' or encode!='' or (message!='' or file!='')):	
		steganography(inputfile,outputfile,message,bitPlane,encode,textFile)
	else:
		if(inputfile!=''):
			print('É necessário declarar uma imagem de entrada')
		if(encode!=''):
			print('A opção encode deve ser selecionada, 1 para encode (guardar uma mensagem ou arquivo), 0 para decode (extrair mensagem ou arquivo)')
		if((message!='' and file!='') and encode=='1'):
			print('Para a opção de encode uma mensagem ou arquivo deve ser selecionado.')


if __name__ == '__main__':
	main(sys.argv[1:])