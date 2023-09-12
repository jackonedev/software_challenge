# FastAPI - FastCHALLENGE

## APP Introduction

La app a continuación tiene dos features:
- Posts
- Authentication

Tech-stack: 
- FastAPI
- Pydantic V2
- SQLite
- Pytest
- ~~Docker~~


## Feature 1: Posts

- **2 APIs:**
	- POST: /input/{query}
	- GET: /get_data/{id}
	- ambas requieren acceso por parte de un usuario logeado
- **POST: /input/{query}:**
	- query: solo acepta valores ["field_1", "author", "description"]
	- el body solicita el siguiente formato: `{"field_1":str, "author":str, "description":str, "my_numeric_field":int}`
	- la base de datos almacena el valor del field correspondiente al query en un formato en mayúsculas, y el resto tal cual lo recibe.
	- el response devuelve un json con el ID del post creado
- **GET: /get_data/{id}:**
	- id: es un integrer, debe ser un ID existente
	- el response devuelve un json con el registro del post correspondiente en la base de datos


## Feature 2: Authentication

- **3 APIs:**
	- POST: /users
	- GET: /users/{user_id}
	- POST: /login
- **POST: /users:**
	- solicita un body correspondiente al siguiente formato ´{"username":str, "password":str}´
	- el sistema almacena la contraseña previamente siendo encriptada por medio del algoritmo HS256
- **GET: /users/{user_id}:**
	- user_id: es un integrer correspondiente al número de usuario existente
	- debe haber un usuario logeado para realizar un request
	- el response devuelve un json con el nombre de usuario, sin exponer datos sensibles
- **POST: /login:**
	- solicita un form-data correspondiente al siguiente formato ´{"username":str, "password":str}´
	- el response token de acceso tipo bearer con un tiempo de expiración de 4 horas


## Validaciones

- **Posts:**
	- El esquema de validación verifica el tipo de dato ingresado en el request body sea el correspondiente (string, int)
	- Todos los campos son obligatorios
	- No existen valores por default
	- El campo ID es una serie numérica creciente autogenerada
- **Users:**
	- El esquema de validación solo acepta datos tipo string
	- Todos los campos son obligatorios
	- El campo username debe ser único
	- No existen valores por default
	- Los campos id, created_at, son autogenerados
	- el campo id es una serie numérica autogenerada
	- el campo created_at es una fecha formato datetime autogenerado

## Testing

- **Es posible ejecutar todos los test en una sola línea de comando:**
	- cmd: pytest -vv

- **POST: /input/{query}:**
	- cmd: pytest tests/test_create_post.py -vv -s
	- ejecuta 1 test, 1 vez por cada valor que toma el parámetro 'query'
	- son 3 valores alternativos que toma el parámetros en cada test:
		- ["field_1", "author", "description"]
	- se crea un registro en la test_db por medio de cliente autorizado
	- se obtiene el id del registro creado
	- se consulta el registro en la test_db por medio de ORM
	- se valida el registro con esquema Pydatic
	- se corroboran las siguientes aserciones:
		- status_code == 201 (registro creado exitosamente)
		- si el parámetro es "field_1" que unicamente el valor del "field_1" se convierta en mayúsculas
		- si el parámetro es "author" que unicamente el valor del "author" se convierta en mayúsculas
		- si el parámetro es "description" que unicamente el valor del "description" se convierta en mayúsculas
- **GET: /get_data/{id}**
	- cmd: pytest tests/test_get_post.py -vv -s
	- ejecuta 2 test, 1 de ellos se ejecuta 3 veces, el otro 1 vez
	- el primer test posee 3 parámetros, [1, 2, 3], correspondiente a los id de los test_posts creados en la test_db
	- el primer test solicita por medio de un cliente autorizado el post correspondiente respectivamente a cada parámetro
	- la respuesta se valida por medio de un esquema Pydantic que asignamos la variable "post"
	- se corroboran las siguientes aserciones:
		- status_code == 200 (registro obtenido)
		- el post.ID == id (parámetro)
		- el post.field_1 ==  test_post[id-1].field_1 (test_db)
		- el post.author ==  test_post[id-1].author (test_db)
		- el post.description ==  test_post[id-1].description (test_db)
		- el post.my_numeric_field ==  test_post[id-1].my_numeric_field (test_db)
	- el segundo test utiliza un cliente no autorizado, y los test_post de la test_db
	- el segundo test corroba que el status_code == 401 como única aserción

- **Los siguientes tests se encuentran dentro del mismo módulo, por lo tanto se ejecutan desde el mismo comando:**
	- cmd: pytest tests/test_users.py -vv -s

- **POST: /users**
	- por medio de un cliente no autorizado se envía un POST hardcoded, y la respuesta es validada por un esquema Pydantic
	- el validador de usuario lo asignamos a la variable user
	- se corroboran las siguientes aserciones:
		- status_code == 201
		- user.username == "admin" (hardcoded)

- **POST: /login**
	- por medio de un cliente no autorizado enviamos un POST con y parámetros de un test_user de la test_db
	- validamos con Pydantic el Token recibido en la respuesta
	- desencriptamos el Token recibido para obtener el id del de la firma
	- se corroboran las siguiente aserciones:
		- id (firma) == test_user["id"] (test_db)
		- token_type == "bearer"
		- status_code == 200

- **POST: /login (II)**
	- el test garantiza la respuesta ante error en el login de un usuario al sistema
	- se ejecuta 1 test, 1 vez por cada valor de parámetro, son 3 parámetros, y  5 alternativas de valor de parámetro
	- los parámetros son:
		- ["username", "password", "status_code"]
	- las alternativas de parámetro contempla valores que son equivocados y valores de error de validación
	- los valores equivocados corroboran el status_code == 403
	- los valores erróneos corroban el status_code == 422




## Documentación

- creando un entorno virtual dentro de la carpeta /app
	- cmd: py -m venv venv
- instalando las dependencias del archivo requirements.txt
	- cmd (windows): .\venv\scritps\activate
	- cmd (windows): python.exe -m pip install --upgrade pip
	- cmd (windows): pip install -r requirements.txt
- desplegando la app en un servidor local de uvicorn:
	- cmd: uvicorn main:app --reload
- ingresando en el navegador web colocar en la barra de navegación:
	- localhost:8000/docs
- segunda alternativa:
	- localhost:8000/redoc
	

## Etapas de desarrollo pendiente

- Despliegue en contenedor (Docker)
- Despliegue en servicio en la nube (pythonanywhere, GCP)

## Anexo

- El siguiente párrafo es un fichero .env modelo, el fichero .env debiera ser colocado dentro de la carpeta /app:


`/.env file`
```
SECRET_KEY = "SOME_HASH"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 240
```


<!-- 
### Pendientes:
	- verificar status_code dentro del decorador
	- cambiar el query param llamado 'query' por 'my_target_field' -->
