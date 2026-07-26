"""
app/services/resend_service.py — Helper untuk kirim email menggunakan Resend.
"""
import resend
from flask import current_app

def send_contact_email(nama, email, subjek, pesan):
    """
    Kirim email menggunakan Resend API.
    Return (success_boolean, error_message)
    """
    api_key = current_app.config.get("RESEND_API_KEY")
    sender_email = current_app.config.get("RESEND_SENDER")
    sender_name = current_app.config.get("RESEND_SENDER_NAME")
    owner_email = current_app.config.get("OWNER_EMAIL")

    if not api_key:
        return False, "Resend API Key tidak ditemukan."
    if not sender_email or not owner_email:
        return False, "Email pengirim atau penerima (owner) belum dikonfigurasi."

    resend.api_key = api_key

    # Format email (dikirim ke owner)
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>
    <body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background-color: #f4f4f5; margin: 0; padding: 40px 0; color: #333333;">
        <table width="100%" border="0" cellspacing="0" cellpadding="0" style="max-width: 600px; margin: 0 auto; background-color: #ffffff; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);">
            <tr>
                <td style="padding: 40px 40px 20px 40px; border-bottom: 1px solid #eeeeee;">
                    <h1 style="margin: 0; font-size: 22px; color: #111827; letter-spacing: -0.5px;">Pesan Baru</h1>
                    <p style="margin: 8px 0 0 0; font-size: 14px; color: #6b7280;">Anda menerima pesan baru dari website portofolio.</p>
                </td>
            </tr>
            <tr>
                <td style="padding: 30px 40px;">
                    <table width="100%" border="0" cellspacing="0" cellpadding="0" style="margin-bottom: 25px;">
                        <tr>
                            <td width="80" style="padding: 8px 0; font-size: 13px; font-weight: 600; color: #6b7280; text-transform: uppercase; letter-spacing: 0.5px;">Nama</td>
                            <td style="padding: 8px 0; font-size: 15px; color: #111827;">{nama}</td>
                        </tr>
                        <tr>
                            <td width="80" style="padding: 8px 0; font-size: 13px; font-weight: 600; color: #6b7280; text-transform: uppercase; letter-spacing: 0.5px;">Email</td>
                            <td style="padding: 8px 0; font-size: 15px; color: #111827;"><a href="mailto:{email}" style="color: #2563eb; text-decoration: none;">{email}</a></td>
                        </tr>
                        <tr>
                            <td width="80" style="padding: 8px 0; font-size: 13px; font-weight: 600; color: #6b7280; text-transform: uppercase; letter-spacing: 0.5px;">Subjek</td>
                            <td style="padding: 8px 0; font-size: 15px; color: #111827; font-weight: 500;">{subjek}</td>
                        </tr>
                    </table>
                    
                    <div style="background-color: #f9fafb; border: 1px solid #e5e7eb; border-radius: 6px; padding: 20px;">
                        <h2 style="margin: 0 0 15px 0; font-size: 13px; font-weight: 600; color: #6b7280; text-transform: uppercase; letter-spacing: 0.5px;">Isi Pesan</h2>
                        <div style="font-size: 15px; line-height: 1.6; color: #374151;">{pesan.replace(chr(10), '<br>')}</div>
                    </div>
                </td>
            </tr>
            <tr>
                <td style="background-color: #f8fafc; padding: 20px 40px; text-align: center; border-top: 1px solid #eeeeee;">
                    <p style="margin: 0; font-size: 12px; color: #94a3b8;">Dikirim secara otomatis dari form kontak website Anda</p>
                </td>
            </tr>
        </table>
    </body>
    </html>
    """

    try:
        r = resend.Emails.send({
            "from": f"{sender_name} <{sender_email}>",
            "to": owner_email,
            "subject": f"Contact Form: {subjek}",
            "html": html_content,
            "reply_to": email
        })
        # Jika berhasil r mengembalikan dict/obj dengan id
        if hasattr(r, 'get') and r.get('id') or getattr(r, 'id', None):
            return True, None
        return True, None # resend v2 returns Email object directly
    except Exception as e:
        return False, str(e)
