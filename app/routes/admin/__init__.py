"""
app/routes/admin/__init__.py — Admin Blueprint.

Satu blueprint "admin" dengan url_prefix="/admin".
Sub-modul (auth, dashboard, CRUD) di-import dan route-nya di-register di sini.
"""
from flask import Blueprint

admin_bp = Blueprint(
    "admin",
    __name__,
    url_prefix="/admin",
    template_folder="../../templates/admin",
    static_folder="../../static/admin",
    static_url_path="/admin/static",
)

# ── Import sub-route modules agar route-nya teregistrasi ──────
from . import auth       # noqa: E402, F401
from . import dashboard  # noqa: E402, F401
from . import profiles   # noqa: E402, F401
from . import skills     # noqa: E402, F401
from . import experiences  # noqa: E402, F401
from . import projects   # noqa: E402, F401
from . import contacts   # noqa: E402, F401
from . import upload     # noqa: E402, F401
from . import certificates # noqa: E402, F401
