Para armar el docker usamos:
docker build -t lluvia-australia-nn .

Para correrlo:
docker run -d -p 8000:8000 --name api-lluvia lluvia-australia-nn

Para usarlo, es via localhost con el browser:
http://localhost:8000/docs

Ejecutar una predicción de prueba en esa pantalla:
Se puede observar un título que dice Predicción de Lluvias en Australia y debajo una barra verde que dice POST /predict.
Hacer clic sobre esa barra verde para desplegarla.
Presionar el botón Try it out (arriba a la derecha del cuadro desplegado).
En el recuadro de texto Request body, borrar lo que aparece y pegar un diccionario JSON con datos meteorológicos, por ejemplo:

a) con lluvia:
JSON
{
  "MinTemp": 16.5,
  "MaxTemp": 20.2,
  "Rainfall": 18.4,
  "Evaporation": 2.0,
  "Sunshine": 0.5,
  "WindGustSpeed": 65.0,
  "WindSpeed9am": 24.0,
  "WindSpeed3pm": 30.0,
  "Humidity9am": 92.0,
  "Humidity3pm": 89.0,
  "Pressure9am": 1004.2,
  "Pressure3pm": 1001.5,
  "Cloud9am": 8.0,
  "Cloud3pm": 8.0,
  "Temp9am": 17.8,
  "Temp3pm": 18.5,
  "RainToday": 1
}

b)sin lluvia:

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

Hacer clic en el botón azul ancho que dice Execute.

Abajo en la página, en la sección Responses: si todo está bien, verás un código 200 y el resultado JSON con "RainTomorrow" y "probabilidad_lluvia".

Aclaracion, si necesitamos borrar el docker y armar uno nuevo, hacer lo siguiente:
docker rm -f api-lluvia
docker build -t lluvia-australia-nn .
docker run -d -p 8000:8000 --name api-lluvia lluvia-australia-nn