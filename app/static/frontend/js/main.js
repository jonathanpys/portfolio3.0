/**
 * Public Portfolio Main JS
 * Handles data fetching and DOM injection
 */

document.addEventListener("DOMContentLoaded", () => {
    // Projects Pagination State
    window.projectsDataAll = [];
    window.projectsShowingAll = false;
    // Navbar Scroll Effect
    const navbar = document.getElementById('mainNavbar');
    const navLinks = document.getElementById('navLinks');
    const navDots = document.getElementById('navDots');

    if (navbar && navLinks && navDots) {
        let isExpandedByUser = false;
        
        window.addEventListener('scroll', () => {
            if (window.scrollY > 50) {
                if (!isExpandedByUser) navbar.classList.add('is-scrolled');
            } else {
                navbar.classList.remove('is-scrolled');
                isExpandedByUser = false;
            }
        });

        // Expand navbar when dots are clicked
        navDots.addEventListener('click', () => {
            navbar.classList.remove('is-scrolled');
            isExpandedByUser = true;
        });
    }

    // Scroll Reveal Observer
    const observerOptions = {
        threshold: 0.1,
        rootMargin: "0px"
    };

    window.scrollObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('active');
            } else {
                // Remove active to replay animation on scroll back
                entry.target.classList.remove('active');
            }
        });
    }, observerOptions);

    window.observeElements = function() {
        document.querySelectorAll('.reveal, .reveal-left, .reveal-right').forEach((el) => {
            window.scrollObserver.observe(el);
        });
    };

    // Observe static elements right away
    window.observeElements();

    fetchProfile().then(() => {
        if (window.observeElements) window.observeElements();
    });
    fetchSkills();
    fetchCertificates();
    fetchExperiences();
    fetchProjects();
    
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if(target) {
                target.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });

    // Contact form submit
    document.getElementById('contactForm').addEventListener('submit', submitContact);
    
    // Show More / Show Less Projects
    const btnShowMore = document.getElementById('btn-show-more-projects');
    if (btnShowMore) {
        btnShowMore.addEventListener('click', () => {
            window.projectsShowingAll = !window.projectsShowingAll;
            renderProjects();
        });
    }
    
    // Cursor Glow Effect
    initCursorGlow();
});

function initCursorGlow() {
    const cursorGlow = document.createElement('div');
    cursorGlow.classList.add('cursor-glow');
    document.body.appendChild(cursorGlow);

    document.addEventListener('mousemove', (e) => {
        cursorGlow.style.left = `${e.clientX}px`;
        cursorGlow.style.top = `${e.clientY}px`;
        
        if (!cursorGlow.classList.contains('active')) {
            cursorGlow.classList.add('active');
        }
    });

    document.addEventListener('mouseleave', () => {
        cursorGlow.classList.remove('active');
    });
}

