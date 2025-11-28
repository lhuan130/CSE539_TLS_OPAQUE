#TLS server

#SERVER PART 1: Generate self-signed certificate (at startup)

# Server certificate key generation
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
key = rsa.generate_private_key(public_exponent=65537,key_size=2048)

cert_privatekey_filename = "./server_files/cert_private_key.pem"
cert_path = "./server_files/selfsigned_cert.pem"
# Store private key
import os
os.makedirs(os.path.dirname(cert_privatekey_filename), exist_ok=True)
with open(cert_privatekey_filename, "wb") as f:
    f.write(key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.BestAvailableEncryption(b"bonusproject"),
    ))

#Collect certificate associated data
from cryptography import x509
from cryptography.x509.oid import NameOID
subject = issuer = x509.Name([
    x509.NameAttribute(NameOID.COUNTRY_NAME, "US"),
    x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "Arizona"),
    x509.NameAttribute(NameOID.LOCALITY_NAME, "Tempe"),
    x509.NameAttribute(NameOID.ORGANIZATION_NAME, "ASU"),
    x509.NameAttribute(NameOID.COMMON_NAME, "pwn.college/cse539-s2025"),
])

#Generate certificate
import datetime
from cryptography.hazmat.primitives import hashes
cert = x509.CertificateBuilder().subject_name(
    subject
).issuer_name(
    issuer
).public_key(
    key.public_key()
).serial_number(
    x509.random_serial_number()
).not_valid_before(
    datetime.datetime.now(datetime.timezone.utc)
).not_valid_after(#certificate will be valid for 100 days after generation
    datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=100)
).add_extension(
    x509.SubjectAlternativeName([x509.DNSName("localhost")]),
    critical=False,
).sign(key, hashes.SHA256())
with open(cert_path, "wb") as f:
    f.write(cert.public_bytes(serialization.Encoding.PEM))


#SERVER PART 2: registration
#   We assume that the client's password has already been registered.
#   This means that the username and processed password data has already been registered by the user.
#   For our purposes, because we are not performing the password registration, we will generate by "knowing" the password.
#   Actual OPAQUE would not give the server the password.
username, password = "pakeclient", b'client_opaque_pass'
generated_k = os.urandom(32)
print(len(generated_k),generated_k)

N = 2**256
digest = hashes.Hash(hashes.SHA256())
digest.update(generated_k)
digest.update(password)
blinded_pass = digest.finalize()

#The important components:
#stored generated_k




#SERVER PART 3: the exchange

#Set up listening port
import socket
port = 24601
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind(('', port))
    s.listen(1)
    print("READY TO EXCHANGE") #Run client.py at this point

    #wait
    while True:
        c, addr = s.accept()
        # display client address
        print("CONNECTION FROM:", str(addr))
    
    s.close()
    print("CLOSED")
