# Eye Exercise Reminder

[English](../README.md) · [Русский](README.ru.md) · [简体中文](README.zh-CN.md) · **Español** · [Português](README.pt-BR.md)

**Eye Exercise Reminder** es una aplicación ligera de superposición de escritorio para
Windows, construida con Python y PyQt6. Te recuerda periódicamente hacer ejercicios
oculares, ayudando a reducir la fatiga visual en sesiones largas frente a la pantalla.

El recordatorio aparece como una ventana flotante siempre visible que muestra una imagen con
instrucciones de ejercicios. Es totalmente configurable, soporta 12 idiomas y puede lanzarse
en modo silencioso, sin ventana de consola.

## Características

| Característica | Detalles |
|---|---|
| Intervalo configurable | Recordatorio de 1 a 180 minutos |
| Posponer | Aplaza el recordatorio un número fijo de minutos |
| 12 idiomas | EN, UK, RU, DE, ES, FR, IT, ZH, JA, PL, PT, TR |
| Ajustes persistentes | El idioma se guarda localmente en JSON |
| Siempre visible | La superposición queda sobre las demás ventanas |
| Arrastrable | Mueve la ventana a cualquier parte de la pantalla |
| Lanzador silencioso | Ejecución sin consola mediante `start.pyw` |

## Instalación y ejecución

Requiere Python 3.11+; la única dependencia externa es PyQt6.

```bash
git clone https://github.com/Topicspot/eye-exercise-reminder.git
cd eye-exercise-reminder
pip install PyQt6
python eye_reminder.py    # con salida de consola
pythonw start.pyw         # modo silencioso (solo Windows)
```

La imagen de ejercicios (por defecto `eye_exercises.png`) debe estar en la misma carpeta que
`eye_reminder.py`.

La documentación completa (configuración, privacidad, solución de problemas) está en el
[README en inglés](../README.md).

## Licencia

MIT.
