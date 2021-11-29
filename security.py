from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import json
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

def create_keys():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=4096,
        backend=default_backend()
    )
    
    public_key = private_key.public_key()
    
    pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    
    with open('private_key.pem', 'wb') as f:
        f.write(pem)
    
    pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    
    with open('public_key.pem', 'wb') as f:
        f.write(pem)
    
def read_public_key(): 
    with open("public_key.pem", "rb") as key_file:
        public_key = serialization.load_pem_public_key(
        key_file.read(),
        backend=default_backend()
        )
    return public_key

def read_private_key():
    with open("private_key.pem", "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
            backend=default_backend()
        )
    
    return private_key
        
def encrypt_data(msg, public_key): 
    # Encrypting.
    encrypted_msg = public_key.encrypt(
        msg,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    return encrypted_msg 

def decrypt_data(msg, private_key): 
    decoded_message = private_key.decrypt(
        msg,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    return decoded_message

def testing():
    rover_info =  {"1'10.35.70.21'" :[300,300,5555], "2'10.35.70.21": [400,400,6666], "3'10.35.70.21'" :[300,300,5555], "4'10.35.70.21": [400,400,6666]}
    msg = json.dumps(rover_info).encode('utf-8')

    create_keys()
    public_key = read_public_key()

    encrypted_msg = encrypt_data(msg, public_key)

    private_key = read_private_key()
    decrypted_msg = decrypt_data(encrypted_msg, private_key).decode('utf-8')

    print("ORIGINAL MESSAGE: ", msg)
    print("ENCRYPTED MSG: ", encrypted_msg) 
    print("DECRYPTED MSG: ", decrypted_msg)


if __name__ == '__main__':
    testing()