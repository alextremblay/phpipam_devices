phpIPAM Devices
===============

This is a command-line tool for working with devices in phpIPAM.

It's under developemnt and can currently only retrieve devices, it can't yet create or update devices.

Install
-------

``git clone https://github.com/alextremblay/phpipam_devices``
``cd phpipam_devices``

``chmod u+x phpipam_dev/main.py``
``pip3 install -r requirements.txt``

Install (symlink) the app's entrypoint into your PATH
``link -s phpipam_dev/main.py /usr/bin/phpipam_dev``

Run the command once to go through first-time setup.
``phpipam_dev``

Use
---

``phpipam_dev get`` will print out a table of every device in your phpIPAM installation

``phpipam_dev get -c > devices.csv`` will create a CSV file of every device in your phpIPAM installation

``phpipam_dev get mgmt-`` will show you all devices in phpIPAM which have 'mgmt-' in the name/description/location

More to come soon! (hopefully)