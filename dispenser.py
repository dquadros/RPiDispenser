# Candy Dispenser
# Daniel Quadros nov/17
# https://dqsoft.blogspot.com

from time import sleep
import sys
import imaplib
import email
import lcd_pcf8574

# Controle do dispensador

def servo(pos):
    try:
        with open('/dev/servoblaster', 'a') as sb:
            sb.write('0='+str(pos)+'\n')
    except:
        print 'servoblaster error'

def fecha():
    print
    print 'Fecha'
    servo(70)
    sleep(1)
    servo(0)

def abre():
    print
    print 'Abre'
    servo(180)
    sleep(1)
    servo(0)

def libera():
    print
    print 'Libera'
    servo(240)
    sleep (0.3)
    servo(110)
    sleep (0.3)
    servo(180)
    sleep (0.3)
    servo(70)
    sleep (0.3)
    servo(0)

# Email
def le_email():
    assunto = ''
    remetente = ''
    try:
        mail = imaplib.IMAP4_SSL('servidor.email.com')
        mail.login("usuario", "senhasecreta")
        mail.select("inbox")
        result, data = mail.uid('search', None, '(ALL UNSEEN)')
        if result == 'OK':
            uids = data[0].split()
            if len(uids) > 0:
                result, data = mail.uid('fetch', uids[0], '(BODY[HEADER])')
                if result == 'OK':
                    msg = email.message_from_string(data[0][1])
                    remetente = email.utils.parseaddr(msg['From'])[1]
                    assunto = msg['Subject']
                    print
                    print remetente + ' -> ' + assunto
        mail.close()
        mail.logout()
    except:
        assunto = ''
    return (assunto, remetente)


# Iniciacao
resp = " GRANXBDCQPESJFZOUHVILYWTMK"
lcd = lcd_pcf8574.lcd_pcf8574()
lcd.init()
lcd.backlightOn()
lcd.displayWrite(0, 0, "Baleiro Garoa")

fecha()

# Loop principal
try:
    while True:
        sleep(10)
        
        lcd.clear()
        lcd.displayWrite(0, 0, "Baleiro Garoa")

        assunto, remetente = le_email()

        if assunto != "":
            lcd.clear()
            lcd.displayWrite(0, 0, remetente)
            if assunto[0:4] == "ABRE":
                abre()
            elif assunto[0:5] == "FECHA":
                fecha()
            elif len(assunto) > 3 and assunto[2] == ':':
                ab = assunto[0:2]
                c = assunto[3].upper()
                if ab.isdigit() and c.isalpha():
                    q = int(ab)
                    if q > 0 and q <= 26:
                        if resp[q] == ' ':
                            lcd.displayWrite(1, 0, "Ja respondida")
                        elif resp[q] != c:
                            lcd.displayWrite(1, 0, "Errado")
                        else:
                            lcd.displayWrite(1, 0, "ACERTOU!")
                            resp = resp[0:q] + ' ' + resp[q+1:]
                            libera()

except KeyboardInterrupt:
    sys.exit(0)
