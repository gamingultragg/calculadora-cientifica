/**
 * /api/* — API de cuentas (Cloudflare Pages Functions). La lógica vive en server-lib/api.mjs para poder
 * probarla en Node. Requiere el binding D1 "DB"; sin él, /api/config responde { enabled: false }.
 * Variables: GOOGLE_CLIENT_ID (pública), RESEND_API_KEY (secreta), MAIL_FROM y SITE_URL (opcionales).
 */
import { handle } from "../../server-lib/api.mjs";

export async function onRequest(context) {
  return handle(context.request, context.env);
}
