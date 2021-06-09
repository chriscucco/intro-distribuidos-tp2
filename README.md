## Introducción a los Sistemas Distribuidos (75.43/75.33/95.60) - UPD File Transfer

Esta es una aplicación cliente-servidor que permite subir y descargar archivos desde un cliente a un servdor usando el protocolo UDP y la librería estándar Socket de Python.
La comunicación funciona a partir del protocolo Stop-And-Wait.

### Autores
- Ramiro Santos
- Guido Negri
- Christian Cucco

### Requerimientos: 
- Python 3 


### Utilización

#### Server
Para correr el server se debe ejecutar el siguiente comando en la carpeta root/src:
` python3 start-server.py [-h] [-v | -q] [-H ADDR] [-p PORT] [-s DIRPATH] [-lr LOSSRATE] `

Ejemplo:
` python3 start-server.py -H 127.0.0.1 -p 8090 -v -s lib/ -lr 0.5`

Con -p se indica el puerto donde correrá el server y con -H la dirección IP del host. En caso de no ingresar estos parámetros, por defecto la dirección será 127.0.0.1 (localhost) y el puerto 8090.

Con -v se indica si se quiere información extra en los logs, y con -q si se quiere menos. En caso de poner los dos parámetros se tomará el -v.

Con -s se indica el path donde el servidor almacenará los archivos que reciba y luego mande a los respectivos clientes (no debe comenzar con el caracter '-'). En caso de no indicarse el path por default será root/src/lib. El path se puede indicar tanto con la barra final como no. Por ejemplo, tanto lib como lib/ son válidos.

Con -lr se indica el nivel de pérdida de paquetes. Esta puede variar de 0 a 0.99.

En caso de querer ver la descripción de cada parámetro correr lo siguiente: `python3 start-server.py -h`

Para cerrar el server basta con escribir `exit` en la consola donde el server está corriendo. Esto cerrará todos los sockets y joineará los threads que correspondan, sin perder memoria.

#### Cliente Upload
Para correr el cliente upload se debe correr el siguiente comando en la carpeta root/src:
` python3 upload-file.py [-h] [-v | -q] [-H ADDR] [-p PORT] [-s FILEPATH] [-n FILENAME] [-lr LOSSRATE]`

Ejemplo:
` python3 upload-file.py -H 127.0.0.1 -p 8090 -n Test.txt -s lib/otrotest.txt -q -lr 0.9`

Con -p se indica el puerto y con -H la dirección IP del host a donde quiere enviar mensajes el cliente. En caso de no ingresarse estos parámetros el cliente
intentará conectarse a la dirección 127.0.0.1 (Localhost) y al puerto 8090.

Con -n se indica el nombre del archivo (debe escribirse junto con su extensión y no debe comenzar con '-') que tendrá dentro del servidor. En caso de no indicarse el nombre, el archivo se almacenará en el server por defecto con el nombre test.txt.

Con -s se indica el path donde el cliente accederá para encontrar el archivo y enviarlo (no debe comenzar con el caracter '-'). En caso de no indicarse el path por default será root/src/test.txt (tener en cuenta que si no existe ningún archivo con este nombre el programa explotará). El path se puede indicar tanto con la barra final como no.

El resto de parámetros funciona igual que para el servidor.

Una vez que el archivo es almacenado en el servidor y se recibe la respuesta de que llegó el fin de archivo al servidor el cliente finaliza.
En caso de no recibirse la respuesta, el mensaje será reenviado como máximo 10 veces (aunque se puede configurar desde la constante MAX_RETRIES_AMOUNT). Luego de esto, si el mensaje aun no llegó, el cliente finalizará de todas formas.

#### Cliente Download
Para correr el cliente download se debe correr el siguiente comando en la carpeta root/src:
` python3 download-file.py [-h] [-v | -q] [-H ADDR] [-p PORT] [-d FILEPATH] [-n FILENAME] [-lr LOSSRATE]`

Ejemplo:
` python3 download-file.py -H 127.0.0.1 -p 8090 -v -n Test.txt -d lib/otrotest.txt -lr 0.2 `

Al igual que con el cliente upload los parámetros funcionan de la misma manera, salvo que con -n se está indicando el nombre del archivo que se encuentra en el servidor y se desea recibir, y con -d el path de destino (con nombre de archivo) donde se almacenará.
Nuevamente, si no se ingresa la dirección IP o el puerto al cual conectarse, por defecto se tomarán los valores 127.0.0.1 (Localhost) y 8090 respectivamente.
De no indicarse el path para almacenar el archivo, por defecto será root/src/test.txt. Y de no indicarse el nombre del archivo que se desea obtener del servidor se seteará por default test.txt (tener en cuenta que si no hay un archivo con ese nombre en el servidor no se recibirá nada).

Una vez que el archivo es descargado, el cliente finaliza.

*Todos los nombres de archivos indicados en los comandos -n, -d y -s deben escribirse con su extensión. Queda en manos del usuario poner nombres de archivos y filepaths con mismas extensiones.
