Install this folder in /home/pi


To install packages, run:
```
$ pip install -r requirements.txt
```


To run automatically, in a new terminal, run:
```
sudo crontab -e
```
and type this at the end of the file:
```
@reboot python3 /home/pi/IoT/Water_Delivery_System/water_delivery_system.py

```