async function fetchProfile() {
    try {
        const res = await fetch('/api/profile');
        const json = await res.json();
        
        if (json.status === 'success' && json.data) {
            const data = json.data;
            
            // Hero
            document.getElementById('hero-name').innerText = data.nama_lengkap || 'John Doe';
            document.getElementById('hero-subtitle').innerHTML = `Mahasiswa Sistem Informasi di Universitas Kristen Satya Wacana dengan <span class="text-accent fw-bold">IPK 3.93</span> yang Fokus pada Software Development.`;
            document.title = `${data.nama_panggilan || data.nama_lengkap} - Portfolio`;
            document.getElementById('footer-name').innerText = `© ${new Date().getFullYear()} ${data.nama_lengkap}`;
            if (document.getElementById('footer-address')) {
                document.getElementById('footer-address').innerText = data.alamat || 'Alamat belum diatur';
            }
            
            // Avatar
            const avatarContainer = document.getElementById('hero-avatar');
            if (data.foto_url) {
                avatarContainer.innerHTML = `<img src="${data.foto_url}" alt="${data.nama_lengkap}">`;
            } else {
                avatarContainer.innerHTML = `<div class="d-flex align-items-center justify-content-center w-100 h-100 fs-1 fw-bold rounded-circle bg-dark">${data.nama_lengkap ? data.nama_lengkap.charAt(0) : 'U'}</div>`;
            }

            // Socials (Static for now, could be dynamic later)
            document.getElementById('hero-social').innerHTML = `
                <a href="https://www.linkedin.com/in/jonathanpys" target="_blank"><i class="fa-brands fa-linkedin-in"></i><span class="social-text">LinkedIn</span></a>
                <a href="https://www.instagram.com/jonathanyudya/" target="_blank"><i class="fa-brands fa-instagram"></i><span class="social-text">Instagram</span></a>
                <a href="https://github.com/jonathanpys" target="_blank"><i class="fa-brands fa-github"></i><span class="social-text">GitHub</span></a>
                <a href="https://wa.me/6281326260461" target="_blank"><i class="fa-brands fa-whatsapp"></i><span class="social-text">WhatsApp</span></a>
            `;

            // About
            const aboutPhoto = document.getElementById('about-photo-container');
            if (data.foto_tentang_url) {
                aboutPhoto.innerHTML = `<img src="${data.foto_tentang_url}" alt="Foto Tentang ${data.nama_lengkap}" style="width: 100%; height: 100%; object-fit: cover;">`;
            }
            
            document.getElementById('about-title').innerText = `Tentang Saya`;
            document.getElementById('about-desc').innerText = data.deskripsi || 'Seorang profesional di bidang teknologi.';
            
            document.getElementById('about-info').innerHTML = `
                <li class="mb-2 d-flex align-items-start"><i class="fa-solid fa-envelope fa-fw text-accent me-3 mt-1"></i> <span class="text-break">${data.email || '-'}</span></li>
                <li class="mb-2 d-flex align-items-start"><i class="fa-solid fa-phone fa-fw text-accent me-3 mt-1"></i> <span>${data.telepon || '-'}</span></li>
                <li class="mb-2 d-flex align-items-start"><i class="fa-solid fa-graduation-cap fa-fw text-accent me-3 mt-1"></i> <span>${data.universitas || '-'}</span></li>
                <li class="mb-2 d-flex align-items-start"><i class="fa-solid fa-location-dot fa-fw text-accent me-3 mt-1"></i> <span>${data.tempat_lahir || '-'}</span></li>
            `;
        }
    } catch (err) {
        console.error("Error fetching profile", err);
        document.getElementById('hero-name').innerText = 'Error memuat data';
    }
}

async function fetchSkills() {
    try {
        const res = await fetch('/api/skills');
        const json = await res.json();
        const container = document.getElementById('skills-container');
        
        if (json.status === 'success' && json.data) {
            container.innerHTML = '';
            if (json.data.length === 0) {
                container.innerHTML = '<span class="text-muted">Belum ada skill yang ditambahkan.</span>';
                return;
            }
            
            json.data.forEach(skill => {
                let iconHtml = '';
                if (skill.icon_class) {
                    if (skill.icon_class.startsWith('http')) {
                        iconHtml = `<img src="${skill.icon_class}" alt="${skill.nama_skill}">`;
                    } else {
                        iconHtml = `<i class="${skill.icon_class}"></i>`;
                    }
                }
                
                container.innerHTML += `
                    <div class="skill-badge">
                        ${iconHtml} ${skill.nama_skill}
                    </div>
                `;
            });
        }
    } catch (err) {
        console.error("Error fetching skills", err);
    }
}

