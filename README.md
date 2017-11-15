# RPiDispenser
Dispensador de Doces Controlado por um Raspberry Pi Zero W

Para controle do servo é necessário que o deamon servoblaster esteja
rodando e configurado para usar o pino correto. Por exemplo

    sudo ./servod --p1pins=7 &
    python dispenser.py
  
Para usar o pino 7 do conector P1 (GPIO4).

servoblaster: <https://github.com/srcshelton/servoblaster>

Mais detalhes sobre o meu projeto: 
<http://dqsoft.blogspot.com.br/2017/11/raspberry-pi-zero-w-como-controlador.html>
