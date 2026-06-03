#!/bin/bash
# ─────────────────────────────────────────────────────────
# backup.sh
# Backup automático del servidor Minecraft y base de datos
# ─────────────────────────────────────────────────────────

FECHA=$(date +%Y-%m-%d_%H-%M)
BACKUP_DIR="/backups/minecraft"
CONTENEDOR="minecraft"
MYSQL_CONTENEDOR="mysql"
MYSQL_USER="mcuser"
MYSQL_PASSWORD="mcpassword"
MYSQL_DB="minecraft_analytics"
DIAS_RETENCION=7

mkdir -p "$BACKUP_DIR"

echo "================================================"
echo " Backup iniciado: $FECHA"
echo "================================================"

# ── 1. Backup del mundo ───────────────────────────────────
echo "[1/3] Guardando mundo de Minecraft..."
docker exec $CONTENEDOR rcon-cli save-off
docker exec $CONTENEDOR rcon-cli save-all
sleep 5
docker cp $CONTENEDOR:/data/world "$BACKUP_DIR/world_$FECHA"
docker exec $CONTENEDOR rcon-cli save-on
echo "      ✓ Mundo guardado en: world_$FECHA"

# ── 2. Backup de MySQL ────────────────────────────────────
echo "[2/3] Exportando base de datos MySQL..."
docker exec $MYSQL_CONTENEDOR mysqldump \
  -u $MYSQL_USER \
  -p$MYSQL_PASSWORD \
  $MYSQL_DB > "$BACKUP_DIR/db_$FECHA.sql"
echo "      ✓ Base de datos guardada en: db_$FECHA.sql"

# ── 3. Limpieza de backups antiguos ──────────────────────
echo "[3/3] Eliminando backups con más de $DIAS_RETENCION días..."
find "$BACKUP_DIR" -mtime +$DIAS_RETENCION -exec rm -rf {} \;
echo "      ✓ Limpieza completada"

echo "================================================"
echo " Backup finalizado correctamente: $FECHA"
echo "================================================"
