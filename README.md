# README — Laboratorio: DVWA con Burp, cURL, Hydra y Python

> **Aviso legal y ético**: Este repositorio y las instrucciones están diseñadas **únicamente para pruebas en entornos controlados y con permiso explícito** (por ejemplo, DVWA corriendo localmente). No realice ataques a sistemas que no sean de su propiedad o para los que no tenga autorización. El autor no se hace responsable del uso indebido.

---

## Requisitos

- Docker
    
- docker-compose
    
- Burp Suite (versión Free está bien)
    
- Hydra (THC Hydra)
    
- curl
    
- Python 3.x (con `requests`)
    

Opcionales:

- Navegador web (Chrome/Firefox)
    
- Wordlists (ej.: `rockyou.txt` u otras listas de diccionario personalizadas)
    

---

## Estructura recomendada del repositorio

```
cripto-lab2/
├─ DVWA_files/            # docker-compose modificado y ficheros relacionados
├─ cURL/                  # ejemplos .sh o .txt con comandos curl exportados
├─ Hydra/                 # ejemplos de comandos hydra y wordlists pequeñas
├─ Python/                # scripts en python (requests) para automatizar pruebas
└─ README.md              # este archivo
```

---

## 1) Docker / docker-compose (DVWA)

1. Clonar el repositorio de DVWA (o usar el contenido que ya está incluido):
    

```bash
git clone https://github.com/digininja/DVWA.git
cd DVWA
```

2. Usar el `docker-compose.yml` modificado que se encuentra en `DVWA_files/`. Ejemplo de `ports` para exponer DVWA en el puerto `8080` del host

3. Levantar los servicios:
    

```bash
docker-compose up -d
```

4. Abrir en el navegador (según puerto elegido):
    

```
http://localhost:8080 
```

5. Para usar Burp: configurar el proxy del navegador a la IP y puerto donde Burp escucha (en Firefox se hace en Preferencias → Red → Ajustes de conexión). En Burp, activar `Proxy → Intercept` para capturar tráfico.
    

### Flujo con Burp (básico)

- Navegar a la página vulnerable con el proxy activo.
    
- Capturar la petición que te interesa en Burp (p. ej. formulario de login).
    
- Enviar la petición a **Intruder** → seleccionar los parámetros (posiciones) que quieres atacar.
    
- Cargar diccionarios (wordlists) en la pestaña `Payloads` y ejecutar el ataque.
    

---

## 2) cURL — obtener cookies y reproducir peticiones

### Obtener cookies desde el navegador

1. En el navegador: `Inspeccionar` → pestaña `Application` (Chrome) o `Storage` (Firefox) → `Cookies` → copiar el par `name=value` de la cookie que te interese (ej. `PHPSESSID=abcd1234`).
    
2. Alternativamente, en la pestaña `Network` seleccionar la petición, click derecho → **Copy -> Copy as cURL** (o similar). Esto te dará un comando `curl` completo que reproduce la petición.
    

### Ejecutar el `curl` copiado

Pegar y ejecutar en la terminal. Ejemplo manual con cookie:

```bash
curl -v -X POST "http://localhost:8080/login.php" \
  -H "User-Agent: Mozilla/5.0" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  --cookie "PHPSESSID=abcd1234; other=valor" \
  --data "username=admin&password=1234&Login=Login"
```

Ejemplos exportados desde el navegador en `cURL/`.

---

## 3) Hydra — ataque por diccionario (form-based)

> **Advertencia**: Hydra es una herramienta potente. Úsala solo en entornos autorizados.

### Instalación (ejemplos)

- Debian/Ubuntu:
    

```bash
sudo apt update
sudo apt install hydra -y
```

- Arch Linux:
    

```bash
sudo pacman -S hydra
```

### Ejemplo: ataque a formulario POST

Supongamos que el formulario de login está en `/login.php` y los parámetros son `username` y `password`. Ejemplo de uso de `hydra` con `http-post-form` (modo genérico):

```bash
hydra -L usuarios.txt -P passwords.txt 127.0.0.1 -s 8080 http-post-form \
"/login.php:username=^USER^&password=^PASS^&Login=Login:Invalid username or password" -V
```

- `-L usuarios.txt` lista de usuarios
    
- `-P passwords.txt` wordlist de contraseñas
    
- `127.0.0.1 -s 8080` host y puerto
    
- `http-post-form` indica ataque por formulario POST
    
- Tras los dos puntos viene la expresión que describe la petición y una cadena que indica fallo (`Invalid username or password`). Ajustar según la respuesta real del servidor.
    

Si necesitas enviar cookies o encabezados adicionales, puedes usar la opción `-H` de hydra (ej: `-H "Cookie: PHPSESSID=abcd1234"`).

Los comandos de ejemplo en `Hydra/`.

---

## 4) Python (automatizar con `requests`)

### Preparar entorno

```bash
python3 -m venv venv
source venv/bin/activate
pip install requests
```

Obtención de cookies siguiendo pasos anteriores.
### Script de ejemplo (`Python/brute.py`)

Scripts en `Python/`.

    

---

## Referencias y recursos

- DVWA: [https://github.com/digininja/DVWA](https://github.com/digininja/DVWA)
    
- Burp Suite (PortSwigger): [https://portswigger.net/burp](https://portswigger.net/burp)
    
- THC Hydra: [https://github.com/vanhauser-thc/thc-hydra](https://github.com/vanhauser-thc/thc-hydra)
    
- `requests` (Python): [https://docs.python-requests.org/](https://docs.python-requests.org/)
    

---
