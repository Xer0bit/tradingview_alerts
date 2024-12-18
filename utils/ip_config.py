import requests
import socket

def get_public_ip():
    hostname = '139.59.121.41'
    return socket.gethostbyname(hostname)

def get_available_port(start_port=80):
    return start_port  # You can implement port checking if needed
