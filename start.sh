#!/usr/bin/bash
rm .env
echo 'TERMINAL_ID=1' >> .env
echo 'RABBIT_IP=' >> .env
echo 'RABBIT_PORT=' >> .env
echo 'RABBIT_VHOST=' >> .env
echo 'RABBIT_USER=' >> .env
echo 'RABBIT_PASS=' >> .env

sudo apt install -y python3-pip

pip install python-dotenv
pip install pika

