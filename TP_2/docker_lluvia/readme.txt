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
Haz clic en el botón azul ancho que dice Execute.

Baja un poco la página hasta la sección Responses: si todo está bien, verás un código 200 y el resultado JSON con "RainTomorrow" y "probabilidad_lluvia".