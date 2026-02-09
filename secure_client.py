#!/usr/bin/env python3
"""Secure communication client using TLS."""
from __future__ import annotations

import argparse
import socket
import ssl


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="TLS-secured client")
    parser.add_argument("--host", default="127.0.0.1", help="Server host")
    parser.add_argument("--port", type=int, default=8443, help="Server port")
    parser.add_argument(
        "--ca",
        default="server.crt",
        help="CA or server certificate to trust (PEM)",
    )
    parser.add_argument(
        "--insecure",
        action="store_true",
        help="Disable certificate verification (not recommended)",
    )
    return parser.parse_args()


def run_client(host: str, port: int, ca: str, insecure: bool) -> None:
    if insecure:
        context = ssl._create_unverified_context()
    else:
        context = ssl.create_default_context(cafile=ca)

    with socket.create_connection((host, port)) as sock:
        with context.wrap_socket(sock, server_hostname=host) as tls_sock:
            banner = tls_sock.recv(4096)
            if banner:
                print(banner.decode("utf-8").rstrip())
            print("Type messages, or press Ctrl+D to quit.")
            try:
                while True:
                    line = input("> ")
                    tls_sock.sendall(line.encode("utf-8") + b"\n")
                    response = tls_sock.recv(4096)
                    if not response:
                        break
                    print(response.decode("utf-8").rstrip())
            except EOFError:
                print("\nClosing connection.")


def main() -> None:
    args = parse_args()
    run_client(args.host, args.port, args.ca, args.insecure)


if __name__ == "__main__":
    main()
