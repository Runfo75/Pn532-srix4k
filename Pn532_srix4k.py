import serial
from serial import SerialException
def porta_com():
    global porta
    for i in range(0,20):
        porta1=('COM'+str(i))
        try:
            seriale = serial.Serial(porta1, 115200, timeout=0.05)
            seriale.write([85,85,0,0,0,0,0,255,3,253,212,20,1,23,0])
            response = seriale.readline()
            if len(response)==15:
                try:
                    seriale.write([85,85,0,0,0,0,0,255,3,253,212,20,1,23,0])
                    response = seriale.readline()
                    if len(response)==15:
                        porta=porta1
                        print('')
                        print('PN532 trovato su porta:',porta)
                        print('Leggo la chiave, aspetta')
                        print('')
                        return()
                except SerialException:
                    pass
        except SerialException:
            pass
    for i in range(0,9):
        porta1=('/dev/tty.usbserial-000'+str(i))
        try:
            seriale = serial.Serial(porta1, 115200, timeout=0.05)
            seriale.write([85,85,0,0,0,0,0,255,3,253,212,20,1,23,0])
            response = seriale.readline()
            if len(response)==15:
                try:
                    seriale.write([85,85,0,0,0,0,0,255,3,253,212,20,1,23,0])
                    response = seriale.readline()
                    if len(response)==15:
                        porta=porta1
                        return()
                except SerialException:
                    pass
        except SerialException:
            pass
    for i in range(0,9):
        porta1=('/dev/ttyUSB'+str(i))
        try:
            seriale = serial.Serial(porta1, 115200, timeout=0.05)
            seriale.write([85,85,0,0,0,0,0,255,3,253,212,20,1,23,0])
            response = seriale.readline()
            if len(response)==15:
                try:
                    seriale.write([85,85,0,0,0,0,0,255,3,253,212,20,1,23,0])
                    response = seriale.readline()
                    if len(response)==15:
                        porta=porta1
                        return()
                except SerialException:
                    pass
        except SerialException:
            pass
    print('Nessun PN532')
    porta=0
def leggi_chiave():
    global porta
    if porta==0:
        return()
    seriale = serial.Serial(porta, 115200, timeout=0.1)
    if seriale.is_open:
        pass
    else:
        print ("Collegamento non effettuato con successo")
        return()
    seriale.write([85,85,0,0,0,0,0,255,3,253,212,20,1,23,0])
    response = seriale.readline()
    if len(response)==15:
        pass
    else:
        print('Non funzionante')
        return()
    seriale.write([0,0,255,5,251,212,74,1,3,0,222,0])
    response = seriale.readline()
    if len(response)==6:
        pass
    else:
        print('Non funzionante')
        retunr()
    seriale.write([0,0,255,4,252,212,66,6,0,228,0])
    response = seriale.readline()
    seriale.write([0,0,255,4,252,212,66,6,0,228,0])
    response = seriale.readline()
    if len(response)==17:
        pass
    else:
        print('Non funzionante')
        return()
    a=response[14]
    b=768-(212+66+14+a)
    if b>511: b=b-512
    if b>255: b=b-256
    seriale.write([0,0,255,4,252,212,66,14,a,b,0])
    response = seriale.readline()
    if len(response)==17:
        pass
    else:
        print('Non funzionante')
        return()
    print('UID:')
    seriale.write([0,0,255,3,253,212,66,11,223,0])
    response = seriale.readline()
    if len(response)<24:
        response1 = seriale.readline() 
        response=response+response1  
    if len(response)<24:
        response1 = seriale.readline() 
        response=response+response1 
    if len(response)<24:
        response1 = seriale.readline() 
        response=response+response1           
    if len(response)==24:
        print(hex(response[21])[2:].zfill(2).upper()+hex(response[20])[2:].zfill(2).upper()+hex(response[19])[2:].zfill(2).upper()+hex(response[18])[2:].zfill(2).upper()+hex(response[17])[2:].zfill(2).upper()+hex(response[16])[2:].zfill(2).upper()+hex(response[15])[2:].zfill(2).upper()+hex(response[14])[2:].zfill(2).upper())
    else:
        print('Non funzionante')
        return()
    print('Stampa Stringhe:')
    for i in range(128):
        c=768-212-66-8-i
        if c>511: c=c-512
        if c>255: c=c-256
        seriale.write([0,0,255,4,252,212,66,8,i,c,0])
        response = seriale.readline()
        if len(response)<20:
            response1 = seriale.readline() 
            response=response+response1   
        if len(response)<20:
            response1 = seriale.readline() 
            response=response+response1  
        if len(response)<20:
            response1 = seriale.readline() 
            response=response+response1  
        if len(response)<20:
            response1 = seriale.readline() 
            response=response+response1  
        if len(response)<20:
            response1 = seriale.readline() 
            response=response+response1  
        if len(response)==20:
            print('Stringa',(str(i))+': ',hex(response[14])[2:].zfill(2).upper()+hex(response[15])[2:].zfill(2).upper()+hex(response[16])[2:].zfill(2).upper()+hex(response[17])[2:].zfill(2).upper())
        else:
            print('Non funzionante')
            return()    
    seriale.close()    
