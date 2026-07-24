/**
 * app/static/admin/js/admin.js
 * Handle all SPA logic for Admin Dashboard via Fetch API.
 */

let currentEntity = 'profiles';
let currentAction = 'create'; // 'create' or 'update'
let currentId = null;

// Initialize on load
document.addEventListener("DOMContentLoaded", () => {
    // Load default tab (profiles)
    loadData('profiles');

    // Attach click listeners to tabs
    document.querySelectorAll('.nav-link[data-bs-toggle="tab"]').forEach(tab => {
        tab.addEventListener('shown.bs.tab', (e) => {
            currentEntity = e.target.getAttribute('data-entity');
            loadData(currentEntity);
        });
    });

    // Attach form submit handler
    document.getElementById('crudForm').addEventListener('submit', submitForm);
});

/**
 * Fetch data for a specific entity and render the table
 */
async function loadData(entity) {
    const tbody = document.querySelector(`#${entity}-table tbody`);
    if (!tbody) return;
    
    tbody.innerHTML = '<tr><td colspan="5" class="text-center">Loading...</td></tr>';
    
    try {
        const res = await fetch(`/admin/${entity}`, {
            headers: { "Accept": "application/json" }
        });
        
        if (res.status === 401) {
            window.location.href = '/admin/login';
            return;
        }
        
        const json = await res.json();
        const data = json.data || [];
        
        tbody.innerHTML = '';
        if (data.length === 0) {
            tbody.innerHTML = '<tr><td colspan="5" class="text-center text-muted">Belum ada data</td></tr>';
            return;
        }

        data.forEach(item => {
            const tr = document.createElement('tr');
            
            // Kolom tabel berbeda tergantung entity
            if (entity === 'profiles') {
                tr.innerHTML = `
                    <td>${item.nama_lengkap || '-'}</td>
                    <td>${item.email || '-'}</td>
                    <td>${item.universitas || '-'}</td>
                    <td>
                        <button class="btn btn-sm btn-info" onclick="openForm('profiles', ${item.id})">Edit</button>
                    </td>
                `;
            } else if (entity === 'skills') {
                const iconDisplay = item.icon_class ? 
                    (item.icon_class.startsWith('http') ? `<img src="${item.icon_class}" height="30">` : `<span>${item.icon_class}</span>`) 
                    : '-';
                tr.innerHTML = `
                    <td>${item.id}</td>
                    <td>${item.nama_skill}</td>
                    <td>${iconDisplay}</td>
                    <td>
                        <button class="btn btn-sm btn-info" onclick="openForm('skills', ${item.id})">Edit</button>
                        <button class="btn btn-sm btn-danger" onclick="deleteData('skills', ${item.id})">Hapus</button>
                    </td>
                `;
            } else if (entity === 'experiences') {
                const catBadge = item.kategori === 'pekerjaan' ? '<span class="badge bg-primary">Kerja</span>' : 
                                 item.kategori === 'organisasi' ? '<span class="badge bg-info">Organisasi</span>' :
                                 '<span class="badge bg-warning text-dark">Prestasi</span>';
                tr.innerHTML = `
                    <td>${item.posisi} <br>${catBadge}</td>
                    <td>${item.perusahaan}</td>
                    <td>${item.durasi || '-'}</td>
                    <td>
                        <button class="btn btn-sm btn-info" onclick="openForm('experiences', ${item.id})">Edit</button>
                        <button class="btn btn-sm btn-danger" onclick="deleteData('experiences', ${item.id})">Hapus</button>
                    </td>
                `;
            } else if (entity === 'projects') {
                const imgDisplay = item.gambar_url ? `<img src="${item.gambar_url}" height="30">` : '-';
                tr.innerHTML = `
                    <td>${item.judul}</td>
                    <td>${item.link_project ? `<a href="${item.link_project}" target="_blank" class="text-tertiary">Link</a>` : '-'}</td>
                    <td>${imgDisplay}</td>
                    <td>
                        <button class="btn btn-sm btn-info" onclick="openForm('projects', ${item.id})">Edit</button>
                        <button class="btn btn-sm btn-danger" onclick="deleteData('projects', ${item.id})">Hapus</button>
                    </td>
                `;
            } else if (entity === 'certificates') {
                tr.innerHTML = `
                    <td>${item.judul}</td>
                    <td>${item.penerbit}</td>
                    <td>${item.tanggal_terbit || '-'}</td>
                    <td>${item.link_kredensial ? `<a href="${item.link_kredensial}" target="_blank" class="text-tertiary">Link</a>` : '-'}</td>
                    <td>
                        <button class="btn btn-sm btn-info" onclick="openForm('certificates', ${item.id})">Edit</button>
                        <button class="btn btn-sm btn-danger" onclick="deleteData('certificates', ${item.id})">Hapus</button>
                    </td>
                `;
            } else if (entity === 'contacts') {
                tr.innerHTML = `
                    <td>${item.created_at || '-'}</td>
                    <td>${item.nama} (${item.email})</td>
                    <td>${item.subjek}</td>
                    <td>${item.status}</td>
                    <td>
                        <button class="btn btn-sm btn-danger" onclick="deleteData('contacts', ${item.id})">Hapus</button>
                    </td>
                `;
            }
            tbody.appendChild(tr);
        });
    } catch (err) {
        tbody.innerHTML = `<tr><td colspan="5" class="text-center text-danger">Error fetching data: ${err.message}</td></tr>`;
    }
}

