bin/bash

ngrok http 80 --log=stdout > /tmp/ngrok.log &
sleep 3
cat /tmp/ngrok.log