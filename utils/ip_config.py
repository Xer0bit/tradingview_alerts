import requests
import socket

def get_public_ip():
    hostname = socket.gethostname()
    return socket.gethostbyname(hostname)

def get_available_port(start_port=8000):
    return start_port  # You can implement port checking if needed
