"""
data-collector.py
Recolector de métricas del servidor Minecraft vía RCON.
Se conecta cada 60 segundos y almacena datos en MySQL.
"""

import time
import mysql.connector
from mcrcon import MCRcon
from datetime import datetime

# ── Configuración ──────────────────────────────────────────
RCON_HOST     = "minecraft"
RCON_PORT     = 25575
RCON_PASSWORD = "tu_password_rcon"

DB_HOST     = "mysql"
DB_PORT     = 3306
DB_NAME     = "minecraft_analytics"
DB_USER     = "mcuser"
DB_PASSWORD = "mcpassword"

INTERVALO_SEGUNDOS = 60
# ───────────────────────────────────────────────────────────


def conectar_db():
    """Establece conexión con MySQL."""
    return mysql.connector.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )


def obtener_metricas_rcon():
    """Obtiene TPS y jugadores conectados vía RCON."""
    with MCRcon(RCON_HOST, RCON_PASSWORD, port=RCON_PORT) as rcon:
        tps_raw     = rcon.command("tps")
        players_raw = rcon.command("list")
    return tps_raw, players_raw


def parsear_tps(tps_raw):
    """
    Extrae el TPS del último minuto.
    Formato típico: 'TPS from last 1m, 5m, 15m: 20.0, 20.0, 20.0'
    """
    try:
        partes = tps_raw.split(":")[-1].strip().split(",")
        return float(partes[0].strip())
    except Exception:
        return 0.0


def parsear_jugadores(players_raw):
    """
    Extrae número de jugadores conectados.
    Formato típico: 'There are X of a max of Y players online'
    """
    try:
        return int(players_raw.split("There are")[1].split("of")[0].strip())
    except Exception:
        return 0


def guardar_metricas(cursor, tps, jugadores):
    """Inserta un registro de métricas en la base de datos."""
    sql = """
        INSERT INTO metricas_rendimiento (timestamp, tps, jugadores_conectados)
        VALUES (%s, %s, %s)
    """
    cursor.execute(sql, (datetime.now(), tps, jugadores))


def main():
    print("=" * 50)
    print("  Minecraft Analytics - Data Collector")
    print("  Intervalo: 60 segundos")
    print("=" * 50)

    while True:
        try:
            tps_raw, players_raw = obtener_metricas_rcon()
            tps       = parsear_tps(tps_raw)
            jugadores = parsear_jugadores(players_raw)

            db     = conectar_db()
            cursor = db.cursor()
            guardar_metricas(cursor, tps, jugadores)
            db.commit()
            cursor.close()
            db.close()

            print(f"[{datetime.now()}] ✓ TPS: {tps} | Jugadores: {jugadores}")

        except Exception as e:
            print(f"[{datetime.now()}] ✗ ERROR: {e}")

        time.sleep(INTERVALO_SEGUNDOS)


if __name__ == "__main__":
    main()
