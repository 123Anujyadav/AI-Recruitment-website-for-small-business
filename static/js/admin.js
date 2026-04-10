const API = '/admin-panel/api';
let currentSection = 'overview';
let statsChartInstance = null;
let cachedStats = null;

// ─── CSRF ───
function getCsrf() {
  const m = document.cookie.match(/csrftoken=([^;]+)/);
  return m ? m[1] : '';
}

async function req(method, path, body) {
  const opts = { method, credentials: 'include',
    headers: { 'Content-Type': 'application/json', 'X-CSRFToken': getCsrf() } };
  if (body) opts.body = JSON.stringify(body);
  const r = await fetch(API + path, opts);
  return { ok: r.ok, status: r.status, data: await r.json().catch(() => ({})) };
}

// ─── TOAST ───
function toast(msg, type='success') {
  const t = document.getElementById('toast');
  document.getElementById('toast-msg').textContent = msg;
  t.className = `show ${type}`;
  setTimeout(() => t.className = '', 2800);
}

// ─── AUTH ───
async function doLogin() {
  const btn = document.getElementById('login-btn');
  const err = document.getElementById('login-error');
  btn.textContent = 'Signing in…'; btn.disabled = true;
  err.style.display = 'none';
  // Fetch CSRF first
  await req('GET', '/login');
  const r = await req('POST', '/login', {
    username: document.getElementById('admin-user').value,
    password: document.getElementById('admin-pass').value
  });
  btn.textContent = 'Sign In to Admin Panel'; btn.disabled = false;
  if (r.ok) {
    document.getElementById('sidebar-username').textContent = r.data.username || 'Admin';
    document.getElementById('avatar-initials').textContent = (r.data.username || 'A')[0].toUpperCase();
    document.getElementById('login-screen').style.display = 'none';
    document.getElementById('app').style.display = 'flex';
    loadStats();
  } else {
    err.textContent = r.data.error || 'Login failed';
    err.style.display = 'block';
  }
}
document.addEventListener('keydown', e => {
  if (e.key === 'Enter' && document.getElementById('login-screen').style.display !== 'none') doLogin();
});

async function doLogout() {
  await req('POST', '/logout');
  location.reload();
}

async function checkSession() {
  const r = await req('GET', '/check');
  if (r.ok && r.data.authenticated) {
    document.getElementById('sidebar-username').textContent = r.data.username || 'Admin';
    document.getElementById('avatar-initials').textContent = (r.data.username || 'A')[0].toUpperCase();
    document.getElementById('login-screen').style.display = 'none';
    document.getElementById('app').style.display = 'flex';
    loadStats();
  }
}
checkSession();

// ─── NAVIGATION ───
const sectionMeta = {
  overview:     { title: 'Dashboard',           sub: 'Platform overview & statistics' },
  users:        { title: 'Users',               sub: 'Manage all user accounts' },
  jobs:         { title: 'Jobs',                sub: 'Manage job listings' },
  applications: { title: 'Applications',        sub: 'View & update all applications' },
  candidates:   { title: 'Candidate Profiles',  sub: 'Manage candidate information' },
  employers:    { title: 'Employer Profiles',   sub: 'Manage employer companies' },
};

function showSection(name, el) {
  document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
  document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
  document.getElementById('section-' + name).classList.add('active');
  el.classList.add('active');
  currentSection = name;
  const m = sectionMeta[name];
  document.getElementById('page-title').textContent = m.title;
  document.getElementById('page-sub').textContent = m.sub;
  const loaders = { overview: loadStats, users: loadUsers, jobs: loadJobs, applications: loadApplications, candidates: loadCandidates, employers: loadEmployers };
  if (loaders[name]) loaders[name]();
}

function closeModal(id) { document.getElementById(id).classList.remove('open'); }
function openModal(id)  { document.getElementById(id).classList.add('open'); }

