"""
app/services/email_service.py — Helper kirim email via Resend.
"""
# TODO: Implementasi fungsi berikut:
#
# import resend
# from flask import current_app
#
#
# def send_contact_email(sender_name, sender_email, subject, message):
#     """Kirim notifikasi email ke pemilik portofolio saat ada pesan baru."""
#     resend.api_key = current_app.config["RESEND_API_KEY"]
#
#     recipient = current_app.config["OWNER_EMAIL"]
#     from_address = (
#         f'{current_app.config["RESEND_SENDER_NAME"]} '
#         f'<{current_app.config["RESEND_SENDER"]}>'
#     )
#
#     params = {
#         "from": from_address,
#         "to": [recipient],
#         "subject": f"[Portfolio] {subject}",
#         "html": f"<p><strong>Dari:</strong> {sender_name} ({sender_email})</p>"
#                 f"<p>{message}</p>",
#     }
#     return resend.Emails.send(params)
