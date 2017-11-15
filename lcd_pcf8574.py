import smbus  
from time import sleep 

# Classe para simplificar o acesso ao I2C (so escrita)
class i2c_device:  
    
    # construtor
    def __init__(self, addr):  
        # salva o endereco
        self.addr = addr  
        
        # seleciona o i2c conforme a versao do Raspberry Pi
        self.revision = ([l[12:-1] for l in open('/proc/cpuinfo','r').readlines() if l[:8]=="Revision"]+['0000'])[0]
        self.bus = smbus.SMBus(1)

    # escreve um byte
    def write(self, byte):  
        self.bus.write_byte(self.addr, byte)  

# Classe para acesso ao LCD
class lcd_pcf8574:
    
    #construtor
    def __init__(self, addr=0x27, bitRS=0, bitRW=1, bitE=2, bitBL=3, bitD4=4, bitD5=5, bitD6=6, bitD7=7):
        # salva a configuracao
        self.mskRS = 1 << bitRS
        self.mskRW = 1 << bitRW
        self.mskE = 1 << bitE
        self.mskBL = 1 << bitBL
        self.mskD4 = 1 << bitD4
        self.mskD5 = 1 << bitD5
        self.mskD6 = 1 << bitD6
        self.mskD7 = 1 << bitD7
        
        # inicia o acesso ao PCF8574
        self.lcd_device = i2c_device(0x27)
        self.valorAtual = 0x00
        self.lcd_device.write(self.valorAtual);
        
        # constantes
        self.LOW = 0
        self.HIGH = 1
        self.CMD = self.LOW
        self.DADO = self.HIGH
        self.CMD_CLS = 0x01
        self.CMD_DISPON = 0x0C
        self.CMD_POSCUR = 0x80
        self.CMD_FUNCTIONSET = 0x20
        self.LCD_4BITMODE = 0x00
        self.LCD_2LINE = 0x08
        self.LCD_5x8DOTS = 0x00

    # controla sinal RS
    def setRS(self, valor):
        if valor == self.LOW:
            self.valorAtual = self.valorAtual & ~self.mskRS
        else:
            self.valorAtual = self.valorAtual | self.mskRS
        self.lcd_device.write(self.valorAtual)

    # controla sinal RW
    def setRW(self, valor):
        if valor == self.LOW:
            self.valorAtual = self.valorAtual & ~self.mskRW
        else:
            self.valorAtual = self.valorAtual | self.mskRW
        self.lcd_device.write(self.valorAtual)

    # controla sinal E (enable)
    def setE(self, valor):
        if valor == self.LOW:
            self.valorAtual = self.valorAtual & ~self.mskE
        else:
            self.valorAtual = self.valorAtual | self.mskE
        self.lcd_device.write(self.valorAtual)

    # controla backlight
    def setBL(self, valor):
        if valor == self.LOW:
            self.valorAtual = self.valorAtual & ~self.mskBL
        else:
            self.valorAtual = self.valorAtual | self.mskBL
        self.lcd_device.write(self.valorAtual)

    # controla os pinos de dados (D4 a D7)
    def setDado(self, nib):
        self.valorAtual = self.valorAtual & ~(self.mskD4 | self.mskD5 | self.mskD6 | self.mskD7)
        if (nib & 8) != 0:
            self.valorAtual = self.valorAtual | self.mskD7
        if (nib & 4) != 0:
            self.valorAtual = self.valorAtual | self.mskD6
        if (nib & 2) != 0:
            self.valorAtual = self.valorAtual | self.mskD5
        if (nib & 1) != 0:
            self.valorAtual = self.valorAtual | self.mskD4
        self.lcd_device.write(self.valorAtual)

    # envia um byte para o display
    def writeByte(self, rs, dado):
        self.setRS(rs)
        self.setE(self.HIGH)
        self.setDado (dado >> 4)
        self.setE(self.LOW)
        self.setE(self.HIGH)
        self.setDado (dado)
        self.setE(self.LOW)

    # envia um comando para o display
    def writeCmd(self, cmd):
        self.writeByte(self.CMD, cmd)

    # envia um caracter para o display
    def writeChar(self, chr):
        self.writeByte(self.DADO, chr)
    
    # inicia o display
    def init(self):
        # para o caso de ter acabado de ligar
        sleep(0.1)
        # vamos sempre fazer escrita
        self.setRW(self.LOW)
        # sequencia para garantir modo 4 bits
        self.writeCmd(0x03)
        sleep(0.005)
        self.writeCmd(0x03)
        sleep(0.001)
        self.writeCmd(0x03)
        sleep(0.001)
        self.writeCmd(0x02)
        sleep(0.001)
        # configura o display
        self.writeCmd(self.CMD_FUNCTIONSET | self.LCD_4BITMODE | self.LCD_2LINE | self.LCD_5x8DOTS);
        sleep(0.001)
        # limpa a tela e liga o display
        self.writeCmd(self.CMD_CLS)
        sleep(0.002)
        self.writeCmd(self.CMD_DISPON)

    # liga o backlight
    def backlightOn(self):
        self.setBL(self.HIGH)

    # desliga o backlight
    def backlightOff(self):
        self.setBL(self.LOW)

    # limpa a tela
    def clear(self):
        self.writeCmd(self.CMD_CLS)
        sleep(0.002)
    
    # escreve um texto no display
    def displayWrite(self, lin, col, texto):
        self.ender = col
        if lin == 1:
            self.ender = self.ender + 0x40
        self.writeCmd (self.CMD_POSCUR + self.ender)
        for chr in texto:
            self.writeChar(ord(chr))

# Teste simples
if __name__ == "__main__":
    lcd = lcd_pcf8574()
    lcd.init()
    lcd.backlightOn()
    lcd.displayWrite(0, 0, "DQSoft")
    lcd.displayWrite(1, 0, "Display I2C")

