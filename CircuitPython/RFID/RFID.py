import board
import digitalio
import busio
import time
import binascii

# Classe para tratar o leitor TFID
class RFID(object):
    
    # construtor
    def __init__(self):
        self.uart = busio.UART(board.TX, board.RX, baudrate=9600)
    
    # decodifica um digito hexa
    def decodhex(self, data):
        if (data >= 0x61) and (data <= 0x66):
            return data - 0x61 + 10
        if (data >= 0x41) and (data <= 0x66):
            return data - 0x41 + 10
        if (data >= 0x30) and (data <= 0x39):
            return data - 0x30
        return 0
    
    # lê o próximo tag
    # mensagem do leitor: 0x02 [id = 10 dígitos hexa] [checksum = 2 dígitos hexa] 0x03
    def read(self):
        tag = bytearray(5)
        pos = 0
        while True:
            if self.uart.in_waiting > 0:
                d = self.uart.read(1)
                data = d[0]
                print (str(pos) + ": " + hex(data))
                if data == 0x02:
                    # inicio da identificação
                    pos = 1
                elif data == 0x03:
                    # fim da identificação
                    if pos == 13:
                        # leu corretamente um tag
                        return tag
                    else:
                        # ignora tag parcial ou incorreto
                        pos = 0
                else:
                    if (pos > 0) and (pos < 11):
                        # dígito hexa da identificação
                        ind = (pos-1) // 2
                        tag[ind] = ((tag[ind] << 4) + self.decodhex(data)) & 0xFF
                        pos = pos+1
                    elif pos == 11:
                        # primeiro dígito hexa do checksum
                        check = self.decodhex(data)
                        pos = pos+1
                    elif pos == 12:
                        # segundo dígito hexa do checksum
                        check = (check << 4) + self.decodhex(data)
                        for data in tag:
                            check = check ^ data
                        if check == 0:
                            # checksum ok, aguardar final
                            pos = pos + 1
                        else:
                            # checksum errado, aguardar nova mensagem
                            pos = 0


# Método auxiliar para configurar um pino ligado a LED
def initLED(io):
    led = digitalio.DigitalInOut(io)
    led.direction = digitalio.Direction.OUTPUT
    led.value = False
    return led

# Lista dos pinos onde estão ligados os anodos (+) dos LEDs. Os catodos (-) dos LEDs
# devem ser ligados a um resitor de 220 ohms com a outra ponta ligada em GND
#
# Não usar: IO0, IO45 (Strapping Pins)
#           IO19, IO20 (USB)
#           IO26 (CS PSRAM no WOOVER)
#           IO43, IO44 (Serial0)
#           IO46 (só Input)
ios = [ board.IO1, board.IO2, board.IO3, board.IO4, board.IO5, 
        board.IO6, board.IO7, board.IO10, board.IO11, board.IO12 ] 

leds = [initLED(io) for io in ios]

# Programa principal
tags = {}  # tags já lidos e os leds correspondentes
pos = 0    # ultimo tag reconhecido
rfid = RFID()
while True:
    # Aguarda ler um tag
    tag = binascii.hexlify(rfid.read())
    print (tag)
    # Apaga o LED que estava aceso
    leds[pos].value = False
    # Verifica se o tag é conhecido
    pos = tags.get(tag)
    print(pos)
    if pos is None:
        # tag novo, memoriza se tiver LED disponível
        ntags = len(tags)
        if ntags < len(leds):
            tags[tag] = ntags
            pos = ntags
    # Acende o LED correspondente ao tag (se tiver)
    if not pos is None:
        leds[pos].value = True
