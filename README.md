# telegram-bot

Uso
=====

* Editar el archivo variables.env con los valores para los tokens de TELEGRAM y GOOGLE STATIC MAPS.

* Ejecutar docker-compose up --build


Conflictos
=======

* De acuerdo a las limitaciones de la API de Google puede ocurrir que el static map con las localizaciones no se genere. Cuando eso ocurra el bot enviará un mensaje diciendo: `No se pudo cargar imagen con ubicación de los datos`.
