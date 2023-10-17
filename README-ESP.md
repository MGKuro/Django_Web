# Django App
¡Hola! ¡Soy Mauro Gación y esta es mi Django App!

El propósito de esta App es obtener data para ayudar a mi hermano streamer, TokaSenseiGG, a realizar decisiones basadas en datos.

### Twitch Endpoints
El primer paso fue aprender sobre el API de Twitch tras leer su documentación. Allí, aprendí a crear una App en la consola de Twitch y usar sus endpoints para obtener datos como quién se encuentra en el chat, los subscriptores, seguidores, los juegos más jugados en el momento, etc.

### Google sheets
La idea original del projecto era usar servicios cloud como AWS y GCP para guardar los datos en data lakes. Pero, para mantenerlo simple y gratis, decidí usar google sheets.
He creado una Google App en su consola, obtuve todos los tokens y permisos para acceder a Google Drive y sus sheets, y solo luego de esto ya estaba listo para programar.

### Django
Necesitaba un host gratis, entonces hallé [pythonanywhere](https://pythonanywhere.com). Esta web me permite incluso programar directamente en sus servidores. Aquí, realicé una muy simple aplicación con Django en donde su views.py usa un método HTTP GET HTTP con este link: https://kurocorgi27.pythonanywhere.com/start.
Por supuesto, hay un proceso de validación de tokens para asegurarme que siempre estén listos para realizar el trabajo.
Una vez el método GET es realizado, la aplicación utilizará los endpoints de Twitch para obtener algo de datos. Entonces, formateo esos datos y los escribo directamente en Google sheets, donde los guardo en una especie de data lake.

He creado un cron-job en este sitio web gratis: [cron-job.org](https://cron-job.org/en/) Aquí realizo el método GET cada 5 minutos. Actualmente, los datos son generados automáticamente.

Los datos son privados, no compartiré la información de mi hermano, pero puedo compartir la planilla de los juegos más jugados: [Get_Top_Games](https://docs.google.com/spreadsheets/d/1c8D_tLtjIdq3-4jjsQ__Dg_6LDAzko7hCJUZENALxaU/edit#gid=0)