/**
 * Open form modal for create or update
 */
async function openForm(entity, id = null) {
    currentEntity = entity;
    currentId = id;
    currentAction = id ? 'update' : 'create';
    
    document.getElementById('crudAlert').classList.add('d-none');
    document.getElementById('crudModalLabel').innerText = (id ? 'Edit ' : 'Tambah ') + entity.charAt(0).toUpperCase() + entity.slice(1);
    
    // Inject form fields based on entity
    const fieldsContainer = document.getElementById('dynamicFormFields');
    fieldsContainer.innerHTML = getFormFields(entity);

    // If update, fetch existing data and populate
    if (id) {
        try {
            const res = await fetch(`/admin/${entity}/${id}`, {
                headers: { "Accept": "application/json" }
            });
            const json = await res.json();
            if (res.ok && json.data) {
                const form = document.getElementById('crudForm');
                const data = json.data;
                for (let key in data) {
                    let el = form.elements[key];
                    if (el) {
                        if (el.type === 'file') continue;
                        el.value = data[key] || '';
                    }
                }
                
                // Populate dates for experience if possible
                if (entity === 'experiences' && data.durasi) {
                    const parts = data.durasi.split('—').map(p => p.trim());
                    if (parts.length === 2) {
                        if (form.elements['tanggal_mulai']) form.elements['tanggal_mulai'].value = parts[0];
                        if (parts[1] !== 'Sekarang' && form.elements['tanggal_selesai']) {
                            form.elements['tanggal_selesai'].value = parts[1];
                        }
                    }
                }
            }
        } catch (err) {
            console.error('Error fetching details', err);
        }
    }

    const modal = new bootstrap.Modal(document.getElementById('crudModal'));
    modal.show();
}

/**
 * Define HTML structure for forms
 */
