from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.fernet import Fernet

#ассиметричное шифрование
priv_key = rsa.generate_private_key(65537, 4096)
pub_key = priv_key.public_key()

data = "abc 123 asdfa"
ser_data = data.encode()

crypto_result = pub_key.encrypt(ser_data, padding.OAEP(padding.MGF1(hashes.SHA256()), hashes.SHA256(), None))

decrypt_data = priv_key.decrypt(crypto_result, padding.OAEP(padding.MGF1(hashes.SHA256()), hashes.SHA256(), None))

stringpubKey = pub_key.public_bytes(serialization.Encoding.PEM, serialization.PublicFormat.SubjectPublicKeyInfo)

objPubKey = serialization.load_pem_public_key(stringpubKey)

#симметричное шифрование
key = Fernet.generate_key()
key_obj = Fernet(key)


print(key.decode())
data = "abc123"
cyph_data = key_obj.encrypt(data.encode())

dkey = key.decode()

en_dkey = pub_key.encrypt(dkey.encode(), padding.OAEP(padding.MGF1(hashes.SHA256()), hashes.SHA256(), None))
de_dkey = priv_key.decrypt(en_dkey, padding.OAEP(padding.MGF1(hashes.SHA256()), hashes.SHA256(), None))

key_obj = Fernet(de_dkey)



decyph_data = key_obj.decrypt(cyph_data).decode()

print(cyph_data)
print(decyph_data)


