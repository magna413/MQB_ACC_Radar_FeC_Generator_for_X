#!/usr/bin/python3
import sys
import os
import time
import hashlib

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
		vinTemp=str(input("Enter Vehicle Identification Number: "))
		vinTempArray=bytearray(vinTemp.encode())

		if vinTempArray == b'':
			vinTempArray = b'MJ_Solutions     '


		if (len(vinTempArray) == 17) and (((vinTemp.isalnum())) or vinTempArray==b'MJ_Solutions     ' ):
			break
		
		else:
			print("VIN must be exactly 17 alphanumeric charecters! (A-Z,0-9)\n")
			continue

	if (vinTempArray == b'MJ_Solutions     '):
		return vinTempArray
	else:
		return vinTempArray.upper()


def vcrnEnter():

	while (True):
		try:
			vcrnTempArray=bytearray()
			vcrnTemp=input("Enter VCRN: ")
			if vcrnTemp == '':
				vcrnTemp = 'FFFFFFFFFF'

			for i in range(0,len(vcrnTemp),2):
				vcrnTempArray.append(int(vcrnTemp[i:i+2],16))

		except:
			pass

		if len(vcrnTempArray) == 5:
			break
		elif len(vcrnTempArray) != 5:
			print("Incorrect length. VCRN should be 5 bytes\n")
			continue

	return vcrnTempArray


def fecEnter():

	while True:
		fecTempArray=bytearray()

		count=0
		fecTemp=input("FEC key/s separeted by space: ").split()
		if len(fecTemp) == 0:
			print("Incorrect input. Try Again!\n")
			continue

		for i in fecTemp:
			count+=1
			if len(i) != 8 or not i.isalnum() or i== 0:

				if len(fecTemp) != count:
					print("FEC "+i+" is wrong! FEC length is 8 digits and leading zeroes are important")
				elif len(fecTemp) == count:
					print("FEC "+i+" is wrong! FEC length is 8 digits and leading zeroes are important\n")
				continue
			for j in range(0,len(i),2):

				fecTempArray.append(int(i[j:j+2],16))

		if count*4 == len(fecTempArray):
			break
		else:
			continue

	return fecTempArray,count


def swapBuild(vin,vcrn):
	fecArray,count = fecEnter()
	
	if count == 1:

		fecArray=b''.join([b'\x11\x02',fecArray,b'\x03',vcrn,vin,b'\x00',int(time.time()).to_bytes(4,'big'),b'\x00\x00\x00\x00\x00\x00\x00\x00\x00'])

	if count >= 2:
		fecArray=b''.join([b'\x11\x07',b'\xFF\xFF\xFF\xFF',b'\x03',vcrn,vin,b'\x00',int(time.time()).to_bytes(4,'big'),count.to_bytes(1,'big'),fecArray])


	return fecArray

