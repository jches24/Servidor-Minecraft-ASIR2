# 🎮 Servidor Minecraft Analytics Platform

**Proyecto Intermodular – ASIR 2 | FP Summa | Curso 2025-2026**

> Infraestructura de servidor Minecraft con telemetría en tiempo real, 
> almacenamiento en MySQL y visualización en Grafana.

**Autores:** Dayanna Bracamonte Silva, Rubén Mateos Díaz-Ropero, 
Juan José Cherre Espejo  
**Tutor:** Eliecer Martin  
**Fecha:** Junio 2026

---

## 📋 Descripción

Plataforma completa desplegada en VPS Hetzner (Ubuntu Server 22.04 LTS) 
mediante Docker Compose. Incluye servidor PaperMC v1.20.4, recolección 
automática de métricas vía script Python/RCON, base de datos MySQL 8.0 
y dashboards interactivos en Grafana.

**Resultados:** +3.400 métricas acumuladas · TPS medio 20.0 · 
100% retención de jugadores en 7 días

---

## 🧱 Arquitectura

| Contenedor       | Tecnología         | Puerto  |
|------------------|--------------------|---------|
| minecraft        | PaperMC v1.20.4    | 25565   |
| mysql            | MySQL 8.0          | interno |
| grafana          | Grafana OSS        | 3000    |
| data-collector   | Python 3 + RCON    | -       |
| bluemap          | BlueMap v3.21      | 8100    |
| plan             | Plan Analytics     | 8804    |

---

## 🚀 Instalación y despliegue

### Requisitos
- VPS con Ubuntu Server 22.04 LTS
- Docker Engine + Docker Compose
- Acceso SSH con clave pública

### Pasos

```bash
# 1. Clonar el repositorio
git clone https://github.com/tu-usuario/servidor-minecraft-analytics.git
cd servidor-minecraft-analytics

# 2. Levantar los contenedores
docker compose up -d

# 3. Verificar que todo está corriendo
docker compose ps
```

### Accesos
- **Minecraft:** `178.105.93.155:25565`
- **Grafana:** `http://178.105.93.155:3000`
- **Plan Analytics:** `http://178.105.93.155:8804`
- **BlueMap:** `http://178.105.93.155:8100`

---

## 🔒 Seguridad

- Firewall UFW con puertos mínimos abiertos
- SSH exclusivo por clave pública (sin contraseña)
- MySQL accesible solo en red interna Docker
- Backups automáticos diarios vía cron

---

## 📁 Contenido del repositorio

- `docker-compose.yml` – Orquestación de contenedores
- `scripts/` – Script Python de recolección y backup Bash
- `config/` – Configuraciones de Grafana y MySQL
- `memoria/` – Memoria técnica completa en PDF
- `evidencias/` – Capturas de dashboards y pruebas

---

## 🤖 Uso de IA

Para la realización de este proyecto se han utilizado herramientas de 
apoyo como asistentes de IA para revisión de documentación. El equipo 
declara que comprende, ha revisado y puede defender el contenido técnico 
presentado.
