# GAIP-Cero-Auto — Consola de Google AI Pro en español

Aplicación local para Windows 10/11 que administra cuentas y ejecuta tareas relacionadas con Google AI Pro mediante una interfaz web.

**Aviso:** los resultados de promociones y suscripciones no están garantizados. Antes de confirmar cualquier pago, comprobá el precio y las condiciones reales que muestre Google.

## Requisitos

- Windows 10 u 11.
- Google Chrome instalado.
- Python 3.10 o superior, disponible en PATH.
- Conexión de red; proxy opcional configurable desde la consola.

## Inicio

1. Ejecutá `1_首次运行_安装依赖并启动.bat` la primera vez.
2. Para los siguientes usos, ejecutá `2_启动控制台.bat`.
3. Abrí `http://127.0.0.1:8765` si el navegador no se inicia automáticamente.

## Configuración

En **Configuración general**, ingresá la información de pago, la región y el proxy cuando corresponda. Revisá que los datos sean correctos antes de iniciar una tarea.

## Importar cuentas

En **Importar cuentas**, pegá una cuenta por línea. Los formatos admitidos por el programa incluyen:

- `correo----contraseña----correo_recuperacion`
- `correo----contraseña----clave_2FA`
- `correo----contraseña----correo_recuperacion----clave_2FA`

## Ejecutar tareas

Desde **Cola de cuentas** podés iniciar, detener, restablecer o eliminar tareas, además de elegir la etapa inicial de ejecución. Los errores y estados se muestran en español en el panel de registros.

## Seguridad

Las contraseñas, claves 2FA, datos de tarjeta, capturas y perfiles del navegador son sensibles. No subas configuraciones, registros o capturas con esos datos a GitHub. Ejecutá el programa únicamente en equipos de confianza.

## Traducción

La interfaz y los mensajes de servidor están en español. El motor traduce los mensajes operativos antes de mostrarlos, pero conserva los textos originales utilizados para reconocer páginas y botones de Google en distintos idiomas.

## Validación

Las comprobaciones automáticas de sintaxis se definen en `.github/workflows/validar-traduccion-es.yml`. La ejecución real de compras o suscripciones no forma parte de esas pruebas.
