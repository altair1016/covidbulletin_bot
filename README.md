# covidbulletin_bot
Is Telegram bot project to get real-time informations about COVID propagation in Italy. 
Data source referenced is the following Official repo from Protezione Civile Italiana https://github.com/pcm-dpc/COVID-19

If you want to see how the bot is working try to open the telegram bot: (https://t.me/covidbulletin_bot).


# Current Instance
Current instance is running on Google Cloud Platform account on a Virtual instance made by 2cpus and 4gb ram with Linux Ubuntu 16.04 installed. 
# Create a new instance, your Instance
## All you need is...

Computer or server service where to host the python scripts.
Create a Telegram bot and get the Token id of your new born bot.
python3.7 intepreter with following modules installed: 

- json
- matplotlib
- urllib
- flask
- folium
- telepot
- selenium
- pyvirtualdisplay
- speech_recognition
- pydub

## Installation  

1. Run a `git clone https://github.com/Datalux/COVID19-it-bot` command or download files from my repo.
2. Creare un file `config.json` con la seguente struttura:
```
{
    "token": "110201543:AAHdqTcvCH1vGWJxfSeofSAs0K5PALDsaw",
    "channel" : "@my_channel_name"
}
```
3. Lanciare `python3 run.py`