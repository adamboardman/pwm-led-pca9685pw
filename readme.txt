
sudo apt-get install i2c-tools
sudo apt-get install python-smbus
sudo adduser <yourusername> i2c
i2cdetect -y 0

may use in future
sudo apt-get install python-rpi.gpio

Run indivdual tests:
python -m unittest pca9685pw_testpy.TestPCM.test_setColourCyan

