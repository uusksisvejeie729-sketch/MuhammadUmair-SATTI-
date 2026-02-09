#!/usr/bin/env python3
"""Secure communication server using TLS."""
from __future__ import annotations

import argparse
import socket
import ssl


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="TLS-secured echo server")
    parser.add_argument("--host", default="0.0.0.0", help="Bind host")
    parser.add_argument("--port", type=int, default=8443, help="Bind port")
    parser.add_argument(
        "--cert",
        default="server.crt",
        help="Path to server certificate (PEM)",
    )
    parser.add_argument(
        "--key",
        default="server.key",
        help="Path to server private key (PEM)",
    )
    return parser.parse_args()


def run_server(host: str, port: int, cert: str, key: str) -> None:
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile=cert, keyfile=key)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((host, port))
        sock.listen(5)
        print(f"Secure server listening on {host}:{port}")

        with context.wrap_socket(sock, server_side=True) as tls_sock:
            conn, addr = tls_sock.accept()
            print(f"Accepted TLS connection from {addr}")
            with conn:
                conn.sendall(b"Welcome to the secure echo server.\n")
                while True:
                    data = conn.recv(4096)
                    if not data:
                        break
                    conn.sendall(b"Echo: " + data)
            print("Client disconnected")


def main() -> None:
    args = parse_args()
    run_server(args.host, args.port, args.cert, args.key)


if __name__ == "__main__":
    main()
