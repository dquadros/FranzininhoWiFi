# FranzininhoWiFi - CircuitPython - MP3 Serial
Este exemplo utiliza a interface serial assíncrona para controlar um módulo MP3
DFPlayer Mini e tocar sequencialmente dois arquivos MP3. Detalhes sobre este módulo 
podem ser vistos [neste blog](http://dqsoft.blogspot.com/2018/09/modulo-mp3-dfplayer-mini.html)

O datasheet do módulo pode ser baixado (em PDF) do 
[github do fabricante](https://github.com/DFRobot/DFRobotDFPlayerMini/blob/master/doc/FN-M16P%2BEmbedded%2BMP3%2BAudio%2BModule%2BDatasheet.pdf)

Por simplificação não são tratadas as respostas do módulo, o sinal de ocupado
(*Busy*) é usado para detectar quando o módulo encerrou de tocar um arquivo. 
Portanto é testada somente a transmissão pela UART.

Para montagem deste projeto é necessário:

* Módulo MP3 DFPlayer Mini
* Um cartão micro SD contendo arquivos 0001.mp3 e 0002.mp3 no diretório /mp3
* Alto falante de 4 ou 8 ohms
* Protoboard e fios

