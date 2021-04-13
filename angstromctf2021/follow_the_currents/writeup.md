# AngstromCTF2021 Folow the Currents

From the code provided we spot that the key is only two bytes. This enables us to do an exhaustive search of the key-space.

```
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
```

The solution script tries every key and tries to decode the decrypted data as uft-8. If the decoding succeeds it prints the decrypted values as utf-8.

Luckly only one key decrypts the data into uft-8 and we get the flag.

```
actf{low_entropy_keystream}
```
