# Integrantes
-   Cesar Figueroa
-   Francisco Cornejo
-   James Pérez

## comando para instalar todas las librerías

```
pip install -r requirements.txt
```

## Cosas que se instalarán

```
pip install matplotlib==3.6.0
pip install pytesseract==0.3.10
pip install pdf2image==1.16.2
pip install PyMuPDF==1.22.3
pip install fpdf==1.7.2
pip install syltippy==1.0
pip install syllables==1.0.7
pip install es-core-news-sm
pip install fastapi==0.95.2
pip install python-multipart==0.0.6
pip install uvicorn==0.22.0
pip install spacy
pip install pymongo==3.12.3
pip install dnspython==2.4.2
pip install passlib==1.7.4
pip install cryptography==41.0.4
pip install openpyxl==3.1.2
pip install bcrypt==4.0.1
pip install python-jose==3.3.0
pip install pydantic
beanie==1.8.10

python -m spacy download en_core_web_sm
```


## Trabajar con FastApi (crea server y Api)

Deben irse a la carpeta del proyecto, ejecutar SIEMPRE todos los pasos (excepto el primero que solo una vez se ejecuta), no olvidar desactivar el ambiente

```
#Instala la librería de virtualenv
pip install virtualenv virtualenv

#Antes de este paso moverse desde terminal a donde está el proyecto
#Crea un ambiente virtual
virtualenv venv

#Activa el ambiente
Set-ExecutionPolicy Unrestricted -Scope Process
venv\Scripts\activate

#Instala en el ambiente todas las librerías a utilizar
pip install -r requirements.txt

#Ejecuta el server
uvicorn API:app --reload --workers 4

#Correr unicamente en consola
python lecto.py

#Desactiva el ambiente
deactivate
```


## Trabajar con Docker

-   Instalar <a href="https://www.youtube.com/watch?v=U8RcrCoL9q4">WSL y Docker Desktop</a>
-   En terminal irse a la ruta del proyecto (puede ser desde la terminal de visual studio code en powershell)
-   Poner el comando:
```
docker compose up
```
-   Esperar a que se termine el proceso (toma entre 100-140 segundos)
-   En cualquier navegador irse a la ruta <a href='http://localhost:8080/lecto'>http://localhost:8080/lecto</a> o <a href='http://0.0.0.0:8080/lecto'>http://0.0.0.0:8080/lecto</a>
