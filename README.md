Air-Con Control with Temperature & Humidity Monitoring:

Code Summary:<br>
1.) IR_receive.py: CircuitPython code to receive any remote control button signal and print it. While running the code, aim remote control at the IR receiver and press the button. <br>
2.) control_AC.py: CircuitPython code used for running the Air-Con control with temperature and humidity monitoring. Note that CIRCUITPY_PYSTACK_SIZE may have to be increased in settings.toml to prevent "Pystack exhausted" errors. 

Key Hardware Components:<br>
1.) Raspberry Pi Pico W<br>
2.) DHT 11 sensor<br>
3.) IR receiver<br>
4.) IR transmitter

Other requirements:<br>
An Adafruit IO account is required. Create 4 feeds, temperature feed, humidity feed, on control feed and off control feed. Create a dashboard with gauges for the temperature and humidity feeds and momentary button for the on and off control feeds.