def signingFunc(paddedHash):

	secrets_dict={"PQ26":{"priv":0x5F8B87115F7B26D5A9163F7CDC8098EA70FDB2D452FE9E650AE2BDB904EFDB67DA62F6D1CF312602313C477BBE2F2ABDD95ED618ACFC84F2994667DEEF427ECE2128D0D049A9AAD249AB2C241CEAF0A8A1796F0779E564D8667F5CBDC5AE51FF9BACA08229F9FF92DFDA5809CC06F4E68475E2830BF30CF308E21BCB9A19A12B,"mod":0x8F514A9A0F38BA407DA15F3B4AC0E55FA97C8C3E7C7DED9790541C958767C91BC794723AB6C9B90349DA6B399D46C01CC60E4125037AC76BE5E99BCE66E3BE36C0ADB33CF2F197BA8FEFED150C93BFD61FC35F83BDBD40C8A94B029FB4F9E6B33EA881766629AFAE152422BD7762D915E322CC2149522AA1858D00F8EBFD0537},"3Q0":{"priv":0x8C822993F1414860198E1076742855544F9B0B965E97FBFFCEE9256909C2988588C1FF6FCC2ADDD3FFD14E94D69EF3D0E8EDEF6B5E93BE7C35E6F69A377F76E5F1010B152E1E9DC9DA7214080A24AE38F70D6A4F21EEF604B7DE49508126E64C92FA9B086D6F36E41E7E803AFA3DAA83B9FA5392558293B0C72F6D72F57E8FDB,"mod":0xD2C33E5DE9E1EC90265518B1AE3C7FFE776891618DE3F9FFB65DB81D8EA3E4C84D22FF27B2404CBDFFB9F5DF41EE6DB95D64E7210DDD9DBA50DA71E7533F325ABAC8A6D399D96426F94903EEE5A9F678F419D963CFE22720DD0B1FC6EB9DD20132F4DC7D25A06BBB227251500A3A1CD79F3A7BC30AA87084717ED54D1E082DFF},"3QF":{"priv":0x682FA29DB3D27AD89F7B56A6F74DB5CC76F20967188044CAC8E8358E1743EF17C0790A90A710F0B01091A1251BA2EC37B419D5D1C2BAF96FCF171BF8BD368CD47368C8009F2ACC7D2BCF606016F0938B01BA8BA064589538B06528564E3EF7EC6AB306E18247656CB0D71E644D4EB24C7B6B9C3B89B0021F4586869CA0AE863B,"mod":0x9C4773EC8DBBB844EF3901FA72F490B2B26B0E1AA4C067302D5C505522E5E6A3A0B58FD8FA99690818DA71B7A97462538E26C0BAA4187627B6A2A9F51BD1D3403DA04B88D73105951A057F848E8313BF841A22B2C0D7CE51EAB19C614BBF96EF4F555A297F991B1BDE08E0973E9FF210E3F9668A458E9FFF22F114EBF5E0BA37},"2Q0":{"priv":0x6EC84650F6C95ECECB42F56E4528A08CFF4B2E584C9F1E34F5BB27E1AD149D76FA096622D63ED7BCE7F21FAC3F769E5B2052901FE0C5552DDC57943F05698B9E6A7357AA775C4E835251F37C3D87F11DAC9378A747901E9F3D0D66A79BB538F8055C0BFDD46B6157EFAA5C8BDDC654104B70A5FE81790652A613690DF2EABD6B,"mod":0xA62C6979722E0E3630E4702567BCF0D37EF0C58472EEAD4F7098BBD2839EEC32770E1934415E439B5BEB2F825F31ED88B07BD82FD127FFC4CA835E5E881E516F3C3B523792D653A1844A01E3F938A4B625271C2B937E7153D0D1468FEA1D7906EED1AAE2F72212DFDD2D03668B60FCCE4DFB50593A51AE7B2640CB62EBA9758B}}
	
	while True:
		print("")
		print("1. 5Q0_MRR PQ26     - MRR1Plus  - First 'flat' MRR radar in Golf?")
		print("2. 3Q0_MRR MQB      - MRRevo14F - Radar in Passat and Superb")
		print("3. 3QF_5Q0_MRR MQB  - MRRevo14F - Radar in Golf and Passat 8.5")
		print("4. 2Q0_MRR MQB      - Continental radar")
		
		
		sel = input("Select project [1-4]: ")
		if sel == "1":
			return pow(int.from_bytes(paddedHash,'big'),secrets_dict["PQ26"]["priv"],secrets_dict["PQ26"]["mod"]).to_bytes(128,'big')
			break
		
		elif sel == "2":
			return pow(int.from_bytes(paddedHash,'big'),secrets_dict["3Q0"]["priv"],secrets_dict["3Q0"]["mod"]).to_bytes(128,'big')
			break
		
		elif sel == "3":
			return pow(int.from_bytes(paddedHash,'big'),secrets_dict["3QF"]["priv"],secrets_dict["3QF"]["mod"]).to_bytes(128,'big')
			break
		
		elif sel == "4":
			return pow(int.from_bytes(paddedHash,'big'),secrets_dict["2Q0"]["priv"],secrets_dict["2Q0"]["mod"]).to_bytes(128,'big')
			break
		else:
			print("Incorrect selection",end="\n\n")
			continue

def ripemd160WithRSASignature(incompleteSWAP):
	ripemd160RSAsigningPadding=b'\x00\x01\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x000!0\t\x06\x05+$\x03\x02\x01\x05\x00\x04\x14'
	ripemd160hash=(hashlib.new("ripemd160",incompleteSWAP)).digest()

	return b''.join([incompleteSWAP,signingFunc(b''.join([ripemd160RSAsigningPadding,ripemd160hash]))])



def main():

	welcomeScreen()

	print("\nSWaP is: " + str(hex(int.from_bytes(bytearray().join([ripemd160WithRSASignature(swapBuild(vinEnter(),vcrnEnter()))]),'big')).upper()[2:]))

	




main()

