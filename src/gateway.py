import os
import requests
import urllib.parse
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

SERVER_URL = "http://10.234.165.156:8000"
DIRECTORY = "/home/debbie/temp"

with open("client.key", "rb") as f:
    key = Ed25519PrivateKey.from_private_bytes(f.read())

for fname in os.listdir(DIRECTORY):
    path = os.path.join(DIRECTORY, fname)
    if not os.path.isfile(path):
        continue

    with open(path, "rb") as f:
        data = f.read()

    message = fname.encode() + b":" + data
    sig = key.sign(message)

    headers = {
        "Filename": urllib.parse.quote(fname),
        "Signature": sig.hex()
    }

    r = requests.post(SERVER_URL, headers=headers, data=data)

    print(fname, r.status_code)
shutdown_msg = b"SHUTDOWN"
sig = key.sign(shutdown_msg)

headers = {
    "Filename": "__shutdown__",
    "Signature": sig.hex()
}

try:
    requests.post(SERVER_URL, headers=headers, data=shutdown_msg, timeout=2)
except Exception:
    pass

print("shutdown sent")
