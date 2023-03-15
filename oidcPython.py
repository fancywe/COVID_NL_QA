#!/usr/bin/env python3
import requests
import sys
import socket

def main():

    RP_HOST=sys.argv[1]
    
    RP_PORT=sys.argv[2]
    host_url='http://'+RP_HOST+':'+str(RP_PORT)
    PROVIDER_HOST=sys.argv[3]
    PROVIDER_PORT=sys.argv[4]
    forward_url='http://'+PROVIDER_HOST+':'+str(PROVIDER_PORT)
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # http://127.0.0.1:1025/authorize?client_id=oidc&redirect_uri=http://127.0.0.1:1024/auth/callback&response_type=code&scope=openid&state=12345678
    soc.bind((RP_HOST, int(RP_PORT)))
    soc.listen(10)
    conn, addr = soc.accept()
    # response = requests.get(uri, auth=('oidc', 'app-secret'))
    response='HTTP/1.1 302 Found\r\nLocation:'+forward_url+'/authorize?client_id=oidc&redirect_uri='+host_url+'/auth/callback&response_type=code&scope=openid&state=12345678\r\nSet-Cookie: state=ABCDEFGH\r\nContent-Length: 0\r\n\r\n'
    conn.send(response.encode('utf-8'))




if __name__ == '__main__':
    main()
