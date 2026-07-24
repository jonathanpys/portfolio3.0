"""
Admin routes: Contacts — CRUD API untuk data pesan pengunjung.

Endpoints:
    GET    /admin/contacts              → List semua pesan kontak
    DELETE /admin/contacts/<id>         → Hapus pesan
"""
from flask import request
from flask_login import login_required
from . import admin_bp
from app.extensions import db
from app.models import Contact
from app.utils import api_response


def _serialize_contact(c):
    """Convert Contact model ke dict."""
    return {
        "id": c.id,
        "nama": c.nama,
        "email": c.email,
        "subjek": c.subjek,
        "pesan": c.pesan,
        "status": c.status,
        "created_at": str(c.created_at) if c.created_at else None,
    }


@admin_bp.route("/contacts", methods=["GET"])
@login_required
def list_contacts():
    """List semua pesan."""
    contacts = Contact.query.order_by(Contact.created_at.desc()).all()
    data = [_serialize_contact(c) for c in contacts]
    return api_response("success", f"Ditemukan {len(data)} pesan.", data=data)


@admin_bp.route("/contacts/<int:contact_id>", methods=["DELETE"])
@login_required
def delete_contact(contact_id):
    """Hapus pesan berdasarkan ID."""
    contact = Contact.query.get(contact_id)
    if not contact:
        return api_response("error", "Pesan tidak ditemukan.", status_code=404)

    db.session.delete(contact)
    db.session.commit()
    return api_response("success", "Pesan berhasil dihapus.")
