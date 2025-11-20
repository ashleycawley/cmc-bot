# cmc-bot (Cornwall Meshtastic Community Discord Bot)
A python command line script to receive messages from Meshtastic and then publish those to a Discord server channel. Run either the <b>'cmc-bot-serial.py'</b> script OR the <b>'cmc-bot-tcp.py'</b> script, and it will connect to your radio (via either Serial or TCP) and display any text messages received by your node, on any channel, including private/direct messages and will then publish those to a Discord server channel of your choosing.

Script is confirmed to work on Windows and Linux (and possibly other OSs).

I built this because this functionality is not available using the Meshtastic CLI (as of time of publishing).

# Installation
* git clone https://github.com/ashleycawley/cmc-bot.git
* cd cmc-bot
* pip3 install -r requirements.txt

# Usage
* Firstly, decide if you will be connecting to your node via serial or via TCP. If using serial, edit <b>'cmc-bot-serial.py'</b> and set the serial port for your Meshtastic node (usually /dev/ttyUSB0 or /dev/ttyACM0 on Linux, or COM<u><i>x</i></u> on Windows). If using TCP, edit <b>'cmc-bot-tcp.py'</b> and set the IP address of your Meshtastic node.
* Configure your Discord Server Channel that you wish to publish to, [obtain the Webhook](https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks) you will need from Discord, once you have that Webhook URL modify the code replacing "YOUR_DISCORD_WEBHOOK_URL_HERE" with your Webhook URL.
* Then to run the script:
* For Serial: python cmc-bot-serial.py
* For TCP: python cmc-bot-tcp.py

* To exit, use Ctrl-C

# Credit
* To [brad28b](https://github.com/brad28b) for the original project at [https://github.com/brad28b/meshtastic-cli-receive-text](https://github.com/brad28b/meshtastic-cli-receive-text) which gave me the basis to build this Discord bot, thank you.
