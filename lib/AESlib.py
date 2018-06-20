from Crypto.Hash import SHA256
from Crypto.Cipher import AES
import os, random

def encrypt(key, filename):
    digestKey = SHA256.new(key.encode('utf-8')).digest()
    outFile = os.path.join(os.path.dirname(filename), os.path.basename(filename)[3:])
    chunksize = 64 * 1024
    filesize = str(os.path.getsize(filename)).zfill(16)
    IV = os.urandom(16)

    encryptor = AES.new(digestKey, AES.MODE_CBC, IV)

    with open(filename, "rb") as infile:
        with open(outFile, "wb") as outfile:
            outfile.write(filesize.encode())
            outfile.write(IV)
            while True:
                chunk = infile.read(chunksize)

                if len(chunk) == 0:
                    break

                elif len(chunk) % 16 !=0:
                    chunk += (' ' *  (16 - (len(chunk) % 16))).encode()

                    outfile.write(encryptor.encrypt(chunk))


def decrypt(key, filename):
    digestKey = SHA256.new(key.encode('utf-8')).digest()
    outFile = os.path.join(os.path.dirname(filename), "(tmp)"+os.path.basename(filename)[9:])
    fileNameBack = outFile
    chunksize = 64 * 1024
    with open(filename, "rb") as infile:
        filesize = infile.read(16)
        IV = infile.read(16)

        decryptor = AES.new(digestKey, AES.MODE_CBC, IV)

        with open(outFile, "wb") as outfile:
            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break

                outfile.write(decryptor.decrypt(chunk))

            outfile.truncate(int(filesize))

    return fileNameBack