// ─── STATS ───
async function loadStats() {
  const r = await req('GET', '/stats');
  if (!r.ok) {
    document.getElementById('stats-grid').innerHTML = '<div class="empty">Failed to load platform stats. Please refresh.</div>';
    return;
  }
  cachedStats = r.data;
  const { total_users, total_jobs, total_applications, total_candidates, total_employers } = r.data;
  const cards = [
    { label:'Total Jobs',         value: total_jobs,         icon:'💼' },
    { label:'Applications',       value: total_applications, icon:'📋' },
    { label:'Candidates',         value: total_candidates,   icon:'🎯' },
    { label:'Employers',          value: total_employers,    icon:'🏢' },
  ];
  document.getElementById('stats-grid').innerHTML = cards.map(c => `
    <div class="stat-card">
      <div class="label">${c.label}</div>
      <div class="value">${c.value}</div>
      <div class="icon-bg">${c.icon}</div>
    </div>`).join('');

  // Small delay to ensure flex container layout is ready
  requestAnimationFrame(() => renderChart());
}

function renderChart() {
  if (!cachedStats || typeof Chart === 'undefined') return;
  
  const ctx = document.getElementById('statsChart').getContext('2d');
  const type = document.getElementById('chartType').value;
  const { total_users, total_jobs, total_applications, total_candidates, total_employers } = cachedStats;
  const dataValues = [total_jobs, total_applications, total_candidates, total_employers];
  const bgColors = [
    'rgba(139, 92, 246, 0.8)',
    'rgba(16, 185, 129, 0.8)',
    'rgba(6, 182, 212, 0.8)',
    'rgba(245, 158, 11, 0.8)'
  ];

  if (statsChartInstance) {
    statsChartInstance.destroy();
  }

  Chart.defaults.color = '#64748b';
  Chart.defaults.font.family = "'Inter', sans-serif";

  const isPie = type === 'pie';

  statsChartInstance = new Chart(ctx, {
    type: type,
    data: {
      labels: ['Jobs', 'Applications', 'Candidates', 'Employers'],
      datasets: [{
        label: 'Total Count',
        data: dataValues,
        backgroundColor: bgColors,
        borderRadius: isPie ? 0 : 6,
        borderWidth: isPie ? 2 : 0,
        borderColor: 'rgba(17, 24, 39, 1)' // surface background
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: isPie, position: 'bottom', labels: { padding: 20 } }
      },
      scales: isPie ? {} : {
        y: {
          beginAtZero: true,
          ticks: { stepSize: 1 },
          grid: { color: 'rgba(255, 255, 255, 0.05)', drawBorder: false }
        },
        x: {
          grid: { display: false, drawBorder: false }
        }
      }
    }
  });
}

// ─── USERS ───
async function loadUsers() {
  document.getElementById('users-table').innerHTML = `<div class="loading"><div class="spinner"></div> Loading…</div>`;
  const r = await req('GET', '/users');
  if (!r.ok) { document.getElementById('users-table').innerHTML = `<div class="empty">Failed to load users</div>`; return; }
  const rows = r.data.map((u, i) => `
    <tr>
      <td>${i + 1}</td>
      <td>${fmtID(u.id, u.role, u.is_staff)}</td>
      <td><strong>${esc(u.username)}</strong></td>
      <td>${esc(u.email||'—')}</td>
      <td>${u.is_staff ? '<span class="badge-role badge-admin">Admin</span>' : `<span class="badge-role badge-${u.role}">${u.role}</span>`}</td>
      <td>${u.is_active ? '✅' : '❌'}</td>
      <td><div class="td-actions">
        <button class="btn-sm btn-edit" onclick='openUserModal(${JSON.stringify(u)})'>Edit</button>
        <button class="btn-sm btn-danger" onclick="deleteUser(${u.id})">Delete</button>
      </div></td>
    </tr>`).join('');
  document.getElementById('users-table').innerHTML = rows
    ? `<table><thead><tr><th>S.No</th><th>ID</th><th>Username</th><th>Email</th><th>Role</th><th>Active</th><th>Actions</th></tr></thead><tbody>${rows}</tbody></table>`
    : `<div class="empty">No users found</div>`;
}

function openUserModal(u) {
  document.getElementById('user-modal-title').textContent = u ? 'Edit User' : 'Add User';
  document.getElementById('um-id').value = u ? u.id : '';
  document.getElementById('um-username').value = u ? u.username : '';
  document.getElementById('um-email').value = u ? (u.email||'') : '';
  document.getElementById('um-password').value = '';
  document.getElementById('um-role').value = u ? (u.role||'candidate') : 'candidate';
  document.getElementById('um-staff').value = u ? String(u.is_staff) : 'false';
  toggleRoleSelect();
  openModal('user-modal');
}

