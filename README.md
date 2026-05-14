# Secure Auth API: FastAPI + SQLModel + Argon2id

Sistema de gestión de identidades y autenticación robusta desarrollado como parte del programa de Ingeniería en Sistemas. Este proyecto implementa estándares modernos de criptografía, incluyendo **Hashing**, **Salting** y **Peppering** para garantizar la máxima protección de las credenciales de usuario.



## Capas de Seguridad Implementadas

Para este sistema, se ha seguido el principio de **Defensa en Profundidad**:

*   **Argon2id**: Utilizado como algoritmo de derivación de claves (KDF) por su alta resistencia a ataques de fuerza bruta, GPU y canal lateral.
*   **Salting Automático**: Cada usuario posee una semilla aleatoria única generada por Argon2, evitando ataques de Tablas Arcoíris (Rainbow Tables).
*   **Peppering**: Implementación de un secreto global del servidor almacenado en variables de entorno. Este secreto se concatena a la contraseña antes del hashing, protegiendo los datos incluso ante una filtración de la base de datos.
*   **Persistencia Segura**: Uso de SQLModel para gestionar una base de datos SQLite con restricciones de integridad y unicidad.

##  Tecnologías Utilizadas

*   **Framework Web:** [FastAPI](https://fastapi.tiangolo.com/)
*   **ORM / Base de Datos:** [SQLModel](https://sqlmodel.tiangolo.com/) (basado en SQLAlchemy y Pydantic)
*   **Criptografía:** [Argon2-cffi](https://argon2-cffi.readthedocs.io/)
*   **Base de Datos:** SQLite

## Instalación y Configuración

1.  **Instalar dependencias:**
    
    pip install fastapi sqlmodel argon2-cffi python-dotenv uvicorn
   

2.  **Configurar el Pepper:**
   
   load_dotenv()
    
    SECRET_PEPPER=TuClaveSecretaMuyLargaYAleatoria
   

## Ejecución

Inicia el servidor local con Uvicorn:

python -m uvicorn main:app --reload