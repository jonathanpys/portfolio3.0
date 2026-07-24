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
    <div style="font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; max-width: 600px; margin: 0 auto; background-color: #0B0F19; padding: 30px; border-radius: 12px; border: 1px solid #1C253C;">
        <div style="text-align: center; margin-bottom: 30px;">
            <h2 style="color: #CCFF00; margin: 0; font-size: 24px; text-transform: uppercase; letter-spacing: 1px;">Pesan Baru</h2>
            <p style="color: #94A3B8; font-size: 14px; margin-top: 5px;">Dari website portofolio Anda</p>
        </div>
        
        <div style="background-color: #141B2D; padding: 20px; border-radius: 8px; margin-bottom: 25px;">
            <p style="margin: 0 0 12px; color: #FFFFFF;"><strong style="color: #94A3B8; width: 70px; display: inline-block;">Nama:</strong> {nama}</p>
            <p style="margin: 0 0 12px; color: #FFFFFF;"><strong style="color: #94A3B8; width: 70px; display: inline-block;">Email:</strong> <a href="mailto:{email}" style="color: #CCFF00; text-decoration: none;">{email}</a></p>
            <p style="margin: 0; color: #FFFFFF;"><strong style="color: #94A3B8; width: 70px; display: inline-block;">Subjek:</strong> {subjek}</p>
        </div>

        <div style="background-color: #141B2D; padding: 20px 25px; border-radius: 8px; color: #FFFFFF; line-height: 1.6;">
            <h3 style="margin-top: 0; color: #CCFF00; font-size: 16px; border-bottom: 1px solid #1C253C; padding-bottom: 12px; margin-bottom: 15px;">Isi Pesan:</h3>
            <div style="font-size: 15px;">{pesan.replace(chr(10), '<br>')}</div>
        </div>
        
        <div style="text-align: center; margin-top: 30px; padding-top: 20px; border-top: 1px solid #1C253C; color: #64748B; font-size: 12px;">
            <p style="margin: 0;">Email ini dikirim secara otomatis melalui form kontak di website portofolio Anda.</p>
        </div>
    </div>
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