async function fetchCertificates() {
    try {
        const res = await fetch('/api/certificates');
        const json = await res.json();
        const container = document.getElementById('certificates-container');
        
        if (json.status === 'success' && json.data) {
            container.innerHTML = '';
            if (json.data.length === 0) {
                container.innerHTML = '<div class="col-12"><span class="text-muted">Belum ada sertifikasi yang ditambahkan.</span></div>';
                return;
            }
            
            json.data.forEach((cert, index) => {
                const imgSrc = cert.gambar_url || 'https://via.placeholder.com/600x400/141B2D/CCFF00?text=No+Image';
                const delayClass = (index % 4) * 100 === 0 ? '' : `delay-${(index % 4) * 100}`;
                
                // Menyimpan data ke window agar bisa diakses modal
                window.certificatesData = json.data;
                
                const iconSrc = cert.icon_penerbit_url || cert.gambar_url || 'https://via.placeholder.com/150/141B2D/CCFF00?text=Icon';
                
                container.innerHTML += `
                    <div class="col-12 col-md-6 col-lg-4 reveal ${delayClass}">
                        <div class="glass-card p-3 h-100 d-flex align-items-center" style="cursor: pointer; transition: transform 0.3s ease;" onclick="openCertModal(${index})" onmouseover="this.style.transform='scale(1.03)'" onmouseout="this.style.transform='scale(1)'">
                            <div style="width: 50px; height: 50px; border-radius: 8px; overflow: hidden; flex-shrink: 0; background: var(--bg-input); display: flex; align-items: center; justify-content: center; margin-right: 15px;">
                                <img src="${iconSrc}" alt="${cert.penerbit}" style="max-width: 100%; max-height: 100%; object-fit: contain;">
                            </div>
                            <h6 class="mb-0 fw-bold text-start" style="font-size: 0.95rem;">${cert.judul}</h6>
                        </div>
                    </div>
                `;
            });
            if (window.observeElements) window.observeElements();
        }
    } catch (err) {
        console.error("Error fetching certificates", err);
    }
}

function openCertModal(index) {
    if (!window.certificatesData || !window.certificatesData[index]) return;
    
    const cert = window.certificatesData[index];
    const imgSrc = cert.gambar_url || 'https://via.placeholder.com/800x600/141B2D/CCFF00?text=No+Image';
    
    document.getElementById('certModalImg').src = imgSrc;
    document.getElementById('certModalName').innerText = cert.judul;
    document.querySelector('#certModalPublisher span').innerText = cert.penerbit;
    document.querySelector('#certModalDate span').innerText = cert.tanggal_terbit ? cert.tanggal_terbit : 'Tanggal tidak tersedia';
    
    const linkContainer = document.getElementById('certModalLinkContainer');
    if (cert.link_kredensial) {
        linkContainer.innerHTML = `<a href="${cert.link_kredensial}" target="_blank" class="btn btn-outline-accent mt-3 px-4 py-2 rounded-pill"><i class="fa-solid fa-arrow-up-right-from-square me-2"></i>Lihat Kredensial Asli</a>`;
    } else {
        linkContainer.innerHTML = '';
    }
    
    const modal = new bootstrap.Modal(document.getElementById('certModal'));
    modal.show();
}

function formatDateId(dateString) {
    if (!dateString || dateString.toLowerCase() === 'sekarang') return 'Sekarang';
    const date = new Date(dateString);
    if (isNaN(date.getTime())) return dateString;
    const months = ['Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni', 'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember'];
    return `${date.getDate()} ${months[date.getMonth()]} ${date.getFullYear()}`;
}

async function fetchExperiences() {
    try {
        const res = await fetch('/api/experiences');
        const json = await res.json();
        const container = document.getElementById('experience-container');
        
        if (json.status === 'success' && json.data) {
            container.innerHTML = '';
            if (json.data.length === 0) {
                container.innerHTML = '<span class="text-muted">Belum ada pengalaman yang ditambahkan.</span>';
                return;
            }
            
            let html = '';
            json.data.forEach((exp, index) => {
                let dateText = exp.durasi || 'Tahun Tidak Diketahui';
                if (dateText !== 'Tahun Tidak Diketahui') {
                    const parts = dateText.split('—').map(p => p.trim());
                    if (parts.length === 2) {
                        dateText = `${formatDateId(parts[0])} — ${formatDateId(parts[1])}`;
                    }
                }
                
                const catBadge = exp.kategori === 'pekerjaan' ? '<span class="badge bg-primary ms-2" style="font-size: 0.7rem;">Kerja</span>' : 
                                 exp.kategori === 'organisasi' ? '<span class="badge bg-info ms-2" style="font-size: 0.7rem;">Organisasi</span>' :
                                 '<span class="badge bg-warning text-dark ms-2" style="font-size: 0.7rem;">Prestasi</span>';
                
                const dotColorClass = exp.kategori === 'organisasi' ? 'dot-info' : 
                                      exp.kategori === 'prestasi' ? 'dot-warning' : '';
                
                const delayClass = (index % 5) * 100 === 0 ? '' : `delay-${(index % 5) * 100}`;
                html += `
                    <div class="timeline-item reveal ${delayClass}">
                        <div class="timeline-dot ${dotColorClass}"></div>
                        <div class="timeline-content hover-container">
                            <div class="timeline-date">${dateText}</div>
                            <h4 class="mb-1 d-flex align-items-center">${exp.posisi} ${catBadge}</h4>
                            <div class="text-accent mb-2 fw-medium">${exp.perusahaan}</div>
                            <div class="hover-desc-wrapper">
                                <p class="text-muted mb-0 hover-desc">${exp.deskripsi || ''}</p>
                            </div>
                        </div>
                    </div>
                `;
            });
            container.innerHTML = html;
            if (window.observeElements) window.observeElements();
        }
    } catch (err) {
        console.error("Error fetching experiences", err);
    }
}

