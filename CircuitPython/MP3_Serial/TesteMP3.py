# Toca sequencialmente dois arquivos MP3, utilizando um módulo
# MP3 DFPlayer Mini

# As conexões a serem feitas no módulo MP3 são:
#
# pino 1 - pino 5V do Franzininho WiFi           +--------------------------+
# pino 2 - pino TX do Franzininho WiFi           ! 16 15 14 13 12 11 10  9  |
# pino 6 - alto falante                          |                          |
# pino 8 - alto falante                          )                      SD  |
# pino 10 - pino GND do Franzininho WiFi         |                          |
# pino 16 - pino 42 do Franzininho WiFi          |  1  2  3  4  5  6  7  8  |
#                                                +--------------------------+

import board
import digitalio
import busio
import time

# Classe para interface com o tocador MP3
class MP3(object):

    # envia comando ao modulo
    def enviaCmd(self, cmd, param):
        # coloca comando e param no buffer
        self.bufCmd[3] = cmd
        self.bufCmd[5] = param >> 8
        self.bufCmd[6] = param & 0xFF
        # calcula o checksum e coloca no buffer
        check = 0
        for i in range(1, 7):
            check = check + self.bufCmd[i]
        check = -check
        self.bufCmd[7] = (check >> 8) & 0xFF
        self.bufCmd[8] = check & 0xFF
        # transmite o buffer para o modulo
        self.uart.write (self.bufCmd)

    # construtor
    def __init__(self, ioBusy):
        self.uart = busio.UART(board.TX, board.RX, baudrate=9600)
        self.pinBusy = digitalio.DigitalInOut(ioBusy)
        self.pinBusy.direction = digitalio.Direction.INPUT
        self.bufCmd = bytearray(10)
        self.bufCmd[0] = 0x7E  # marca do inicio
        self.bufCmd[1] = 0xFF  # versao do protocolo
        self.bufCmd[2] = 6     # tamanho dos dados
        self.bufCmd[4] = 0     # nao queremos resposta
        self.bufCmd[9] = 0xEF  # marca do fim

    # inicia o modulo
    def init(self):
        self.enviaCmd(0x06, 30)   # volume
        time.sleep(0.1)
        self.enviaCmd(0x07, 1)    # equalizacao pop
        time.sleep(0.1)
        
    # inicia uma faixa
    def toca(self, faixa):
        self.enviaCmd (0x12, faixa)
        # aguarda comecar a tocar
        timeout = time.monotonic()+3.0
        while self.pinBusy.value and (time.monotonic() < timeout):
            time.sleep(0.01)
            
    # espera terminar de tocar
    def espera(self):
        while not self.pinBusy.value:
            time.sleep(0.01)

# Importante: o 'print' envia dados para a serial emulada pela USB
#             busio.UART dá acesso à UART nativa da Franzininho

print('Iniciando')
mp3 = MP3 (board.IO42)
mp3.init()
print('Iniciado')
mp3.toca(1)
print('Tocando 1')
mp3.espera()
print('Acabou 1')
mp3.toca(2)
print('Tocando 2')
mp3.espera()
print('Acabou 2')
print ('Fim')
