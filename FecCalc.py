import sys
import os
import time


from Crypto.Hash import RIPEMD160

def welcomeScreen():
	print("###############################################################################")
	print("#*****************************************************************************#")
	print("#***************************MAGNA413 FeC Calculator***************************#")
	print("#*****************************************************************************#")
	print("#*****************************************************************************#")
	print("#*******************************By  MJsolutions*******************************#")
	print("#*****************************************************************************#")
	print("#*****************************************************************************#")
	print("#*****************************************************************************#")
	print("###############################################################################")
	print("")
	print("")


def vinEnter():

	
	 
	while (True):
		vinTempArray=bytearray()
		print("Enter Vehicle Identification Number: ",end="")
		vinTemp=str(input().upper())

		if (len(vinTemp) != 17) or (not(vinTemp.isalnum())):
			print("VIN must be exactly 17 alphanumeric charecters!")
		elif (len(vinTemp) == 17) and (vinTemp.isalnum()):
			for i in vinTemp:
				vinTempArray.append(ord(i))

			
			break
	return vinTempArray


def vcrnEnter():
	while (True):
		try:
			vcrnTempArray=bytearray()
			print("Enter VCRN: ",end="")
			vcrnTemp=input()

			for i in range(0,len(vcrnTemp),2):
				vcrnTempArray.append(int(vcrnTemp[i:i+2],16))

		except:
			print("Incorrect length. VCRN should be 5 bytes")

		print(vcrnTempArray)
		print(len(vcrnTempArray))

		if len(vcrnTempArray) == 5:
			break
		elif len(vcrnTempArray) != 5:
			print("Incorrect length. VCRN should be 5 bytes")
	return vcrnTempArray


def fecEnter():

	while True:

		try:
			print("Start of loop array: "+str(fecTempArray))
		except:
			print("",end="")

		fecTempArray=bytearray()
		print("After declaring of loop array: "+str(fecTempArray))

		count=0
		print("FEC key/s separeted by space: ",end="")
		fecTemp=input().split()
		if len(fecTemp) == 0:
			print("Incorrect input. Try Again!")
			continue

		for i in fecTemp:
			count+=1
			print("Teine pikkus: "+ str(len(i)))
			if len(i) != 8 or not i.isalnum() or i== 0:

				print("FEC "+i+" is wrong! FEC length is 8 digits and leading zeroes are important")
				continue
			for j in range(0,len(i),2):

				fecTempArray.append(int(i[j:j+2],16))
				print("Ajutine array: "+str(fecTempArray))

		#if len(fecTempArray) == 
		print("Ajutine array pikkus: "+str(len(fecTempArray))+" Count arv: "+str(count) )
		if count*4 == len(fecTempArray):
			break
		else:
			continue

	print("count: "+str(count)+" Array: "+str(fecTempArray))
	return fecTempArray,count


def swapBuild(vin,vcrn):
	fecArray,count = fecEnter()
	
	if count == 1:

		print(fecArray)
		#fecArray=b''.join([b'1102',fecArray,b'03',vcrn,vin,b'00'] )
		fecArray=b''.join([b'\x11\x02',fecArray,b'\x03',vcrn,vin,b'\x00',int(time.time()).to_bytes(4,'big'),b'\x00\x00\x00\x00\x00\x00\x00\x00\x00'] )


		#b'1102'+fecArray+b'03'+vcrn+vin+b'00'
		

		print("1 fec")
		print(vcrn)
		print(fecArray)
	if count >= 2:
		fecArray=b''.join([b'\x11\x07',b'\xFF\xFF\xFF\xFF',b'\x03',vcrn,vin,b'\x00',int(time.time()).to_bytes(4,'big'),fecArray] )
		print(fecArray)
		print("2 fec")

	return fecArray

def signingFunc(paddedHash):

	print("1. 5Q0_MRR PQ26")
	print("Select project [1-4]: ",end="")
	input()


	PQ26_mod=0x8F514A9A0F38BA407DA15F3B4AC0E55FA97C8C3E7C7DED9790541C958767C91BC794723AB6C9B90349DA6B399D46C01CC60E4125037AC76BE5E99BCE66E3BE36C0ADB33CF2F197BA8FEFED150C93BFD61FC35F83BDBD40C8A94B029FB4F9E6B33EA881766629AFAE152422BD7762D915E322CC2149522AA1858D00F8EBFD0537
	pq26_priv=0x5F8B87115F7B26D5A9163F7CDC8098EA70FDB2D452FE9E650AE2BDB904EFDB67DA62F6D1CF312602313C477BBE2F2ABDD95ED618ACFC84F2994667DEEF427ECE2128D0D049A9AAD249AB2C241CEAF0A8A1796F0779E564D8667F5CBDC5AE51FF9BACA08229F9FF92DFDA5809CC06F4E68475E2830BF30CF308E21BCB9A19A12B


	#print(paddedHash)
	return pow(int.from_bytes(paddedHash,'big'),pq26_priv,PQ26_mod).to_bytes(128,'big')

def ripemd160WithRSASignature(incompleteSWAP):
	ripmed160RSAsigningPadding=b'\x00\x01\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x000!0\t\x06\x05+$\x03\x02\x01\x05\x00\x04\x14'
	ripemd160hash=RIPEMD160.new()
	ripemd160hash.update(incompleteSWAP)

	return b''.join([incompleteSWAP,signingFunc(b''.join([ripemd160hash.digest()]))])




def main():

	if sys.version_info < (3, 10):
		sys.exit("Please use Python 3.10 or higher.")


	welcomeScreen()
	#print(vinEnter())

	#i=ripemd160WithRSASignature(swapBuild(vinEnter(),vcrnEnter()))

	#for j in i:
		#print(chr(j))

	#with open('SWAP.bin', 'wb',) as file:

		#print((ripemd160WithRSASignature(swapBuild(vinEnter(),vcrnEnter())),).decode)

	print("SWaP is: " + str(hex(int.from_bytes(bytearray().join([ripemd160WithRSASignature(swapBuild(vinEnter(),vcrnEnter()))]),'big')).upper()[2:]))

	#fecEnter()
	




main()