async function fetchProjects() {
    try {
        const res = await fetch('/api/projects');
        const json = await res.json();
        
        if (json.status === 'success' && json.data) {
            window.projectsDataAll = json.data;
            window.projectsData = json.data;
            renderProjects();
        }
    } catch (err) {
        console.error("Error fetching projects", err);
    }
}

function renderProjects() {
    const container = document.getElementById('projects-container');
    const showMoreContainer = document.getElementById('projects-show-more-container');
    
    container.innerHTML = '';
    
    if (!window.projectsDataAll || window.projectsDataAll.length === 0) {
        container.innerHTML = '<div class="col-12"><span class="text-muted">Belum ada proyek yang ditambahkan.</span></div>';
        if (showMoreContainer) showMoreContainer.classList.add('d-none');
        return;
    }
    
    const limit = window.projectsShowingAll ? window.projectsDataAll.length : 3;
    const projectsToShow = window.projectsDataAll.slice(0, limit);
    
    projectsToShow.forEach((proj, index) => {
        const imgSrc = proj.gambar_url || 'https://via.placeholder.com/600x400/141B2D/CCFF00?text=No+Image';
        
        container.innerHTML += `
            <div class="col-md-6 col-lg-4">
                <div class="glass-card project-card" style="cursor: pointer; transition: transform 0.3s ease;" onclick="openProjectModal(${index})" onmouseover="this.style.transform='scale(1.03)'" onmouseout="this.style.transform='scale(1)'">
                    <div class="project-img-wrapper">
                        <img src="${imgSrc}" alt="${proj.judul}">
                    </div>
                    <div class="project-card-body text-center">
                        <h4 class="project-title mb-0">${proj.judul}</h4>
                    </div>
                </div>
            </div>
        `;
    });
    
    if (showMoreContainer) {
        if (window.projectsDataAll.length > 3) {
            showMoreContainer.classList.remove('d-none');
            
            const btnIcon = showMoreContainer.querySelector('i');
            const btnText = showMoreContainer.querySelector('.project-link-text');
            
            if (window.projectsShowingAll) {
                btnIcon.className = 'fa-solid fa-arrow-up m-0';
                btnText.innerText = 'Show Less';
            } else {
                btnIcon.className = 'fa-solid fa-arrow-down m-0';
                btnText.innerText = 'Show More';
            }
        } else {
            showMoreContainer.classList.add('d-none');
        }
    }
}

