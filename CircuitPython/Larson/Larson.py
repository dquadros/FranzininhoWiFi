# Acende sequencialmente LEDs até que um botão seja apertado

import board
import digitalio
import time

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

# Pino usado para o botão
# Neste pino deve ser ligado um botão de contato momentâneo, a outra
# ponta do botão deve ser ligada a GND
# Valem as mesmas restrições que para os LEDs, exceto que IO46 pode ser usado
pinoBotao = board.IO15

botao = digitalio.DigitalInOut(pinoBotao)
botao.direction = digitalio.Direction.INPUT
botao.pull = digitalio.Pull.UP

# Laço principal
while botao.value:
    for led in leds:
        led.value = True
        time.sleep(0.1)
        led.value = False
    leds.reverse()
