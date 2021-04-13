import os
import zlib

def keystream_decode(key):
	index = 0
	while 1:
		index+=1
		if index >= len(key):
			key += zlib.crc32(key).to_bytes(4,'big')
		yield key[index]

with open("enc","rb") as f:
	ciphertext = f.read()
	for i in range(65536):
		plain = []
		k = keystream_decode((i).to_bytes(2, 'big'))
		for i in ciphertext:
			plain.append(i ^ next(k))
		try:
			if bytes(plain).decode("utf-8"):
				print(bytes(plain))
		except:
			pass
