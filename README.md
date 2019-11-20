# SI7020 Temp Humidity Sensor Kernel Module [![Build Status](https://travis-ci.org/vondraussen/si7020-rpi-kernel-module.svg?branch=master)](https://travis-ci.org/vondraussen/si7020-rpi-kernel-module)
This repo will auto build the si7020.ko for the official Raspbian Kernel, as 
soon as a new tag is released on the [official repo](https://github.com/raspberrypi/linux).

[Latest release](https://github.com/vondraussen/si7020-rpi-kernel-module/releases)

## Installation
1. download the right archive for your device
2. `sudo tar xzvf si7020_module_rpi_2_3_3p_raspberrypi-kernel_1.20190925-1.tar.gz
 -C /lib/modules/4.19.66-v7+/kernel/`
3. `sudo depmod`
4. `sudo modprobe si7020`
5. optional to autoload the module on boot, add it to `/etc/modules`

# SI7020 Specific
The module alone will not probe for the device/sensor. In order to get the driver loaded and the device probed, you can create a systemd service.

## Autoload I2C Driver
Create a systemd service unit in /etc/systemd/system/si7020.service

``` bash
# /etc/systemd/system/si7020.service
[Unit]
Description=load si7020 i2c driver

[Service]
Type=oneshot
ExecStart=/bin/echo si7020 0x40 > /sys/bus/i2c/devices/i2c-1/new_device

[Install]
WantedBy=multi-user.target
```
To enable and start the service:
``` bash
sudo systemctl daemon-reload
sudo systemctl enable si7020
sudo systemctl start si7020
```
## Read SI7020 Values from the IIO sysfs interface
### Temperature
``` bash
cat /sys/module/si7020/drivers/i2c\:si7020/1-0040/iio\:device0/in_temp_raw
# 6052
cat /sys/module/si7020/drivers/i2c\:si7020/1-0040/iio\:device0/in_temp_offset
# -4368
cat /sys/module/si7020/drivers/i2c\:si7020/1-0040/iio\:device0/in_temp_scale
# 10.725097656

# calc the result
# (raw + offset) * scale
# we can use bc to calc that for us (example in Degree C)
echo "((6053-4368)*10.7251)/1000" | bc -l
# 18.07179350000000000000

# or as a one liner (could be saved as a script)
TEMP=$(cat /sys/module/si7020/drivers/i2c\:si7020/1-0040/iio\:device0/in_temp_raw) && \
OFF=$(cat /sys/module/si7020/drivers/i2c\:si7020/1-0040/iio\:device0/in_temp_offset) && \
SCALE=$(cat /sys/module/si7020/drivers/i2c\:si7020/1-0040/iio\:device0/in_temp_scale) && \
echo "(($TEMP + $OFF)*$SCALE)/1000" | bc -l
```

### Humidity
See temperature for details.
``` bash
HUMI=$(cat /sys/module/si7020/drivers/i2c\:si7020/1-0040/iio\:device0/in_humidityrelative_raw) && \
OFF=$(cat /sys/module/si7020/drivers/i2c\:si7020/1-0040/iio\:device0/in_humidityrelative_offset) && \
SCALE=$(cat /sys/module/si7020/drivers/i2c\:si7020/1-0040/iio\:device0/in_humidityrelative_scale) && \
echo "(($HUMI + $OFF)*$SCALE)/1000" | bc -l
```