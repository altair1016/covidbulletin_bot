# covidbulletin_bot
Is Telegram bot project to get real-time informations about COVID propagation in Italy. 
Data source referenced is the following Official repo from Protezione Civile Italiana https://github.com/pcm-dpc/COVID-19

If you want to see how the bot is working try to open the telegram bot: (https://t.me/covidbulletin_bot).


# Current Instance
Current instance is running on Google Cloud Platform account on a Virtual instance made by 2cpus and 4gb ram with Linux Ubuntu 16.04 installed. 
# Create a new instance, your Instance
## All you need is...

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

1. Eseguire `git clone https://github.com/Datalux/COVID19-it-bot` o scaricare il .zip della repository
2. Creare un file `config.json` con la seguente struttura:
```
{
    "token": "110201543:AAHdqTcvCH1vGWJxfSeofSAs0K5PALDsaw",
    "channel" : "@my_channel_name"
}
```
3. Lanciare `python3 run.py`