function openProjectModal(index) {
    if (!window.projectsData || !window.projectsData[index]) return;
    
    const proj = window.projectsData[index];
    const imgSrc = proj.gambar_url || 'https://via.placeholder.com/800x600/141B2D/CCFF00?text=No+Image';
    const imgContainer = document.getElementById('projectModalImgContainer');
    
    if (proj.link_youtube) {
        // Ekstrak video ID dari URL
        let videoId = '';
        const matchV = proj.link_youtube.match(/[?&]v=([^&]+)/);
        const matchShort = proj.link_youtube.match(/youtu\.be\/([^?]+)/);
        const matchEmbed = proj.link_youtube.match(/youtube\.com\/embed\/([^?]+)/);
        const matchShorts = proj.link_youtube.match(/youtube\.com\/shorts\/([^?]+)/);
        
        if (matchV) videoId = matchV[1];
        else if (matchShort) videoId = matchShort[1];
        else if (matchEmbed) videoId = matchEmbed[1];
        else if (matchShorts) videoId = matchShorts[1];
        
        if (videoId) {
            imgContainer.innerHTML = `
                <div style="position: relative; width: 100%; padding-bottom: 56.25%; height: 0; border-radius: 8px; overflow: hidden; box-shadow: 0 10px 30px rgba(0,0,0,0.5);">
                    <iframe src="https://www.youtube.com/embed/${videoId}" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: 0;" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
                </div>
            `;
        } else {
            // Fallback jika bukan URL YouTube yang valid
            imgContainer.innerHTML = `<img id="projectModalImg" src="${imgSrc}" alt="Proyek" style="max-width: 100%; max-height: 50vh; object-fit: contain; border-radius: 8px; box-shadow: 0 10px 30px rgba(0,0,0,0.5);">`;
        }
    } else {
        imgContainer.innerHTML = `<img id="projectModalImg" src="${imgSrc}" alt="Proyek" style="max-width: 100%; max-height: 50vh; object-fit: contain; border-radius: 8px; box-shadow: 0 10px 30px rgba(0,0,0,0.5);">`;
    }
    
    document.getElementById('projectModalName').innerText = proj.judul;
    document.getElementById('projectModalDesc').innerText = proj.deskripsi || 'Tidak ada deskripsi.';
    
    const linkContainer = document.getElementById('projectModalLinkContainer');
    if (proj.link_project) {
        linkContainer.innerHTML = `
            <a href="${proj.link_project}" target="_blank" class="btn btn-outline-accent project-link-btn-custom" title="Lihat Proyek">
                <i class="fa-solid fa-arrow-up-right-from-square m-0"></i>
                <span class="project-link-text">Open Project</span>
            </a>
        `;
    } else {
        linkContainer.innerHTML = '';
    }
    
    const modal = new bootstrap.Modal(document.getElementById('projectModal'));
    modal.show();
}

async function submitContact(e) {
    e.preventDefault();
    
    const form = e.target;
    const btn = document.getElementById('btnSubmitContact');
    const originalBtnText = btn.innerHTML;
    
    // Disable button & loading
    btn.disabled = true;
    btn.innerHTML = `<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Mengirim...`;
    
    const formData = new FormData(form);
    const data = Object.fromEntries(formData.entries());
    
    try {
        const res = await fetch('/api/contact', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        
        const result = await res.json();
        
        if (res.ok && result.status === 'success') {
            showToast(result.message || 'Pesan berhasil dikirim!', 'success');
            form.reset();
        } else {
            showToast(result.message || 'Gagal mengirim pesan.', 'error');
        }
    } catch (err) {
        showToast('Terjadi kesalahan jaringan.', 'error');
    } finally {
        btn.disabled = false;
        btn.innerHTML = originalBtnText;
    }
}

// Premium Custom Toast Helper
function showToast(text, type) {
    let container = document.getElementById('custom-toast-container');
    if (!container) {
        container = document.createElement('div');
        container.id = 'custom-toast-container';
        document.body.appendChild(container);
    }
    
    const toast = document.createElement('div');
    toast.className = `custom-toast toast-${type}`;
    
    const iconClass = type === 'success' ? 'fa-solid fa-circle-check' : 'fa-solid fa-circle-exclamation';
    
    toast.innerHTML = `
        <i class="${iconClass} toast-icon"></i>
        <span>${text}</span>
        <div class="toast-progress" style="animation-duration: 3s;"></div>
    `;
    
    container.appendChild(toast);
    
    // Auto remove after 3s
    setTimeout(() => {
        toast.classList.add('toast-hiding');
        toast.addEventListener('animationend', () => {
            toast.remove();
        });
    }, 3000);
}
