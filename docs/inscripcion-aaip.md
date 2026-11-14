# Inscripción de la base de datos en la AAIP (Ley 25.326)

Trámite **gratuito y online**, a cargo del titular del sitio: requiere su Clave Fiscal, por eso no lo puede hacer otra persona ni un asistente.
Los pasos y requisitos salen de las páginas oficiales (confirmarlos antes de empezar, porque pueden cambiar):
<https://www.argentina.gob.ar/registrar-bases-de-datos-personales-privadas> y
<https://www.argentina.gob.ar/servicio/inscribir-un-responsable-de-bases-de-datos-personales-privadas>.

## Requisitos
- Clave Fiscal (AFIP/ARCA) **nivel 2 o superior**.
- Un mail válido (todas las comunicaciones de la AAIP llegan ahí).
- Entrar a **Trámites a Distancia (TAD)**: <https://tramitesadistancia.gob.ar>.

## Paso 1 — Inscribir al responsable
En TAD buscar **"Inscripción del Responsable al Registro Nacional de Bases de Datos"**. Al confirmar llega un mail con el
**código de registro del responsable**: guardarlo (también queda en la solapa "Notificaciones" de TAD).

## Paso 2 — Inscribir la base
En TAD buscar **"Inscripción de bases de datos privadas"**. Con esto llega la constancia con el **número de registro de la base**.

Respuestas sugeridas (describen lo que el sistema hace de verdad; el formulario puede pedir otros campos, ver el instructivo oficial en PDF
que enlaza la página):

| Dato | Qué cargar |
|---|---|
| Nombre de la base | Cuentas de usuarios de calculadoracientifica.com.ar |
| Finalidad | Identificar a la persona usuaria, guardar y sincronizar entre dispositivos sus favoritas, historial de cálculos y preferencias, y mantener el servicio seguro. No hay fines comerciales ni de marketing. |
| Titulares de los datos | Personas que crean una cuenta (mayores de 13 años) |
| Datos tratados | Mail, nombre (solo si ingresa con Google), identificador de cuenta de Google, hash de contraseña, fecha de último ingreso, versión y fecha de aceptación de los términos, favoritas, historial de cálculos y tema. **No hay datos sensibles.** |
| Origen de los datos | Los da la propia persona al crear la cuenta |
| Sistema de tratamiento | Automatizado, en línea |
| Cesiones | Ninguna a terceros con fines propios. Encargados de tratamiento: Cloudflare (alojamiento y base de datos), Google (solo ingreso con Google), Resend (mails de verificación y de recuperación de contraseña). |
| Transferencia internacional | Sí: los proveedores anteriores operan servidores fuera del país (p. ej. Estados Unidos). Se informa y se pide el consentimiento al crear la cuenta (Política de Privacidad, sección "Transferencia internacional"). |
| Medidas de seguridad | HTTPS; contraseñas con PBKDF2-SHA256 y sal; tokens de sesión y de verificación guardados solo como hash; cookie de sesión HttpOnly/Secure; límites de intentos; acceso a la base restringido al titular. |
| Conservación | Hasta que la persona elimine su cuenta (lo puede hacer desde "Mi cuenta"; borra todo al instante). |
| Ejercicio de derechos | Desde "Mi cuenta" o por mail a contacto@calculadoracientifica.com.ar (acceso: 10 días corridos; rectificación y supresión: 5 días hábiles). |

## Después
- Si la AAIP observa algo, escribe por mail.
- La inscripción no vence, pero **si cambia algo de lo declarado** (por ejemplo, otro proveedor o nuevos datos) hay que modificarla.
- Cuando llegue el número de registro, se agrega a la Política de Privacidad (sección "Responsable").
- Consultas: registrobasesdedatos@aaip.gob.ar.

> Nota: esta guía y los textos legales del sitio fueron preparados sin asesoramiento profesional. Cubren los requisitos
> habituales de la Ley 25.326 y de la Ley 24.240, pero no reemplazan la opinión de un abogado si el sitio crece o cambia de uso.
