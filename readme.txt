1) crear conexión a base de datos postgresql

2) modelo:
"id":
"field_1": str
"author": str
"description": str
"my_numeric_field": 123

3) Schema de validacion: Todos los campos obligatorios, sin valor por default

4) API: dos rutas /get_data y /input
GET: /get_data/{post_id}: para obtener info del post
POST: /input/{f"{field}"}: para crear un post

5) Manejo de excepciones

6) Autenticación

7) Documentación

8) Despliegue