function toggleRoleSelect() {
  const isStaff = document.getElementById('um-staff').value === 'true';
  const roleSel = document.getElementById('um-role');
  roleSel.disabled = isStaff;
  if (isStaff) roleSel.style.opacity = '0.5';
  else roleSel.style.opacity = '1';
}

async function saveUser() {
  const id = document.getElementById('um-id').value;
  const body = {
    username: document.getElementById('um-username').value,
    email: document.getElementById('um-email').value,
    password: document.getElementById('um-password').value,
    role: document.getElementById('um-role').value,
    is_staff: document.getElementById('um-staff').value === 'true',
  };
  const r = id ? await req('PATCH', `/users/${id}`, body) : await req('POST', '/users', body);
  if (r.ok) { closeModal('user-modal'); toast(id ? 'User updated' : 'User created'); loadUsers(); }
  else toast(JSON.stringify(r.data), 'error');
}

async function deleteUser(id) {
  if (!confirm('Delete this user? This cannot be undone.')) return;
  const r = await req('DELETE', `/users/${id}`);
  if (r.ok) { toast('User deleted'); loadUsers(); }
  else toast(r.data.error || 'Delete failed', 'error');
}

// ─── JOBS ───
async function loadJobs() {
  document.getElementById('jobs-table').innerHTML = `<div class="loading"><div class="spinner"></div> Loading…</div>`;
  const r = await req('GET', '/jobs');
  if (!r.ok) { document.getElementById('jobs-table').innerHTML = `<div class="empty">Failed to load jobs</div>`; return; }
  const rows = r.data.map((j, i) => `
    <tr>
      <td>${i + 1}</td>
      <td>${fmtID(j.id, 'job')}</td>
      <td><strong>${esc(j.title)}</strong></td>
      <td>${esc(j.company_name||'—')}</td>
      <td style="max-width:200px;overflow:hidden;text-overflow:ellipsis">${esc(j.required_skills)}</td>
      <td>${esc(j.pincode)}</td>
      <td style="color:#10b981;font-weight:600">${j.salary ? '\u20b9' + Number(j.salary).toLocaleString('en-IN') : '—'}</td>
      <td><div class="td-actions">
        <button class="btn-sm btn-edit" onclick='openJobModal(${JSON.stringify(j)})'>Edit</button>
        <button class="btn-sm btn-danger" onclick="deleteJob(${j.id})">Delete</button>
      </div></td>
    </tr>`).join('');
  document.getElementById('jobs-table').innerHTML = rows
    ? `<table><thead><tr><th>S.No</th><th>ID</th><th>Title</th><th>Company</th><th>Skills</th><th>Pincode</th><th>Salary</th><th>Actions</th></tr></thead><tbody>${rows}</tbody></table>`
    : `<div class="empty">No jobs found</div>`;
}

function openJobModal(j) {
  document.getElementById('job-modal-title').textContent = j ? 'Edit Job' : 'Add Job';
  document.getElementById('jm-id').value = j ? j.id : '';
  document.getElementById('jm-title').value = j ? j.title : '';
  document.getElementById('jm-skills').value = j ? j.required_skills : '';
  document.getElementById('jm-pincode').value = j ? j.pincode : '';
  document.getElementById('jm-salary').value = j ? (j.salary || '') : '';
  document.getElementById('jm-employer').value = j ? (j.employer||'') : '';
  openModal('job-modal');
}

async function saveJob() {
  const id = document.getElementById('jm-id').value;
  const body = {
    title: document.getElementById('jm-title').value,
    required_skills: document.getElementById('jm-skills').value,
    pincode: document.getElementById('jm-pincode').value,
    salary: document.getElementById('jm-salary').value,
    employer_id: document.getElementById('jm-employer').value,
  };
  const r = id ? await req('PATCH', `/jobs/${id}`, body) : await req('POST', '/jobs', body);
  if (r.ok) { closeModal('job-modal'); toast(id ? 'Job updated' : 'Job created'); loadJobs(); }
  else toast(JSON.stringify(r.data), 'error');
}

