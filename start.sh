#!/usr/bin/bash
rm .env
echo 'TERMINAL_ID=1' >> .env
echo 'CP_ID=' >> .env
echo 'CP_PORT=' >> .env
echo 'CHANNEL_NAME=' >> .env
echo 'PLAIN_USER=' >> .env
echo 'PLAIN_PASS=' >> .env

sudo apt install -y python3-pip

pip install python-dotenv
pip install pika

python3 sender.py
