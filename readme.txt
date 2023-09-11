# FastAPI - FastCHALLENGE

## APP tech stack: FastAPI, SQLite, Pytest, Docker

La app a continuación tiene dos features:
	- Posts
	- Authentication


## Posts

- 2 APIs:
	- POST: /input/{query}
	- GET: /get_data/{id}
	- ambas requieren acceso por parte de un usuario logeado
- POST: /input/{query}:
	- query: solo acepta valores ["field_1", "author", "description"]
	- el body solicita el siguiente formato: `{"field_1":str, "author":str, "description":str, "my_numeric_field":int}`
	- la base de datos almacena el valor del field correspondiente al query en un formato en mayúsculas, y el resto tal cual lo recibe.
	- el response devuelve un json con el ID del post creado
- GET: /get_data/{id}:
	- id: es un integrer, debe ser un ID existente
	- el response devuelve un json con el registro del post correspondiente en la base de datos


## Authentication

- 3 APIs:
	- POST: /users
	- GET: /users/{user_id}
	- POST: /login
- POST: /users:
	- solicita un body correspondiente al siguiente formato ´{"username":str, "password":str}´
	- el sistema almacena la contraseña previamente siendo encriptada por medio del algoritmo HS256
- GET: /users/{user_id}:
	- user_id: es un integrer correspondiente al número de usuario existente
	- debe haber un usuario logeado para realizar un request
	- el response devuelve un json con el nombre de usuario, sin exponer datos sensibles
- POST: /login:
	- solicita un form-data correspondiente al siguiente formato ´{"username":str, "password":str}´
	- el response token de acceso tipo bearer con un tiempo de expiración de 4 horas


## Validaciones

- Posts:
	- El esquema de validación verifica el tipo de dato ingresado en el request body sea el correspondiente (string, int)
	- Todos los campos son obligatorios
	- No existen valores por default
	- El campo ID es una serie numérica creciente autogenerada
- Users:
	- El esquema de validación solo acepta datos tipo string
	- Todos los campos son obligatorios
	- El campo username debe ser único
	- No existen valores por default
	- Los campos id, created_at, son autogenerados
	- el campo id es una serie numérica autogenerada
	- el campo created_at es una fecha formato datetime autogenerado

## Testing

- POST: /input/{query}:
	- 

7) Documentación

8) Despliegue

9) Pendientes:
	- verificar status_code dentro del decorador
	- cambiar el query param llamado 'query' por 'my_target_field'