function getFormFields(entity) {
    if (entity === 'profiles') {
        return `
            <div class="col-md-6">
                <label class="form-label">Nama Lengkap <span class="text-danger">*</span></label>
                <div class="input-group">
                    <span class="input-group-text text-muted"><i class="fa-solid fa-user"></i></span>
                    <input type="text" class="form-control border-start-0 ps-0" name="nama_lengkap" required placeholder="John Doe">
                </div>
            </div>
            <div class="col-md-6">
                <label class="form-label">Nama Panggilan</label>
                <div class="input-group">
                    <span class="input-group-text text-muted"><i class="fa-regular fa-user"></i></span>
                    <input type="text" class="form-control border-start-0 ps-0" name="nama_panggilan" placeholder="John">
                </div>
            </div>
            <div class="col-md-6">
                <label class="form-label">Email</label>
                <div class="input-group">
                    <span class="input-group-text text-muted"><i class="fa-solid fa-envelope"></i></span>
                    <input type="email" class="form-control border-start-0 ps-0" name="email" placeholder="john@example.com">
                </div>
            </div>
            <div class="col-md-6">
                <label class="form-label">Telepon</label>
                <div class="input-group">
                    <span class="input-group-text text-muted"><i class="fa-solid fa-phone"></i></span>
                    <input type="text" class="form-control border-start-0 ps-0" name="telepon" placeholder="0812...">
                </div>
            </div>
            <div class="col-md-6">
                <label class="form-label">Universitas</label>
                <div class="input-group">
                    <span class="input-group-text text-muted"><i class="fa-solid fa-graduation-cap"></i></span>
                    <input type="text" class="form-control border-start-0 ps-0" name="universitas" placeholder="Nama Universitas">
                </div>
            </div>
            <div class="col-md-6">
                <label class="form-label">Fakultas</label>
                <div class="input-group">
                    <span class="input-group-text text-muted"><i class="fa-solid fa-building"></i></span>
                    <input type="text" class="form-control border-start-0 ps-0" name="fakultas" placeholder="Fakultas">
                </div>
            </div>
            <div class="col-md-6">
                <label class="form-label">Program Studi</label>
                <div class="input-group">
                    <span class="input-group-text text-muted"><i class="fa-solid fa-book"></i></span>
                    <input type="text" class="form-control border-start-0 ps-0" name="prodi" placeholder="Program Studi">
                </div>
            </div>
            <div class="col-md-6">
                <label class="form-label">Semester</label>
                <div class="input-group">
                    <span class="input-group-text text-muted"><i class="fa-solid fa-hashtag"></i></span>
                    <input type="text" class="form-control border-start-0 ps-0" name="semester" placeholder="Misal: 6">
                </div>
            </div>
            <div class="col-md-6">
                <label class="form-label">Tempat Lahir</label>
                <div class="input-group">
                    <span class="input-group-text text-muted"><i class="fa-solid fa-location-dot"></i></span>
                    <input type="text" class="form-control border-start-0 ps-0" name="tempat_lahir" placeholder="Kota">
                </div>
            </div>
            <div class="col-md-6">
                <label class="form-label">Tanggal Lahir</label>
                <div class="input-group">
                    <span class="input-group-text text-muted"><i class="fa-solid fa-calendar-days"></i></span>
                    <input type="date" class="form-control border-start-0 ps-0" name="tanggal_lahir">
                </div>
            </div>
            <div class="col-md-6">
                <label class="form-label">Foto Profil (Upload)</label>
                <div class="input-group">
                    <span class="input-group-text text-muted"><i class="fa-solid fa-image"></i></span>
                    <input type="file" class="form-control border-start-0 ps-0" name="foto" accept="image/png, image/jpeg, image/webp">
                </div>
            </div>
            <div class="col-md-6">
                <label class="form-label">Foto Tentang Saya</label>
                <div class="input-group">
                    <span class="input-group-text text-muted"><i class="fa-solid fa-address-card"></i></span>
                    <input type="file" class="form-control border-start-0 ps-0" name="foto_tentang" accept="image/png, image/jpeg, image/webp">
                </div>
            </div>
            <div class="col-md-12">
                <label class="form-label">Alamat</label>
                <div class="input-group">
                    <span class="input-group-text bg-transparent text-muted align-items-start pt-3"><i class="fa-solid fa-map-pin"></i></span>
                    <textarea class="form-control border-start-0 ps-0" rows="3" name="alamat" placeholder="Alamat lengkap..."></textarea>
                </div>
            </div>
            <div class="col-md-12">
                <label class="form-label">Deskripsi Diri</label>
                <div class="input-group">
                    <span class="input-group-text bg-transparent text-muted align-items-start pt-3"><i class="fa-solid fa-align-left"></i></span>
                    <textarea class="form-control border-start-0 ps-0" rows="5" name="deskripsi" placeholder="Tuliskan deskripsi singkat mengenai diri Anda..."></textarea>
                </div>
            </div>
        `;
    } else if (entity === 'skills') {
        return `
            <div class="col-md-12">
                <label class="form-label">Nama Skill <span class="text-danger">*</span></label>
                <div class="input-group">
                    <span class="input-group-text text-muted"><i class="fa-solid fa-code"></i></span>
                    <input type="text" class="form-control border-start-0 ps-0" name="nama_skill" required placeholder="Python, React, dll">
                </div>
            </div>
            <div class="col-md-12 mt-4">
                <label class="form-label fw-bold text-accent"><i class="fa-solid fa-icons me-2"></i>Pilih Icon Skill (Satu Saja)</label>
                
                <div class="card bg-transparent border-secondary p-3 mt-2">
                    <label class="form-label text-muted small">Opsi A: Upload Gambar</label>
                    <div class="input-group mb-3">
                        <span class="input-group-text text-muted"><i class="fa-solid fa-upload"></i></span>
                        <input type="file" class="form-control border-start-0 ps-0" name="icon" accept="image/png, image/jpeg, image/webp">
                    </div>
                    
                    <div class="text-center text-muted mb-3 small">-- ATAU --</div>
                    
                    <label class="form-label text-muted small">Opsi B: FontAwesome Class</label>
                    <div class="input-group">
                        <span class="input-group-text text-muted"><i class="fa-brands fa-font-awesome"></i></span>
                        <input type="text" class="form-control border-start-0 ps-0" name="icon_class" placeholder="fa-brands fa-python">
                    </div>
                </div>
            </div>
        `;
    } else if (entity === 'experiences') {
        return `
            <div class="col-md-6">
                <label class="form-label">Posisi <span class="text-danger">*</span></label>
                <div class="input-group">
                    <span class="input-group-text text-muted"><i class="fa-solid fa-user-tie"></i></span>
                    <input type="text" class="form-control border-start-0 ps-0" name="posisi" required placeholder="Frontend Engineer">
                </div>
            </div>
            <div class="col-md-6">
                <label class="form-label">Perusahaan <span class="text-danger">*</span></label>
                <div class="input-group">
                    <span class="input-group-text text-muted"><i class="fa-solid fa-building"></i></span>
                    <input type="text" class="form-control border-start-0 ps-0" name="perusahaan" required placeholder="PT Contoh">
                </div>
            </div>
            <div class="col-md-6">
                <label class="form-label">Kategori <span class="text-danger">*</span></label>
                <div class="input-group">
                    <span class="input-group-text text-muted"><i class="fa-solid fa-tags"></i></span>
                    <select class="form-select border-start-0 ps-0" name="kategori" required>
                        <option value="pekerjaan">Pekerjaan</option>
                        <option value="organisasi">Organisasi</option>
                        <option value="prestasi">Prestasi / Lomba</option>
                    </select>
                </div>
            </div>
            <div class="col-md-12">
                <label class="form-label">Tanggal Mulai</label>
                <div class="input-group">
                    <span class="input-group-text text-muted"><i class="fa-solid fa-calendar-plus"></i></span>
                    <input type="date" class="form-control border-start-0 ps-0" name="tanggal_mulai">
                </div>
            </div>
            <div class="col-md-6">
                <label class="form-label">Tanggal Selesai (Kosongkan jika aktif)</label>
                <div class="input-group">
                    <span class="input-group-text text-muted"><i class="fa-solid fa-calendar-check"></i></span>
                    <input type="date" class="form-control border-start-0 ps-0" name="tanggal_selesai">
                </div>
            </div>
            <div class="col-md-12">
                <label class="form-label">Deskripsi</label>
                <div class="input-group">
                    <span class="input-group-text bg-transparent text-muted align-items-start pt-3"><i class="fa-solid fa-align-left"></i></span>
                    <textarea class="form-control border-start-0 ps-0" rows="4" name="deskripsi_pekerjaan" placeholder="Jelaskan peran Anda..."></textarea>
                </div>
            </div>
        `;
    } else if (entity === 'projects') {
        return `
            <div class="col-md-12">
                <label class="form-label">Judul <span class="text-danger">*</span></label>
                <div class="input-group">
                    <span class="input-group-text text-muted"><i class="fa-solid fa-laptop-code"></i></span>
                    <input type="text" class="form-control border-start-0 ps-0" name="judul" required placeholder="Aplikasi E-Commerce">
                </div>
            </div>
            <div class="col-md-12">
                <label class="form-label">Link Project</label>
                <div class="input-group">
                    <span class="input-group-text text-muted"><i class="fa-solid fa-link"></i></span>
                    <input type="url" class="form-control border-start-0 ps-0" name="link_project" placeholder="https://github.com/...">
                </div>
            </div>
            <div class="col-md-12">
                <label class="form-label">Link YouTube (Opsional)</label>
                <div class="input-group">
                    <span class="input-group-text text-muted"><i class="fa-brands fa-youtube"></i></span>
                    <input type="url" class="form-control border-start-0 ps-0" name="link_youtube" placeholder="https://www.youtube.com/watch?v=...">
                </div>
            </div>
            <div class="col-md-12">
                <label class="form-label">Gambar (Upload)</label>
                <div class="input-group">
                    <span class="input-group-text text-muted"><i class="fa-solid fa-image"></i></span>
                    <input type="file" class="form-control border-start-0 ps-0" name="gambar" accept="image/png, image/jpeg, image/webp">
                </div>
            </div>
            <div class="col-md-12">
                <label class="form-label">Deskripsi</label>
                <div class="input-group">
                    <span class="input-group-text bg-transparent text-muted align-items-start pt-3"><i class="fa-solid fa-align-left"></i></span>
                    <textarea class="form-control border-start-0 ps-0" rows="4" name="deskripsi" placeholder="Deskripsi singkat tentang fitur proyek..."></textarea>
                </div>
            </div>
        `;
    } else if (entity === 'certificates') {
        return `
            <div class="col-md-6">
                <label class="form-label">Judul Sertifikasi <span class="text-danger">*</span></label>
                <div class="input-group">
                    <span class="input-group-text text-muted"><i class="fa-solid fa-certificate"></i></span>
                    <input type="text" class="form-control border-start-0 ps-0" name="judul" required placeholder="AWS Certified Developer">
                </div>
            </div>
            <div class="col-md-6">
                <label class="form-label">Penerbit <span class="text-danger">*</span></label>
                <div class="input-group">
                    <span class="input-group-text text-muted"><i class="fa-solid fa-building"></i></span>
                    <input type="text" class="form-control border-start-0 ps-0" name="penerbit" required placeholder="Amazon Web Services">
                </div>
            </div>
            <div class="col-md-6">
                <label class="form-label">Tanggal Terbit</label>
                <div class="input-group">
                    <span class="input-group-text text-muted"><i class="fa-solid fa-calendar-check"></i></span>
                    <input type="date" class="form-control border-start-0 ps-0" name="tanggal_terbit">
                </div>
            </div>
            <div class="col-md-6">
                <label class="form-label">Link Kredensial</label>
                <div class="input-group">
                    <span class="input-group-text text-muted"><i class="fa-solid fa-link"></i></span>
                    <input type="url" class="form-control border-start-0 ps-0" name="link_kredensial" placeholder="https://www.credly.com/...">
                </div>
            </div>
            <div class="col-md-6">
                <label class="form-label">Icon Penerbit (Opsional)</label>
                <div class="input-group">
                    <span class="input-group-text text-muted"><i class="fa-solid fa-image"></i></span>
                    <input type="file" class="form-control border-start-0 ps-0" name="icon_penerbit" accept="image/png, image/jpeg, image/webp">
                </div>
            </div>
            <div class="col-md-12">
                <label class="form-label">Gambar Full Sertifikat (Opsional)</label>
                <div class="input-group">
                    <span class="input-group-text text-muted"><i class="fa-solid fa-image"></i></span>
                    <input type="file" class="form-control border-start-0 ps-0" name="gambar" accept="image/png, image/jpeg, image/webp, application/pdf">
                </div>
            </div>
        `;
    }
    return '';
}

