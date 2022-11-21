import re
import os
import ipaddress
import getpass
import requests
import json
import threading
import time

def ssh_test():
    debug_log = ''
    url = "https://x.x.x.x:p/restconf/data/Cisco-IOS-XE-native:native/line/vty"

    payload={}

    headers = {
        'Content-type': 'application/yang-data+json ',
        'Accept': 'application/yang-data+json'
    }

    #Primer GET
    basic = requests.auth.HTTPBasicAuth('admin', 'hackathon')
    response = requests.get(url, headers=headers, auth=basic, verify=False, data=payload)
    print(response.json())

    #ssh = response.json()['Cisco-IOS-XE-native:vty'][0]['transport']['input']['input']
    ssh = response.json()['Cisco-IOS-XE-native:vty'][0]['transport']['input']
    print(ssh)
    debug_log += str(ssh) + '\n'

    if "none" in ssh:
        debug_log += 'VTY TRANSPORT en NONE, habilitando SSH\n'
        #{u'Cisco-IOS-XE-native:vty': [{u'length': 0, u'last': 4, u'login': {u'local': [None]}, u'transport': {u'input': {u'none': [None]}}, u'first': 0}, {u'login': {u'local': [None]}, u'last': 15, u'transport': {u'input': {u'none': [None]}}, u'first': 5}]}
        payload ='''{
       "Cisco-IOS-XE-native:vty":[
          {
             "length":0,
             "last":4,
             "login":{
                "local":[
                   ""
                ]
             },
             "transport":{
                "input":{
                   "input": [
                      "ssh"
                   ]
                }
             },
             "first":0
          },
          {
             "login":{
                "local":[
                   ""
                ]
             },
             "last":15,
             "transport":{
                "input":{
                   "none":[
                      ""
                   ]
                }
             },
             "first":5
          }
       ]
    }'''
        response = requests.patch(url, headers=headers, auth=basic, verify=False, data=payload)
        print(response)
    elif "telnet" in ssh['input']:
        debug_log += 'VTY TRANSPORT con TELNET, borrando TELNET\n'
        payload ='''{
       "Cisco-IOS-XE-native:vty":[
          {
             "length":0,
             "last":4,
             "login":{
                "local":[
                   ""
                ]
             },
             "transport":{
                "input":{
                   "none": [
                      ""
                   ]
                }
             },
             "first":0
          },
          {
             "login":{
                "local":[
                   ""
                ]
             },
             "last":15,
             "transport":{
                "input":{
                   "none":[
                      ""
                   ]
                }
             },
             "first":5
          }
       ]
    }'''
        response = requests.patch(url, headers=headers, auth=basic, verify=False, data=payload)
        print(response)

        payload ='''{
       "Cisco-IOS-XE-native:vty":[
          {
             "length":0,
             "last":4,
             "login":{
                "local":[
                   ""
                ]
             },
             "transport":{
                "input":{
                   "input": [
                      "ssh"
                   ]
                }
             },
             "first":0
          },
          {
             "login":{
                "local":[
                   ""
                ]
             },
             "last":15,
             "transport":{
                "input":{
                   "none":[
                      ""
                   ]
                }
             },
             "first":5
          }
       ]
    }'''
        debug_log += 'VTY TRANSPORT habilitando SSH\n'
        response = requests.patch(url, headers=headers, auth=basic, verify=False, data=payload)
        print(response)
    else:
        debug_log += 'SSH OK!\n'
    with open("output/log/HT22.log", "a") as outfile:
        outfile.write(debug_log)

def opcion1():
    '''Ingresar direccion IP y ejecutar ping. (Utilizar unicamente Expresiones Regulares para la validacion de IP)'''
    print("OPCION 1")
    ip = input("Ingresar direccion IP:\n")
    ipRegex = r"\d+.\d+.\d+.\d+"
    if re.match(ipRegex, ip):
        print("Ejecutando ping a la dirección "+ip+" ...")
        ipaddr = ipaddress.ip_address(ip)
        response = os.system("ping -c 1 " + str(ipaddr) + ">/dev/null 2>&1")
        if response == 0:
            print(ip+" esta UP!!")
        else:
            print(ip+" esta DOWN!!")
    else:
        print("Dirección IP inválida")

def opcion2():
    '''Remediacion continua. (Integrar la Posta 1, interrumpiendo la remedicacion continua presionando la tecla 'q')'''
    print("OPCION 2")
    WAIT_SECONDS = 15
    ticker = threading.Event()
    while not ticker.wait(WAIT_SECONDS):
        ssh_test()
        q = input(">")
        if q == 'q':
            break


def opcion3():
    '''Estadisticas. (Enviar correo electronico a automation@la.logicalis.com enviando cuantas veces se ejecuto cada opcion)'''
    global cont_opc1
    global cont_opc2
    global cont_opc3
    global cont_opc0
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    mail_content = "Estadísticas:\n\tOpcion 1: "+str(cont_opc1)+" veces/times\n\tOpcion 2: "+str(cont_opc2)+" veces/times\n\tOpcion 3: "+str(cont_opc3)+" veces/times\n\tOpcion 0: "+str(cont_opc0)+" veces/times"
    #The mail addresses and password
    sender_address = 'someOther@mail.com'
    sender_pass = 'pass'
    receiver_address = 'some@mail.com'
    #Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'subject'   #The subject line
    #The body and the attachments for the mail
    message.attach(MIMEText(mail_content, 'plain'))
    #Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.office365.com', 587) 
    session.starttls() #enable security
    session.login(sender_address, sender_pass) #login with mail_id and password
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    print('Mail Sent')

    #stats = "Estadísticas:\n\tOpcion 1: "+str(cont_opc1)+" veces/times\n\tOpcion 2: "+str(cont_opc2)+" veces/times\n\tOpcion 3: "+str(cont_opc3)+" veces/times\n\tOpcion 0: "+str(cont_opc0)+" veces/times"
    print(mail_content)


def opcion0():
    '''Salir'''
    print("SALIENDO...")

def mainMenu():
    opciones = {
        '1': ('Ingresar direccion IP y ejecutar ping.', opcion1),
        '2': ('Remediacion continua.', opcion2),
        '3': ('Estadisticas.', opcion3),
        '0': ('Salir/Exit', opcion0)
    }
    createMenu(opciones, '0')

def createMenu(opciones, opcion_salida):
    opcion = None
    global cont_opc1
    global cont_opc2
    global cont_opc3
    global cont_opc0
    while opcion != opcion_salida:
        mostrar_menu(opciones)
        opcion = leer_opcion(opciones)
        if int(opcion) == 1:
            cont_opc1 += 1
        elif int(opcion) == 2:
            cont_opc2 += 1
        elif int(opcion) == 3:
            cont_opc3 += 1
        elif int(opcion) == 0:
            cont_opc0 += 1
        ejecutar_opcion(opcion, opciones)
        print()

def mostrar_menu(opciones):
    print('')
    print('#####################')
    print('##### MAIN #####')
    print('#####################')
    print('#####  MENU  #####')
    print('#####################')
    print('')
    for clave in sorted(opciones):
        print(f'Opcion {clave}: {opciones[clave][0]}')

def leer_opcion(opciones):
    a = input('Opcion: ')
    while a not in opciones:
        a = input('Opcion: ')
        print('Opcion incorrecta')
    return a

def ejecutar_opcion(opcion, opciones):
    opciones[opcion][1]()

cont_opc1 = 0
cont_opc2 = 0
cont_opc3 = 0
cont_opc0 = 0

if __name__ == '__main__':
    mainMenu()

