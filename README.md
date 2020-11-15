# amazon-bot
A simple Amazon price tracking bot.

## Brief description of the code
This Telegram bot checks if the price of a given Amazon item is below a given threshold value, both the url and the limit value are provided by a csv file.
The modules you have to import are:
* [Pandas](https://pandas.pydata.org/) - to manage the csv file
* [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) - to scrap Amazon website
* [Telegram API](https://python-telegram-bot.readthedocs.io/en/stable/index.html) - of course, this is a Telegram Bot
Scheduling of the searching jobs are managed by 'Telegram.ext.job_queue'(https://python-telegram-bot.readthedocs.io/en/stable/telegram.ext.jobqueue.html) class, in this way you can avoid a 'while True' loop that will prevent to send new commands to the Bot.

## Links that I found useful
[Job_queue](https://stackoverflow.com/questions/52556939/how-to-use-jobqueue-in-python-telegram-bot)
[BS4 tutorial](https://www.youtube.com/watch?v=dQw4w9WgXcQ)