/**
 * Submit Form via Fetch (using FormData to support File Uploads)
 */
async function submitForm(e) {
    if (e) e.preventDefault();
    
    const form = document.getElementById('crudForm');
    if (!form.reportValidity()) return;

    const saveBtn = document.getElementById('saveBtn');
    const alertBox = document.getElementById('crudAlert');
    
    saveBtn.disabled = true;
    saveBtn.innerText = 'Menyimpan...';
    alertBox.classList.add('d-none');

    const formData = new FormData(form);
    
    // Determine method and URL
    let url = `/admin/${currentEntity}`;
    let method = 'POST';
    if (currentAction === 'update') {
        url += `/${currentId}`;
        method = 'PUT';
    }

    try {
        const res = await fetch(url, {
            method: method,
            headers: { "Accept": "application/json" },
            body: formData
        });
        
        const result = await res.json();
        
        if (res.ok && result.status === 'success') {
            // Close modal
            const modalEl = document.getElementById('crudModal');
            const modal = bootstrap.Modal.getInstance(modalEl);
            modal.hide();
            
            // Reload table
            loadData(currentEntity);
        } else {
            alertBox.innerText = result.message || 'Terjadi kesalahan pada input.';
            alertBox.classList.remove('d-none');
        }
    } catch (err) {
        alertBox.innerText = `Network error: ${err.message}`;
        alertBox.classList.remove('d-none');
    } finally {
        saveBtn.disabled = false;
        saveBtn.innerText = 'Simpan';
    }
}

/**
 * Delete data
 */
async function deleteData(entity, id) {
    if (!confirm('Apakah Anda yakin ingin menghapus data ini?')) return;
    
    try {
        const res = await fetch(`/admin/${entity}/${id}`, { 
            method: 'DELETE',
            headers: { "Accept": "application/json" }
        });
        if (res.ok) {
            loadData(entity);
        } else {
            const json = await res.json();
            alert(`Gagal menghapus: ${json.message}`);
        }
    } catch (err) {
        alert(`Error: ${err.message}`);
    }
}
