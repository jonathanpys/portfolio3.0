"""
app/models/__init__.py — Re-export semua model.

Semua model di-mapping ke tabel existing di TiDB:
    - User       → tabel `users`
    - Profile    → tabel `profiles`
    - Skill      → tabel `skills`
    - Experience → tabel `experiences`
    - Project    → tabel `projects`

Tabel `contacts` ditambahkan untuk fitur Resend + DB.
"""
from app.models.user import User                # noqa: F401
from app.models.profile import Profile          # noqa: F401
from app.models.skill import Skill              # noqa: F401
from app.models.experience import Experience    # noqa: F401
from app.models.project import Project          # noqa: F401
from app.models.contact import Contact          # noqa: F401
from app.models.certificate import Certificate  # noqa: F401
