# MuhammadUmair-SATTI-
AI chatbot

## Secure communication app (Python)
This repo now includes a simple TLS-secured client/server example.

### 1) Generate a self-signed certificate
```bash
openssl req -x509 -newkey rsa:2048 -sha256 -days 365 -nodes \
  -keyout server.key -out server.crt -subj "/CN=localhost"
```

### 2) Start the server
```bash
python3 secure_server.py --host 0.0.0.0 --port 8443 --cert server.crt --key server.key
```

### 3) Connect with the client
```bash
python3 secure_client.py --host 127.0.0.1 --port 8443 --ca server.crt
```

### Optional: skip verification (not recommended)
```bash
python3 secure_client.py --host 127.0.0.1 --port 8443 --insecure
```
