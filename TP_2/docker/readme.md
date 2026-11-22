para armar el docker usamos:
docker build -t lluvia-australia-nn .

para correrlo:
docker run -d -p 8000:8000 --name api-lluvia lluvia-australia-nn

para usarlo, es via localhost con el browser:
http://localhost:8000/docs

Ejecuta una predicción de prueba en esa pantalla:
Verás un título que dice Predicción de Lluvias en Australia y debajo una barra verde que dice POST /predict.

Haz clic sobre esa barra verde para desplegarla.

Presiona el botón Try it out (arriba a la derecha del cuadro desplegado).

En el recuadro de texto Request body, borra lo que aparece y pega un diccionario JSON con datos meteorológicos, por ejemplo:

JSON
{
  "MinTemp": 13.4,
  "MaxTemp": 22.9,
  "Rainfall": 0.6,
  "Humidity3pm": 22.0,
  "Pressure3pm": 1007.1,
  "RainToday": 0
}


{
  "MinTemp": 14.0,
  "MaxTemp": 28.5,
  "Rainfall": 0.0,
  "Evaporation": 8.4,
  "Sunshine": 11.2,
  "WindGustSpeed": 28.0,
  "WindSpeed9am": 11.0,
  "WindSpeed3pm": 15.0,
  "Humidity9am": 45.0,
  "Humidity3pm": 24.0,
  "Pressure9am": 1024.5,
  "Pressure3pm": 1022.0,
  "Cloud9am": 1.0,
  "Cloud3pm": 1.0,
  "Temp9am": 19.5,
  "Temp3pm": 27.2,
  "RainToday": 0
}


Haz clic en el botón azul ancho que dice Execute.

Baja un poco la página hasta la sección Responses: si todo está bien, verás un código 200 y el resultado JSON con "RainTomorrow" y "probabilidad_lluvia".