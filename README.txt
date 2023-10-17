# Django App
Hi! I'm Mauro Gación and this is my Django App!

* Para los hablantes en español, leer README-ESP.md

The porpuse of this project is to gather data from Twitch API in order to help my streamer brother, TokaSenseiGG, to make data-driven decisions.

### Twitch Endpoints
The first step was learning about Twitch API reading its documentation. There, I learned how to create an App in Twitch console and use its endpoints to get data like chatters in the broadcaster's session, subscriptions in the channel, the followers of the channel, the top games being played at the time, and so on.

### Google sheets
The original idea for this project was to use a cloud service like AWS and GCP to store the data in a data lake. But, in order to keep it free and simple, I decided to use google sheets.
So, I create a Google App in its console, get all the tokens and permissions to access to Google Drive and sheets, and then I was able to start coding.

### Django
I neeeded a free host, so I found [pythonanywhere](https://pythonanywhere.com). It even let me code right in its web. Here, I made a very simple Django app where its views.py use a GET HTTP method with this link: https://kurocorgi27.pythonanywhere.com/start.
Of course there is a token validation process to ensure my tokens are always ready to work.
Once you made a get method on that link, the app would use Twitch endpoints to gather some data. Then, I formatted that data and write it right into Google sheets, where I store them in my drive like a data lake.

I created a cron-job in this free web: [cron-job.org](https://cron-job.org/en/) where I made a GET method on the link above every five minutes. Now, data is collected automatically.

Data is private, I won't share my brother's info, but I can share to you the sheet of the top played games: [Get_Top_Games](https://docs.google.com/spreadsheets/d/1c8D_tLtjIdq3-4jjsQ__Dg_6LDAzko7hCJUZENALxaU/edit#gid=0)