def scrivi_chiave(n_stringa_int,stringa_hex):
    global porta 
    stringa_hex=bytearray.fromhex(stringa_hex)
    seriale = serial.Serial(porta, 115200, timeout=5)
    if seriale.is_open:
        print ("\n Il collegamento è stato effettuato con successo  \n")
    else:
        print ("Collegamento non effettuato con successo")
        return()
    print('WAKEUP')
    seriale.write([85,85,0,0,0,0,0,255,3,253,212,20,1,23,0])
    response = seriale.readline()
    if len(response)==15:
        print('OK')
    else:
        print('Non funzionante')
        return()
    print('lettura TAG B')
    seriale.write([0,0,255,5,251,212,74,1,3,0,222,0])
    response = seriale.readline()
    if len(response)==6:
        print('OK')
    else:
        print('Non funzionante')
        return()
    print('apertura TAG Srix4k')
    seriale.write([0,0,255,4,252,212,66,6,0,228,0])
    response = seriale.readline()
    print('seconda apertura TAG Srix4k')
    seriale.write([0,0,255,4,252,212,66,6,0,228,0])
    response = seriale.readline()
    if len(response)==17:
        print('OK')
    else:
        print('Non funzionante')
        return()
    a=response[14]
    b=768-(212+66+14+a)
    if b>511: b=b-512
    if b>255: b=b-256
    print('invio comando al TAG')
    seriale.write([0,0,255,4,252,212,66,14,a,b,0])
    response = seriale.readline()
    if len(response)==17:
        print('OK')
    else:
        print('Non funzionante')
        return()
    print('Scrivo chiave')
    c=1536-(212+66+9+n_stringa_int+stringa_hex[0]+stringa_hex[1]+stringa_hex[2]+stringa_hex[3])
    if c>1279: c=c-1280    
    if c>1023: c=c-1024
    if c>767: c=c-768
    if c>511: c=c-512
    if c>255: c=c-256
    seriale.write([0,0,255,8,248,212,66,9,n_stringa_int,stringa_hex[0],stringa_hex[1],stringa_hex[2],stringa_hex[3],c,0])
    response = seriale.readline()
    if len(response)==16:
        print('OK')
    else:
        print('Non funzionante')
        return()
    print('WAKEUP')
    seriale.write([85,85,0,0,0,0,0,255,3,253,212,20,1,23,0])
    response = seriale.readline()
    if len(response)==15:
        print('OK')
    else:
        print('Non funzionante')
        return()
    print('lettura TAG B')
    seriale.write([0,0,255,5,251,212,74,1,3,0,222,0])
    response = seriale.readline()
    if len(response)==6:
        print('OK')
    else:
        print('Non funzionante')
        return()
    print('apertura TAG Srix4k')
    seriale.write([0,0,255,4,252,212,66,6,0,228,0])
    response = seriale.readline()
    print('seconda apertura TAG Srix4k')
    seriale.write([0,0,255,4,252,212,66,6,0,228,0])
    response = seriale.readline()
    if len(response)==17:
        print('OK')
    else:
        print('Non funzionante')
        return()
    a=response[14]
    b=768-(212+66+14+a)
    if b>511: b=b-512
    if b>255: b=b-256
    print('invio comando al TAG')
    seriale.write([0,0,255,4,252,212,66,14,a,b,0])
    response = seriale.readline()
    if len(response)==17:
        print('OK')
    else:
        print('Non funzionante')
        return()
    print('Stampa Stringhe:')
    d=768-212-66-8-n_stringa_int
    if d>511: d=d-512
    if d>255: d=d-256
    seriale.write([0,0,255,4,252,212,66,8,n_stringa_int,d,0])
    response = seriale.readline()
    if len(response)<20:
        response1 = seriale.readline() 
        response=response+response1 
    if len(response)<20:
        response1 = seriale.readline() 
        response=response+response1 
    if len(response)<20:
        response1 = seriale.readline() 
        response=response+response1    
    if len(response)<20:
        response1 = seriale.readline() 
        response=response+response1    
    if len(response)<20:
        response1 = seriale.readline() 
        response=response+response1     
    if len(response)==20:
        print('Stringa',(str(n_stringa_int))+': ',hex(response[14])[2:].zfill(2).upper()+hex(response[15])[2:].zfill(2).upper()+hex(response[16])[2:].zfill(2).upper()+hex(response[17])[2:].zfill(2).upper())
    else:
        print('Non funzionante')
        return()    
    seriale.close()   
a=3
while a>=1:
    print('')
    print('Premi 1 per leggere chiave')
    print('Premi 2 per scrivere blocco')
    print('premi 0 per uscire')
    a=input('Cosa vuoi fare ? ')
    a=int(a)
    if a==1: 
        porta_com()
        leggi_chiave()
    else:
        if a==2:
            print('')
            b=input('Indicare numero stringa in intero:')
            c=input('Indicare stringa da scrivere in HEX unito senza spazi (tipo FFFFFFFF):')
            porta_com()
            scrivi_chiave(int(b,10),c)
        