async function deleteJob(id) {
  if (!confirm('Delete this job? All applications will also be removed.')) return;
  const r = await req('DELETE', `/jobs/${id}`);
  if (r.ok) { toast('Job deleted'); loadJobs(); }
  else toast(r.data.error || 'Delete failed', 'error');
}

// ─── APPLICATIONS ───
async function loadApplications() {
  document.getElementById('applications-table').innerHTML = `<div class="loading"><div class="spinner"></div> Loading…</div>`;
  const r = await req('GET', '/applications');
  if (!r.ok) { document.getElementById('applications-table').innerHTML = `<div class="empty">Failed to load applications</div>`; return; }
  const rows = r.data.map((a, i) => `
    <tr>
      <td>${i + 1}</td>
      <td>${fmtID(a.id, 'application')}</td>
      <td>${esc(a.candidate_name||'—')}</td>
      <td>${esc(a.job_title||'—')}</td>
      <td>${(+a.match_score||0).toFixed(1)}%</td>
      <td>
        <select class="status-sel" onchange="updateAppStatus(${a.id},this.value)">
          <option ${a.status==='Applied'?'selected':''}>Applied</option>
          <option ${a.status==='Shortlisted'?'selected':''}>Shortlisted</option>
          <option ${a.status==='Rejected'?'selected':''}>Rejected</option>
        </select>
      </td>
      <td><button class="btn-sm btn-danger" onclick="deleteApp(${a.id})">Delete</button></td>
    </tr>`).join('');
  document.getElementById('applications-table').innerHTML = rows
    ? `<table><thead><tr><th>S.No</th><th>ID</th><th>Candidate</th><th>Job</th><th>Score</th><th>Status</th><th>Actions</th></tr></thead><tbody>${rows}</tbody></table>`
    : `<div class="empty">No applications found</div>`;
}

async function updateAppStatus(id, status) {
  const r = await req('PATCH', `/applications/${id}`, { status });
  if (r.ok) toast('Status updated');
  else toast(r.data.error || 'Update failed', 'error');
}

async function deleteApp(id) {
  if (!confirm('Delete this application?')) return;
  const r = await req('DELETE', `/applications/${id}`);
  if (r.ok) { toast('Application deleted'); loadApplications(); }
  else toast(r.data.error || 'Delete failed', 'error');
}

// ─── CANDIDATES ───
async function loadCandidates() {
  document.getElementById('candidates-table').innerHTML = `<div class="loading"><div class="spinner"></div> Loading…</div>`;
  const r = await req('GET', '/candidates');
  if (!r.ok) { document.getElementById('candidates-table').innerHTML = `<div class="empty">Failed to load candidates</div>`; return; }
  const rows = r.data.map((c, i) => `
    <tr>
      <td>${i + 1}</td>
      <td>${fmtID(c.id, 'candidate')}</td>
      <td>${esc(c.username||'—')}</td>
      <td style="max-width:200px;overflow:hidden;text-overflow:ellipsis">${esc(c.skills||'—')}</td>
      <td>${c.experience} yrs</td>
      <td>${esc(c.pincode||'—')}</td>
      <td><div class="td-actions">
        <button class="btn-sm btn-edit" onclick='openCandModal(${JSON.stringify(c)})'>Edit</button>
        <button class="btn-sm btn-danger" onclick="deleteCand(${c.id})">Delete</button>
      </div></td>
    </tr>`).join('');
  document.getElementById('candidates-table').innerHTML = rows
    ? `<table><thead><tr><th>S.No</th><th>ID</th><th>User</th><th>Skills</th><th>Experience</th><th>Pincode</th><th>Actions</th></tr></thead><tbody>${rows}</tbody></table>`
    : `<div class="empty">No candidate profiles found</div>`;
}

