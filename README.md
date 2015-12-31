# BlinkyTape Python Animation Sequences

Playing with BlinkyTape, an RGB LED strip with integrated USB controller, using a RaspberryPi and a Windows7 PC.

Code was borrowed wholesale from BlinkinLabs' [Python library and example for the BlinkyTape](https://github.com/Blinkinlabs/BlinkyTape_Python)

Based on [painful connection lessons learned](http://upthebuzzard.tumblr.com/post/136270814260/connecting-to-blinkytape-using-python-on-raspberry), BlinkyTape.py has been tweaked to (try and) auto-detect the port/device name via which BlinkyTape has been connected - encapsulated in private method _\_identify\_port.

Some simple animations have been created in sequences.py.