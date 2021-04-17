# FranzininhoWiFi - CircuitPython - RFID
Este exemplo utiliza a interface serial assíncrona para receber mensagens de um
leitor RFID 125KHz. O leitor usado nos testes não é mais comercializado, mas
existem leitores com o mesmo protocolo.

Quando um tag é detectado, o leitor envia pela serial assíncrona (9600bps, 8N1)
a seguinte sequência:

* 0x02 (marca de início)
* a identificação da tag, no formato de 10 dígitos hexadecimais
* dois dígitos hexadecimais com o checksum
* 0x03 (marca de fim)

O checksum é o xor dos bytes da identificação. Uma vez que o xor de um valor
com ele mesmo é zero, a conferência pode ser feita fazendo um xor dos 8 bytes
da identificação com o byte de checksum; valor diferente de zero indica erro.

O leitor utilizado só envia uma vez a identificação do código de um tag, para
enviar novamente ele precisa ser afastado e reaproximado.

Para fins de demonstração, cada tag vai sendo associado a um LED na ordem em
que é lido.

Para montagem deste projeto é necessário:

* LEDs - podem ser LEDs avulsos ou um _display de 10 segmentos bargraph_
(conjunto com 10 LEDs em um encapsulamento DIP)
* Um resistor de 220 ohms para cada LED
* Módulo RFID e tags
* Protoboard e fios