function openCandModal(c) {
  document.getElementById('cm-id').value = c.id;
  document.getElementById('cm-skills').value = c.skills||'';
  document.getElementById('cm-exp').value = c.experience||0;
  document.getElementById('cm-pincode').value = c.pincode||'';
  openModal('candidate-modal');
}
async function saveCandidate() {
  const id = document.getElementById('cm-id').value;
  const r = await req('PATCH', `/candidates/${id}`, {
    skills: document.getElementById('cm-skills').value,
    experience: parseInt(document.getElementById('cm-exp').value)||0,
    pincode: document.getElementById('cm-pincode').value,
  });
  if (r.ok) { closeModal('candidate-modal'); toast('Candidate updated'); loadCandidates(); }
  else toast(JSON.stringify(r.data), 'error');
}
async function deleteCand(id) {
  if (!confirm('Delete this candidate profile?')) return;
  const r = await req('DELETE', `/candidates/${id}`);
  if (r.ok) { toast('Profile deleted'); loadCandidates(); }
  else toast(r.data.error || 'Delete failed', 'error');
}

// ─── EMPLOYERS ───
async function loadEmployers() {
  document.getElementById('employers-table').innerHTML = `<div class="loading"><div class="spinner"></div> Loading…</div>`;
  const r = await req('GET', '/employers');
  if (!r.ok) { document.getElementById('employers-table').innerHTML = `<div class="empty">Failed to load employers</div>`; return; }
  const rows = r.data.map((e, i) => `
    <tr>
      <td>${i + 1}</td>
      <td>${fmtID(e.id, 'employer')}</td>
      <td>${esc(e.username||'—')}</td>
      <td>${esc(e.company_name||'—')}</td>
      <td>${esc(e.pincode||'—')}</td>
      <td>${esc(e.contact_name||'—')}</td>
      <td>${esc(e.contact_phone||'—')}</td>
      <td>${esc(e.contact_email||'—')}</td>
      <td><div class="td-actions">
        <button class="btn-sm btn-edit" onclick='openEmpModal(${JSON.stringify(e)})'>Edit</button>
        <button class="btn-sm btn-danger" onclick="deleteEmp(${e.id})">Delete</button>
      </div></td>
    </tr>`).join('');
  document.getElementById('employers-table').innerHTML = rows
    ? `<table><thead><tr><th>S.No</th><th>ID</th><th>User</th><th>Company</th><th>Pincode</th><th>HR Name</th><th>Contact</th><th>Email</th><th>Actions</th></tr></thead><tbody>${rows}</tbody></table>`
    : `<div class="empty">No employer profiles found</div>`;
}

function openEmpModal(e) {
  document.getElementById('em-id').value = e.id;
  document.getElementById('em-company').value = e.company_name||'';
  document.getElementById('em-pincode').value = e.pincode||'';
  document.getElementById('em-contact-name').value = e.contact_name||'';
  document.getElementById('em-contact-phone').value = e.contact_phone||'';
  document.getElementById('em-contact-email').value = e.contact_email||'';
  openModal('employer-modal');
}
async function saveEmployer() {
  const id = document.getElementById('em-id').value;
  const r = await req('PATCH', `/employers/${id}`, {
    company_name: document.getElementById('em-company').value,
    pincode: document.getElementById('em-pincode').value,
    contact_name: document.getElementById('em-contact-name').value,
    contact_phone: document.getElementById('em-contact-phone').value,
    contact_email: document.getElementById('em-contact-email').value,
  });
  if (r.ok) { closeModal('employer-modal'); toast('Employer updated'); loadEmployers(); }
  else toast(JSON.stringify(r.data), 'error');
}
async function deleteEmp(id) {
  if (!confirm('Delete this employer profile?')) return;
  const r = await req('DELETE', `/employers/${id}`);
  if (r.ok) { toast('Profile deleted'); loadEmployers(); }
  else toast(r.data.error || 'Delete failed', 'error');
}

// ─── UTILS ───
function fmtID(id, type, isStaff=false) {
  if (isStaff) return 'AD' + String(id).padStart(2, '0');
  if (type === 'employer') return 'EM' + String(id).padStart(4, '0');
  if (type === 'candidate') return 'CA' + String(id).padStart(4, '0');
  if (type === 'job') return 'JB' + String(id).padStart(4, '0');
  if (type === 'application') return 'AP' + String(id).padStart(4, '0');
  return id;
}

function esc(s) {
  if (!s) return '';
  return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}

// Close modal on overlay click
document.querySelectorAll('.modal-overlay').forEach(o => {
  o.addEventListener('click', e => { if (e.target === o) o.classList.remove('open'); });
});
