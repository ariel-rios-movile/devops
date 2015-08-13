========
 DevOps
========

DevOps tools in Python & other herbs.

Requirements for Python tools
=============================

.. code-block:: bash

   ~/devops$ sudo apt install python-pip
   ~/devops$ sudo pip install virtualenv
   ~/devops$ virtualenv env
   ~/devops$ source env/bin/activate
   (env) ~/devops$ pip install -r requirements.txt

edm.py
======

ExternalDataMapper remote manager (currently it only restarts it :P). Currently
it has configured buenosaires01 & buenosaires02 as backend containers. Maybe
you need to change then in order to use it properl. Don't forget to change
related variable names ;)

How to use it
-------------

.. code-block:: bash

   ~/devops$ export BUENOSAIRES01_MANAGER_USER <user>
   ~/devops$ export BUENOSAIRES01_MANAGER_PASSWORD <password>
   ~/devops$ export BUENOSAIRES02_MANAGER_USER <user>
   ~/devops$ export BUENOSAIRES02_MANAGER_PASSWORD <password>
   ~/devops$ python edm.py  # check for logger output about progress
