# Полный код фронтенда Orkestrator Bot

## Содержание
1. [Html Templates](#html-templates)
2. [Frontend Src](#frontend-src)
3. [Frontend](#frontend)

---

## Html Templates

### admin_full.html

```html
<!doctype html>
<html lang="ru" data-theme="light">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Admin Panel | AI SDLC System</title>
  <style>
    /* ============== Theme Tokens (Совместимость с UI) ============== */
    :root {
      --bg: #ffffff;
      --bg-sec: #f6f7fb;
      --surface: #ffffff;
      --text-main: #121417;
      --text-sec: #5b6472;
      --border: #e6e8ef;
      
      --primary: #2f6fed;
      --primary-hover: #1f4fb8;
      --primary-light: #eef2ff;
      --danger: #d0342c;
      --success: #0f8a4b;
      --warning: #b7791f;
      --info: #3b82f6;
      
      --chip: #eef2ff;
      --chip-text: #243b76;
      
      --radius: 14px;
      --shadow: 0 10px 24px rgba(17,24,39,.08);
      --font: system-ui, -apple-system, Segoe UI, Roboto, sans-serif;
      
      --sidebar-w: 260px;
    }

    [data-theme="dark"] {
      --bg: #0b1220;
      --bg-sec: #0f1a2e;
      --surface: #0e1730;
      --text-main: #e9edf5;
      --text-sec: #a6b0c3;
      --border: rgba(255,255,255,.10);
      
      --primary: #6aa3ff;
      --primary-hover: #3f7fff;
      --primary-light: rgba(106,163,255,.1);
      --danger: #ff6b63;
      --success: #35d07f;
      
      --chip: rgba(106,163,255,.14);
      --chip-text: #b9d1ff;
      --shadow: 0 14px 30px rgba(0,0,0,.35);
    }

    /* ================= RESET & BASE ================= */
    * { box-sizing: border-box; outline: none; }
    body { 
      margin: 0; font-family: var(--font); 
      background: var(--bg-sec); color: var(--text-main); 
      height: 100vh; overflow: hidden; display: flex; 
    }
    a { text-decoration: none; color: inherit; }
    button { cursor: pointer; border: none; font-family: inherit; background: none; }
    input, select, textarea { font-family: inherit; }

    /* ================= LAYOUT ================= */
    .sidebar {
      width: var(--sidebar-w);
      background: var(--surface);
      border-right: 1px solid var(--border);
      display: flex; flex-direction: column;
      flex-shrink: 0; transition: background 0.3s; z-index: 20;
    }

    .main-content {
      flex: 1; display: flex; flex-direction: column;
      overflow: hidden; position: relative;
    }

    .top-bar {
      height: 64px;
      background: var(--surface);
      border-bottom: 1px solid var(--border);
      display: flex; align-items: center; justify-content: space-between;
      padding: 0 32px; flex-shrink: 0;
    }

    .view-area {
      flex: 1; overflow-y: auto; padding: 32px;
      position: relative;
    }

    /* ================= COMPONENTS ================= */
    /* Brand */
    .brand {
      display: flex; align-items: center; gap: 12px; 
      padding: 24px 16px; margin-bottom: 10px;
    }
    .brand-icon {
      width: 32px; height: 32px; 
      background: radial-gradient(circle at 30% 20%, var(--primary), transparent 60%),
                  radial-gradient(circle at 70% 70%, var(--success), transparent 60%);
      border-radius: 8px; border: 1px solid var(--border);
    }

    /* Navigation */
    .nav-list { flex: 1; overflow-y: auto; padding: 0 16px; }
    .nav-header {
      font-size: 11px; text-transform: uppercase; letter-spacing: 0.5px;
      color: var(--text-sec); margin: 24px 0 8px 12px; font-weight: 700;
    }
    .nav-item {
      display: flex; align-items: center; gap: 12px; padding: 12px;
      color: var(--text-sec); border-radius: 12px; transition: 0.2s;
      margin-bottom: 4px; font-size: 14px; font-weight: 500; cursor: pointer;
    }
    .nav-item:hover { background: var(--bg-sec); color: var(--text-main); }
    .nav-item.active { background: var(--chip); color: var(--chip-text); font-weight: 600; }
    .nav-icon { width: 20px; text-align: center; }

    /* Buttons */
    .btn {
      padding: 10px 16px; border-radius: 10px; font-weight: 500; font-size: 13px;
      display: inline-flex; align-items: center; gap: 8px; transition: 0.2s; border: 1px solid var(--border);
      background: var(--surface); color: var(--text-main);
    }
    .btn:hover { background: var(--bg-sec); border-color: var(--text-sec); }
    .btn:active { transform: translateY(1px); }
    
    .btn-primary { background: var(--primary); color: white; border-color: transparent; }
    .btn-primary:hover { background: var(--primary-hover); }
    
    .btn-danger { background: rgba(208,52,44,0.1); color: var(--danger); border-color: transparent; }
    .btn-danger:hover { background: rgba(208,52,44,0.15); }

    .btn-icon { padding: 8px; border-radius: 8px; border: none; color: var(--text-sec); }
    .btn-icon:hover { background: var(--bg-sec); color: var(--text-main); }
    
    .btn-sm { padding: 6px 12px; font-size: 12px; }

    /* Cards */
    .card {
      background: var(--surface); border: 1px solid var(--border);
      border-radius: var(--radius); box-shadow: var(--shadow);
      margin-bottom: 24px; overflow: hidden;
    }
    .card-header {
      padding: 16px 24px; border-bottom: 1px solid var(--border);
      display: flex; justify-content: space-between; align-items: center;
      background: rgba(127,127,127,0.03); font-weight: 600;
    }
    .card-body { padding: 24px; }

    /* Tables */
    .table-wrapper { overflow-x: auto; }
    table { width: 100%; border-collapse: collapse; font-size: 13px; min-width: 600px; }
    th { text-align: left; padding: 12px 16px; color: var(--text-sec); font-weight: 600; border-bottom: 1px solid var(--border); }
    td { padding: 16px; border-bottom: 1px solid var(--border); vertical-align: middle; }
    tr:last-child td { border-bottom: none; }
    tr:hover td { background: var(--bg-sec); cursor: default; }
    .clickable-row { cursor: pointer; }

    /* Badges */
    .badge {
      padding: 4px 10px; border-radius: 20px; font-size: 11px; font-weight: 600;
      display: inline-flex; align-items: center; gap: 6px; border: 1px solid transparent;
    }
    .badge-role { background: var(--chip); color: var(--chip-text); border-color: var(--border); }
    .badge-active { background: rgba(15,138,75,0.12); color: var(--success); }
    .badge-inactive { background: rgba(208,52,44,0.12); color: var(--danger); }
    .badge-warn { background: rgba(183,121,31,0.12); color: var(--warning); }
    .badge-blue { background: var(--primary-light); color: var(--primary); }

    /* Forms */
    .form-group { margin-bottom: 16px; }
    .form-label { display: block; font-size: 12px; font-weight: 600; margin-bottom: 6px; color: var(--text-sec); }
    .form-input, .form-select {
      width: 100%; padding: 10px 12px; border-radius: 10px; border: 1px solid var(--border);
      background: var(--bg-sec); color: var(--text-main); font-size: 14px;
    }
    .form-input:focus { border-color: var(--primary); box-shadow: 0 0 0 2px var(--chip); }

    /* Modal */
    .modal-overlay {
      position: fixed; inset: 0; background: rgba(0,0,0,0.4); z-index: 100;
      display: flex; justify-content: center; align-items: center;
      backdrop-filter: blur(4px); opacity: 0; pointer-events: none; transition: opacity 0.2s;
    }
    .modal-overlay.open { opacity: 1; pointer-events: auto; }
    .modal {
      background: var(--surface); width: 500px; max-width: 92vw;
      border-radius: 16px; box-shadow: var(--shadow);
      transform: scale(0.95); transition: transform 0.2s; border: 1px solid var(--border);
    }
    .modal-overlay.open .modal { transform: scale(1); }
    .modal-head { padding: 16px 24px; border-bottom: 1px solid var(--border); display: flex; justify-content: space-between; align-items: center; }
    .modal-body { padding: 24px; max-height: 70vh; overflow-y: auto; }
    .modal-foot { padding: 16px 24px; background: rgba(127,127,127,0.03); border-top: 1px solid var(--border); display: flex; justify-content: flex-end; gap: 12px; border-radius: 0 0 16px 16px; }

    /* DRAWER (Side Panel for Complex Edits) */
    .drawer-overlay {
      position: fixed; inset: 0; background: rgba(0,0,0,0.2); z-index: 90;
      opacity: 0; pointer-events: none; transition: 0.3s;
    }
    .drawer-overlay.open { opacity: 1; pointer-events: auto; }
    .drawer {
      position: fixed; top: 0; right: 0; bottom: 0; width: 600px; max-width: 90vw;
      background: var(--surface); border-left: 1px solid var(--border);
      box-shadow: -5px 0 30px rgba(0,0,0,0.1);
      transform: translateX(100%); transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1);
      display: flex; flex-direction: column; z-index: 95;
    }
    .drawer.open { transform: translateX(0); }
    .drawer-content { flex: 1; overflow-y: auto; padding: 24px; }
    
    /* Tabs inside Drawer */
    .tabs { display: flex; border-bottom: 1px solid var(--border); margin-bottom: 24px; gap: 24px; }
    .tab { padding: 10px 0; font-size: 13px; font-weight: 500; color: var(--text-sec); cursor: pointer; border-bottom: 2px solid transparent; }
    .tab.active { color: var(--primary); border-bottom-color: var(--primary); font-weight: 600; }
    .tab-pane { display: none; animation: fadeIn 0.3s; }
    .tab-pane.active { display: block; }
    @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }

    /* Toast */
    .toast-container { position: fixed; bottom: 20px; right: 20px; z-index: 200; display: flex; flex-direction: column; gap: 10px; }
    .toast {
      padding: 12px 20px; background: #333; color: #fff; border-radius: 10px; font-size: 14px;
      box-shadow: 0 10px 20px rgba(0,0,0,0.2); display: flex; align-items: center; gap: 10px;
      animation: slideUp 0.3s; min-width: 250px;
    }
    @keyframes slideUp { from { transform: translateY(20px); opacity: 0; } to { transform: translateY(0); opacity: 1; } }

    /* Switch Toggle */
    .switch { position: relative; display: inline-block; width: 40px; height: 22px; }
    .switch input { opacity: 0; width: 0; height: 0; }
    .slider { position: absolute; cursor: pointer; inset: 0; background-color: #ccc; transition: .3s; border-radius: 22px; }
    .slider:before { position: absolute; content: ""; height: 18px; width: 18px; left: 2px; bottom: 2px; background-color: white; transition: .3s; border-radius: 50%; }
    input:checked + .slider { background-color: var(--primary); }
    input:checked + .slider:before { transform: translateX(18px); }

  </style>
</head>
<body>

  <aside class="sidebar">
    <div class="brand">
      <div class="brand-icon"></div>
      <div>
        <div style="font-weight: 700; font-size:15px;">Admin Panel</div>
        <div style="font-size: 11px; color: var(--text-sec);">AI Orchestrator</div>
      </div>
    </div>

    <div class="nav-list">
      <div id="nav-container"></div>
    </div>

    <div style="padding: 16px; border-top: 1px solid var(--border); background: var(--bg-sec);">
      <div style="font-size:10px; font-weight:700; color:var(--text-sec); margin-bottom:8px; display:flex; justify-content:space-between; align-items:center;">
        SIMULATE ROLE
        <span onclick="app.resetData()" style="cursor:pointer; color:var(--primary)">↺ Reset</span>
      </div>
      <div class="form-group" style="margin-bottom:12px;">
        <select class="form-select" id="role-switcher" onchange="app.switchRole(this.value)" style="padding:6px; font-size:12px;">
          <option value="admin">System Admin</option>
          <option value="lead">Team Lead (Alpha)</option>
        </select>
      </div>
      <div style="display:flex; align-items:center; gap:10px;">
        <div id="user-avatar" style="width:32px; height:32px; border-radius:50%; background:var(--primary); color:#fff; display:grid; place-items:center; font-size:12px; font-weight:700;">AD</div>
        <div>
          <div id="user-name" style="font-size:13px; font-weight:600">Administrator</div>
          <div id="user-email" style="font-size:11px; color:var(--text-sec);">admin@sys.com</div>
        </div>
      </div>
    </div>
  </aside>

  <main class="main-content">
    <header class="top-bar">
      <h2 id="page-title" style="font-size: 16px; margin: 0; font-weight:600;">Dashboard</h2>
      
      <div style="display:flex; gap:12px; align-items:center;">
        <select class="btn btn-sm" onchange="app.setLang(this.value)" style="border:none; background:transparent;">
          <option value="ru">🇷🇺 RU</option>
          <option value="en">🇺🇸 EN</option>
        </select>
        <button class="btn btn-sm" onclick="app.toggleTheme()">🌗</button>
      </div>
    </header>

    <div id="view-container" class="view-area"></div>
  </main>

  <div id="modal-overlay" class="modal-overlay">
    <div class="modal">
      <div class="modal-head">
        <h3 id="modal-title" style="margin: 0; font-size: 16px;">Title</h3>
        <button onclick="ui.closeModal()" class="btn-icon">✕</button>
      </div>
      <div id="modal-body" class="modal-body"></div>
      <div id="modal-foot" class="modal-foot"></div>
    </div>
  </div>

  <div id="drawer-overlay" class="drawer-overlay" onclick="ui.closeDrawer()"></div>
  <aside id="drawer" class="drawer">
    <div class="card-header" style="background:var(--bg-sec)">
      <h3 id="drawer-title" style="margin:0; font-size:16px">Details</h3>
      <button onclick="ui.closeDrawer()" class="btn-icon">✕</button>
    </div>
    <div id="drawer-content" class="drawer-content"></div>
  </aside>

  <div class="toast-container" id="toast-container"></div>

<script>
/* ==========================================================================
   1. CONFIG & TRANSLATIONS
   ========================================================================== */
const I18N = {
  ru: {
    nav: { overview: "Обзор", teams: "Команды", users: "Пользователи", projects: "Проекты", monitor: "Мониторинг", access: "Роли и Доступ", audit: "Аудит", system: "Система" },
    lbl: { create: "Создать", edit: "Ред.", delete: "Удалить", save: "Сохранить", cancel: "Отмена", status: "Статус", role: "Роль", team: "Команда", actions: "Действия" },
    st: { active: "Активен", blocked: "Блок", testing: "Тест", running: "Работает", error: "Ошибка", waiting: "Ожидание" },
    msg: { saved: "Успешно сохранено", deleted: "Объект удален", confirm: "Вы уверены?", welcome: "Режим: " }
  },
  en: {
    nav: { overview: "Overview", teams: "Teams", users: "Users", projects: "Projects", monitor: "Monitoring", access: "Access Control", audit: "Audit Log", system: "System" },
    lbl: { create: "Create", edit: "Edit", delete: "Delete", save: "Save", cancel: "Cancel", status: "Status", role: "Role", team: "Team", actions: "Actions" },
    st: { active: "Active", blocked: "Blocked", testing: "Testing", running: "Running", error: "Error", waiting: "Waiting" },
    msg: { saved: "Successfully saved", deleted: "Item deleted", confirm: "Are you sure?", welcome: "Mode: " }
  }
};

/* ==========================================================================
   2. DATA STORE (MOCK DB)
   ========================================================================== */
const DEFAULT_DB = {
  users: [
    { id: 1, name: "Alex Admin", email: "admin@sys.com", role: "admin", teamId: null, status: "active" },
    { id: 2, name: "Ivan Lead", email: "ivan@alpha.com", role: "teamlead", teamId: 101, status: "active" },
    { id: 3, name: "Sarah Dev", email: "sarah@alpha.com", role: "developer", teamId: 101, status: "active" },
    { id: 4, name: "Bot Agent", email: "bot@sys.ai", role: "bot", teamId: 102, status: "active" }
  ],
  teams: [
    { id: 101, name: "Alpha Squad", code: "ALPHA", desc: "Core Product Development", ownerId: 2 },
    { id: 102, name: "Beta Ops", code: "BETA", desc: "Internal Tools & Infra", ownerId: 0 }
  ],
  projects: [
    { id: 50, name: "E-Commerce API", teamId: 101, repo: "git/shop-api", status: "active", lang: "Python" },
    { id: 51, name: "Mobile App", teamId: 101, repo: "git/mobile-ios", status: "testing", lang: "Swift" },
    { id: 52, name: "Ops Dashboard", teamId: 102, repo: "git/ops-dash", status: "active", lang: "React" }
  ],
  integrations: {
    50: { telegram: true, telegram_key: "123:ABC...", jira: false },
    51: { telegram: false, telegram_key: "", jira: true }
  },
  monitoring: [
    { id: "sess_1", agent: "Architect", project: "E-Commerce API", status: "running", tokens: 1200, time: "5m" },
    { id: "sess_2", agent: "Coder", project: "Mobile App", status: "waiting", tokens: 450, time: "1m" },
    { id: "sess_3", agent: "Reviewer", project: "E-Commerce API", status: "error", tokens: 0, time: "10s" }
  ],
  audit: [
    { time: "2023-10-25 10:00", user: "Alex Admin", action: "User Created", target: "Sarah Dev" },
    { time: "2023-10-25 10:30", user: "Ivan Lead", action: "Project Update", target: "Mobile App" }
  ]
};

const store = {
  lang: 'ru',
  currentUser: { role: 'admin', teamId: null },
  
  init() {
    const saved = localStorage.getItem('gem_admin_db_v4');
    this.data = saved ? JSON.parse(saved) : JSON.parse(JSON.stringify(DEFAULT_DB));
  },
  save() {
    localStorage.setItem('gem_admin_db_v4', JSON.stringify(this.data));
    app.render(); // Re-render views on change
  },
  reset() {
    localStorage.removeItem('gem_admin_db_v4');
    location.reload();
  },
  t(k) { return I18N[this.lang][k.split('_')[0]]?.[k.split('_')[1]] || k; },
  log(action, target) {
    const user = this.currentUser.role === 'admin' ? "Alex Admin" : "Ivan Lead";
    this.data.audit.unshift({
      time: new Date().toLocaleTimeString(), user, action, target
    });
    this.save();
  }
};

/* ==========================================================================
   3. APP LOGIC & ROUTER
   ========================================================================== */
const app = {
  view: 'overview',
  
  init() {
    store.init();
    this.renderSidebar();
    this.navigate('overview');
    
    // Fake monitoring loop
    setInterval(() => {
      if(this.view === 'monitor') {
        store.data.monitoring.forEach(m => {
          if(m.status === 'running') m.tokens += Math.floor(Math.random()*20);
        });
        views.monitor(document.getElementById('view-container'), true); // update only
      }
    }, 2000);
  },

  setLang(l) { store.lang = l; this.renderSidebar(); this.navigate(this.view); },
  
  toggleTheme() {
    const html = document.documentElement;
    html.setAttribute('data-theme', html.getAttribute('data-theme') === 'dark' ? 'light' : 'dark');
  },

  switchRole(role) {
    store.currentUser.role = role;
    store.currentUser.teamId = role === 'lead' ? 101 : null;
    
    // Update User Profile UI
    const isAdm = role === 'admin';
    document.getElementById('user-name').innerText = isAdm ? 'Administrator' : 'Ivan Lead';
    document.getElementById('user-email').innerText = isAdm ? 'admin@sys.com' : 'ivan@alpha.com';
    document.getElementById('user-avatar').innerText = isAdm ? 'AD' : 'IL';
    
    this.renderSidebar();
    this.navigate('overview');
    ui.toast(store.t('msg_welcome') + role.toUpperCase());
  },
  
  resetData() { if(confirm("Reset all data?")) store.reset(); },

  navigate(viewId) {
    this.view = viewId;
    document.querySelectorAll('.nav-item').forEach(e => e.classList.remove('active'));
    const navItem = document.getElementById('nav-' + viewId);
    if(navItem) navItem.classList.add('active');
    
    document.getElementById('page-title').innerText = store.t('nav_'+viewId);
    
    const container = document.getElementById('view-container');
    container.innerHTML = '';
    if(views[viewId]) views[viewId](container);
  },

  renderSidebar() {
    const role = store.currentUser.role;
    const menu = [
      { id: 'overview', icon: '📊' },
      { id: 'teams', icon: '🏢' },
      { id: 'users', icon: '👥' },
      { id: 'projects', icon: '🚀' },
      { head: 'system' },
      { id: 'monitor', icon: '⚡' },
      { id: 'access', icon: '🛡️', adminOnly: true }, // Only admin
      { id: 'audit', icon: '📜', adminOnly: true }
    ];

    let html = '';
    menu.forEach(item => {
      if(item.adminOnly && role !== 'admin') return;
      if(item.head) {
        html += `<div class="nav-header">${store.t('nav_'+item.head)}</div>`;
      } else {
        html += `
          <div id="nav-${item.id}" class="nav-item" onclick="app.navigate('${item.id}')">
            <div class="nav-icon">${item.icon}</div>
            <span>${store.t('nav_'+item.id)}</span>
          </div>
        `;
      }
    });
    document.getElementById('nav-container').innerHTML = html;
  }
};

/* ==========================================================================
   4. VIEWS
   ========================================================================== */
const views = {
  overview: (el) => {
    const isLead = store.currentUser.role === 'lead';
    const myTeamId = store.currentUser.teamId;
    
    const d = store.data;
    const users = isLead ? d.users.filter(u => u.teamId === myTeamId) : d.users;
    const projects = isLead ? d.projects.filter(p => p.teamId === myTeamId) : d.projects;
    
    el.innerHTML = `
      <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap:20px; margin-bottom:24px;">
        <div class="card card-body">
          <div class="text-sec" style="font-size:11px; font-weight:700">TOTAL USERS</div>
          <div style="font-size:28px; font-weight:700">${users.length}</div>
        </div>
        <div class="card card-body">
          <div class="text-sec" style="font-size:11px; font-weight:700">PROJECTS</div>
          <div style="font-size:28px; font-weight:700; color:var(--primary)">${projects.length}</div>
        </div>
        <div class="card card-body">
          <div class="text-sec" style="font-size:11px; font-weight:700">AGENTS ACTIVE</div>
          <div style="font-size:28px; font-weight:700; color:var(--success)">${d.monitoring.filter(m=>m.status==='running').length}</div>
        </div>
      </div>
      
      ${isLead ? `<div class="card card-body" style="background:var(--chip); color:var(--chip-text); border:1px solid var(--primary);">
        <b>Team Lead Mode:</b> You are viewing resources for <i>Alpha Squad</i> only.
      </div>` : ''}

      <div class="card">
        <div class="card-header">Recent Activity</div>
        ${ui.tableAudit(d.audit.slice(0,5))}
      </div>
    `;
  },

  teams: (el) => {
    const isLead = store.currentUser.role === 'lead';
    let list = store.data.teams;
    if(isLead) list = list.filter(t => t.id === store.currentUser.teamId);
    
    const btn = !isLead ? `<button class="btn btn-primary btn-sm" onclick="actions.editTeam()">+ ${store.t('lbl_create')}</button>` : '';

    el.innerHTML = `
      <div class="card">
        <div class="card-header"><span>Teams</span> ${btn}</div>
        <div class="table-wrapper">
          <table>
            <thead><tr><th>Name</th><th>Description</th><th>Members</th><th></th></tr></thead>
            <tbody>
              ${list.map(t => {
                const count = store.data.users.filter(u => u.teamId === t.id).length;
                return `<tr class="clickable-row" onclick="actions.openTeamDrawer(${t.id})">
                  <td><b>${t.name}</b> <span class="text-sec text-xs">(${t.code})</span></td>
                  <td>${t.desc}</td>
                  <td><span class="badge badge-role">${count} users</span></td>
                  <td style="text-align:right">➔</td>
                </tr>`;
              }).join('')}
            </tbody>
          </table>
        </div>
      </div>
    `;
  },

  users: (el) => {
    const isLead = store.currentUser.role === 'lead';
    let users = store.data.users;
    if(isLead) users = users.filter(u => u.teamId === store.currentUser.teamId);

    const btn = `<button class="btn btn-primary btn-sm" onclick="actions.editUser()">+ ${store.t('lbl_create')}</button>`;

    const rows = users.map(u => {
      const team = store.data.teams.find(t => t.id === u.teamId)?.name || '-';
      const badgeClass = u.status === 'active' ? 'badge-active' : 'badge-inactive';
      
      return `
        <tr>
          <td>
            <div style="font-weight:600">${u.name}</div>
            <div style="font-size:11px; color:var(--text-sec)">${u.email}</div>
          </td>
          <td><span class="badge badge-role">${u.role}</span></td>
          <td>${team}</td>
          <td><span class="badge ${badgeClass}">${store.t('st_'+u.status)}</span></td>
          <td style="text-align:right">
            <button class="btn btn-icon" onclick="actions.editUser(${u.id})">✏️</button>
            <button class="btn btn-icon" style="color:var(--danger)" onclick="actions.deleteUser(${u.id})">🗑️</button>
          </td>
        </tr>
      `;
    }).join('');

    el.innerHTML = `<div class="card"><div class="card-header"><span>Users Directory</span> ${btn}</div><div class="table-wrapper"><table><thead><tr><th>User</th><th>Role</th><th>Team</th><th>Status</th><th style="text-align:right">Actions</th></tr></thead><tbody>${rows}</tbody></table></div></div>`;
  },

  projects: (el) => {
    const isLead = store.currentUser.role === 'lead';
    let projects = store.data.projects;
    if(isLead) projects = projects.filter(p => p.teamId === store.currentUser.teamId);

    const btn = `<button class="btn btn-primary btn-sm" onclick="actions.createProject()">+ ${store.t('lbl_create')}</button>`;

    const rows = projects.map(p => {
      const team = store.data.teams.find(t => t.id === p.teamId)?.code || 'GLOBAL';
      return `
        <tr class="clickable-row" onclick="actions.openProjectDrawer(${p.id})">
          <td><b>${p.name}</b></td>
          <td><span class="badge badge-role">${team}</span></td>
          <td><span style="font-family:monospace; color:var(--primary)">${p.repo}</span></td>
          <td><span class="badge badge-blue">${p.status}</span></td>
          <td style="text-align:right">⚙️</td>
        </tr>
      `;
    }).join('');

    el.innerHTML = `<div class="card"><div class="card-header"><span>Projects</span> ${btn}</div><div class="table-wrapper"><table><thead><tr><th>Name</th><th>Team</th><th>Repo</th><th>Status</th><th></th></tr></thead><tbody>${rows}</tbody></table></div></div>`;
  },

  monitor: (el, updateOnly = false) => {
    const isLead = store.currentUser.role === 'lead';
    let data = store.data.monitoring;
    if(isLead) {
      // Filter sessions for owned projects
      const myProjNames = store.data.projects.filter(p => p.teamId === store.currentUser.teamId).map(p => p.name);
      data = data.filter(m => myProjNames.includes(m.project));
    }

    const rows = data.map(m => {
      let badge = m.status === 'running' ? 'badge-active' : (m.status === 'error' ? 'badge-inactive' : 'badge-warn');
      return `
        <tr>
          <td><span style="font-family:monospace">${m.id}</span></td>
          <td>${m.agent}</td>
          <td>${m.project}</td>
          <td><span class="badge ${badge}">${store.t('st_'+m.status)}</span></td>
          <td>${m.tokens}</td>
          <td>${m.time}</td>
        </tr>
      `;
    }).join('');

    if(updateOnly) {
      const tbody = document.getElementById('monitor-body');
      if(tbody) tbody.innerHTML = rows;
      return;
    }

    el.innerHTML = `<div class="card"><div class="card-header"><span>Active Agents</span> <span class="badge badge-active">LIVE</span></div><div class="table-wrapper"><table><thead><tr><th>ID</th><th>Agent</th><th>Project</th><th>Status</th><th>Tokens</th><th>Duration</th></tr></thead><tbody id="monitor-body">${rows}</tbody></table></div></div>`;
  },

  audit: (el) => {
    el.innerHTML = `<div class="card"><div class="card-header">Global Audit Log</div>${ui.tableAudit(store.data.audit)}</div>`;
  }
};

/* ==========================================================================
   5. ACTIONS (LOGIC)
   ========================================================================== */
const actions = {
  // USER CRUD
  editUser: (id) => {
    const isEdit = !!id;
    const u = id ? store.data.users.find(x => x.id === id) : { name: '', email: '', role: 'developer', teamId: '', status: 'active' };
    
    // Filter teams based on role
    let teams = store.data.teams;
    if(store.currentUser.role === 'lead') teams = teams.filter(t => t.id === store.currentUser.teamId);

    const teamOpts = teams.map(t => `<option value="${t.id}" ${u.teamId==t.id?'selected':''}>${t.name}</option>`).join('');
    
    const html = `
      <div class="form-group"><label class="form-label">Name</label><input id="u_name" class="form-input" value="${u.name}"></div>
      <div class="form-group"><label class="form-label">Email</label><input id="u_email" class="form-input" value="${u.email}"></div>
      <div class="form-group"><label class="form-label">Team</label><select id="u_team" class="form-select">${teamOpts}</select></div>
      <div class="form-group"><label class="form-label">Role</label><select id="u_role" class="form-select">
        <option value="developer" ${u.role==='developer'?'selected':''}>Developer</option>
        <option value="qa" ${u.role==='qa'?'selected':''}>QA</option>
        <option value="teamlead" ${u.role==='teamlead'?'selected':''}>Team Lead</option>
      </select></div>
      <div class="form-group"><label class="form-label">Status</label><select id="u_status" class="form-select">
        <option value="active" ${u.status==='active'?'selected':''}>Active</option>
        <option value="blocked" ${u.status==='blocked'?'selected':''}>Blocked</option>
      </select></div>
    `;

    ui.openModal(isEdit ? 'Edit User' : 'New User', html, () => {
      const payload = {
        id: id || Date.now(),
        name: document.getElementById('u_name').value,
        email: document.getElementById('u_email').value,
        teamId: Number(document.getElementById('u_team').value),
        role: document.getElementById('u_role').value,
        status: document.getElementById('u_status').value
      };
      
      if(isEdit) {
        const idx = store.data.users.findIndex(x => x.id === id);
        store.data.users[idx] = payload;
        store.log("User Updated", payload.email);
      } else {
        store.data.users.push(payload);
        store.log("User Created", payload.email);
      }
      store.save();
      ui.closeModal();
      ui.toast(store.t('msg_saved'));
    });
  },

  deleteUser: (id) => {
    if(confirm(store.t('msg_confirm'))) {
      store.data.users = store.data.users.filter(u => u.id !== id);
      store.log("User Deleted", "ID: " + id);
      store.save();
      ui.toast(store.t('msg_deleted'));
    }
  },

  // PROJECT DRAWER
  createProject: () => {
    ui.openModal('New Project', `
      <div class="form-group"><label class="form-label">Project Name</label><input id="np_name" class="form-input"></div>
      <div class="form-group"><label class="form-label">Repo URL</label><input id="np_repo" class="form-input"></div>
    `, () => {
      const name = document.getElementById('np_name').value;
      if(name) {
        store.data.projects.push({
          id: Date.now(), name, repo: document.getElementById('np_repo').value,
          teamId: store.currentUser.teamId || 101, status: 'active', lang: 'Other'
        });
        store.save();
        ui.closeModal();
        ui.toast("Project created");
      }
    });
  },

  openProjectDrawer: (id) => {
    const p = store.data.projects.find(x => x.id === id);
    const integ = store.data.integrations[id] || { telegram: false, telegram_key: '', jira: false };

    // TAB 1: GENERAL
    const tab1 = `
      <div class="form-group"><label class="form-label">Project Name</label><input class="form-input" value="${p.name}"></div>
      <div class="form-group"><label class="form-label">Repository</label><input class="form-input" value="${p.repo}"></div>
      <div class="form-group"><label class="form-label">Stack</label><input class="form-input" value="${p.lang}"></div>
      <div style="margin-top:20px; text-align:right"><button class="btn btn-primary" onclick="ui.toast('${store.t('msg_saved')}')">Update Info</button></div>
    `;

    // TAB 2: INTEGRATIONS (Secrets)
    const tab2 = `
      <div class="card" style="box-shadow:none; border:1px solid var(--border)">
        <div class="card-body">
          <div style="display:flex; justify-content:space-between; margin-bottom:12px">
            <span style="font-weight:600">Telegram Bot</span>
            <label class="switch"><input type="checkbox" ${integ.telegram?'checked':''}><span class="slider"></span></label>
          </div>
          <div class="form-group">
            <label class="form-label">Bot Token (Masked)</label>
            <input type="password" class="form-input" value="${integ.telegram_key}" placeholder="123:ABC...">
          </div>
        </div>
      </div>
       <div class="card" style="box-shadow:none; border:1px solid var(--border)">
        <div class="card-body">
          <div style="display:flex; justify-content:space-between; margin-bottom:12px">
            <span style="font-weight:600">Jira Sync</span>
            <label class="switch"><input type="checkbox" ${integ.jira?'checked':''}><span class="slider"></span></label>
          </div>
        </div>
      </div>
      <button class="btn btn-primary" onclick="ui.toast('Keys Updated')">Save Secrets</button>
    `;

    // TAB 3: MODELS
    const tab3 = `
       <div class="form-group">
         <label class="form-label">Planner Model</label>
         <select class="form-select"><option>GPT-4 Turbo</option><option>Claude 3 Opus</option></select>
       </div>
       <div class="form-group">
         <label class="form-label">Coder Model</label>
         <select class="form-select"><option>GPT-4 Turbo</option><option>DeepSeek Coder</option></select>
       </div>
    `;

    ui.openDrawer(p.name, [
      { name: "General", content: tab1 },
      { name: "Integrations", content: tab2 },
      { name: "AI Models", content: tab3 }
    ]);
  },
  
  openTeamDrawer: (id) => {
    const t = store.data.teams.find(x => x.id === id);
    ui.openDrawer(t.name, [{ name: "Details", content: `
      <div class="form-group"><label class="form-label">Name</label><input class="form-input" value="${t.name}"></div>
      <div class="form-group"><label class="form-label">Description</label><textarea class="form-input">${t.desc}</textarea></div>
      <button class="btn btn-primary" onclick="ui.toast('Saved')">Update</button>
    ` }]);
  }
};

/* ==========================================================================
   6. UI UTILS
   ========================================================================== */
const ui = {
  tableAudit: (list) => {
    if(!list.length) return '<div style="padding:20px; text-align:center; color:var(--text-sec)">No logs</div>';
    return `<div class="table-wrapper"><table><thead><tr><th>Time</th><th>User</th><th>Action</th><th>Target</th></tr></thead><tbody>${list.map(l => `<tr><td>${l.time}</td><td><b>${l.user}</b></td><td>${l.action}</td><td>${l.target}</td></tr>`).join('')}</tbody></table></div>`;
  },
  
  openModal: (title, html, onSave) => {
    document.getElementById('modal-title').innerText = title;
    document.getElementById('modal-body').innerHTML = html;
    document.getElementById('modal-foot').innerHTML = `<button class="btn" onclick="ui.closeModal()">${store.t('lbl_cancel')}</button><button class="btn btn-primary" id="modal-save">${store.t('lbl_save')}</button>`;
    if(onSave) document.getElementById('modal-save').onclick = onSave;
    document.getElementById('modal-overlay').classList.add('open');
  },
  closeModal: () => document.getElementById('modal-overlay').classList.remove('open'),
  
  openDrawer: (title, tabs) => {
    document.getElementById('drawer-title').innerText = title;
    const content = document.getElementById('drawer-content');
    
    // Build Tabs
    let headers = '<div class="tabs">';
    let bodies = '';
    
    tabs.forEach((t, i) => {
      headers += `<div class="tab ${i===0?'active':''}" onclick="ui.switchTab(this, ${i})">${t.name}</div>`;
      bodies += `<div class="tab-pane ${i===0?'active':''}" id="tab-${i}">${t.content}</div>`;
    });
    headers += '</div>';
    
    content.innerHTML = headers + bodies;
    document.getElementById('drawer-overlay').classList.add('open');
    document.getElementById('drawer').classList.add('open');
  },
  closeDrawer: () => {
    document.getElementById('drawer-overlay').classList.remove('open');
    document.getElementById('drawer').classList.remove('open');
  },
  switchTab: (el, idx) => {
    document.querySelectorAll('.tab').forEach(e => e.classList.remove('active'));
    document.querySelectorAll('.tab-pane').forEach(e => e.classList.remove('active'));
    el.classList.add('active');
    document.getElementById('tab-'+idx).classList.add('active');
  },
  toast: (msg) => {
    const d = document.createElement('div');
    d.className = 'toast'; d.innerText = "✅ " + msg;
    document.getElementById('toast-container').appendChild(d);
    setTimeout(() => d.remove(), 3000);
  }
};

// Start App
app.init();
</script>
</body>
</html>
```

### gpt_bot_ii.html

```html
bash -lc cat > /mnt/data/demo_ai_pm_system.html <<'HTML'
<!doctype html>
<html lang="ru" data-theme="light">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Demo: AI Multi‑Agent SDLC System</title>
  <style>
    /* ============== Theme tokens (CSS variables) ============== */
    :root{
      --bg: #ffffff;
      --bg2: #f6f7fb;
      --card: #ffffff;
      --text: #121417;
      --muted: #5b6472;
      --border: #e6e8ef;
      --shadow: 0 10px 24px rgba(17,24,39,.08);
      --primary: #2f6fed;
      --primary2:#1f4fb8;
      --danger: #d0342c;
      --warn: #b7791f;
      --ok: #0f8a4b;
      --chip: #eef2ff;
      --chipText:#243b76;
      --mono: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
      --radius: 16px;
    }
    [data-theme="dark"]{
      --bg: #0b1220;
      --bg2: #0f1a2e;
      --card: #0e1730;
      --text: #e9edf5;
      --muted: #a6b0c3;
      --border: rgba(255,255,255,.10);
      --shadow: 0 14px 30px rgba(0,0,0,.35);
      --primary: #6aa3ff;
      --primary2:#3f7fff;
      --danger: #ff6b63;
      --warn: #ffb14a;
      --ok: #35d07f;
      --chip: rgba(106,163,255,.14);
      --chipText:#b9d1ff;
    }

    /* ============== Base ============== */
    *{box-sizing:border-box}
    body{
      margin:0;
      font-family: system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif;
      background: linear-gradient(180deg,var(--bg),var(--bg2));
      color:var(--text);
    }
    a{color:inherit}
    button, input, select, textarea{font:inherit}

    /* ============== Layout ============== */
    .app{
      display:grid;
      grid-template-columns: 280px 1fr;
      min-height: 100vh;
    }

    .sidebar{
      border-right:1px solid var(--border);
      background: rgba(255,255,255,.02);
      padding: 18px;
      position: sticky;
      top:0;
      height:100vh;
      overflow:auto;
    }
    .brand{
      display:flex;
      gap:10px;
      align-items:center;
      padding: 10px 10px 14px;
    }
    .logo{
      width:40px;height:40px;border-radius:12px;
      background: radial-gradient(circle at 30% 20%, var(--primary), transparent 60%),
                  radial-gradient(circle at 70% 70%, var(--ok), transparent 60%),
                  linear-gradient(135deg, rgba(255,255,255,.10), rgba(255,255,255,.02));
      border:1px solid var(--border);
      box-shadow: var(--shadow);
    }
    .brand h1{font-size:14px;margin:0;line-height:1.2}
    .brand p{font-size:12px;margin:2px 0 0;color:var(--muted)}

    .nav{
      margin-top:10px;
      display:flex;
      flex-direction:column;
      gap:6px;
    }
    .nav a{
      text-decoration:none;
      padding:10px 10px;
      border-radius: 12px;
      border:1px solid transparent;
      display:flex;
      align-items:center;
      justify-content:space-between;
      gap:10px;
      color: var(--text);
    }
    .nav a:hover{background: rgba(127,127,127,.08)}
    .nav a.active{border-color: var(--border); background: rgba(127,127,127,.10)}

    .sideSection{margin-top:14px; padding-top:14px; border-top:1px solid var(--border)}
    .sideTitle{font-size:12px; color:var(--muted); margin:0 0 8px 10px; text-transform:uppercase; letter-spacing:.08em}

    .chip{
      display:inline-flex;
      align-items:center;
      gap:8px;
      padding:6px 10px;
      border-radius: 999px;
      background: var(--chip);
      color: var(--chipText);
      border:1px solid var(--border);
      font-size:12px;
      white-space:nowrap;
    }

    .main{
      padding: 18px 18px 40px;
      overflow:auto;
    }

    .topbar{
      display:flex;
      gap:12px;
      align-items:center;
      justify-content:space-between;
      padding: 10px 12px;
      border: 1px solid var(--border);
      background: rgba(255,255,255,.04);
      border-radius: var(--radius);
      box-shadow: var(--shadow);
      position: sticky;
      top: 12px;
      z-index: 5;
      backdrop-filter: blur(10px);
    }

    .topLeft{display:flex; align-items:center; gap:10px; min-width: 0}
    .crumbs{display:flex; align-items:center; gap:8px; min-width: 0}
    .crumbs .sep{color:var(--muted)}
    .crumbs a{color:var(--muted); text-decoration:none}
    .crumbs a:hover{color:var(--text)}
    .crumbs .current{font-weight:700; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; max-width: 38vw}

    .topRight{display:flex; align-items:center; gap:10px}

    .btn{
      border:1px solid var(--border);
      background: rgba(127,127,127,.08);
      padding: 9px 12px;
      border-radius: 12px;
      color:var(--text);
      cursor:pointer;
      transition: transform .04s ease, background .15s ease;
      display:inline-flex;
      align-items:center;
      gap:8px;
      white-space:nowrap;
    }
    .btn:hover{background: rgba(127,127,127,.12)}
    .btn:active{transform: translateY(1px)}
    .btn.primary{background: var(--primary); border-color: transparent; color: #fff}
    .btn.primary:hover{background: var(--primary2)}
    .btn.danger{background: rgba(208,52,44,.12); border-color: rgba(208,52,44,.3); color: var(--danger)}

    .seg{
      display:flex;
      border:1px solid var(--border);
      border-radius: 14px;
      overflow:hidden;
      background: rgba(127,127,127,.06);
    }
    .seg button{
      border:0;
      background: transparent;
      padding: 8px 10px;
      cursor:pointer;
      color:var(--muted);
    }
    .seg button.active{background: rgba(127,127,127,.12); color: var(--text); font-weight:700}

    .grid{
      display:grid;
      gap: 14px;
      margin-top: 14px;
    }
    .grid.cols2{grid-template-columns: 1.2fr .8fr}
    .grid.cols3{grid-template-columns: 1fr 1fr 1fr}

    @media (max-width: 1100px){
      .app{grid-template-columns: 1fr}
      .sidebar{position: relative; height:auto}
      .grid.cols2{grid-template-columns: 1fr}
      .grid.cols3{grid-template-columns: 1fr}
      .crumbs .current{max-width: 60vw}
    }

    .card{
      border:1px solid var(--border);
      background: rgba(255,255,255,.06);
      border-radius: var(--radius);
      box-shadow: var(--shadow);
      overflow:hidden;
    }
    .cardHead{
      padding: 14px 14px 10px;
      display:flex;
      align-items:flex-start;
      justify-content:space-between;
      gap:12px;
      border-bottom:1px solid var(--border);
      background: rgba(127,127,127,.05);
    }
    .cardHead h2{font-size:14px;margin:0}
    .cardHead p{margin:4px 0 0; color:var(--muted); font-size:12px}
    .cardBody{padding: 14px}

    .kpi{
      display:flex;
      flex-direction:column;
      gap:4px;
      padding: 12px;
      border:1px solid var(--border);
      border-radius: 14px;
      background: rgba(127,127,127,.06);
    }
    .kpi b{font-size:18px}
    .kpi span{font-size:12px;color:var(--muted)}

    .table{
      width:100%;
      border-collapse: collapse;
    }
    .table th, .table td{
      border-bottom:1px solid var(--border);
      padding: 10px 8px;
      font-size: 13px;
      text-align:left;
      vertical-align:top;
    }
    .table th{color:var(--muted); font-weight:600; font-size:12px}

    .tag{font-size:12px; padding:4px 8px; border-radius:999px; border:1px solid var(--border); display:inline-flex; align-items:center; gap:6px}
    .tag.ok{background: rgba(15,138,75,.12); color: var(--ok); border-color: rgba(15,138,75,.25)}
    .tag.warn{background: rgba(183,121,31,.14); color: var(--warn); border-color: rgba(183,121,31,.28)}
    .tag.bad{background: rgba(208,52,44,.12); color: var(--danger); border-color: rgba(208,52,44,.28)}
    .tag.neu{background: rgba(127,127,127,.10); color: var(--muted)}

    .progress{
      height: 10px;
      border-radius: 999px;
      border:1px solid var(--border);
      background: rgba(127,127,127,.10);
      overflow:hidden;
    }
    .progress > i{display:block; height:100%; width:0%; background: var(--primary)}

    .split{
      display:grid;
      grid-template-columns: 1.2fr .8fr;
      gap: 14px;
    }
    @media (max-width: 1100px){ .split{grid-template-columns:1fr} }

    /* ============== Tree ============== */
    .tree{display:flex; flex-direction:column; gap:10px}
    details.treeNode{border:1px solid var(--border); border-radius: 14px; background: rgba(127,127,127,.06)}
    details.treeNode > summary{
      cursor:pointer;
      list-style:none;
      display:flex;
      align-items:center;
      justify-content:space-between;
      gap:10px;
      padding: 12px 12px;
    }
    details.treeNode > summary::-webkit-details-marker{display:none}
    .nodeLeft{display:flex; flex-direction:column; gap:2px; min-width:0}
    .nodeTitle{font-weight:800; font-size:13px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis}
    .nodeMeta{font-size:12px; color:var(--muted); display:flex; gap:8px; flex-wrap:wrap}
    .nodeBody{padding: 0 12px 12px}
    .taskRow{
      display:flex;
      align-items:center;
      justify-content:space-between;
      gap:10px;
      padding: 10px 10px;
      border:1px solid var(--border);
      border-radius: 12px;
      background: rgba(255,255,255,.04);
      margin-top:8px;
    }
    .taskRow:hover{background: rgba(127,127,127,.10)}
    .taskRow .tLeft{min-width:0}
    .taskRow .tTitle{font-weight:700; font-size:13px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis}
    .taskRow .tSub{font-size:12px; color:var(--muted); margin-top:2px; display:flex; gap:8px; flex-wrap:wrap}
    .taskRow .tRight{display:flex; align-items:center; gap:8px}

    /* ============== Drawer/Modal ============== */
    .backdrop{position:fixed; inset:0; background: rgba(0,0,0,.45); display:none; z-index: 50}
    .drawer{
      position:fixed;
      top:0; right:0;
      width: min(560px, 92vw);
      height:100vh;
      background: var(--card);
      border-left:1px solid var(--border);
      box-shadow: var(--shadow);
      transform: translateX(100%);
      transition: transform .22s ease;
      z-index: 60;
      display:flex;
      flex-direction:column;
    }
    .drawer.open{transform: translateX(0)}
    .backdrop.open{display:block}
    .drawerHead{padding: 14px; border-bottom:1px solid var(--border); display:flex; justify-content:space-between; gap:10px}
    .drawerHead h3{margin:0; font-size:14px}
    .drawerBody{padding: 14px; overflow:auto}
    .drawerFoot{padding: 12px 14px; border-top:1px solid var(--border); display:flex; gap:10px; justify-content:flex-end; background: rgba(127,127,127,.05)}

    .field{display:flex; flex-direction:column; gap:6px; margin-bottom: 10px}
    .field label{font-size:12px; color:var(--muted)}
    .field input, .field textarea, .field select{
      border:1px solid var(--border);
      background: rgba(127,127,127,.08);
      padding: 10px 10px;
      border-radius: 12px;
      color: var(--text);
      outline:none;
    }
    textarea{min-height: 92px; resize: vertical}

    /* ============== Toasts ============== */
    .toasts{
      position: fixed;
      bottom: 16px;
      right: 16px;
      display:flex;
      flex-direction:column;
      gap:10px;
      z-index: 80;
      width: min(420px, 92vw);
    }
    .toast{
      border:1px solid var(--border);
      background: rgba(255,255,255,.08);
      border-radius: 14px;
      box-shadow: var(--shadow);
      padding: 12px;
      display:flex;
      gap:10px;
      align-items:flex-start;
    }
    .toast i{display:inline-flex; width:10px; height:10px; border-radius:999px; margin-top:4px; background: var(--primary)}
    .toast.ok i{background: var(--ok)}
    .toast.warn i{background: var(--warn)}
    .toast.bad i{background: var(--danger)}
    .toast b{font-size:13px}
    .toast p{margin:4px 0 0; color:var(--muted); font-size:12px}

    /* ============== Chat ============== */
    .chatBox{
      display:flex; flex-direction:column; gap:10px;
    }
    .chatLog{
      border:1px solid var(--border);
      border-radius: 14px;
      background: rgba(127,127,127,.06);
      padding: 12px;
      height: 320px;
      overflow:auto;
    }
    .msg{display:flex; gap:10px; margin-bottom: 10px}
    .avatar{width:28px;height:28px;border-radius:10px;border:1px solid var(--border); background: rgba(127,127,127,.10)}
    .bubble{
      border:1px solid var(--border);
      background: rgba(255,255,255,.05);
      border-radius: 14px;
      padding: 10px 10px;
      max-width: 100%;
    }
    .metaLine{font-size:11px;color:var(--muted); display:flex; gap:8px; align-items:center; margin-bottom:6px}
    .bubble pre{margin:0; white-space:pre-wrap; word-break:break-word; font-family: var(--mono); font-size:12px; color: var(--text)}

    .chatInput{display:flex; gap:10px}
    .chatInput input{
      flex:1;
      border:1px solid var(--border);
      border-radius: 12px;
      padding: 10px 10px;
      background: rgba(127,127,127,.08);
      color: var(--text);
    }

    /* ============== Tiny icons (inline) ============== */
    .ico{width:16px;height:16px; display:inline-block; vertical-align:middle}
    .muted{color:var(--muted)}
    .mono{font-family: var(--mono)}

    /* ============== Accessibility ============== */
    :focus-visible{outline: 3px solid rgba(47,111,237,.35); outline-offset: 2px}

  </style>
</head>
<body>
<div class="app" id="app">
  <aside class="sidebar">
    <div class="brand">
      <div class="logo" aria-hidden="true"></div>
      <div>
        <h1 id="t_brand">AI SDLC Orchestrator</h1>
        <p id="t_brandSub">Demo UI · no auth</p>
      </div>
    </div>

    <nav class="nav" id="nav">
      <a href="#/dashboard" data-route="dashboard"><span id="t_nav_dashboard">Dashboard</span><span class="chip" id="nav_projects_count">0</span></a>
      <a href="#/projects" data-route="projects"><span id="t_nav_projects">Projects</span><span class="chip" id="nav_active_count">0</span></a>
      <a href="#/docs" data-route="docs"><span id="t_nav_docs">Documents</span><span class="chip" id="nav_docs_count">0</span></a>
      <a href="#/activity" data-route="activity"><span id="t_nav_activity">Activity</span><span class="chip" id="nav_events_count">0</span></a>
      <a href="#/help" data-route="help"><span id="t_nav_help">Help</span></a>
    </nav>

    <div class="sideSection">
      <p class="sideTitle" id="t_side_quick">Quick actions</p>
      <div style="display:flex; gap:10px; padding: 0 10px 10px; flex-wrap:wrap">
        <button class="btn primary" id="btn_new_project">＋ <span id="t_new_project">New project</span></button>
        <button class="btn" id="btn_upload_doc">⤒ <span id="t_upload_doc">Upload doc</span></button>
      </div>
      <div style="padding: 0 10px 10px">
        <div class="chip" title="Mock backend">
          <span>●</span> <span id="t_mock_backend">Mock backend</span>
        </div>
      </div>
    </div>

    <div class="sideSection">
      <p class="sideTitle" id="t_side_settings">Settings</p>
      <div style="display:flex; flex-direction:column; gap:10px; padding: 0 10px 10px">
        <div>
          <div class="muted" style="font-size:12px; margin-bottom:6px" id="t_theme">Theme</div>
          <div class="seg" role="tablist" aria-label="Theme">
            <button id="btn_theme_light" class="active" role="tab">☀ <span id="t_light">Light</span></button>
            <button id="btn_theme_dark" role="tab">🌙 <span id="t_dark">Dark</span></button>
          </div>
        </div>
        <div>
          <div class="muted" style="font-size:12px; margin-bottom:6px" id="t_lang">Language</div>
          <div class="seg" role="tablist" aria-label="Language">
            <button id="btn_lang_ru" class="active" role="tab">RU</button>
            <button id="btn_lang_en" role="tab">EN</button>
          </div>
        </div>
      </div>
    </div>

    <div class="sideSection">
      <p class="sideTitle" id="t_side_hint">Hint</p>
      <div style="padding:0 10px 16px; font-size:12px; color:var(--muted); line-height:1.4">
        <span id="t_hint">Try opening a project and running a cycle. Use chat commands: </span>
        <span class="mono">/pause</span>, <span class="mono">/resume</span>, <span class="mono">/replan</span>, <span class="mono">/status</span>.
      </div>
    </div>

  </aside>

  <main class="main">
    <div class="topbar">
      <div class="topLeft">
        <div class="crumbs" id="crumbs"></div>
        <span class="chip" id="chip_system_status">● <span id="t_status_ready">Ready</span></span>
      </div>
      <div class="topRight">
        <button class="btn" id="btn_seed_data">⟲ <span id="t_reset_demo">Reset demo</span></button>
        <button class="btn" id="btn_export_json">⤓ <span id="t_export">Export JSON</span></button>
      </div>
    </div>

    <div id="view" style="margin-top:14px"></div>
  </main>
</div>

<!-- Task drawer -->
<div class="backdrop" id="backdrop"></div>
<aside class="drawer" id="drawer" aria-label="Task details">
  <div class="drawerHead">
    <div style="min-width:0">
      <h3 id="drawer_title">Task</h3>
      <div class="muted" style="font-size:12px; margin-top:4px" id="drawer_sub">—</div>
    </div>
    <button class="btn" id="drawer_close">✕</button>
  </div>
  <div class="drawerBody" id="drawer_body"></div>
  <div class="drawerFoot">
    <button class="btn" id="drawer_btn_mark_fail"><span id="t_mark_failed">Mark failed</span></button>
    <button class="btn" id="drawer_btn_mark_done"><span id="t_mark_done">Mark done</span></button>
  </div>
</aside>

<!-- Modals (simple drawers reused) -->
<div class="drawer" id="drawer_modal" aria-label="Modal" style="width:min(620px, 92vw)"></div>

<!-- Toasts -->
<div class="toasts" id="toasts"></div>

<script>
(() => {
  "use strict";

  /* =====================================================
     i18n strings
  ===================================================== */
  const STR = {
    ru: {
      brand: "AI‑система управления разработкой ПО",
      brandSub: "Демо UI · без авторизации",
      nav: {dashboard:"Дашборд", projects:"Проекты", docs:"Документы", activity:"События", help:"Справка"},
      side: {quick:"Быстрые действия", settings:"Настройки", hint:"Подсказка"},
      buttons: {
        newProject:"Новый проект", uploadDoc:"Загрузить документ", resetDemo:"Сбросить демо", export:"Экспорт JSON",
        open:"Открыть", view:"Просмотр", create:"Создать", save:"Сохранить", cancel:"Отмена",
        start:"Запустить", pause:"Пауза", resume:"Продолжить", approvePlan:"Утвердить план", replan:"Пересобрать план",
        addEpic:"Добавить эпик", addTask:"Добавить задачу", addStage:"Добавить этап",
        markDone:"Отметить готово", markFailed:"Отметить ошибка",
        upload:"Загрузить", attach:"Прикрепить", remove:"Удалить",
      },
      labels: {
        theme:"Тема", light:"Светлая", dark:"Тёмная", language:"Язык", mock:"Мок‑данные",
        statusReady:"Готово", statusRunning:"Выполнение", statusPaused:"Пауза",
        search:"Поиск", filter:"Фильтр", sort:"Сортировка",
        project:"Проект", projects:"Проекты", docs:"Документы", activity:"Активность", help:"Справка",
        progress:"Прогресс", stages:"Этапы", epics:"Эпики", tasks:"Задачи", cycle:"Цикл",
        chat:"Чат с ботом", commandPlaceholder:"Напишите сообщение или команду…",
        recent:"Недавнее", files:"Файлы", uploads:"Загрузки",
        details:"Детали", description:"Описание", artifacts:"Артефакты", logs:"Логи", dependencies:"Зависимости", agent:"Агент/роль",
        plan:"План", planDraft:"План (черновик)", planApproved:"План (утверждён)",
        history:"История циклов",
        repo:"Репозиторий", model:"Модель",
        empty:"Пока пусто",
      },
      statuses: {
        queued:"В очереди", running:"Выполняется", done:"Выполнено", failed:"Ошибка", blocked:"Заблокировано",
        draft:"Черновик", approved:"Утверждено",
        active:"Активный", testing:"Готово к тестированию", completed:"Завершён",
      },
      help: {
        title:"Что проверяем в демо",
        items:[
          "Двуязычность RU/EN и переключение тем (по умолчанию светлая).",
          "Дашборд проектов и карточка проекта.",
          "Иерархия Этап → Эпик → Задачи, статусы и прогресс.",
          "Просмотр деталей задачи (описание, артефакты, логи).",
          "Загрузка документов проекта и создание нового проекта.",
          "Демо‑оркестрация: запуск/пауза/продолжить, имитация выполнения и обновления статусов.",
          "Чат‑команды: /pause /resume /replan /status.",
        ],
        note:"Функции авторизации и управления пользователями в этом демо намеренно отключены (админка отдельно)."
      },
      hint:"Откройте проект и запустите цикл. Команды: ",
      toast:{
        created:"Создано", updated:"Обновлено", uploaded:"Загружено", running:"Процесс запущен", paused:"Процесс на паузе", resumed:"Процесс продолжен", replanned:"План обновлён",
        exported:"Экспорт готов",
      }
    },
    en: {
      brand: "AI SDLC Orchestrator",
      brandSub: "Demo UI · no auth",
      nav: {dashboard:"Dashboard", projects:"Projects", docs:"Documents", activity:"Activity", help:"Help"},
      side: {quick:"Quick actions", settings:"Settings", hint:"Hint"},
      buttons: {
        newProject:"New project", uploadDoc:"Upload document", resetDemo:"Reset demo", export:"Export JSON",
        open:"Open", view:"View", create:"Create", save:"Save", cancel:"Cancel",
        start:"Start", pause:"Pause", resume:"Resume", approvePlan:"Approve plan", replan:"Replan",
        addEpic:"Add epic", addTask:"Add task", addStage:"Add stage",
        markDone:"Mark done", markFailed:"Mark failed",
        upload:"Upload", attach:"Attach", remove:"Remove",
      },
      labels: {
        theme:"Theme", light:"Light", dark:"Dark", language:"Language", mock:"Mock backend",
        statusReady:"Ready", statusRunning:"Running", statusPaused:"Paused",
        search:"Search", filter:"Filter", sort:"Sort",
        project:"Project", projects:"Projects", docs:"Documents", activity:"Activity", help:"Help",
        progress:"Progress", stages:"Stages", epics:"Epics", tasks:"Tasks", cycle:"Cycle",
        chat:"Bot chat", commandPlaceholder:"Type a message or command…",
        recent:"Recent", files:"Files", uploads:"Uploads",
        details:"Details", description:"Description", artifacts:"Artifacts", logs:"Logs", dependencies:"Dependencies", agent:"Agent/role",
        plan:"Plan", planDraft:"Plan (draft)", planApproved:"Plan (approved)",
        history:"Iteration history",
        repo:"Repository", model:"Model",
        empty:"Nothing here yet",
      },
      statuses: {
        queued:"Queued", running:"Running", done:"Done", failed:"Failed", blocked:"Blocked",
        draft:"Draft", approved:"Approved",
        active:"Active", testing:"Ready for testing", completed:"Completed",
      },
      help: {
        title:"What this demo covers",
        items:[
          "RU/EN localization and theme toggle (default: light).",
          "Projects dashboard and project page.",
          "Hierarchy Stage → Epic → Tasks, statuses and progress.",
          "Task details (description, artifacts, logs).",
          "Project document upload and new project creation.",
          "Demo orchestration: start/pause/resume, simulated execution and live statuses.",
          "Chat commands: /pause /resume /replan /status.",
        ],
        note:"Authentication and user management are intentionally omitted in this demo (admin panel will be separate)."
      },
      hint:"Open a project and run a cycle. Commands: ",
      toast:{
        created:"Created", updated:"Updated", uploaded:"Uploaded", running:"Process started", paused:"Process paused", resumed:"Process resumed", replanned:"Plan updated",
        exported:"Export ready",
      }
    }
  };

  const LS_KEYS = {
    theme:"demo_theme",
    lang:"demo_lang",
    state:"demo_state_v1"
  };

  /* =====================================================
     Mock backend (in-memory + localStorage persistence)
  ===================================================== */
  function uid(prefix="id"){
    return `${prefix}_${Math.random().toString(16).slice(2)}_${Date.now().toString(16)}`;
  }

  function nowISO(){
    const d = new Date();
    return d.toISOString();
  }

  const DEFAULT_STATE = () => ({
    meta:{
      createdAt: nowISO(),
      version:"demo-1",
    },
    docs: [
      {
        id: uid("doc"),
        projectId: "p1",
        name: "ТЗ: многоагентная AI‑система управления разработкой ПО.docx",
        type:"docx",
        sizeKb: 284,
        uploadedAt: nowISO(),
        tags:["ТЗ","requirements"],
        source:"local demo"
      },
      {
        id: uid("doc"),
        projectId: "p2",
        name: "Architecture notes.pdf",
        type:"pdf",
        sizeKb: 512,
        uploadedAt: nowISO(),
        tags:["архитектура","RAG"],
        source:"local demo"
      }
    ],
    events: [],
    projects: [
      {
        id:"p1",
        nameRU:"Оркестратор разработки (MVP)",
        nameEN:"SDLC Orchestrator (MVP)",
        status:"active", // active | testing | completed
        repo:"gitlab.com/company/orchestrator",
        llmModel:"gpt-4 / claude (demo)",
        createdAt: nowISO(),
        updatedAt: nowISO(),
        currentIterationId:"it1",
        iterations:[
          {
            id:"it1",
            number:1,
            status:"draft", // draft | approved
            createdAt: nowISO(),
            approvedAt: null,
            stages:[
              {
                id:"s1",
                titleRU:"Этап 1 — Планирование и каркас",
                titleEN:"Stage 1 — Planning & scaffold",
                descriptionRU:"Разбор ТЗ, план, базовая структура проекта.",
                descriptionEN:"Requirement analysis, plan approval, project scaffold.",
                epics:[
                  {
                    id:"e1",
                    titleRU:"План и структура задач",
                    titleEN:"Plan & task structure",
                    descriptionRU:"Сформировать дерево Этап→Эпик→Задачи и механизм статусов.",
                    descriptionEN:"Create Stage→Epic→Task tree and status tracking.",
                    tasks:[
                      task("t1","Сформировать структуру плана","Build plan structure","planner","queued",[], ["ui","plan"]),
                      task("t2","Утверждение плана пользователем","Plan approval flow","planner","queued",["t1"], ["ui","workflow"]),
                      task("t3","Двуязычный интерфейс","Bilingual UI","frontend","queued",[], ["ui","i18n"]),
                    ]
                  },
                  {
                    id:"e2",
                    titleRU:"Интеграция Git (мок)",
                    titleEN:"Git integration (mock)",
                    descriptionRU:"Показ веток/коммитов/PR как артефактов задач.",
                    descriptionEN:"Show branches/commits/PRs as task artifacts.",
                    tasks:[
                      task("t4","Создать ветку под задачу (мок)","Create task branch (mock)","agent-coder","queued",[], ["git"]),
                      task("t5","Коммит тестов (мок)","Commit tests (mock)","agent-tester","queued",["t4"], ["git","tests"]),
                      task("t6","Коммит реализации (мок)","Commit implementation (mock)","agent-coder","queued",["t5"], ["git","code"]),
                    ]
                  }
                ]
              },
              {
                id:"s2",
                titleRU:"Этап 2 — Валидация",
                titleEN:"Stage 2 — Validation",
                descriptionRU:"AI‑ревью и тест‑прогон (в демо — симуляция).",
                descriptionEN:"AI review and test run (simulated in demo).",
                epics:[
                  {
                    id:"e3",
                    titleRU:"Код‑ревью и тесты",
                    titleEN:"Code review & tests",
                    descriptionRU:"Проверка соответствия ТЗ и прогон тестов, цикл исправлений.",
                    descriptionEN:"Verify requirements, run tests, iterate fixes.",
                    tasks:[
                      task("t7","AI код‑ревью (мок отчёт)","AI code review (mock report)","agent-reviewer","blocked",["t6"],["review"]),
                      task("t8","Запуск тестов (мок)","Run tests (mock)","agent-tester","blocked",["t6"],["tests","ci"]),
                      task("t9","Создать задачи на исправление (пример)","Create fix tasks (example)","planner","blocked",["t7","t8"],["workflow"]),
                    ]
                  }
                ]
              }
            ]
          }
        ]
      },
      {
        id:"p2",
        nameRU:"RAG‑хранилище проекта",
        nameEN:"Project Knowledge Base (RAG)",
        status:"testing",
        repo:"github.com/company/rag-store",
        llmModel:"local llama (demo)",
        createdAt: nowISO(),
        updatedAt: nowISO(),
        currentIterationId:"it2",
        iterations:[
          {
            id:"it2",
            number:2,
            status:"approved",
            createdAt: nowISO(),
            approvedAt: nowISO(),
            stages:[
              {
                id:uid("s"),
                titleRU:"Этап 1 — Индексация",
                titleEN:"Stage 1 — Indexing",
                descriptionRU:"Загрузка кода, обновление embeddings.",
                descriptionEN:"Load codebase and refresh embeddings.",
                epics:[
                  {
                    id:uid("e"),
                    titleRU:"Инкрементальное обновление",
                    titleEN:"Incremental refresh",
                    descriptionRU:"Индексация после каждого мерджа.",
                    descriptionEN:"Re-index after each merge.",
                    tasks:[
                      task(uid("t"),"Сканировать репозиторий","Scan repository","agent-devops","done",[],["rag"]),
                      task(uid("t"),"Построить индекс","Build index","agent-devops","done",[],["rag"]),
                      task(uid("t"),"Проверить поиск","Validate retrieval","agent-reviewer","done",[],["rag","qa"]),
                    ]
                  }
                ]
              }
            ]
          }
        ]
      }
    ],
    runtime:{
      activeProjectId: "p1",
      runState: "ready", // ready|running|paused
      runner: {timer:0, tickMs:1200, currentTaskId:null}
    }
  });

  function task(id, ru, en, role, status, deps=[], tags=[]){
    return {
      id,
      titleRU: ru,
      titleEN: en,
      role,
      status, // queued|running|done|failed|blocked
      deps,
      tags,
      descriptionRU: `Подробности: ${ru}.\n\nОжидаемый результат: демонстрация шага конвейера (план → реализация → проверка).`,
      descriptionEN: `Details: ${en}.\n\nExpected outcome: show the SDLC pipeline step (plan → build → validate).`,
      artifacts: [],
      logs: [],
      startedAt: null,
      finishedAt: null,
    };
  }

  const store = {
    load(){
      const raw = localStorage.getItem(LS_KEYS.state);
      if(!raw) return DEFAULT_STATE();
      try{
        const data = JSON.parse(raw);
        // simple schema guard
        if(!data || !Array.isArray(data.projects)) return DEFAULT_STATE();
        return data;
      }catch(e){
        return DEFAULT_STATE();
      }
    },
    save(state){
      localStorage.setItem(LS_KEYS.state, JSON.stringify(state));
    }
  };

  let STATE = store.load();

  /* =====================================================
     Helpers
  ===================================================== */
  const $ = (sel, root=document) => root.querySelector(sel);
  const $$ = (sel, root=document) => Array.from(root.querySelectorAll(sel));

  function t(){
    const lang = getLang();
    return STR[lang];
  }
  function getLang(){
    return localStorage.getItem(LS_KEYS.lang) || "ru";
  }
  function setLang(lang){
    localStorage.setItem(LS_KEYS.lang, lang);
    applyI18n();
    render();
    toast("ok", STR[lang].toast.updated, lang === "ru" ? "Язык переключён" : "Language switched");
  }

  function getTheme(){
    return localStorage.getItem(LS_KEYS.theme) || "light";
  }
  function setTheme(theme){
    localStorage.setItem(LS_KEYS.theme, theme);
    document.documentElement.setAttribute("data-theme", theme);
    updateThemeButtons();
    toast("ok", theme === "light" ? (getLang()==="ru"?"Тема":"Theme") : (getLang()==="ru"?"Тема":"Theme"),
          theme === "light" ? (getLang()==="ru"?"Светлая тема включена":"Light theme enabled") : (getLang()==="ru"?"Тёмная тема включена":"Dark theme enabled"));
  }

  function updateThemeButtons(){
    const theme = getTheme();
    $("#btn_theme_light").classList.toggle("active", theme === "light");
    $("#btn_theme_dark").classList.toggle("active", theme === "dark");
  }
  function updateLangButtons(){
    const lang = getLang();
    $("#btn_lang_ru").classList.toggle("active", lang === "ru");
    $("#btn_lang_en").classList.toggle("active", lang === "en");
  }

  function fmtDate(iso){
    if(!iso) return "—";
    const d = new Date(iso);
    return d.toLocaleString(getLang()==="ru"?"ru-RU":"en-GB", {year:"numeric",month:"short",day:"2-digit",hour:"2-digit",minute:"2-digit"});
  }

  function statusTag(status){
    const S = t().statuses;
    const map = {
      queued:{cls:"neu", label:S.queued},
      running:{cls:"warn", label:S.running},
      done:{cls:"ok", label:S.done},
      failed:{cls:"bad", label:S.failed},
      blocked:{cls:"neu", label:S.blocked},
    };
    const v = map[status] || {cls:"neu", label:status};
    return `<span class="tag ${v.cls}">${escapeHtml(v.label)}</span>`;
  }

  function projectStatusTag(pStatus){
    const S = t().statuses;
    const map = {
      active:{cls:"warn", label:S.active},
      testing:{cls:"neu", label:S.testing},
      completed:{cls:"ok", label:S.completed}
    };
    const v = map[pStatus] || {cls:"neu", label:pStatus};
    return `<span class="tag ${v.cls}">${escapeHtml(v.label)}</span>`;
  }

  function escapeHtml(str){
    return (str ?? "").toString()
      .replaceAll("&","&amp;")
      .replaceAll("<","&lt;")
      .replaceAll(">","&gt;")
      .replaceAll('"',"&quot;")
      .replaceAll("'","&#039;");
  }

  function findProject(pid){
    return STATE.projects.find(p => p.id === pid);
  }

  function getActiveProject(){
    return findProject(STATE.runtime.activeProjectId) || STATE.projects[0];
  }

  function getIteration(project){
    return project.iterations.find(it => it.id === project.currentIterationId) || project.iterations[0];
  }

  function allTasks(iteration){
    const out=[];
    for(const st of iteration.stages){
      for(const ep of st.epics){
        for(const tk of ep.tasks) out.push({stage:st, epic:ep, task:tk});
      }
    }
    return out;
  }

  function computeProgress(iteration){
    const tasks = allTasks(iteration).map(x=>x.task);
    const total = tasks.length || 1;
    const done = tasks.filter(t=>t.status==="done").length;
    const failed = tasks.filter(t=>t.status==="failed").length;
    const running = tasks.filter(t=>t.status==="running").length;
    return {total, done, failed, running, pct: Math.round((done/total)*100)};
  }

  function addEvent(type, title, details){
    STATE.events.unshift({
      id: uid("ev"),
      at: nowISO(),
      type,
      title,
      details
    });
    if(STATE.events.length>60) STATE.events.length = 60;
  }

  function toast(kind, title, text){
    const box = $("#toasts");
    const el = document.createElement("div");
    el.className = `toast ${kind||""}`;
    el.innerHTML = `<i aria-hidden="true"></i><div><b>${escapeHtml(title||"")}</b><p>${escapeHtml(text||"")}</p></div>`;
    box.appendChild(el);
    setTimeout(()=>{ el.style.opacity = "0"; el.style.transform = "translateY(6px)"; }, 3200);
    setTimeout(()=>{ el.remove(); }, 3600);
  }

  /* =====================================================
     Router
  ===================================================== */
  const routes = {
    dashboard: renderDashboard,
    projects: renderProjects,
    docs: renderDocs,
    activity: renderActivity,
    help: renderHelp,
    project: renderProject,
  };

  function parseHash(){
    const hash = location.hash || "#/dashboard";
    const parts = hash.replace(/^#\//,"").split("/");
    const name = parts[0] || "dashboard";
    return {name, parts};
  }

  function setActiveNav(route){
    $$(".nav a").forEach(a => a.classList.toggle("active", a.dataset.route===route));
  }

  function setCrumbs(list){
    const c = $("#crumbs");
    c.innerHTML = "";
    const lang = getLang();
    const frag = [];
    for(let i=0;i<list.length;i++){
      const it = list[i];
      if(i>0) frag.push(`<span class="sep">›</span>`);
      if(it.href) frag.push(`<a href="${it.href}">${escapeHtml(it.label)}</a>`);
      else frag.push(`<span class="current">${escapeHtml(it.label)}</span>`);
    }
    c.innerHTML = frag.join(" ");
  }

  function render(){
    const {name, parts} = parseHash();
    const view = $("#view");
    const lang = getLang();

    // update counters in side nav
    $("#nav_projects_count").textContent = STATE.projects.length;
    $("#nav_active_count").textContent = STATE.projects.filter(p=>p.status==="active").length;
    $("#nav_docs_count").textContent = STATE.docs.length;
    $("#nav_events_count").textContent = STATE.events.length;

    // system status chip
    const run = STATE.runtime.runState;
    const chip = $("#chip_system_status");
    chip.innerHTML = "● " + escapeHtml(run === "running" ? t().labels.statusRunning : run === "paused" ? t().labels.statusPaused : t().labels.statusReady);

    if(name === "project"){
      setActiveNav(null);
    }else{
      setActiveNav(name);
    }

    const fn = routes[name] || renderDashboard;
    view.innerHTML = fn(parts);

    // bind view-specific actions
    bindViewActions();

    // persist
    store.save(STATE);
  }

  window.addEventListener("hashchange", render);

  /* =====================================================
     Renderers
  ===================================================== */
  function renderDashboard(){
    setCrumbs([
      {label: t().nav.dashboard}
    ]);

    const cards = STATE.projects.map(p => {
      const it = getIteration(p);
      const pr = computeProgress(it);
      const title = getLang()==="ru" ? p.nameRU : p.nameEN;
      return `
        <div class="card">
          <div class="cardHead">
            <div style="min-width:0">
              <h2 style="white-space:nowrap; overflow:hidden; text-overflow:ellipsis">${escapeHtml(title)}</h2>
              <p>${projectStatusTag(p.status)} <span class="muted">·</span> <span class="muted">${escapeHtml(t().labels.repo)}:</span> <span class="mono">${escapeHtml(p.repo)}</span></p>
            </div>
            <div style="display:flex; gap:10px; align-items:center; flex-wrap:wrap; justify-content:flex-end">
              <div style="min-width:160px">
                <div class="muted" style="font-size:12px; margin-bottom:6px">${escapeHtml(t().labels.progress)}: <b>${pr.pct}%</b></div>
                <div class="progress" aria-label="progress"><i style="width:${pr.pct}%"></i></div>
              </div>
              <a class="btn primary" href="#/project/${encodeURIComponent(p.id)}">${escapeHtml(t().buttons.open)}</a>
            </div>
          </div>
          <div class="cardBody">
            <div class="grid cols3">
              <div class="kpi"><b>${pr.done}/${pr.total}</b><span>${escapeHtml(t().labels.tasks)} · ${escapeHtml(t().statuses.done)}</span></div>
              <div class="kpi"><b>${pr.running}</b><span>${escapeHtml(t().statuses.running)}</span></div>
              <div class="kpi"><b>${STATE.docs.filter(d=>d.projectId===p.id).length}</b><span>${escapeHtml(t().labels.docs)}</span></div>
            </div>
          </div>
        </div>
      `;
    }).join("\n");

    return `
      <div class="grid" style="gap:14px">
        <div class="card">
          <div class="cardHead">
            <div>
              <h2>${escapeHtml(getLang()==="ru"?"Обзор":"Overview")}</h2>
              <p>${escapeHtml(getLang()==="ru"?"Система демонстрирует управление проектами, планом и симуляцией выполнения.":"The demo shows projects, planning and a simulated execution loop.")}</p>
            </div>
            <div style="display:flex; gap:10px; align-items:center; flex-wrap:wrap">
              <button class="btn primary" data-action="openNewProject">＋ ${escapeHtml(t().buttons.newProject)}</button>
              <button class="btn" data-action="openUploadDoc">⤒ ${escapeHtml(t().buttons.uploadDoc)}</button>
            </div>
          </div>
          <div class="cardBody">
            <div class="grid cols3">
              <div class="kpi"><b>${STATE.projects.length}</b><span>${escapeHtml(t().labels.projects)}</span></div>
              <div class="kpi"><b>${STATE.docs.length}</b><span>${escapeHtml(t().labels.docs)}</span></div>
              <div class="kpi"><b>${STATE.events.length}</b><span>${escapeHtml(t().nav.activity)}</span></div>
            </div>
          </div>
        </div>

        ${cards}
      </div>
    `;
  }

  function renderProjects(){
    setCrumbs([
      {label: t().nav.projects}
    ]);

    const q = (new URLSearchParams(location.hash.split("?")[1]||"")).get("q") || "";
    const list = STATE.projects
      .filter(p => {
        const name = (p.nameRU+" "+p.nameEN+" "+p.repo).toLowerCase();
        return name.includes(q.toLowerCase());
      })
      .map(p => {
        const title = getLang()==="ru" ? p.nameRU : p.nameEN;
        const it = getIteration(p);
        const pr = computeProgress(it);
        return `
          <tr>
            <td>
              <div style="display:flex; flex-direction:column; gap:4px">
                <b>${escapeHtml(title)}</b>
                <span class="muted" style="font-size:12px">${escapeHtml(p.repo)}</span>
              </div>
            </td>
            <td>${projectStatusTag(p.status)}</td>
            <td style="min-width:220px">
              <div style="display:flex; align-items:center; gap:10px">
                <div class="progress" style="flex:1"><i style="width:${pr.pct}%"></i></div>
                <span class="muted" style="font-size:12px">${pr.pct}%</span>
              </div>
            </td>
            <td class="muted" style="font-size:12px">${fmtDate(p.updatedAt)}</td>
            <td style="text-align:right">
              <a class="btn primary" href="#/project/${encodeURIComponent(p.id)}">${escapeHtml(t().buttons.open)}</a>
            </td>
          </tr>
        `;
      }).join("\n");

    return `
      <div class="card">
        <div class="cardHead">
          <div>
            <h2>${escapeHtml(t().labels.projects)}</h2>
            <p>${escapeHtml(getLang()==="ru"?"Список проектов (мок‑данные).":"Project list (mock data).")}</p>
          </div>
          <div style="display:flex; gap:10px; flex-wrap:wrap; align-items:center">
            <input id="projects_search" placeholder="${escapeHtml(t().labels.search)}" value="${escapeHtml(q)}" style="border:1px solid var(--border); border-radius:12px; padding:9px 10px; background: rgba(127,127,127,.08); color:var(--text)" />
            <button class="btn primary" data-action="openNewProject">＋ ${escapeHtml(t().buttons.newProject)}</button>
          </div>
        </div>
        <div class="cardBody" style="padding:0">
          <table class="table" aria-label="projects">
            <thead>
              <tr>
                <th>${escapeHtml(getLang()==="ru"?"Название":"Name")}</th>
                <th>${escapeHtml(getLang()==="ru"?"Статус":"Status")}</th>
                <th>${escapeHtml(t().labels.progress)}</th>
                <th>${escapeHtml(getLang()==="ru"?"Обновлено":"Updated")}</th>
                <th></th>
              </tr>
            </thead>
            <tbody>${list || `
              <tr><td colspan="5" class="muted" style="padding:14px">${escapeHtml(t().labels.empty)}</td></tr>
            `}</tbody>
          </table>
        </div>
      </div>
    `;
  }

  function renderDocs(){
    setCrumbs([{label: t().nav.docs}]);

    const rows = STATE.docs.map(d => {
      const p = findProject(d.projectId);
      const pName = p ? (getLang()==="ru" ? p.nameRU : p.nameEN) : "—";
      return `
        <tr>
          <td><b>${escapeHtml(d.name)}</b><div class="muted" style="font-size:12px">${escapeHtml(d.tags.join(", "))}</div></td>
          <td class="muted" style="font-size:12px">${escapeHtml(pName)}</td>
          <td class="muted" style="font-size:12px">${escapeHtml(d.type.toUpperCase())} · ${escapeHtml(d.sizeKb)} KB</td>
          <td class="muted" style="font-size:12px">${fmtDate(d.uploadedAt)}</td>
          <td style="text-align:right">
            <button class="btn" data-action="previewDoc" data-doc="${escapeHtml(d.id)}">${escapeHtml(t().buttons.view)}</button>
            <button class="btn danger" data-action="removeDoc" data-doc="${escapeHtml(d.id)}">${escapeHtml(t().buttons.remove)}</button>
          </td>
        </tr>
      `;
    }).join("\n");

    return `
      <div class="card">
        <div class="cardHead">
          <div>
            <h2>${escapeHtml(t().labels.docs)}</h2>
            <p>${escapeHtml(getLang()==="ru"?"Загрузка и привязка документов к проектам (в демо — локальные записи).":"Upload and attach docs to projects (demo stores local entries).")}</p>
          </div>
          <div style="display:flex; gap:10px; flex-wrap:wrap">
            <button class="btn primary" data-action="openUploadDoc">⤒ ${escapeHtml(t().buttons.uploadDoc)}</button>
          </div>
        </div>
        <div class="cardBody" style="padding:0">
          <table class="table" aria-label="docs">
            <thead>
              <tr>
                <th>${escapeHtml(getLang()==="ru"?"Документ":"Document")}</th>
                <th>${escapeHtml(t().labels.project)}</th>
                <th>${escapeHtml(getLang()==="ru"?"Тип / размер":"Type / size")}</th>
                <th>${escapeHtml(getLang()==="ru"?"Загружено":"Uploaded")}</th>
                <th></th>
              </tr>
            </thead>
            <tbody>${rows || `<tr><td colspan="5" class="muted" style="padding:14px">${escapeHtml(t().labels.empty)}</td></tr>`}</tbody>
          </table>
        </div>
      </div>
    `;
  }

  function renderActivity(){
    setCrumbs([{label: t().nav.activity}]);

    const rows = STATE.events.map(ev => {
      return `
        <tr>
          <td class="muted" style="font-size:12px">${fmtDate(ev.at)}</td>
          <td><b>${escapeHtml(ev.title)}</b><div class="muted" style="font-size:12px">${escapeHtml(ev.details||"")}</div></td>
          <td class="muted" style="font-size:12px">${escapeHtml(ev.type)}</td>
        </tr>
      `;
    }).join("\n");

    return `
      <div class="card">
        <div class="cardHead">
          <div>
            <h2>${escapeHtml(t().nav.activity)}</h2>
            <p>${escapeHtml(getLang()==="ru"?"Лента изменений и событий процесса (мок).":"Event log for the process (mock).")}</p>
          </div>
          <div style="display:flex; gap:10px">
            <button class="btn" data-action="clearEvents">${escapeHtml(getLang()==="ru"?"Очистить":"Clear")}</button>
          </div>
        </div>
        <div class="cardBody" style="padding:0">
          <table class="table" aria-label="events">
            <thead>
              <tr>
                <th style="width:190px">${escapeHtml(getLang()==="ru"?"Время":"Time")}</th>
                <th>${escapeHtml(getLang()==="ru"?"Событие":"Event")}</th>
                <th style="width:150px">${escapeHtml(getLang()==="ru"?"Тип":"Type")}</th>
              </tr>
            </thead>
            <tbody>${rows || `<tr><td colspan="3" class="muted" style="padding:14px">${escapeHtml(t().labels.empty)}</td></tr>`}</tbody>
          </table>
        </div>
      </div>
    `;
  }

  function renderHelp(){
    setCrumbs([{label: t().nav.help}]);
    const H = t().help;
    return `
      <div class="grid cols2">
        <div class="card">
          <div class="cardHead">
            <div>
              <h2>${escapeHtml(H.title)}</h2>
              <p>${escapeHtml(getLang()==="ru"?"Ориентировано на ТЗ: дашборд проектов, страница проекта, дерево задач, детали задачи, чат/команды, уведомления, двуязычность.":"Aligned to the spec: project dashboard, project page, task tree, task details, chat/commands, notifications, bilingual UI.")}</p>
            </div>
          </div>
          <div class="cardBody">
            <ol style="margin:0; padding-left:18px; color:var(--text); line-height:1.6">
              ${H.items.map(x=>`<li>${escapeHtml(x)}</li>`).join("\n")}
            </ol>
            <div style="margin-top:12px; color:var(--muted); font-size:12px">${escapeHtml(H.note)}</div>
          </div>
        </div>
        <div class="card">
          <div class="cardHead">
            <div>
              <h2>${escapeHtml(getLang()==="ru"?"Горячие сценарии":"Quick scenarios")}</h2>
              <p>${escapeHtml(getLang()==="ru"?"Проверяйте навигацию и консистентность статусов.":"Validate navigation and status consistency.")}</p>
            </div>
          </div>
          <div class="cardBody" style="line-height:1.6">
            <div class="chip">1</div> ${escapeHtml(getLang()==="ru"?"Откройте проект → запустите цикл → поставьте на паузу → продолжите.":"Open a project → start → pause → resume.")}
            <br/><br/>
            <div class="chip">2</div> ${escapeHtml(getLang()==="ru"?"Клик по задаче → смотреть артефакты/логи → вручную отметить done/failed.":"Click a task → inspect artifacts/logs → mark done/failed.")}
            <br/><br/>
            <div class="chip">3</div> ${escapeHtml(getLang()==="ru"?"Загрузите документ и привяжите к проекту.":"Upload a document and attach to a project.")}
            <br/><br/>
            <div class="chip">4</div> ${escapeHtml(getLang()==="ru"?"Создайте новый проект с ТЗ (вставьте текст) → сформируйте план (мок) → утвердите.":"Create a project with a spec text → generate plan (mock) → approve.")}
          </div>
        </div>
      </div>
    `;
  }

  function renderProject(parts){
    const pid = decodeURIComponent(parts[1]||STATE.runtime.activeProjectId||"p1");
    const p = findProject(pid) || getActiveProject();
    STATE.runtime.activeProjectId = p.id;

    const it = getIteration(p);
    const pr = computeProgress(it);

    setCrumbs([
      {label: t().nav.projects, href: "#/projects"},
      {label: getLang()==="ru"?p.nameRU:p.nameEN}
    ]);

    const planStatus = it.status === "approved" ? t().labels.planApproved : t().labels.planDraft;

    const controls = (() => {
      const rs = STATE.runtime.runState;
      const canStart = rs === "ready";
      const canPause = rs === "running";
      const canResume = rs === "paused";

      return `
        <div style="display:flex; gap:10px; flex-wrap:wrap">
          <button class="btn primary" data-action="runStart" ${canStart?"":"disabled"}>▶ ${escapeHtml(t().buttons.start)}</button>
          <button class="btn" data-action="runPause" ${canPause?"":"disabled"}>⏸ ${escapeHtml(t().buttons.pause)}</button>
          <button class="btn" data-action="runResume" ${canResume?"":"disabled"}>⏵ ${escapeHtml(t().buttons.resume)}</button>
          <button class="btn" data-action="replan">⟲ ${escapeHtml(t().buttons.replan)}</button>
          <button class="btn" data-action="approvePlan" ${it.status==="approved"?"disabled":""}>✓ ${escapeHtml(t().buttons.approvePlan)}</button>
        </div>
      `;
    })();

    const docCount = STATE.docs.filter(d=>d.projectId===p.id).length;

    const stageTree = it.stages.map(st => {
      const stTitle = getLang()==="ru"?st.titleRU:st.titleEN;
      const stDesc = getLang()==="ru"?st.descriptionRU:st.descriptionEN;

      const stTasks = [];
      for(const ep of st.epics){
        stTasks.push(...ep.tasks);
      }
      const stProg = {total: stTasks.length||1, done: stTasks.filter(x=>x.status==="done").length};
      const stPct = Math.round((stProg.done/stProg.total)*100);

      const epicsHtml = st.epics.map(ep => {
        const epTitle = getLang()==="ru"?ep.titleRU:ep.titleEN;
        const epDesc = getLang()==="ru"?ep.descriptionRU:ep.descriptionEN;
        const epTotal = ep.tasks.length||1;
        const epDone = ep.tasks.filter(x=>x.status==="done").length;
        const epPct = Math.round((epDone/epTotal)*100);

        const tasksHtml = ep.tasks.map(tk => {
          const title = getLang()==="ru"?tk.titleRU:tk.titleEN;
          const deps = tk.deps?.length ? (getLang()==="ru"?`Зависит от: ${tk.deps.join(", ")}`:`Depends on: ${tk.deps.join(", ")}`) : (getLang()==="ru"?"Без зависимостей":"No dependencies");
          const tags = (tk.tags||[]).map(x=>`<span class="chip">${escapeHtml(x)}</span>`).join(" ");
          return `
            <div class="taskRow" role="button" tabindex="0" data-action="openTask" data-task="${escapeHtml(tk.id)}">
              <div class="tLeft">
                <div class="tTitle">${escapeHtml(title)}</div>
                <div class="tSub">
                  <span class="muted">${escapeHtml(t().labels.agent)}:</span> <span class="mono">${escapeHtml(tk.role)}</span>
                  <span class="muted">·</span>
                  <span class="muted">${escapeHtml(deps)}</span>
                </div>
                <div class="tSub" style="margin-top:6px">${tags}</div>
              </div>
              <div class="tRight">
                ${statusTag(tk.status)}
                <span class="muted" aria-hidden="true">›</span>
              </div>
            </div>
          `;
        }).join("\n");

        return `
          <details class="treeNode">
            <summary>
              <div class="nodeLeft">
                <div class="nodeTitle">${escapeHtml(epTitle)}</div>
                <div class="nodeMeta">
                  <span>${escapeHtml(epDone)}/${escapeHtml(epTotal)} ${escapeHtml(t().labels.tasks)}</span>
                  <span class="muted">·</span>
                  <span>${escapeHtml(epPct)}%</span>
                  <span class="muted">·</span>
                  <span class="muted">${escapeHtml(epDesc)}</span>
                </div>
              </div>
              <div style="display:flex; align-items:center; gap:10px">
                <div class="progress" style="width:140px"><i style="width:${epPct}%"></i></div>
                ${statusTag(epPct===100?"done":"queued")}
              </div>
            </summary>
            <div class="nodeBody">
              <button class="btn" data-action="addTask" data-epic="${escapeHtml(ep.id)}">＋ ${escapeHtml(t().buttons.addTask)}</button>
              ${tasksHtml}
            </div>
          </details>
        `;
      }).join("\n");

      return `
        <details class="treeNode" open>
          <summary>
            <div class="nodeLeft">
              <div class="nodeTitle">${escapeHtml(stTitle)}</div>
              <div class="nodeMeta">
                <span>${escapeHtml(stProg.done)}/${escapeHtml(stProg.total)} ${escapeHtml(t().labels.tasks)}</span>
                <span class="muted">·</span>
                <span>${escapeHtml(stPct)}%</span>
                <span class="muted">·</span>
                <span class="muted">${escapeHtml(stDesc)}</span>
              </div>
            </div>
            <div style="display:flex; align-items:center; gap:10px">
              <div class="progress" style="width:160px"><i style="width:${stPct}%"></i></div>
              ${statusTag(stPct===100?"done":"queued")}
            </div>
          </summary>
          <div class="nodeBody">
            <div style="display:flex; gap:10px; flex-wrap:wrap">
              <button class="btn" data-action="addEpic" data-stage="${escapeHtml(st.id)}">＋ ${escapeHtml(t().buttons.addEpic)}</button>
            </div>
            <div class="tree" style="margin-top:10px">${epicsHtml}</div>
          </div>
        </details>
      `;
    }).join("\n");

    const rightPane = `
      <div class="card">
        <div class="cardHead">
          <div>
            <h2>${escapeHtml(t().labels.details)}</h2>
            <p>${projectStatusTag(p.status)} <span class="muted">·</span> ${escapeHtml(planStatus)}</p>
          </div>
          <div>${controls}</div>
        </div>
        <div class="cardBody">
          <div class="grid cols3">
            <div class="kpi"><b>${pr.pct}%</b><span>${escapeHtml(t().labels.progress)}</span></div>
            <div class="kpi"><b>${docCount}</b><span>${escapeHtml(t().labels.docs)}</span></div>
            <div class="kpi"><b>${escapeHtml(it.number)}</b><span>${escapeHtml(t().labels.cycle)}</span></div>
          </div>
          <div style="margin-top:12px">
            <div class="muted" style="font-size:12px; margin-bottom:6px">${escapeHtml(t().labels.repo)}</div>
            <div class="mono" style="font-size:12px">${escapeHtml(p.repo)}</div>
            <div class="muted" style="font-size:12px; margin:10px 0 6px">${escapeHtml(t().labels.model)}</div>
            <div class="mono" style="font-size:12px">${escapeHtml(p.llmModel)}</div>
          </div>
          <hr style="border:0; border-top:1px solid var(--border); margin: 14px 0" />
          <div style="display:flex; gap:10px; flex-wrap:wrap">
            <button class="btn" data-action="openUploadDoc">⤒ ${escapeHtml(t().buttons.uploadDoc)}</button>
            <button class="btn" data-action="openNewProject">＋ ${escapeHtml(t().buttons.newProject)}</button>
          </div>
        </div>
      </div>

      <div class="card">
        <div class="cardHead">
          <div>
            <h2>${escapeHtml(t().labels.chat)}</h2>
            <p>${escapeHtml(getLang()==="ru"?"Команды управляют процессом (симуляция).":"Commands control the process (simulation).")}</p>
          </div>
        </div>
        <div class="cardBody">
          <div class="chatBox">
            <div class="chatLog" id="chatLog"></div>
            <div class="chatInput">
              <input id="chatInput" placeholder="${escapeHtml(t().labels.commandPlaceholder)}" />
              <button class="btn primary" data-action="sendChat">➤</button>
            </div>
          </div>
        </div>
      </div>

      <div class="card">
        <div class="cardHead">
          <div>
            <h2>${escapeHtml(t().labels.history)}</h2>
            <p>${escapeHtml(getLang()==="ru"?"Переключение циклов в демо (read‑only).":"Switch iterations (read‑only in demo).")}</p>
          </div>
        </div>
        <div class="cardBody">
          ${p.iterations.map(iter => {
            const isCur = iter.id === p.currentIterationId;
            return `
              <div style="display:flex; justify-content:space-between; align-items:center; gap:10px; border:1px solid var(--border); border-radius: 14px; padding: 10px 10px; background: rgba(127,127,127,.06); margin-bottom:10px">
                <div>
                  <b>${escapeHtml(t().labels.cycle)} ${escapeHtml(iter.number)}</b>
                  <div class="muted" style="font-size:12px">${escapeHtml(t().statuses[iter.status] || iter.status)} · ${escapeHtml(getLang()==="ru"?"создан":"created")}: ${fmtDate(iter.createdAt)}</div>
                </div>
                <div style="display:flex; gap:10px; align-items:center">
                  ${isCur ? `<span class="chip">${escapeHtml(getLang()==="ru"?"Текущий":"Current")}</span>` : `<button class="btn" data-action="switchIteration" data-it="${escapeHtml(iter.id)}">${escapeHtml(getLang()==="ru"?"Сделать текущим":"Make current")}</button>`}
                </div>
              </div>
            `;
          }).join("\n")}
        </div>
      </div>
    `;

    return `
      <div class="split">
        <div class="card">
          <div class="cardHead">
            <div>
              <h2>${escapeHtml(t().labels.plan)}</h2>
              <p>${escapeHtml(getLang()==="ru"?"Иерархия Этап → Эпик → Задача и статусы выполнения.":"Stage → Epic → Task hierarchy and execution statuses.")}</p>
            </div>
            <div style="display:flex; gap:10px; flex-wrap:wrap">
              <button class="btn" data-action="addStage">＋ ${escapeHtml(t().buttons.addStage)}</button>
            </div>
          </div>
          <div class="cardBody">
            <div class="tree">${stageTree}</div>
          </div>
        </div>
        <div class="grid" style="gap:14px">
          ${rightPane}
        </div>
      </div>
    `;
  }

  /* =====================================================
     Drawer (task details)
  ===================================================== */
  let CURRENT_TASK = null;

  function openTaskDrawer(projectId, taskId){
    const p = findProject(projectId);
    const it = getIteration(p);
    const match = allTasks(it).find(x=>x.task.id===taskId);
    if(!match) return;

    const tk = match.task;
    CURRENT_TASK = {projectId, taskId};

    const title = getLang()==="ru" ? tk.titleRU : tk.titleEN;
    $("#drawer_title").textContent = title;
    $("#drawer_sub").textContent = `${t().labels.agent}: ${tk.role} · ${t().labels.cycle} ${it.number}`;

    // seed artifacts for demo when task opens first time
    if(tk.artifacts.length===0){
      if(tk.tags.includes("git")){
        tk.artifacts.push({
          type:"git",
          label:"Branch",
          value:`feat/${p.id}-${tk.id}`
        });
        tk.artifacts.push({
          type:"git",
          label:"Commit",
          value:`${Math.random().toString(16).slice(2,9)}${Math.random().toString(16).slice(2,9)}`
        });
        tk.artifacts.push({
          type:"git",
          label:"PR/MR",
          value:`#${Math.floor(10+Math.random()*90)}`
        });
      }
      if(tk.tags.includes("review")){
        tk.artifacts.push({type:"report", label: getLang()==="ru"?"Отчёт ревью":"Review report", value: getLang()==="ru"?"Найдено 2 замечания (пример).":"2 findings (example)."});
      }
      if(tk.tags.includes("tests")){
        tk.artifacts.push({type:"ci", label: getLang()==="ru"?"Прогон тестов":"Test run", value: getLang()==="ru"?"pytest · 12 passed":"pytest · 12 passed"});
      }
    }

    const deps = tk.deps?.length ? tk.deps.map(d=>`<span class="chip">${escapeHtml(d)}</span>`).join(" ") : `<span class="muted">—</span>`;
    const tags = (tk.tags||[]).map(x=>`<span class="chip">${escapeHtml(x)}</span>`).join(" ") || `<span class="muted">—</span>`;

    const desc = getLang()==="ru" ? tk.descriptionRU : tk.descriptionEN;

    const artifacts = (tk.artifacts||[]).length ? tk.artifacts.map(a=>{
      return `
        <div style="display:flex; justify-content:space-between; gap:10px; padding:10px 10px; border:1px solid var(--border); border-radius: 12px; background: rgba(127,127,127,.06); margin-bottom:8px">
          <div>
            <b>${escapeHtml(a.label)}</b>
            <div class="muted" style="font-size:12px">${escapeHtml(a.type)}</div>
          </div>
          <div class="mono" style="font-size:12px; max-width: 60%; overflow:hidden; text-overflow:ellipsis">${escapeHtml(a.value)}</div>
        </div>
      `;
    }).join("\n") : `<div class="muted">${escapeHtml(t().labels.empty)}</div>`;

    const logs = (tk.logs||[]).length ? tk.logs.map(l=>`<div style="border:1px solid var(--border); border-radius:12px; padding:10px; background: rgba(127,127,127,.06); margin-bottom:8px"><div class="muted" style="font-size:11px">${fmtDate(l.at)} · ${escapeHtml(l.level)}</div><div class="mono" style="font-size:12px; margin-top:6px">${escapeHtml(l.msg)}</div></div>`).join("") : `<div class="muted">${escapeHtml(t().labels.empty)}</div>`;

    const html = `
      <div style="display:flex; justify-content:space-between; align-items:center; gap:10px; margin-bottom: 10px">
        <div>${statusTag(tk.status)}</div>
        <div class="muted" style="font-size:12px">${escapeHtml(getLang()==="ru"?"Начало":"Start")}: ${fmtDate(tk.startedAt)} · ${escapeHtml(getLang()==="ru"?"Финиш":"Finish")}: ${fmtDate(tk.finishedAt)}</div>
      </div>
      <div class="field">
        <label>${escapeHtml(t().labels.description)}</label>
        <textarea id="task_desc" spellcheck="false">${escapeHtml(desc)}</textarea>
      </div>
      <div class="grid" style="grid-template-columns: 1fr 1fr">
        <div>
          <div class="muted" style="font-size:12px; margin-bottom:6px">${escapeHtml(t().labels.dependencies)}</div>
          <div>${deps}</div>
        </div>
        <div>
          <div class="muted" style="font-size:12px; margin-bottom:6px">Tags</div>
          <div>${tags}</div>
        </div>
      </div>
      <hr style="border:0; border-top:1px solid var(--border); margin: 14px 0" />
      <div>
        <div class="muted" style="font-size:12px; margin-bottom:8px">${escapeHtml(t().labels.artifacts)}</div>
        ${artifacts}
      </div>
      <hr style="border:0; border-top:1px solid var(--border); margin: 14px 0" />
      <div>
        <div class="muted" style="font-size:12px; margin-bottom:8px">${escapeHtml(t().labels.logs)}</div>
        ${logs}
        <button class="btn" style="margin-top:10px" data-action="addLog">＋ ${escapeHtml(getLang()==="ru"?"Добавить лог (мок)":"Add log (mock)")}</button>
      </div>
    `;

    $("#drawer_body").innerHTML = html;

    // open
    $("#backdrop").classList.add("open");
    $("#drawer").classList.add("open");
  }

  function closeTaskDrawer(){
    $("#drawer").classList.remove("open");
    $("#backdrop").classList.remove("open");
    CURRENT_TASK = null;
  }

  /* =====================================================
     Modals (New project, Upload doc, Doc preview)
  ===================================================== */
  function openModal(html){
    const modal = $("#drawer_modal");
    modal.innerHTML = html;
    $("#backdrop").classList.add("open");
    modal.classList.add("open");
  }
  function closeModal(){
    $("#drawer_modal").classList.remove("open");
    $("#drawer_modal").innerHTML = "";
    $("#backdrop").classList.remove("open");
  }

  function modalShell(title, body, foot){
    return `
      <div class="drawerHead">
        <div style="min-width:0">
          <h3>${escapeHtml(title)}</h3>
        </div>
        <button class="btn" data-action="closeModal">✕</button>
      </div>
      <div class="drawerBody">${body}</div>
      <div class="drawerFoot">${foot || `<button class="btn" data-action="closeModal">${escapeHtml(t().buttons.cancel)}</button>`}</div>
    `;
  }

  function openNewProjectModal(){
    const body = `
      <div class="field">
        <label>${escapeHtml(getLang()==="ru"?"Название (RU)":"Name (RU)")}</label>
        <input id="np_name_ru" placeholder="${escapeHtml(getLang()==="ru"?"Напр.: Новый проект":"e.g. New project")}" />
      </div>
      <div class="field">
        <label>${escapeHtml(getLang()==="ru"?"Название (EN)":"Name (EN)")}</label>
        <input id="np_name_en" placeholder="e.g. My project" />
      </div>
      <div class="field">
        <label>${escapeHtml(t().labels.repo)}</label>
        <input id="np_repo" placeholder="gitlab.com/org/repo" />
      </div>
      <div class="field">
        <label>${escapeHtml(getLang()==="ru"?"ТЗ / описание (вставьте текст)":"Spec / description (paste text)")}</label>
        <textarea id="np_spec" placeholder="${escapeHtml(getLang()==="ru"?"Коротко опишите задачу. В демо будет создан мок‑план.":"Briefly describe the project. Demo will generate a mock plan.")}"></textarea>
      </div>
      <div class="chip">${escapeHtml(getLang()==="ru"?"После создания нажмите «Пересобрать план» в проекте — будет мок‑декомпозиция.":"After creation, open the project and click Replan — a mock decomposition will be generated.")}</div>
    `;
    const foot = `
      <button class="btn" data-action="closeModal">${escapeHtml(t().buttons.cancel)}</button>
      <button class="btn primary" data-action="createProject">${escapeHtml(t().buttons.create)}</button>
    `;
    openModal(modalShell(t().buttons.newProject, body, foot));
  }

  function openUploadDocModal(){
    const options = STATE.projects.map(p => {
      const name = getLang()==="ru"?p.nameRU:p.nameEN;
      return `<option value="${escapeHtml(p.id)}">${escapeHtml(name)}</option>`;
    }).join("");

    const body = `
      <div class="field">
        <label>${escapeHtml(getLang()==="ru"?"Проект":"Project")}</label>
        <select id="ud_project">${options}</select>
      </div>
      <div class="field">
        <label>${escapeHtml(getLang()==="ru"?"Имя файла":"File name")}</label>
        <input id="ud_name" placeholder="requirements.pdf" />
      </div>
      <div class="field">
        <label>${escapeHtml(getLang()==="ru"?"Тип":"Type")}</label>
        <select id="ud_type">
          <option value="pdf">PDF</option>
          <option value="docx">DOCX</option>
          <option value="png">PNG</option>
          <option value="txt">TXT</option>
          <option value="md">MD</option>
        </select>
      </div>
      <div class="field">
        <label>${escapeHtml(getLang()==="ru"?"Теги (через запятую)":"Tags (comma-separated)")}</label>
        <input id="ud_tags" placeholder="api, design, diagrams" />
      </div>
      <div class="field">
        <label>${escapeHtml(getLang()==="ru"?"Содержимое (опционально)":"Content (optional)")}</label>
        <textarea id="ud_content" placeholder="${escapeHtml(getLang()==="ru"?"В демо содержимое хранится как заметка.":"Stored as a note in the demo.")}"></textarea>
      </div>
    `;
    const foot = `
      <button class="btn" data-action="closeModal">${escapeHtml(t().buttons.cancel)}</button>
      <button class="btn primary" data-action="uploadDoc">${escapeHtml(t().buttons.upload)}</button>
    `;
    openModal(modalShell(t().buttons.uploadDoc, body, foot));
  }

  function openDocPreview(docId){
    const d = STATE.docs.find(x=>x.id===docId);
    if(!d) return;
    const p = findProject(d.projectId);
    const pName = p ? (getLang()==="ru"?p.nameRU:p.nameEN) : "—";

    const body = `
      <div style="display:flex; flex-direction:column; gap:8px">
        <div><span class="muted">${escapeHtml(getLang()==="ru"?"Проект":"Project")}: </span><b>${escapeHtml(pName)}</b></div>
        <div><span class="muted">Type:</span> <span class="mono">${escapeHtml(d.type.toUpperCase())}</span> <span class="muted">·</span> <span class="muted">${escapeHtml(getLang()==="ru"?"Размер":"Size")}: </span><span class="mono">${escapeHtml(d.sizeKb)} KB</span></div>
        <div><span class="muted">Tags:</span> ${(d.tags||[]).map(x=>`<span class="chip">${escapeHtml(x)}</span>`).join(" ") || "—"}</div>
        <hr style="border:0; border-top:1px solid var(--border); margin: 10px 0" />
        <div class="muted" style="font-size:12px">${escapeHtml(getLang()==="ru"?"Просмотр в демо": "Demo preview")}</div>
        <div style="border:1px solid var(--border); border-radius: 14px; padding: 12px; background: rgba(127,127,127,.06)">
          <div class="mono" style="font-size:12px; white-space:pre-wrap">
            ${escapeHtml(getLang()==="ru"?"(Содержимое не загружается с диска — это демо.)":"(Content is not loaded from disk — this is a demo.)")}
          </div>
        </div>
      </div>
    `;
    openModal(modalShell(d.name, body, `
      <button class="btn" data-action="closeModal">${escapeHtml(t().buttons.cancel)}</button>
      <button class="btn danger" data-action="removeDoc" data-doc="${escapeHtml(d.id)}">${escapeHtml(t().buttons.remove)}</button>
    `));
  }

  /* =====================================================
     Demo runner (simulated execution pipeline)
  ===================================================== */
  let runnerInterval = null;

  function refreshBlockedTasks(project){
    // If deps are done, blocked -> queued
    const it = getIteration(project);
    const map = new Map();
    for(const {task} of allTasks(it)) map.set(task.id, task);

    for(const {task} of allTasks(it)){
      if(task.status === "blocked"){
        const ok = (task.deps||[]).every(d => map.get(d)?.status === "done");
        if(ok) task.status = "queued";
      }
    }
  }

  function pickNextTask(project){
    const it = getIteration(project);
    const tasks = allTasks(it).map(x=>x.task);
    // ensure deps unblocked
    refreshBlockedTasks(project);

    // If a task is running, keep it.
    const running = tasks.find(t=>t.status==="running");
    if(running) return running;

    // pick first queued whose deps done
    const map = new Map(tasks.map(t=>[t.id,t]));
    for(const tsk of tasks){
      if(tsk.status!=="queued") continue;
      const depsOk = (tsk.deps||[]).every(d => map.get(d)?.status==="done");
      if(depsOk) return tsk;
    }
    return null;
  }

  function runStart(){
    const p = getActiveProject();
    const it = getIteration(p);

    if(STATE.runtime.runState === "running") return;
    STATE.runtime.runState = "running";
    addEvent("run", getLang()==="ru"?"Запуск процесса":"Process started", `${p.id}`);
    toast("ok", t().toast.running, getLang()==="ru"?"Статусы будут обновляться автоматически.":"Statuses will update automatically.");

    // seed chat
    pushChat("system", getLang()==="ru"?"Процесс запущен. Следующая задача будет взята из очереди.":"Process started. Next queued task will be picked.");

    startRunnerLoop();
    render();
  }

  function runPause(){
    if(STATE.runtime.runState !== "running") return;
    STATE.runtime.runState = "paused";
    addEvent("run", getLang()==="ru"?"Пауза":"Paused", "—");
    toast("warn", t().toast.paused, getLang()==="ru"?"Вы можете продолжить позже.":"You can resume later.");
    pushChat("system", getLang()==="ru"?"Пауза. Задачи остановлены.":"Paused. Tasks are stopped.");
    stopRunnerLoop();
    render();
  }

  function runResume(){
    if(STATE.runtime.runState !== "paused") return;
    STATE.runtime.runState = "running";
    addEvent("run", getLang()==="ru"?"Продолжить":"Resumed", "—");
    toast("ok", t().toast.resumed, getLang()==="ru"?"Продолжаем выполнение.":"Continuing execution.");
    pushChat("system", getLang()==="ru"?"Продолжаем. Беру следующую задачу…":"Resuming. Picking next task…");
    startRunnerLoop();
    render();
  }

  function stopRunnerLoop(){
    if(runnerInterval){
      clearInterval(runnerInterval);
      runnerInterval = null;
    }
  }

  function startRunnerLoop(){
    stopRunnerLoop();
    runnerInterval = setInterval(()=>{
      if(STATE.runtime.runState !== "running") return;
      const p = getActiveProject();
      const it = getIteration(p);

      const next = pickNextTask(p);
      if(!next){
        // completed
        STATE.runtime.runState = "ready";
        stopRunnerLoop();
        addEvent("run", getLang()==="ru"?"Очередь пуста":"Queue empty", "—");
        pushChat("system", getLang()==="ru"?"Все задачи в текущем плане выполнены или требуют вмешательства.":"All tasks in the current plan are done or require intervention.");
        toast("ok", getLang()==="ru"?"Готово":"Done", getLang()==="ru"?"Нет задач для выполнения.":"No tasks left.");
        render();
        return;
      }

      // if queued -> running
      if(next.status === "queued"){
        next.status = "running";
        next.startedAt = nowISO();
        next.logs.push({at: nowISO(), level:"INFO", msg: getLang()==="ru"?"Агент запущен (мок).":"Agent started (mock)."});
        addEvent("task", getLang()==="ru"?`Старт: ${next.id}`:`Start: ${next.id}`, (getLang()==="ru"?next.titleRU:next.titleEN));
        pushChat("bot", (getLang()==="ru"?`В работе: ${next.titleRU}`:`Working on: ${next.titleEN}`));
        render();
        return;
      }

      // if running -> decide outcome
      if(next.status === "running"){
        const roll = Math.random();
        const failChance = next.tags.includes("review") ? 0.25 : 0.12;

        if(roll < failChance){
          next.status = "failed";
          next.finishedAt = nowISO();
          next.logs.push({at: nowISO(), level:"ERROR", msg: getLang()==="ru"?"Симулированная ошибка: требуется доработка.":"Simulated failure: requires fixes."});
          addEvent("task", getLang()==="ru"?`Ошибка: ${next.id}`:`Failed: ${next.id}`, (getLang()==="ru"?next.titleRU:next.titleEN));
          pushChat("bot", (getLang()==="ru"?`Задача провалена: ${next.titleRU}. Создаю замечание.`:`Task failed: ${next.titleEN}. Creating a finding.`));

          // auto-create a fix task (demo) after failures in validation
          if(next.tags.includes("review") || next.tags.includes("tests")){
            createFixTask(p, next);
          }

        } else {
          next.status = "done";
          next.finishedAt = nowISO();
          next.logs.push({at: nowISO(), level:"INFO", msg: getLang()==="ru"?"Завершено успешно (мок).":"Completed successfully (mock)."});

          // add mock artifacts
          if(next.tags.includes("git")){
            if(!next.artifacts.find(a=>a.label==="Commit")){
              next.artifacts.push({type:"git", label:"Commit", value:`${Math.random().toString(16).slice(2,9)}${Math.random().toString(16).slice(2,9)}`});
            }
          }

          addEvent("task", getLang()==="ru"?`Готово: ${next.id}`:`Done: ${next.id}`, (getLang()==="ru"?next.titleRU:next.titleEN));
          pushChat("bot", (getLang()==="ru"?`Готово: ${next.titleRU}`:`Done: ${next.titleEN}`));

          // unblocks
          refreshBlockedTasks(p);
        }

        p.updatedAt = nowISO();
        render();
      }

    }, STATE.runtime.runner.tickMs);
  }

  function createFixTask(project, failedTask){
    const it = getIteration(project);
    // find stage 2 epic e3 or create a "Fixes" epic
    let stage = it.stages.find(s=>s.id==="s2") || it.stages[it.stages.length-1];
    let fixesEpic = stage.epics.find(e=>e.id==="fixes");
    if(!fixesEpic){
      fixesEpic = {
        id:"fixes",
        titleRU:"Доработки (авто)",
        titleEN:"Fixes (auto)",
        descriptionRU:"Задачи, созданные по результатам ревью/тестов.",
        descriptionEN:"Tasks created from review/test findings.",
        tasks:[]
      };
      stage.epics.push(fixesEpic);
    }
    const id = uid("fix");
    const tk = task(
      id,
      `Исправить: ${failedTask.titleRU}`,
      `Fix: ${failedTask.titleEN}`,
      "agent-coder",
      "queued",
      [],
      ["bugfix","workflow"]
    );
    tk.descriptionRU = `Контекст: задача «${failedTask.titleRU}» завершилась ошибкой.\n\nДействие: внести исправления и обновить артефакты.`;
    tk.descriptionEN = `Context: task “${failedTask.titleEN}” failed.\n\nAction: apply fixes and update artifacts.`;
    fixesEpic.tasks.unshift(tk);

    addEvent("plan", getLang()==="ru"?"Создана задача на исправление":"Fix task created", id);
    toast("warn", getLang()==="ru"?"Создано":"Created", getLang()==="ru"?"Добавлена задача на исправление.":"Fix task added.");
  }

  /* =====================================================
     Replan / Approve plan
  ===================================================== */
  function approvePlan(){
    const p = getActiveProject();
    const it = getIteration(p);
    if(it.status === "approved") return;
    it.status = "approved";
    it.approvedAt = nowISO();
    addEvent("plan", getLang()==="ru"?"План утвержден":"Plan approved", p.id);
    toast("ok", t().toast.updated, getLang()==="ru"?"План зафиксирован, задачи готовы к выполнению.":"Plan locked, tasks ready.");
    pushChat("system", getLang()==="ru"?"План утвержден. Можно запускать выполнение.":"Plan approved. You can start execution.");
    render();
  }

  function replan(){
    const p = getActiveProject();
    const it = getIteration(p);

    // Simple mock: create one more stage/epic/tasks based on spec length
    const specLen = (p._specText || "").length;
    const extraCount = Math.max(1, Math.min(3, Math.ceil(specLen/400)));

    // Add a new epic under stage 1
    const stage1 = it.stages[0];
    const epicId = uid("ep");
    const epic = {
      id: epicId,
      titleRU:"Авто‑эпик (из ТЗ)",
      titleEN:"Auto epic (from spec)",
      descriptionRU:"Сгенерирован в демо на основе текста ТЗ.",
      descriptionEN:"Generated in demo from the spec text.",
      tasks: []
    };

    for(let i=0;i<extraCount;i++){
      const id = uid("t");
      epic.tasks.push(task(
        id,
        `Авто‑задача ${i+1}: уточнить требование`,
        `Auto task ${i+1}: refine requirement`,
        "planner",
        "queued",
        [],
        ["plan","auto"]
      ));
    }

    stage1.epics.unshift(epic);
    it.status = "draft";
    it.approvedAt = null;

    addEvent("plan", getLang()==="ru"?"План пересобран":"Plan replanned", p.id);
    toast("ok", t().toast.replanned, getLang()==="ru"?"Добавлены авто‑задачи для демонстрации декомпозиции.":"Auto tasks were added to demonstrate decomposition.");
    pushChat("bot", getLang()==="ru"?"План обновлен. Проверьте дерево и утвердите.":"Plan updated. Review the tree and approve.");
    render();
  }

  /* =====================================================
     Chat
  ===================================================== */
  function getChatKey(){
    return `demo_chat_${STATE.runtime.activeProjectId}_${getLang()}`;
  }

  function loadChat(){
    try{
      const raw = localStorage.getItem(getChatKey());
      return raw ? JSON.parse(raw) : [];
    }catch{ return []; }
  }

  function saveChat(msgs){
    localStorage.setItem(getChatKey(), JSON.stringify(msgs.slice(-120)));
  }

  function pushChat(actor, text){
    const msgs = loadChat();
    msgs.push({id:uid("m"), at: nowISO(), actor, text});
    saveChat(msgs);
    // if chat is visible, update
    const log = $("#chatLog");
    if(log) renderChat();
  }

  function renderChat(){
    const log = $("#chatLog");
    if(!log) return;
    const msgs = loadChat();
    log.innerHTML = msgs.map(m=>{
      const isBot = m.actor === "bot";
      const title = m.actor === "system" ? (getLang()==="ru"?"Система":"System") : (isBot ? "Bot" : (getLang()==="ru"?"Вы":"You"));
      return `
        <div class="msg">
          <div class="avatar" aria-hidden="true" style="background:${m.actor==="system"?"rgba(127,127,127,.16)": isBot?"rgba(47,111,237,.16)":"rgba(15,138,75,.14)"}"></div>
          <div class="bubble" style="flex:1">
            <div class="metaLine"><b>${escapeHtml(title)}</b><span class="muted">·</span><span class="muted">${fmtDate(m.at)}</span></div>
            <pre>${escapeHtml(m.text)}</pre>
          </div>
        </div>
      `;
    }).join("");
    log.scrollTop = log.scrollHeight;
  }

  function handleChatSend(){
    const input = $("#chatInput");
    if(!input) return;
    const text = input.value.trim();
    if(!text) return;
    input.value = "";

    pushChat("user", text);

    // commands
    if(text.startsWith("/")){
      const cmd = text.toLowerCase().split(/\s+/)[0];
      if(cmd === "/pause") runPause();
      else if(cmd === "/resume") runResume();
      else if(cmd === "/replan") replan();
      else if(cmd === "/status"){
        const p = getActiveProject();
        const it = getIteration(p);
        const pr = computeProgress(it);
        pushChat("bot", getLang()==="ru"
          ? `Статус: ${t().labels.statusRunning}=${STATE.runtime.runState==="running"?"да":"нет"}, выполнено ${pr.done}/${pr.total} (${pr.pct}%).`
          : `Status: running=${STATE.runtime.runState==="running"?"yes":"no"}, done ${pr.done}/${pr.total} (${pr.pct}%).`
        );
      }
      else {
        pushChat("bot", getLang()==="ru"?"Команда не распознана. Попробуйте /status /pause /resume /replan":"Unknown command. Try /status /pause /resume /replan");
      }
      return;
    }

    // plain message -> canned assistant response
    pushChat("bot", getLang()==="ru"
      ? "Принято. В демо чат не вызывает сервер — но вы можете управлять процессом командами (/status, /pause…)."
      : "Got it. In this demo the chat does not call a server — but commands (/status, /pause…) work."
    );
  }

  /* =====================================================
     Mutations: add stage/epic/task, mark task
  ===================================================== */
  function addStage(){
    const p = getActiveProject();
    const it = getIteration(p);
    const id = uid("s");
    it.stages.push({
      id,
      titleRU:`Этап ${it.stages.length+1} — Новый`,
      titleEN:`Stage ${it.stages.length+1} — New`,
      descriptionRU:"Описание этапа (демо)",
      descriptionEN:"Stage description (demo)",
      epics:[]
    });
    addEvent("plan", getLang()==="ru"?"Добавлен этап":"Stage added", id);
    toast("ok", t().toast.created, getLang()==="ru"?"Этап добавлен.":"Stage added.");
    render();
  }

  function addEpic(stageId){
    const p = getActiveProject();
    const it = getIteration(p);
    const st = it.stages.find(s=>s.id===stageId);
    if(!st) return;
    const id = uid("e");
    st.epics.push({
      id,
      titleRU:`Новый эпик`,
      titleEN:`New epic`,
      descriptionRU:"Описание эпика (демо)",
      descriptionEN:"Epic description (demo)",
      tasks:[]
    });
    addEvent("plan", getLang()==="ru"?"Добавлен эпик":"Epic added", id);
    toast("ok", t().toast.created, getLang()==="ru"?"Эпик добавлен.":"Epic added.");
    render();
  }

  function addTask(epicId){
    const p = getActiveProject();
    const it = getIteration(p);
    for(const st of it.stages){
      const ep = st.epics.find(e=>e.id===epicId);
      if(!ep) continue;
      const id = uid("t");
      ep.tasks.push(task(
        id,
        "Новая задача (демо)",
        "New task (demo)",
        "agent-coder",
        "queued",
        [],
        ["manual"]
      ));
      addEvent("plan", getLang()==="ru"?"Добавлена задача":"Task added", id);
      toast("ok", t().toast.created, getLang()==="ru"?"Задача добавлена.":"Task added.");
      render();
      return;
    }
  }

  function setTaskStatus(taskId, status){
    const p = getActiveProject();
    const it = getIteration(p);
    const entry = allTasks(it).find(x=>x.task.id===taskId);
    if(!entry) return;
    entry.task.status = status;
    if(status==="done") entry.task.finishedAt = nowISO();
    if(status==="failed") entry.task.finishedAt = nowISO();
    entry.task.logs.push({at: nowISO(), level:"INFO", msg: getLang()==="ru"?`Статус изменён вручную: ${status}`:`Manually set status: ${status}`});
    addEvent("task", getLang()==="ru"?"Ручное изменение статуса":"Manual status change", `${taskId} → ${status}`);
    toast(status==="done"?"ok":"bad", t().toast.updated, getLang()==="ru"?"Статус обновлён.":"Status updated.");
    refreshBlockedTasks(p);
    render();
  }

  function addLogToCurrentTask(){
    if(!CURRENT_TASK) return;
    const p = findProject(CURRENT_TASK.projectId);
    const it = getIteration(p);
    const entry = allTasks(it).find(x=>x.task.id===CURRENT_TASK.taskId);
    if(!entry) return;
    entry.task.logs.unshift({at: nowISO(), level:"DEBUG", msg: getLang()==="ru"?"Пример лога агента (мок).":"Sample agent log (mock)."});
    toast("ok", t().toast.updated, getLang()==="ru"?"Лог добавлен.":"Log added.");
    openTaskDrawer(CURRENT_TASK.projectId, CURRENT_TASK.taskId);
  }

  /* =====================================================
     Docs mutations
  ===================================================== */
  function uploadDoc(){
    const pid = $("#ud_project").value;
    const name = $("#ud_name").value.trim();
    const type = $("#ud_type").value;
    const tags = $("#ud_tags").value.split(",").map(s=>s.trim()).filter(Boolean);
    const content = $("#ud_content").value;

    if(!name){
      toast("warn", getLang()==="ru"?"Не заполнено":"Missing", getLang()==="ru"?"Укажите имя файла.":"Please enter a file name.");
      return;
    }

    STATE.docs.unshift({
      id: uid("doc"),
      projectId: pid,
      name,
      type,
      sizeKb: Math.floor(20 + Math.random()*900),
      uploadedAt: nowISO(),
      tags,
      note: content,
      source:"demo upload"
    });

    addEvent("doc", getLang()==="ru"?"Документ загружен":"Document uploaded", name);
    toast("ok", t().toast.uploaded, name);
    closeModal();
    render();
  }

  function removeDoc(docId){
    const idx = STATE.docs.findIndex(d=>d.id===docId);
    if(idx<0) return;
    const d = STATE.docs[idx];
    STATE.docs.splice(idx,1);
    addEvent("doc", getLang()==="ru"?"Документ удален":"Document removed", d.name);
    toast("warn", getLang()==="ru"?"Удалено":"Removed", d.name);
    closeModal();
    render();
  }

  /* =====================================================
     Create project
  ===================================================== */
  function createProject(){
    const ru = $("#np_name_ru").value.trim() || (getLang()==="ru"?"Новый проект":"New project");
    const en = $("#np_name_en").value.trim() || "New project";
    const repo = $("#np_repo").value.trim() || "—";
    const spec = $("#np_spec").value.trim();

    const id = uid("p");
    const itId = uid("it");
    const p = {
      id,
      nameRU: ru,
      nameEN: en,
      status:"active",
      repo,
      llmModel:"(demo) choose later",
      createdAt: nowISO(),
      updatedAt: nowISO(),
      currentIterationId: itId,
      _specText: spec,
      iterations:[
        {
          id: itId,
          number: 1,
          status:"draft",
          createdAt: nowISO(),
          approvedAt: null,
          stages:[
            {
              id: uid("s"),
              titleRU:"Этап 1 — Планирование",
              titleEN:"Stage 1 — Planning",
              descriptionRU:"Авто‑каркас плана (демо).",
              descriptionEN:"Auto plan scaffold (demo).",
              epics:[
                {
                  id: uid("e"),
                  titleRU:"Базовая декомпозиция",
                  titleEN:"Basic decomposition",
                  descriptionRU:"Создано автоматически для демонстрации.",
                  descriptionEN:"Auto-created for the demo.",
                  tasks:[
                    task(uid("t"),"Проанализировать ТЗ","Analyze spec","planner","queued",[],["plan"]),
                    task(uid("t"),"Сформировать план задач","Generate task plan","planner","queued",[],["plan"]),
                    task(uid("t"),"Показать план в UI","Render plan in UI","frontend","queued",[],["ui"]),
                  ]
                }
              ]
            }
          ]
        }
      ]
    };

    STATE.projects.unshift(p);
    STATE.runtime.activeProjectId = id;

    addEvent("project", getLang()==="ru"?"Проект создан":"Project created", ru);
    toast("ok", t().toast.created, ru);
    closeModal();
    location.hash = `#/project/${encodeURIComponent(id)}`;
    render();
  }

  /* =====================================================
     Export
  ===================================================== */
  function exportJSON(){
    const data = JSON.stringify(STATE, null, 2);
    const blob = new Blob([data], {type:"application/json"});
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `demo-state-${Date.now()}.json`;
    document.body.appendChild(a);
    a.click();
    a.remove();
    setTimeout(()=>URL.revokeObjectURL(url), 5000);
    toast("ok", t().toast.exported, getLang()==="ru"?"Файл скачан.":"File downloaded.");
  }

  /* =====================================================
     Binding
  ===================================================== */
  function bindViewActions(){
    // Chat
    renderChat();

    const input = $("#chatInput");
    if(input){
      input.addEventListener("keydown", (e)=>{
        if(e.key === "Enter") handleChatSend();
      });
    }

    // Generic click handler
    $("#view").addEventListener("click", (e)=>{
      const btn = e.target.closest("[data-action]");
      if(!btn) return;
      const action = btn.dataset.action;

      if(action === "openTask"){
        openTaskDrawer(getActiveProject().id, btn.dataset.task);
      }
      if(action === "runStart") runStart();
      if(action === "runPause") runPause();
      if(action === "runResume") runResume();
      if(action === "approvePlan") approvePlan();
      if(action === "replan") replan();
      if(action === "sendChat") handleChatSend();

      if(action === "addStage") addStage();
      if(action === "addEpic") addEpic(btn.dataset.stage);
      if(action === "addTask") addTask(btn.dataset.epic);

      if(action === "openNewProject") openNewProjectModal();
      if(action === "openUploadDoc") openUploadDocModal();

      if(action === "closeModal") closeModal();
      if(action === "createProject") createProject();
      if(action === "uploadDoc") uploadDoc();

      if(action === "previewDoc") openDocPreview(btn.dataset.doc);
      if(action === "removeDoc") removeDoc(btn.dataset.doc);

      if(action === "clearEvents"){
        STATE.events = [];
        toast("warn", getLang()==="ru"?"Очищено":"Cleared", getLang()==="ru"?"События удалены.":"Events cleared.");
        render();
      }

      if(action === "switchIteration"){
        const p = getActiveProject();
        p.currentIterationId = btn.dataset.it;
        addEvent("plan", getLang()==="ru"?"Смена цикла":"Iteration switched", btn.dataset.it);
        toast("ok", t().toast.updated, getLang()==="ru"?"Цикл переключён.":"Iteration switched.");
        render();
      }

      if(action === "addLog") addLogToCurrentTask();

    }, {passive:true});

    // Search in projects
    const ps = $("#projects_search");
    if(ps){
      ps.addEventListener("input", ()=>{
        const v = ps.value.trim();
        const base = "#/projects";
        location.hash = v ? `${base}?q=${encodeURIComponent(v)}` : base;
      });
    }

    // make task rows keyboard-clickable
    $$("[data-action='openTask']").forEach(el=>{
      el.addEventListener("keydown", (e)=>{
        if(e.key === "Enter" || e.key === " "){
          e.preventDefault();
          el.click();
        }
      });
    });
  }

  /* =====================================================
     Global bindings
  ===================================================== */
  $("#btn_theme_light").addEventListener("click", ()=>setTheme("light"));
  $("#btn_theme_dark").addEventListener("click", ()=>setTheme("dark"));
  $("#btn_lang_ru").addEventListener("click", ()=>setLang("ru"));
  $("#btn_lang_en").addEventListener("click", ()=>setLang("en"));

  $("#btn_new_project").addEventListener("click", openNewProjectModal);
  $("#btn_upload_doc").addEventListener("click", openUploadDocModal);

  $("#btn_seed_data").addEventListener("click", ()=>{
    stopRunnerLoop();
    STATE = DEFAULT_STATE();
    store.save(STATE);
    localStorage.removeItem(getChatKey());
    toast("ok", getLang()==="ru"?"Сброшено":"Reset", getLang()==="ru"?"Демо восстановлено к исходным данным.":"Demo restored to initial data.");
    location.hash = "#/dashboard";
    render();
  });

  $("#btn_export_json").addEventListener("click", exportJSON);

  $("#drawer_close").addEventListener("click", closeTaskDrawer);
  $("#backdrop").addEventListener("click", ()=>{
    closeTaskDrawer();
    closeModal();
  });

  $("#drawer_btn_mark_done").addEventListener("click", ()=>{
    if(!CURRENT_TASK) return;
    setTaskStatus(CURRENT_TASK.taskId, "done");
    openTaskDrawer(CURRENT_TASK.projectId, CURRENT_TASK.taskId);
  });
  $("#drawer_btn_mark_fail").addEventListener("click", ()=>{
    if(!CURRENT_TASK) return;
    setTaskStatus(CURRENT_TASK.taskId, "failed");
    openTaskDrawer(CURRENT_TASK.projectId, CURRENT_TASK.taskId);
  });

  // Keep modal and task drawer mutually exclusive
  const _openTaskDrawer = openTaskDrawer;
  openTaskDrawer = (pid, tid) => { closeModal(); _openTaskDrawer(pid, tid); };

  // Apply i18n to static sidebar labels
  function applyI18n(){
    const s = t();
    $("#t_brand").textContent = s.brand;
    $("#t_brandSub").textContent = s.brandSub;

    $("#t_nav_dashboard").textContent = s.nav.dashboard;
    $("#t_nav_projects").textContent = s.nav.projects;
    $("#t_nav_docs").textContent = s.nav.docs;
    $("#t_nav_activity").textContent = s.nav.activity;
    $("#t_nav_help").textContent = s.nav.help;

    $("#t_side_quick").textContent = s.side.quick;
    $("#t_side_settings").textContent = s.side.settings;
    $("#t_side_hint").textContent = s.side.hint;

    $("#t_new_project").textContent = s.buttons.newProject;
    $("#t_upload_doc").textContent = s.buttons.uploadDoc;

    $("#t_theme").textContent = s.labels.theme;
    $("#t_light").textContent = s.labels.light;
    $("#t_dark").textContent = s.labels.dark;
    $("#t_lang").textContent = s.labels.language;

    $("#t_mock_backend").textContent = s.labels.mock;

    $("#t_hint").textContent = s.hint;

    $("#t_reset_demo").textContent = s.buttons.resetDemo;
    $("#t_export").textContent = s.buttons.export;

    // status label chip updates in render()
    updateLangButtons();
  }

  // Initialize
  document.documentElement.setAttribute("data-theme", getTheme());
  updateThemeButtons();
  applyI18n();

  // seed some first chat
  if(loadChat().length===0){
    pushChat("system", getLang()==="ru"?
      "Это демо интерфейса многоагентной системы управления разработкой. Авторизация отключена."
      :
      "This is a demo UI for a multi-agent SDLC system. Authentication is disabled."
    );
    pushChat("bot", getLang()==="ru"?
      "Откройте проект и нажмите «Запустить». Я буду симулировать выполнение задач и обновлять статусы."
      :
      "Open a project and click Start. I will simulate task execution and update statuses."
    );
  }

  // Ensure default route
  if(!location.hash) location.hash = "#/dashboard";

  // Initial render
  render();

})();
</script>
</body>
</html>
HTML
```

### index_GPT.html

```html
<!doctype html>
<html lang="ru">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>OpenHands — Task Orchestrator (Demo)</title>
  <style>
    :root{
      --bg: #0b1020;
      --panel: rgba(255,255,255,.06);
      --panel-2: rgba(255,255,255,.09);
      --text: rgba(255,255,255,.92);
      --muted: rgba(255,255,255,.64);
      --muted2: rgba(255,255,255,.42);
      --border: rgba(255,255,255,.12);

      --ok: #31d07c;
      --run: #f5c84b;
      --idle: rgba(255,255,255,.18);
      --bad: #ff5566;
      --warn: #ffb020;

      --shadow: 0 14px 40px rgba(0,0,0,.35);
      --radius: 16px;
    }

    *{ box-sizing:border-box; }
    html,body{ height:100%; }
    body{
      margin:0;
      font: 14px/1.35 system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif;
      color: var(--text);
      background:
        radial-gradient(1200px 600px at 20% -10%, rgba(93,120,255,.25), transparent 60%),
        radial-gradient(900px 500px at 85% 15%, rgba(49,208,124,.18), transparent 55%),
        radial-gradient(900px 600px at 30% 110%, rgba(245,200,75,.15), transparent 60%),
        var(--bg);
      overflow:hidden;
    }

    .app{
      height:100%;
      display:grid;
      grid-template-columns: 320px 1fr;
      gap: 14px;
      padding: 14px;
    }

    /* Sidebar */
    .sidebar{
      background: var(--panel);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      box-shadow: var(--shadow);
      overflow:hidden;
      display:flex;
      flex-direction:column;
      min-width: 280px;
    }
    .sb-header{
      padding: 16px 16px 12px;
      border-bottom: 1px solid var(--border);
      display:flex;
      gap: 10px;
      align-items:center;
    }
    .logo{
      width: 34px; height: 34px;
      border-radius: 12px;
      background:
        radial-gradient(circle at 30% 30%, rgba(255,255,255,.35), transparent 50%),
        linear-gradient(135deg, rgba(93,120,255,.9), rgba(49,208,124,.9));
      box-shadow: 0 10px 24px rgba(0,0,0,.25);
      flex: 0 0 auto;
    }
    .sb-title{
      display:flex;
      flex-direction:column;
      min-width:0;
    }
    .sb-title strong{ font-size: 14px; letter-spacing: .2px; }
    .sb-title span{ font-size: 12px; color: var(--muted); }

    .sb-search{
      padding: 10px 16px 14px;
      border-bottom: 1px solid var(--border);
    }
    .sb-search input{
      width:100%;
      padding: 10px 12px;
      border-radius: 12px;
      border: 1px solid var(--border);
      background: rgba(0,0,0,.18);
      color: var(--text);
      outline:none;
      transition: border-color .15s ease, transform .15s ease;
    }
    .sb-search input:focus{
      border-color: rgba(93,120,255,.65);
      transform: translateY(-1px);
    }

    .tasklist{
      padding: 12px;
      overflow:auto;
      display:flex;
      flex-direction:column;
      gap: 10px;
    }
    .task{
      border: 1px solid var(--border);
      background: rgba(0,0,0,.16);
      border-radius: 14px;
      padding: 12px;
      cursor:pointer;
      transition: transform .12s ease, background .12s ease, border-color .12s ease;
      display:flex;
      gap: 10px;
      align-items:flex-start;
    }
    .task:hover{ transform: translateY(-1px); background: rgba(0,0,0,.22); }
    .task.active{
      border-color: rgba(93,120,255,.75);
      background: rgba(93,120,255,.10);
    }
    .pulse{
      width:10px; height:10px; border-radius:50%;
      background: var(--idle);
      margin-top: 3px;
      flex: 0 0 auto;
      position:relative;
    }
    .pulse.on{
      background: var(--run);
      box-shadow: 0 0 0 0 rgba(245,200,75,.55);
      animation: pulse 1.2s infinite;
    }
    @keyframes pulse{
      0%{ box-shadow: 0 0 0 0 rgba(245,200,75,.45); }
      70%{ box-shadow: 0 0 0 12px rgba(245,200,75,0); }
      100%{ box-shadow: 0 0 0 0 rgba(245,200,75,0); }
    }
    .task-main{ min-width:0; flex:1; }
    .task-top{
      display:flex; gap: 8px; align-items:center; justify-content:space-between;
      margin-bottom: 6px;
    }
    .task-key{
      font-weight: 650;
      letter-spacing: .2px;
      font-size: 12px;
      color: rgba(255,255,255,.86);
    }
    .badge{
      font-size: 11px;
      padding: 4px 8px;
      border-radius: 999px;
      border: 1px solid var(--border);
      color: var(--muted);
      background: rgba(255,255,255,.06);
      white-space:nowrap;
    }
    .badge.done{ color: rgba(49,208,124,.95); border-color: rgba(49,208,124,.35); background: rgba(49,208,124,.10); }
    .badge.run{ color: rgba(245,200,75,.95); border-color: rgba(245,200,75,.35); background: rgba(245,200,75,.10); }

    .task-title{
      color: rgba(255,255,255,.92);
      font-size: 13px;
      overflow:hidden; text-overflow:ellipsis; white-space:nowrap;
    }
    .task-meta{
      margin-top: 8px;
      color: var(--muted2);
      font-size: 12px;
      display:flex;
      gap: 10px;
      flex-wrap:wrap;
    }

    /* Main area */
    .main{
      background: var(--panel);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      box-shadow: var(--shadow);
      overflow:hidden;
      display:flex;
      flex-direction:column;
      min-width: 0;
      position:relative;
    }

    .topbar{
      padding: 16px 16px 12px;
      border-bottom: 1px solid var(--border);
      display:flex;
      gap: 12px;
      align-items:flex-start;
      justify-content:space-between;
    }

    .headline{
      min-width:0;
      display:flex;
      flex-direction:column;
      gap: 6px;
    }
    .headline .h1{
      display:flex;
      gap: 10px;
      align-items:baseline;
      min-width:0;
    }
    .headline .h1 strong{
      font-size: 16px;
      letter-spacing: .2px;
      overflow:hidden; text-overflow:ellipsis; white-space:nowrap;
      max-width: 64ch;
    }
    .headline .h1 code{
      font-size: 12px;
      color: rgba(255,255,255,.72);
      background: rgba(0,0,0,.18);
      border: 1px solid var(--border);
      padding: 2px 8px;
      border-radius: 999px;
    }
    .subline{
      color: var(--muted);
      font-size: 12px;
      display:flex;
      gap: 10px;
      flex-wrap:wrap;
      align-items:center;
    }
    .progress{
      display:flex;
      align-items:center;
      gap: 8px;
    }
    .bar{
      width: 180px;
      height: 8px;
      border-radius: 999px;
      background: rgba(255,255,255,.08);
      border: 1px solid var(--border);
      overflow:hidden;
    }
    .bar > div{
      height:100%;
      width: 0%;
      background: linear-gradient(90deg, rgba(93,120,255,.9), rgba(49,208,124,.9));
      transition: width .35s ease;
    }

    .actions{
      display:flex;
      gap: 10px;
      align-items:center;
      flex: 0 0 auto;
    }
    .btn{
      border: 1px solid var(--border);
      background: rgba(0,0,0,.18);
      color: var(--text);
      padding: 10px 12px;
      border-radius: 12px;
      cursor:pointer;
      transition: transform .12s ease, background .12s ease, border-color .12s ease;
      user-select:none;
    }
    .btn:hover{ transform: translateY(-1px); background: rgba(0,0,0,.24); }
    .btn:active{ transform: translateY(0px); }
    .btn.primary{
      border-color: rgba(93,120,255,.55);
      background: rgba(93,120,255,.16);
    }

    .content{
      position:relative;
      padding: 14px;
      display:grid;
      grid-template-columns: 1fr 320px;
      gap: 14px;
      height: 100%;
      overflow:hidden;
    }

    .graph-card, .runtime-card{
      background: rgba(0,0,0,.16);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      overflow:hidden;
      position:relative;
      min-width:0;
    }

    .card-h{
      padding: 12px 12px 10px;
      border-bottom: 1px solid var(--border);
      display:flex;
      align-items:center;
      justify-content:space-between;
      gap: 10px;
    }
    .card-h strong{ font-size: 13px; }
    .card-h span{ color: var(--muted); font-size: 12px; }

    .graph-wrap{
      position:relative;
      height: calc(100% - 46px);
      overflow:auto;
      padding: 16px;
    }

    .canvas{
      position:relative;
      min-height: 420px;
      width: max(780px, 100%);
      padding: 10px;
    }

    svg.edges{
      position:absolute;
      inset:0;
      pointer-events:none;
      overflow:visible;
    }
    .edge{
      stroke: rgba(255,255,255,.22);
      stroke-width: 2;
      fill: none;
      marker-end: url(#arrow);
    }
    .edge.active{
      stroke: rgba(245,200,75,.55);
      stroke-dasharray: 8 8;
      animation: dash 1s linear infinite;
    }
    @keyframes dash { to { stroke-dashoffset: -16; } }

    .node{
      position:absolute;
      width: 220px;
      border-radius: 16px;
      border: 1px solid var(--border);
      background: rgba(255,255,255,.04);
      padding: 12px;
      cursor:pointer;
      transition: transform .14s ease, border-color .14s ease, background .14s ease, box-shadow .14s ease;
      box-shadow: 0 10px 20px rgba(0,0,0,.18);
      outline:none;
    }
    .node:hover{ transform: translateY(-2px); background: rgba(255,255,255,.06); }
    .node:focus{ box-shadow: 0 0 0 3px rgba(93,120,255,.35), 0 10px 20px rgba(0,0,0,.18); }

    .node-top{
      display:flex;
      align-items:center;
      justify-content:space-between;
      gap: 10px;
      margin-bottom: 6px;
    }
    .node-title{
      font-weight: 700;
      font-size: 13px;
      letter-spacing: .2px;
    }
    .status-pill{
      font-size: 11px;
      padding: 3px 8px;
      border-radius: 999px;
      border: 1px solid var(--border);
      color: var(--muted);
      background: rgba(0,0,0,.18);
      white-space:nowrap;
    }

    .node-body{
      color: var(--muted);
      font-size: 12px;
      display:flex;
      flex-direction:column;
      gap: 8px;
    }
    .mini{
      display:flex;
      align-items:center;
      justify-content:space-between;
      gap: 8px;
      color: var(--muted2);
    }
    .dot{
      width: 8px; height: 8px; border-radius:50%;
      background: var(--idle);
      box-shadow: 0 0 0 0 rgba(255,255,255,0);
    }

    /* Status coloring */
    .node.done{ border-color: rgba(49,208,124,.40); background: rgba(49,208,124,.08); }
    .node.done .dot{ background: var(--ok); }
    .node.done .status-pill{ color: rgba(49,208,124,.95); border-color: rgba(49,208,124,.35); background: rgba(49,208,124,.10); }

    .node.running{ border-color: rgba(245,200,75,.45); background: rgba(245,200,75,.08); }
    .node.running .dot{ background: var(--run); box-shadow: 0 0 0 10px rgba(245,200,75,0); animation: pulse 1.2s infinite; }
    .node.running .status-pill{ color: rgba(245,200,75,.95); border-color: rgba(245,200,75,.35); background: rgba(245,200,75,.10); }

    .node.error{ border-color: rgba(255,85,102,.55); background: rgba(255,85,102,.10); }
    .node.error .dot{ background: var(--bad); }
    .node.error .status-pill{ color: rgba(255,85,102,.95); border-color: rgba(255,85,102,.35); background: rgba(255,85,102,.12); }

    /* Runtime card */
    .runtime-list{
      padding: 12px;
      display:flex;
      flex-direction:column;
      gap: 10px;
      overflow:auto;
      height: calc(100% - 46px);
    }
    .rt{
      border: 1px solid var(--border);
      border-radius: 14px;
      padding: 10px;
      background: rgba(0,0,0,.14);
      display:flex;
      align-items:flex-start;
      justify-content:space-between;
      gap: 10px;
    }
    .rt strong{ font-size: 12px; }
    .rt small{ color: var(--muted2); display:block; margin-top: 4px; font-size: 11px; }
    .rt .state{
      font-size: 11px;
      padding: 3px 8px;
      border-radius: 999px;
      border: 1px solid var(--border);
      color: var(--muted);
      background: rgba(255,255,255,.04);
      white-space:nowrap;
    }
    .state.idle{ border-color: rgba(255,255,255,.16); color: rgba(255,255,255,.65); }
    .state.busy{ border-color: rgba(245,200,75,.35); color: rgba(245,200,75,.95); background: rgba(245,200,75,.10); }
    .state.error{ border-color: rgba(255,85,102,.35); color: rgba(255,85,102,.95); background: rgba(255,85,102,.10); }
    .state.offline{ border-color: rgba(255,85,102,.35); color: rgba(255,85,102,.95); background: rgba(0,0,0,.18); }

    /* Drawer */
    .drawer-backdrop{
      position:absolute;
      inset:0;
      background: rgba(0,0,0,.45);
      opacity:0;
      pointer-events:none;
      transition: opacity .18s ease;
    }
    .drawer{
      position:absolute;
      top: 0; right: 0;
      height: 100%;
      width: min(520px, 92vw);
      background: rgba(15,18,40,.92);
      border-left: 1px solid rgba(255,255,255,.12);
      box-shadow: -20px 0 50px rgba(0,0,0,.35);
      transform: translateX(105%);
      transition: transform .22s ease;
      display:flex;
      flex-direction:column;
      backdrop-filter: blur(10px);
    }
    .drawer.open{ transform: translateX(0%); }
    .drawer-backdrop.open{
      opacity: 1;
      pointer-events:auto;
    }
    .drawer-h{
      padding: 14px 14px 10px;
      border-bottom: 1px solid rgba(255,255,255,.12);
      display:flex;
      justify-content:space-between;
      gap: 10px;
      align-items:flex-start;
    }
    .drawer-h strong{ font-size: 13px; }
    .drawer-h .meta{ color: var(--muted); font-size: 12px; margin-top: 2px; }
    .x{
      border: 1px solid rgba(255,255,255,.12);
      background: rgba(0,0,0,.18);
      color: var(--text);
      width: 34px; height: 34px;
      border-radius: 12px;
      cursor:pointer;
      transition: transform .12s ease, background .12s ease;
      display:grid; place-items:center;
      flex: 0 0 auto;
    }
    .x:hover{ transform: translateY(-1px); background: rgba(0,0,0,.26); }

    .drawer-controls{
      padding: 10px 14px;
      border-bottom: 1px solid rgba(255,255,255,.12);
      display:flex;
      gap: 10px;
      align-items:center;
      flex-wrap:wrap;
    }
    .seg{
      display:flex;
      border: 1px solid rgba(255,255,255,.14);
      border-radius: 999px;
      overflow:hidden;
    }
    .seg button{
      border:0;
      background: transparent;
      color: rgba(255,255,255,.70);
      padding: 8px 10px;
      cursor:pointer;
    }
    .seg button.active{
      background: rgba(93,120,255,.16);
      color: rgba(255,255,255,.92);
    }

    .events{
      padding: 12px 14px 16px;
      overflow:auto;
    }
    .ev{
      border-left: 2px solid rgba(255,255,255,.14);
      padding-left: 10px;
      margin-left: 6px;
      padding-bottom: 12px;
      position:relative;
    }
    .ev:before{
      content:"";
      position:absolute;
      left: -6px;
      top: 4px;
      width: 10px; height: 10px;
      border-radius:50%;
      background: rgba(255,255,255,.18);
      border: 1px solid rgba(255,255,255,.18);
    }
    .ev.ok:before{ background: rgba(49,208,124,.9); border-color: rgba(49,208,124,.45); }
    .ev.warn:before{ background: rgba(245,200,75,.95); border-color: rgba(245,200,75,.45); }
    .ev.err:before{ background: rgba(255,85,102,.95); border-color: rgba(255,85,102,.45); }

    .ev .t{ color: rgba(255,255,255,.8); font-size: 12px; display:flex; gap: 8px; align-items:center; }
    .ev .t code{ font-size: 11px; color: rgba(255,255,255,.7); background: rgba(0,0,0,.18); border:1px solid rgba(255,255,255,.12); padding: 2px 6px; border-radius: 999px; }
    .ev .d{ margin-top: 6px; color: rgba(255,255,255,.88); font-size: 13px; }
    .ev .m{ margin-top: 4px; color: rgba(255,255,255,.55); font-size: 12px; }

    /* Small screens */
    @media (max-width: 980px){
      .app{ grid-template-columns: 1fr; }
      .sidebar{ height: 40vh; }
      .content{ grid-template-columns: 1fr; }
      .runtime-card{ height: 260px; }
    }
  </style>
</head>
<body>
<div class="app">
  <aside class="sidebar" aria-label="Sidebar">
    <div class="sb-header">
      <div class="logo" aria-hidden="true"></div>
      <div class="sb-title">
        <strong>OpenHands Orchestrator</strong>
        <span>Jira → Planner → Agents → Merge → Review</span>
      </div>
    </div>

    <div class="sb-search">
      <input id="q" type="search" placeholder="Поиск задач (Jira key / title)..." aria-label="Search tasks"/>
    </div>

    <div id="tasklist" class="tasklist" role="listbox" aria-label="Task list"></div>
  </aside>

  <main class="main" aria-label="Dashboard">
    <div class="topbar">
      <div class="headline">
        <div class="h1">
          <strong id="taskTitle">—</strong>
          <code id="taskKey">—</code>
          <span id="taskBadge" class="badge">—</span>
        </div>
        <div class="subline">
          <span id="updatedAt">Updated: —</span>
          <div class="progress" aria-label="Progress">
            <span style="color:var(--muted);font-size:12px">Progress</span>
            <div class="bar" aria-hidden="true"><div id="progressFill"></div></div>
            <span id="progressPct" style="color:var(--muted);font-size:12px">0%</span>
          </div>
        </div>
      </div>

      <div class="actions">
        <button class="btn" id="refreshBtn" type="button">Refresh</button>
        <button class="btn primary" id="simulateBtn" type="button">Simulate tick</button>
      </div>
    </div>

    <div class="content">
      <section class="graph-card" aria-label="Pipeline graph">
        <div class="card-h">
          <strong>Pipeline</strong>
          <span id="pipeHint">Клик по блоку → события</span>
        </div>

        <div class="graph-wrap">
          <div id="canvas" class="canvas" tabindex="-1">
            <svg class="edges" id="edgesSvg" aria-hidden="true">
              <defs>
                <marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto" markerUnits="strokeWidth">
                  <path d="M0,0 L0,6 L9,3 z" fill="rgba(255,255,255,.35)"></path>
                </marker>
              </defs>
            </svg>
          </div>
        </div>
      </section>

      <aside class="runtime-card" aria-label="Runtime statuses">
        <div class="card-h">
          <strong>Runtimes</strong>
          <span id="rtSync">sync: —</span>
        </div>
        <div id="runtimeList" class="runtime-list"></div>
      </aside>
    </div>

    <!-- Drawer -->
    <div id="backdrop" class="drawer-backdrop" aria-hidden="true"></div>
    <div id="drawer" class="drawer" role="dialog" aria-modal="true" aria-label="Node events">
      <div class="drawer-h">
        <div>
          <strong id="drawerTitle">—</strong>
          <div class="meta" id="drawerMeta">—</div>
        </div>
        <button class="x" id="closeDrawer" aria-label="Close">✕</button>
      </div>

      <div class="drawer-controls">
        <div class="seg" role="tablist" aria-label="Event filter">
          <button type="button" class="active" data-filter="all" role="tab">All</button>
          <button type="button" data-filter="warn" role="tab">Warnings</button>
          <button type="button" data-filter="err" role="tab">Errors</button>
        </div>
        <span style="color:var(--muted);font-size:12px" id="drawerCount">—</span>
      </div>

      <div id="events" class="events"></div>
    </div>
  </main>
</div>

<script>
  // ---------------------------
  // Mock domain data
  // ---------------------------
  const now = () => new Date().toISOString();

  function minutesAgo(m){
    return new Date(Date.now() - m*60*1000).toISOString();
  }

  const TASKS = [
    {
      id: "t1",
      jiraKey: "PROJ-173",
      title: "Добавить валидацию схемы для payload в API",
      status: "in_progress",
      updatedAt: minutesAgo(4),
      runtimes: [
        { runtimeId:"rt-eu-1", state:"busy", lastHeartbeat: minutesAgo(1), queueDepth: 2 },
        { runtimeId:"rt-eu-2", state:"idle", lastHeartbeat: minutesAgo(1), queueDepth: 0 },
        { runtimeId:"rt-us-1", state:"idle", lastHeartbeat: minutesAgo(2), queueDepth: 0 },
      ],
      pipeline: {
        nodes: [
          mkNode("planner", "Планировщик", 40, 70, "done", [
            ev("ok", minutesAgo(48), "Fetched Jira issue", "Jira sync: PROJ-173 pulled", "actor: jira-bot"),
            ev("ok", minutesAgo(43), "Decomposed into subtasks", "3 subtasks created for agents", "actor: planner"),
            ev("ok", minutesAgo(39), "Queued subtasks", "Assigned agents: A1, A2, A3", "actor: planner"),
          ]),
          mkNode("workers", "Работники (агенты)", 320, 70, "running", [
            ev("ok", minutesAgo(35), "Agent A1: coding", "Updated validation module", "branch: feature/PROJ-173-a1"),
            ev("warn", minutesAgo(22), "Agent A2: tests failing", "Edge case missing for null payload", "branch: feature/PROJ-173-a2"),
            ev("ok", minutesAgo(8), "Agent A3: tests", "Added schema tests", "branch: feature/PROJ-173-a3"),
          ]),
          mkNode("merge", "Мерж (runtime)", 600, 70, "idle", [
            ev("ok", minutesAgo(12), "CI prepared", "Awaiting green checks before merge", "runtime: rt-eu-1"),
          ]),
          mkNode("review", "Ревью", 600, 250, "idle", [
            ev("ok", minutesAgo(10), "PR draft created", "Waiting for reviewers", "pr: #412"),
          ]),
          mkNode("done", "Завершение", 840, 160, "idle", [
            ev("ok", minutesAgo(5), "Gate", "Will close after approvals + merge", "policy: main-protected"),
          ]),
        ],
        edges: [
          { from:"planner", to:"workers" },
          { from:"workers", to:"merge" },
          { from:"merge", to:"review" },
          { from:"review", to:"done" },
          { from:"review", to:"workers", kind:"loop" }, // loop for changes
        ],
        activeEdge: { from:"workers", to:"merge" }
      }
    },
    {
      id: "t2",
      jiraKey: "PROJ-168",
      title: "Рефакторинг flaky тестов в payments",
      status: "in_progress",
      updatedAt: minutesAgo(12),
      runtimes: [
        { runtimeId:"rt-eu-1", state:"idle", lastHeartbeat: minutesAgo(1), queueDepth: 0 },
        { runtimeId:"rt-eu-2", state:"busy", lastHeartbeat: minutesAgo(1), queueDepth: 1 },
        { runtimeId:"rt-us-1", state:"idle", lastHeartbeat: minutesAgo(2), queueDepth: 0 },
      ],
      pipeline: {
        nodes: [
          mkNode("planner", "Планировщик", 40, 70, "done", [
            ev("ok", minutesAgo(120), "Fetched Jira issue", "Jira sync: PROJ-168 pulled", "actor: jira-bot"),
            ev("ok", minutesAgo(110), "Decomposed into subtasks", "2 subtasks created", "actor: planner"),
          ]),
          mkNode("workers", "Работники (агенты)", 320, 70, "done", [
            ev("ok", minutesAgo(90), "Agent A1: coding", "Stabilized timeouts", "branch: feature/PROJ-168"),
            ev("ok", minutesAgo(76), "Agent A1: tests", "Added retry strategy for CI", "notes: deterministic seed"),
          ]),
          mkNode("merge", "Мерж (runtime)", 600, 70, "running", [
            ev("ok", minutesAgo(40), "CI green", "Ready to merge into develop", "runtime: rt-eu-2"),
            ev("warn", minutesAgo(8), "Rebase required", "Target branch advanced", "action: rebase"),
          ]),
          mkNode("review", "Ревью", 600, 250, "idle", [
            ev("ok", minutesAgo(18), "Review requested", "Waiting for @backend-team", "pr: #405"),
          ]),
          mkNode("done", "Завершение", 840, 160, "idle", [
            ev("ok", minutesAgo(12), "Gate", "Needs approvals", "policy: 2 approvals"),
          ]),
        ],
        edges: [
          { from:"planner", to:"workers" },
          { from:"workers", to:"merge" },
          { from:"merge", to:"review" },
          { from:"review", to:"done" },
          { from:"review", to:"workers", kind:"loop" },
        ],
        activeEdge: { from:"merge", to:"review" }
      }
    },
    {
      id: "t3",
      jiraKey: "PROJ-151",
      title: "Добавить метрики латентности для рантаймов",
      status: "done",
      updatedAt: minutesAgo(240),
      runtimes: [
        { runtimeId:"rt-eu-1", state:"idle", lastHeartbeat: minutesAgo(1), queueDepth: 0 },
        { runtimeId:"rt-eu-2", state:"idle", lastHeartbeat: minutesAgo(1), queueDepth: 0 },
        { runtimeId:"rt-us-1", state:"idle", lastHeartbeat: minutesAgo(2), queueDepth: 0 },
      ],
      pipeline: {
        nodes: [
          mkNode("planner", "Планировщик", 40, 70, "done", [
            ev("ok", minutesAgo(360), "Decomposed", "Metrics agent + dashboard agent", "actor: planner"),
          ]),
          mkNode("workers", "Работники (агенты)", 320, 70, "done", [
            ev("ok", minutesAgo(320), "Agent: coding", "Instrumented runtime heartbeat", "branch: feature/PROJ-151"),
            ev("ok", minutesAgo(305), "Agent: tests", "Added metrics unit tests", "coverage: +2.1%"),
          ]),
          mkNode("merge", "Мерж (runtime)", 600, 70, "done", [
            ev("ok", minutesAgo(290), "Merged", "Merged into main", "runtime: rt-eu-1"),
          ]),
          mkNode("review", "Ревью", 600, 250, "done", [
            ev("ok", minutesAgo(300), "Approved", "2 approvals received", "reviewers: 2"),
          ]),
          mkNode("done", "Завершение", 840, 160, "done", [
            ev("ok", minutesAgo(240), "Closed", "Jira issue transitioned to Done", "actor: jira-bot"),
          ]),
        ],
        edges: [
          { from:"planner", to:"workers" },
          { from:"workers", to:"merge" },
          { from:"merge", to:"review" },
          { from:"review", to:"done" },
          { from:"review", to:"workers", kind:"loop" },
        ],
        activeEdge: null
      }
    }
  ];

  function mkNode(id, title, x, y, status, events){
    return { id, title, x, y, status, events };
  }

  function ev(level, ts, title, desc, meta){
    return { level, ts, title, desc, meta };
  }

  // ---------------------------
  // State
  // ---------------------------
  let state = {
    tasks: structuredClone(TASKS),
    selectedTaskId: "t1",
    drawer: { open:false, nodeId:null, filter:"all" }
  };

  // ---------------------------
  // DOM refs
  // ---------------------------
  const tasklistEl = document.getElementById("tasklist");
  const qEl = document.getElementById("q");

  const taskTitleEl = document.getElementById("taskTitle");
  const taskKeyEl = document.getElementById("taskKey");
  const taskBadgeEl = document.getElementById("taskBadge");
  const updatedAtEl = document.getElementById("updatedAt");
  const progressFillEl = document.getElementById("progressFill");
  const progressPctEl = document.getElementById("progressPct");

  const canvasEl = document.getElementById("canvas");
  const edgesSvg = document.getElementById("edgesSvg");

  const runtimeListEl = document.getElementById("runtimeList");
  const rtSyncEl = document.getElementById("rtSync");

  const drawerEl = document.getElementById("drawer");
  const backdropEl = document.getElementById("backdrop");
  const closeDrawerBtn = document.getElementById("closeDrawer");
  const drawerTitleEl = document.getElementById("drawerTitle");
  const drawerMetaEl = document.getElementById("drawerMeta");
  const drawerCountEl = document.getElementById("drawerCount");
  const eventsEl = document.getElementById("events");

  const refreshBtn = document.getElementById("refreshBtn");
  const simulateBtn = document.getElementById("simulateBtn");

  // ---------------------------
  // Helpers
  // ---------------------------
  function fmtTime(iso){
    const d = new Date(iso);
    const hh = String(d.getHours()).padStart(2,'0');
    const mm = String(d.getMinutes()).padStart(2,'0');
    return `${hh}:${mm}`;
  }

  function getSelectedTask(){
    return state.tasks.find(t => t.id === state.selectedTaskId) ?? state.tasks[0];
  }

  function statusBadge(taskStatus){
    if(taskStatus === "done") return { text:"Завершено", cls:"done" };
    return { text:"В процессе", cls:"run" };
  }

  function nodeStatusLabel(s){
    if(s==="done") return "done";
    if(s==="running") return "running";
    if(s==="error") return "error";
    return "idle";
  }

  function progressForPipeline(p){
    const nodes = p.nodes;
    const done = nodes.filter(n=>n.status==="done").length;
    const total = nodes.length;
    return Math.round((done/total)*100);
  }

  function hasRunningNode(task){
    return task.pipeline.nodes.some(n => n.status === "running");
  }

  function clamp(n, a, b){ return Math.max(a, Math.min(b, n)); }

  // ---------------------------
  // Render: Sidebar
  // ---------------------------
  function renderTaskList(){
    const query = qEl.value.trim().toLowerCase();
    const tasks = state.tasks
      .filter(t => !query || t.jiraKey.toLowerCase().includes(query) || t.title.toLowerCase().includes(query))
      .sort((a,b) => (a.status===b.status) ? (new Date(b.updatedAt)-new Date(a.updatedAt)) : (a.status==="in_progress" ? -1 : 1));

    tasklistEl.innerHTML = "";

    for(const t of tasks){
      const badge = statusBadge(t.status==="done" ? "done" : "in_progress");
      const row = document.createElement("div");
      row.className = "task" + (t.id===state.selectedTaskId ? " active" : "");
      row.setAttribute("role","option");
      row.setAttribute("tabindex","0");
      row.setAttribute("aria-selected", t.id===state.selectedTaskId ? "true":"false");

      const pulse = document.createElement("div");
      pulse.className = "pulse" + (hasRunningNode(t) ? " on":"");
      pulse.title = hasRunningNode(t) ? "Есть активные блоки" : "Нет активных блоков";

      const main = document.createElement("div");
      main.className = "task-main";

      const top = document.createElement("div");
      top.className = "task-top";

      const key = document.createElement("div");
      key.className = "task-key";
      key.textContent = t.jiraKey;

      const b = document.createElement("span");
      b.className = "badge " + (badge.cls === "done" ? "done":"run");
      b.textContent = badge.text;

      top.appendChild(key);
      top.appendChild(b);

      const title = document.createElement("div");
      title.className = "task-title";
      title.textContent = t.title;

      const meta = document.createElement("div");
      meta.className = "task-meta";
      const p = progressForPipeline(t.pipeline);
      meta.innerHTML = `<span>progress: ${p}%</span><span>updated: ${fmtTime(t.updatedAt)}</span>`;

      main.appendChild(top);
      main.appendChild(title);
      main.appendChild(meta);

      row.appendChild(pulse);
      row.appendChild(main);

      row.addEventListener("click", () => selectTask(t.id));
      row.addEventListener("keydown", (e) => {
        if(e.key==="Enter" || e.key===" "){
          e.preventDefault();
          selectTask(t.id);
        }
      });

      tasklistEl.appendChild(row);
    }
  }

  function selectTask(id){
    state.selectedTaskId = id;
    // close drawer on task switch
    closeDrawer();
    renderAll(true);
  }

  // ---------------------------
  // Render: Topbar + runtime
  // ---------------------------
  function renderHeader(){
    const t = getSelectedTask();
    taskTitleEl.textContent = t.title;
    taskKeyEl.textContent = t.jiraKey;

    const badge = statusBadge(t.status==="done" ? "done" : "in_progress");
    taskBadgeEl.className = "badge " + badge.cls;
    taskBadgeEl.textContent = badge.text;

    updatedAtEl.textContent = `Updated: ${fmtTime(t.updatedAt)}`;

    const p = progressForPipeline(t.pipeline);
    progressFillEl.style.width = `${p}%`;
    progressPctEl.textContent = `${p}%`;
  }

  function renderRuntimes(){
    const t = getSelectedTask();
    runtimeListEl.innerHTML = "";
    rtSyncEl.textContent = `sync: ${fmtTime(now())}`;

    for(const r of t.runtimes){
      const row = document.createElement("div");
      row.className = "rt";
      const left = document.createElement("div");
      const name = document.createElement("strong");
      name.textContent = r.runtimeId;
      const small = document.createElement("small");
      small.textContent = `heartbeat: ${fmtTime(r.lastHeartbeat)} • queue: ${r.queueDepth ?? 0}`;
      left.appendChild(name);
      left.appendChild(small);

      const st = document.createElement("span");
      st.className = `state ${r.state}`;
      st.textContent = r.state;

      row.appendChild(left);
      row.appendChild(st);
      runtimeListEl.appendChild(row);
    }
  }

  // ---------------------------
  // Render: Graph
  // ---------------------------
  function clearGraph(){
    // remove nodes
    [...canvasEl.querySelectorAll(".node")].forEach(n=>n.remove());
    // remove edges
    [...edgesSvg.querySelectorAll("path")].forEach(p=>p.remove());
  }

  function renderGraph(animate=false){
    const t = getSelectedTask();
    const p = t.pipeline;

    clearGraph();

    // Nodes
    for(const n of p.nodes){
      const node = document.createElement("div");
      node.className = `node ${nodeStatusLabel(n.status)}`;
      node.style.left = n.x + "px";
      node.style.top = n.y + "px";
      node.setAttribute("tabindex","0");
      node.setAttribute("role","button");
      node.setAttribute("aria-label", `Open events for ${n.title}`);

      node.innerHTML = `
        <div class="node-top">
          <div class="node-title">${n.title}</div>
          <span class="status-pill">${n.status}</span>
        </div>
        <div class="node-body">
          <div class="mini">
            <span>last:</span>
            <span>${n.events?.[n.events.length-1]?.title ?? "—"}</span>
          </div>
          <div class="mini">
            <span>events:</span>
            <span><span class="dot"></span> ${n.events?.length ?? 0}</span>
          </div>
        </div>
      `;

      node.addEventListener("click", ()=> openDrawer(n.id));
      node.addEventListener("keydown", (e)=>{
        if(e.key==="Enter" || e.key===" "){
          e.preventDefault();
          openDrawer(n.id);
        }
      });

      canvasEl.appendChild(node);

      // little entrance animation
      if(animate){
        node.style.transform = "translateY(6px)";
        node.style.opacity = "0";
        requestAnimationFrame(()=>{
          node.style.transition = "transform .22s ease, opacity .22s ease, border-color .14s ease, background .14s ease, box-shadow .14s ease";
          node.style.transform = "translateY(0px)";
          node.style.opacity = "1";
        });
      }
    }

    // Edges (SVG)
    const nodeById = Object.fromEntries(p.nodes.map(n=>[n.id,n]));
    for(const e of p.edges){
      const a = nodeById[e.from];
      const b = nodeById[e.to];
      if(!a || !b) continue;

      // from right-center to left-center by default
      const x1 = a.x + 220;
      const y1 = a.y + 70;
      const x2 = b.x;
      const y2 = b.y + 70;

      // nice curve
      const dx = Math.max(80, Math.abs(x2-x1) * 0.45);
      const c1x = x1 + dx;
      const c1y = y1;
      const c2x = x2 - dx;
      const c2y = y2;

      const path = document.createElementNS("http://www.w3.org/2000/svg","path");
      const d = `M ${x1} ${y1} C ${c1x} ${c1y}, ${c2x} ${c2y}, ${x2} ${y2}`;
      path.setAttribute("d", d);
      path.setAttribute("class", "edge" + (isActiveEdge(e) ? " active":""));

      // loop edge subtly different
      if(e.kind === "loop"){
        path.style.stroke = "rgba(255,255,255,.14)";
        path.style.markerEnd = "url(#arrow)";
      }

      edgesSvg.appendChild(path);
    }
  }

  function isActiveEdge(edge){
    const t = getSelectedTask();
    const a = t.pipeline.activeEdge;
    return a && a.from===edge.from && a.to===edge.to;
  }

  // ---------------------------
  // Drawer (events)
  // ---------------------------
  function openDrawer(nodeId){
    state.drawer.open = true;
    state.drawer.nodeId = nodeId;

    renderDrawer();
    drawerEl.classList.add("open");
    backdropEl.classList.add("open");
  }

  function closeDrawer(){
    state.drawer.open = false;
    state.drawer.nodeId = null;

    drawerEl.classList.remove("open");
    backdropEl.classList.remove("open");
  }

  function renderDrawer(){
    const t = getSelectedTask();
    const node = t.pipeline.nodes.find(n => n.id === state.drawer.nodeId);
    if(!node) return;

    drawerTitleEl.textContent = node.title;
    drawerMetaEl.textContent = `${t.jiraKey} • status: ${node.status} • events: ${node.events.length}`;

    const filter = state.drawer.filter;
    const list = node.events.filter(e=>{
      if(filter==="all") return true;
      if(filter==="warn") return e.level==="warn";
      if(filter==="err") return e.level==="err";
      return true;
    });

    drawerCountEl.textContent = `showing: ${list.length}/${node.events.length}`;
    eventsEl.innerHTML = "";

    for(const e of list.slice().reverse()){
      const div = document.createElement("div");
      div.className = `ev ${e.level}`;
      div.innerHTML = `
        <div class="t"><span>${fmtTime(e.ts)}</span><code>${e.level.toUpperCase()}</code></div>
        <div class="d">${escapeHtml(e.title)}</div>
        <div class="m">${escapeHtml(e.desc)} • ${escapeHtml(e.meta ?? "")}</div>
      `;
      eventsEl.appendChild(div);
    }
  }

  function escapeHtml(s){
    return String(s).replace(/[&<>"']/g, (c)=>({
      "&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#039;"
    }[c]));
  }

  // Drawer events: filter tabs
  document.querySelectorAll(".seg button").forEach(btn=>{
    btn.addEventListener("click", ()=>{
      document.querySelectorAll(".seg button").forEach(b=>b.classList.remove("active"));
      btn.classList.add("active");
      state.drawer.filter = btn.dataset.filter;
      renderDrawer();
    });
  });

  closeDrawerBtn.addEventListener("click", closeDrawer);
  backdropEl.addEventListener("click", closeDrawer);
  window.addEventListener("keydown", (e)=>{ if(e.key==="Escape") closeDrawer(); });

  // ---------------------------
  // Simulation logic
  // ---------------------------
  function tick(){
    const t = getSelectedTask();

    // Update runtimes (simple random)
    for(const r of t.runtimes){
      // heartbeat
      r.lastHeartbeat = now();

      // small chance of flipping state
      const p = Math.random();
      if(p < 0.10) r.state = "busy";
      else if(p < 0.18) r.state = "idle";
      else if(p < 0.20) r.state = "error";
      if(r.state==="error" && Math.random() < 0.55) r.state = "idle";

      // queue depth
      r.queueDepth = clamp((r.queueDepth ?? 0) + (r.state==="busy" ? 1 : -1), 0, 6);
    }

    // Pipeline progression
    const nodes = t.pipeline.nodes;
    const planner = nodes.find(n=>n.id==="planner");
    const workers = nodes.find(n=>n.id==="workers");
    const merge = nodes.find(n=>n.id==="merge");
    const review = nodes.find(n=>n.id==="review");
    const done = nodes.find(n=>n.id==="done");

    // Determine next step based on current statuses
    // Very simplified: move running forward, sometimes loop back from review
    const rnd = Math.random();

    if(workers.status==="running"){
      t.pipeline.activeEdge = { from:"workers", to:"merge" };
      if(rnd < 0.45){
        // workers finishes
        workers.status = "done";
        workers.events.push(ev("ok", now(), "All subtasks completed", "Agents finished code+tests", "actors: A1,A2,A3"));
        merge.status = "running";
        merge.events.push(ev("ok", now(), "Merge runtime started", "Collecting branches, running CI", "runtime: rt-eu-1"));
      } else {
        workers.events.push(ev(rnd<0.12?"warn":"ok", now(), "Agent activity", rnd<0.12?"Flaky test spotted, retrying":"Pushing incremental commits", "branch: feature/*"));
      }
    } else if(merge.status==="running"){
      t.pipeline.activeEdge = { from:"merge", to:"review" };
      if(rnd < 0.50){
        merge.status = "done";
        merge.events.push(ev("ok", now(), "Merged to integration", "All checks green", "target: develop"));
        review.status = "running";
        review.events.push(ev("ok", now(), "Review started", "Reviewers assigned", "reviewers: @team"));
      } else {
        merge.events.push(ev(rnd<0.18?"warn":"ok", now(), "CI update", rnd<0.18?"Rebase required":"Checks running", "ci: pipeline"));
      }
    } else if(review.status==="running"){
      // sometimes request changes -> loop back
      if(rnd < 0.30){
        t.pipeline.activeEdge = { from:"review", to:"workers" };
        review.events.push(ev("warn", now(), "Changes requested", "Please handle edge cases and naming", "review: requested_changes"));
        review.status = "idle";
        workers.status = "running";
        workers.events.push(ev("ok", now(), "Round 2 started", "Applying review feedback", "actor: agent A1"));
      } else if(rnd < 0.70){
        t.pipeline.activeEdge = { from:"review", to:"done" };
        review.status = "done";
        review.events.push(ev("ok", now(), "Approved", "LGTM — ready to close", "approvals: 2"));
        done.status = "running";
        done.events.push(ev("ok", now(), "Closing", "Transitioning Jira to Done", "actor: jira-bot"));
      } else {
        review.events.push(ev("ok", now(), "Comment added", "Minor notes", "reviewer: @dev"));
      }
    } else if(done.status==="running"){
      t.pipeline.activeEdge = null;
      if(rnd < 0.65){
        done.status = "done";
        done.events.push(ev("ok", now(), "Closed", "Issue moved to Done", "jira: transition"));
        // mark task done if all blocks done
        if(planner.status==="done" && workers.status==="done" && merge.status==="done" && review.status==="done" && done.status==="done"){
          t.status = "done";
        }
      } else {
        done.events.push(ev("ok", now(), "Waiting", "Final checks / notifications", "step: post-merge"));
      }
    } else {
      // If nothing running, start workers if task not done
      if(t.status !== "done"){
        t.pipeline.activeEdge = { from:"planner", to:"workers" };
        if(planner.status !== "done"){
          planner.status = "done";
          planner.events.push(ev("ok", now(), "Planner finalized", "Subtasks confirmed", "actor: planner"));
        }
        workers.status = "running";
        workers.events.push(ev("ok", now(), "Work started", "Agents started execution", "actors: A1,A2"));
      } else {
        t.pipeline.activeEdge = null;
      }
    }

    // Update task updatedAt
    t.updatedAt = now();

    // Recompute task status if necessary
    if(t.status !== "done"){
      const allDone = nodes.every(n=>n.status==="done");
      if(allDone) t.status = "done";
    }

    renderAll(false);
  }

  // ---------------------------
  // Render all
  // ---------------------------
  function renderAll(animate){
    renderTaskList();
    renderHeader();
    renderGraph(animate);
    renderRuntimes();
    if(state.drawer.open) renderDrawer();
  }

  // ---------------------------
  // Wire up controls
  // ---------------------------
  qEl.addEventListener("input", renderTaskList);

  refreshBtn.addEventListener("click", ()=>{
    // In real app: fetch tasks + pipeline + runtimes
    // Here: just re-render with small animation
    renderAll(true);
  });

  simulateBtn.addEventListener("click", tick);

  // Auto polling simulation
  setInterval(()=>{
    // light auto updates: runtimes + maybe small events if drawer open
    const t = getSelectedTask();
    for(const r of t.runtimes){
      r.lastHeartbeat = now();
      if(Math.random()<0.06) r.state = (r.state==="busy" ? "idle" : "busy");
      if(Math.random()<0.02) r.state = "error";
      if(r.state==="error" && Math.random()<0.50) r.state = "idle";
    }
    rtSyncEl.textContent = `sync: ${fmtTime(now())}`;
    renderRuntimes();
  }, 3500);

  // Init
  renderAll(true);
</script>
</body>
</html>
```

## Frontend Src

### dashboard/frontend/src/AdminApp.tsx

```typescript
import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate, useNavigate } from 'react-router-dom';
import axios from 'axios';
import AdminSidebar from './components/AdminSidebar';
import AdminTopbar from './components/AdminTopbar';
import AdminDashboard from './pages/AdminDashboard';
import AdminUsers from './pages/AdminUsers';
import AdminLLMConfigs from './pages/AdminLLMConfigs';
import AdminRepositories from './pages/AdminRepositories';
import AdminIntegrations from './pages/AdminIntegrations';

// Placeholder pages for other admin sections
const AdminTeams = () => <div className="admin-page">Teams Management (Coming Soon)</div>;
const AdminProjects = () => <div className="admin-page">Projects Management (Coming Soon)</div>;
const AdminRoles = () => <div className="admin-page">Roles & Access (Coming Soon)</div>;
const AdminSecrets = () => <div className="admin-page">Secrets Management (Coming Soon)</div>;
const AdminMonitoring = () => <div className="admin-page">Monitoring (Coming Soon)</div>;
const AdminAudit = () => <div className="admin-page">Audit Log (Coming Soon)</div>;
const AdminUserEdit = () => <div className="admin-page">Edit User (Coming Soon)</div>;
const AdminLLMConfigEdit = () => <div className="admin-page">Edit LLM Config (Coming Soon)</div>;
const AdminRepoEdit = () => <div className="admin-page">Edit Repository (Coming Soon)</div>;

interface User {
  name: string;
  email: string;
  role: string;
}

const AdminLayout: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    checkAuth();
  }, []);

  const checkAuth = async () => {
    try {
      // Check if user is authenticated
      const token = localStorage.getItem('auth_token');
      if (!token) {
        navigate('/login');
        return;
      }

      // Fetch user info
      const response = await axios.get('/api/auth/me', {
        headers: { Authorization: `Bearer ${token}` }
      });
      
      setUser({
        name: response.data.username || 'Admin User',
        email: response.data.email,
        role: 'System Admin' // This should come from API
      });
    } catch (error) {
      console.error('Authentication error:', error);
      navigate('/login');
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('auth_token');
    navigate('/login');
  };

  if (loading) {
    return (
      <div className="admin-loading">
        <div className="loading-spinner"></div>
        <p>Loading Admin Console...</p>
      </div>
    );
  }

  return (
    <div className="admin-app">
      <AdminSidebar />
      <div className="admin-main">
        <AdminTopbar user={user || undefined} onLogout={handleLogout} />
        <div className="admin-content">
          {children}
        </div>
      </div>
    </div>
  );
};

const AdminApp: React.FC = () => {
  return (
    <Router>
      <Routes>
        <Route path="/admin" element={
          <AdminLayout>
            <AdminDashboard />
          </AdminLayout>
        } />
        <Route path="/admin/users" element={
          <AdminLayout>
            <AdminUsers />
          </AdminLayout>
        } />
        <Route path="/admin/users/new" element={
          <AdminLayout>
            <AdminUserEdit />
          </AdminLayout>
        } />
        <Route path="/admin/users/:id/edit" element={
          <AdminLayout>
            <AdminUserEdit />
          </AdminLayout>
        } />
        <Route path="/admin/teams" element={
          <AdminLayout>
            <AdminTeams />
          </AdminLayout>
        } />
        <Route path="/admin/projects" element={
          <AdminLayout>
            <AdminProjects />
          </AdminLayout>
        } />
        <Route path="/admin/roles" element={
          <AdminLayout>
            <AdminRoles />
          </AdminLayout>
        } />
        <Route path="/admin/integrations" element={
          <AdminLayout>
            <AdminIntegrations />
          </AdminLayout>
        } />
        <Route path="/admin/secrets" element={
          <AdminLayout>
            <AdminSecrets />
          </AdminLayout>
        } />
        <Route path="/admin/llm-configs" element={
          <AdminLayout>
            <AdminLLMConfigs />
          </AdminLayout>
        } />
        <Route path="/admin/llm-configs/new" element={
          <AdminLayout>
            <AdminLLMConfigEdit />
          </AdminLayout>
        } />
        <Route path="/admin/llm-configs/:id/edit" element={
          <AdminLayout>
            <AdminLLMConfigEdit />
          </AdminLayout>
        } />
        <Route path="/admin/repositories" element={
          <AdminLayout>
            <AdminRepositories />
          </AdminLayout>
        } />
        <Route path="/admin/repositories/new" element={
          <AdminLayout>
            <AdminRepoEdit />
          </AdminLayout>
        } />
        <Route path="/admin/repositories/:id/edit" element={
          <AdminLayout>
            <AdminRepoEdit />
          </AdminLayout>
        } />
        <Route path="/admin/monitoring" element={
          <AdminLayout>
            <AdminMonitoring />
          </AdminLayout>
        } />
        <Route path="/admin/audit" element={
          <AdminLayout>
            <AdminAudit />
          </AdminLayout>
        } />
        <Route path="*" element={<Navigate to="/admin" replace />} />
      </Routes>
    </Router>
  );
};

export default AdminApp;
```

### dashboard/frontend/src/App.tsx

```typescript
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { I18nProvider } from './i18n/I18nProvider';
import AdminApp from './AdminApp';
import MainApp from './MainApp';
import Login from './pages/Login';
import Projects from './pages/Projects';
import ProjectDetails from './pages/ProjectDetails';

export default function App() {
  return (
    <I18nProvider defaultLocale="ru">
      <Router>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/admin/*" element={<AdminApp />} />
          <Route path="/projects" element={<Projects />} />
          <Route path="/projects/:id" element={<ProjectDetails />} />
          <Route path="/*" element={<MainApp />} />
          <Route path="/" element={<Navigate to="/admin" replace />} />
        </Routes>
      </Router>
    </I18nProvider>
  );
}
```

### dashboard/frontend/src/MainApp.tsx

```typescript
import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';
import { Pipeline, LogChunk, Task } from './types';
import Sidebar from './components/Sidebar';
import PipelineGraph from './components/PipelineGraph';
import RuntimeList from './components/RuntimeList';
import EventDrawer from './components/EventDrawer';

function Dashboard() {
    const { id } = useParams<{ id: string }>();
    const navigate = useNavigate();

    const [pipelines, setPipelines] = useState<Pipeline[]>([]);
    const [activePipeline, setActivePipeline] = useState<Pipeline | null>(null);
    const [isDrawerOpen, setDrawerOpen] = useState(false);
    const [drawerLogs, setDrawerLogs] = useState<LogChunk[]>([]);
    const [drawerTitle, setDrawerTitle] = useState("Events");
    const [loadingLogs, setLoadingLogs] = useState(false);

    // Fetch Pipelines List
    useEffect(() => {
        const fetchPipelines = async () => {
            try {
                const res = await axios.get('/api/pipelines');
                setPipelines(res.data);
            } catch (e) {
                console.error("Failed to fetch pipelines", e);
            }
        };
        fetchPipelines();
        const interval = setInterval(fetchPipelines, 5000);
        return () => clearInterval(interval);
    }, []);

    // Fetch Active Pipeline Details
    useEffect(() => {
        if (!id) {
            setActivePipeline(null);
            return;
        }
        const fetchDetails = async () => {
            try {
                const res = await axios.get(`/api/pipelines/${id}`);
                setActivePipeline(res.data);
            } catch (e) {
                console.error("Failed to fetch details", e);
            }
        };
        fetchDetails();
        const interval = setInterval(fetchDetails, 2000);
        return () => clearInterval(interval);
    }, [id]);

    const handleNodeClick = async (title: string, stageId?: string) => {
        if (!stageId) return;
        setDrawerTitle(`${title} Events`);
        setDrawerOpen(true);
        setLoadingLogs(true);

        // Fetch logs for all tasks in this stage
        // Note: The API currently fetches logs per task.
        // We need to aggregate.
        try {
            // Find stage in activePipeline
            const stage = activePipeline?.stages?.find(s => s.id === stageId);
            if (!stage || !stage.tasks) {
                setDrawerLogs([]);
                setLoadingLogs(false);
                return;
            }

            const allLogs: LogChunk[] = [];
            for (const task of stage.tasks) {
                const res = await axios.get(`/api/tasks/${task.id}/logs`);
                allLogs.push(...res.data);
            }
            // Sort by id or timestamp
            allLogs.sort((a, b) => a.id - b.id);
            setDrawerLogs(allLogs);
        } catch (e) {
            console.error(e);
        } finally {
            setLoadingLogs(false);
        }
    };

    // Calculate Progress
    const progress = activePipeline?.stages ? Math.round((activePipeline.stages.filter(s => s.status === 'COMPLETED').length / activePipeline.stages.length) * 100) : 0;

    // Aggregate all tasks for Runtime List
    const allTasks: Task[] = [];
    activePipeline?.stages?.forEach(s => {
        if (s.tasks) allTasks.push(...s.tasks);
    });

    return (
        <div className="app">
            <Sidebar pipelines={pipelines} />

            <main className="main" aria-label="Dashboard">
                <div className="topbar">
                    <div className="headline">
                        <div className="h1">
                            <strong>{activePipeline?.objective || "Select a pipeline"}</strong>
                            {activePipeline && <code id="taskKey">PIPE-{activePipeline.id.slice(-4)}</code>}
                            {activePipeline && (
                                <span className={`badge ${activePipeline.status === 'SUCCESS' ? 'done' : activePipeline.status === 'RUNNING' ? 'run' : ''}`}>
                                    {activePipeline.status}
                                </span>
                            )}
                        </div>
                        <div className="subline">
                            <span id="updatedAt">Updated: {new Date().toLocaleTimeString()}</span>
                            {activePipeline && (
                                <div className="progress" aria-label="Progress">
                                    <span style={{ color: 'var(--muted)', fontSize: '12px' }}>Progress</span>
                                    <div className="bar" aria-hidden="true">
                                        <div style={{ width: `${progress}%` }}></div>
                                    </div>
                                    <span style={{ color: 'var(--muted)', fontSize: '12px' }}>{progress}%</span>
                                </div>
                            )}
                        </div>
                    </div>

                    <div className="actions">
                        <button className="btn" type="button" onClick={() => window.location.reload()}>Refresh</button>
                    </div>
                </div>

                <div className="content">
                    <section className="graph-card" aria-label="Pipeline graph">
                        <div className="card-h">
                            <strong>Pipeline</strong>
                            <span>Live Graph</span>
                        </div>
                        <PipelineGraph pipeline={activePipeline || undefined} onNodeClick={handleNodeClick} />
                    </section>

                    <aside className="runtime-card" aria-label="Runtime statuses">
                        <div className="card-h">
                            <strong>Runtimes</strong>
                            <span>Real-time</span>
                        </div>
                        <RuntimeList tasks={allTasks} />
                    </aside>
                </div>

                <EventDrawer
                    isOpen={isDrawerOpen}
                    onClose={() => setDrawerOpen(false)}
                    title={drawerTitle}
                    logs={drawerLogs}
                    loading={loadingLogs}
                />
            </main>
        </div>
    );
}

export default Dashboard;
```

### dashboard/frontend/src/admin-dashboard.css

```css
/* Admin Dashboard */
.admin-dashboard {
    max-width: 1400px;
    margin: 0 auto;
}

.dashboard-header {
    margin-bottom: 30px;
}

.dashboard-header h1 {
    font-size: 28px;
    margin: 0 0 8px;
}

.subtitle {
    color: var(--muted);
    font-size: 16px;
    margin: 0;
}

.stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
    gap: 16px;
    margin-bottom: 30px;
}

.stat-card {
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 20px;
    display: flex;
    align-items: center;
    gap: 16px;
    transition: all 0.2s ease;
}

.stat-card:hover {
    background: rgba(255, 255, 255, 0.05);
    transform: translateY(-2px);
}

.stat-icon {
    width: 48px;
    height: 48px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(93, 120, 255, 0.1);
    color: rgba(93, 120, 255, 0.9);
}

.stat-icon.users { background: rgba(93, 120, 255, 0.1); color: rgba(93, 120, 255, 0.9); }
.stat-icon.teams { background: rgba(49, 208, 124, 0.1); color: rgba(49, 208, 124, 0.9); }
.stat-icon.projects { background: rgba(245, 200, 75, 0.1); color: rgba(245, 200, 75, 0.9); }
.stat-icon.monitoring { background: rgba(255, 85, 102, 0.1); color: rgba(255, 85, 102, 0.9); }

.stat-content {
    flex: 1;
}

.stat-value {
    font-size: 28px;
    font-weight: 700;
    line-height: 1;
    margin-bottom: 4px;
}

.stat-label {
    font-size: 14px;
    color: var(--muted);
}

.stat-link {
    font-size: 12px;
    color: var(--muted);
    text-decoration: none;
    transition: color 0.2s ease;
}

.stat-link:hover {
    color: var(--text);
}

.section {
    margin-bottom: 30px;
}

.section-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 20px;
}

.section-header h2 {
    font-size: 20px;
    margin: 0;
    display: flex;
    align-items: center;
    gap: 10px;
}

.view-all {
    font-size: 14px;
    color: var(--muted);
    text-decoration: none;
    transition: color 0.2s ease;
}

.view-all:hover {
    color: var(--text);
}

.quick-actions-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
    gap: 16px;
}

.quick-action-card {
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 20px;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 12px;
    text-decoration: none;
    color: var(--text);
    transition: all 0.2s ease;
}

.quick-action-card:hover {
    background: rgba(255, 255, 255, 0.05);
    transform: translateY(-2px);
    border-color: rgba(93, 120, 255, 0.3);
}

.action-icon {
    width: 48px;
    height: 48px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
}

.action-icon.blue { background: rgba(93, 120, 255, 0.1); color: rgba(93, 120, 255, 0.9); }
.action-icon.green { background: rgba(49, 208, 124, 0.1); color: rgba(49, 208, 124, 0.9); }
.action-icon.purple { background: rgba(168, 85, 247, 0.1); color: rgba(168, 85, 247, 0.9); }
.action-icon.orange { background: rgba(245, 200, 75, 0.1); color: rgba(245, 200, 75, 0.9); }
.action-icon.red { background: rgba(255, 85, 102, 0.1); color: rgba(255, 85, 102, 0.9); }
.action-icon.teal { background: rgba(20, 184, 166, 0.1); color: rgba(20, 184, 166, 0.9); }

.action-label {
    font-size: 14px;
    font-weight: 500;
}

.two-column-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 30px;
    margin-bottom: 30px;
}

.activity-list,
.health-list {
    display: flex;
    flex-direction: column;
    gap: 12px;
}

.activity-item {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    padding: 12px;
    background: rgba(255, 255, 255, 0.02);
    border: 1px solid var(--border);
    border-radius: 12px;
}

.activity-icon {
    width: 24px;
    height: 24px;
    border-radius: 6px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(93, 120, 255, 0.1);
    color: rgba(93, 120, 255, 0.9);
    flex-shrink: 0;
}

.activity-content {
    flex: 1;
}

.activity-action {
    font-size: 14px;
    margin-bottom: 4px;
}

.activity-meta {
    display: flex;
    align-items: center;
    gap: 12px;
    font-size: 12px;
    color: var(--muted);
}

.health-item {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 12px;
    background: rgba(255, 255, 255, 0.02);
    border: 1px solid var(--border);
    border-radius: 12px;
}

.health-label {
    font-size: 14px;
}

.health-status-indicator {
    display: flex;
    align-items: center;
    gap: 8px;
}

.status-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
}

.status-dot.healthy { background: rgba(49, 208, 124, 0.9); }
.status-dot.warning { background: rgba(245, 200, 75, 0.9); }
.status-dot.critical { background: rgba(255, 85, 102, 0.9); }

.status-text {
    font-size: 12px;
    color: var(--muted);
}

.last-check {
    font-size: 11px;
    color: var(--muted2);
}

.alert-section {
    background: rgba(255, 255, 255, 0.02);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 20px;
}

.alert-list {
    display: flex;
    flex-direction: column;
    gap: 12px;
}

.alert-item {
    display: flex;
    align-items: center;
    gap: 16px;
    padding: 16px;
    border-radius: 12px;
}

.alert-item.warning {
    background: rgba(245, 200, 75, 0.05);
    border: 1px solid rgba(245, 200, 75, 0.2);
}

.alert-item.info {
    background: rgba(93, 120, 255, 0.05);
    border: 1px solid rgba(93, 120, 255, 0.2);
}

.alert-icon {
    font-size: 20px;
    flex-shrink: 0;
}

.alert-content {
    flex: 1;
}

.alert-title {
    font-size: 14px;
    font-weight: 600;
    margin-bottom: 4px;
}

.alert-description {
    font-size: 13px;
    color: var(--muted);
}
```

### dashboard/frontend/src/admin-login.css

```css
/* Login Page */
.login-page {
    height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 20px;
    background: var(--bg);
}

.login-container {
    width: 100%;
    max-width: 480px;
}

.login-header {
    text-align: center;
    margin-bottom: 40px;
}

.logo {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 16px;
    margin-bottom: 16px;
}

.logo-icon {
    width: 48px;
    height: 48px;
    border-radius: 12px;
    background: linear-gradient(135deg, rgba(93, 120, 255, 0.9), rgba(49, 208, 124, 0.9));
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 24px;
}

.login-header h1 {
    font-size: 32px;
    margin: 0;
    font-weight: 700;
    background: linear-gradient(135deg, rgba(93, 120, 255, 0.9), rgba(49, 208, 124, 0.9));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.subtitle {
    color: var(--muted);
    font-size: 16px;
    margin: 8px 0 0;
}

.login-card {
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    box-shadow: var(--shadow);
    padding: 32px;
}

.card-header {
    text-align: center;
    margin-bottom: 24px;
}

.card-header h2 {
    font-size: 24px;
    margin: 0 0 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 12px;
}

.card-header p {
    color: var(--muted);
    margin: 0;
    font-size: 14px;
}

.login-form {
    display: flex;
    flex-direction: column;
    gap: 20px;
}

.form-group {
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.form-group label {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 14px;
    font-weight: 500;
    color: var(--text);
}

.form-group input {
    padding: 12px 16px;
    background: rgba(0, 0, 0, 0.18);
    border: 1px solid var(--border);
    border-radius: 12px;
    color: var(--text);
    font-size: 14px;
    outline: none;
    transition: all 0.2s ease;
}

.form-group input:focus {
    border-color: rgba(93, 120, 255, 0.6);
    box-shadow: 0 0 0 3px rgba(93, 120, 255, 0.1);
}

.form-group input:disabled {
    opacity: 0.6;
    cursor: not-allowed;
}

.form-options {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 8px;
}

.checkbox {
    display: flex;
    align-items: center;
    gap: 8px;
    cursor: pointer;
    font-size: 13px;
    color: var(--muted);
}

.checkbox input[type="checkbox"] {
    width: 16px;
    height: 16px;
    border-radius: 4px;
    border: 1px solid var(--border);
    background: rgba(255, 255, 255, 0.05);
    cursor: pointer;
}

.checkbox input[type="checkbox"]:checked {
    background: rgba(93, 120, 255, 0.3);
    border-color: rgba(93, 120, 255, 0.6);
}

.forgot-password {
    font-size: 13px;
    color: rgba(93, 120, 255, 0.9);
    text-decoration: none;
    transition: color 0.2s ease;
}

.forgot-password:hover {
    color: rgba(93, 120, 255, 1);
}

.login-footer {
    margin-top: 24px;
    padding-top: 24px;
    border-top: 1px solid var(--border);
    text-align: center;
}

.demo-credentials {
    background: rgba(93, 120, 255, 0.05);
    border: 1px solid rgba(93, 120, 255, 0.2);
    border-radius: 12px;
    padding: 12px;
    margin-bottom: 16px;
    font-size: 13px;
    color: var(--muted);
}

.demo-credentials strong {
    color: var(--text);
}

.text-sm {
    font-size: 12px;
}

.text-muted {
    color: var(--muted2);
}

.login-info {
    margin-top: 40px;
}

.info-card {
    background: rgba(255, 255, 255, 0.02);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 20px;
}

.info-card h3 {
    font-size: 16px;
    margin: 0 0 12px;
    color: var(--text);
}

.info-card ul {
    margin: 0;
    padding-left: 20px;
    list-style: none;
}

.info-card li {
    color: var(--muted);
    font-size: 13px;
    margin-bottom: 8px;
    position: relative;
}

.info-card li:before {
    content: "•";
    position: absolute;
    left: -15px;
    color: rgba(93, 120, 255, 0.9);
}

/* Spinner for loading states */
.spinner {
    width: 16px;
    height: 16px;
    border: 2px solid var(--border);
    border-top-color: rgba(93, 120, 255, 0.9);
    border-radius: 50%;
    animation: spin 1s linear infinite;
}

.admin-loading {
    height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 16px;
}

.admin-loading .loading-spinner {
    width: 48px;
    height: 48px;
    border-width: 4px;
}

.admin-loading p {
    color: var(--muted);
    font-size: 16px;
}
```

### dashboard/frontend/src/admin-tables.css

```css
/* Admin Tables */
.table-container {
    background: rgba(255, 255, 255, 0.02);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    overflow: hidden;
}

.data-table {
    width: 100%;
    border-collapse: collapse;
}

.data-table th {
    text-align: left;
    padding: 16px;
    background: rgba(255, 255, 255, 0.03);
    border-bottom: 1px solid var(--border);
    font-size: 13px;
    font-weight: 600;
    color: var(--muted);
}

.data-table td {
    padding: 16px;
    border-bottom: 1px solid var(--border);
    font-size: 14px;
}

.data-table tr:hover {
    background: rgba(255, 255, 255, 0.02);
}

.data-table tr.inactive {
    opacity: 0.6;
}

.checkbox-cell {
    width: 40px;
    text-align: center;
}

.checkbox-cell input[type="checkbox"] {
    width: 18px;
    height: 18px;
    border-radius: 4px;
    border: 1px solid var(--border);
    background: rgba(255, 255, 255, 0.05);
    cursor: pointer;
}

.checkbox-cell input[type="checkbox"]:checked {
    background: rgba(93, 120, 255, 0.3);
    border-color: rgba(93, 120, 255, 0.6);
}

/* User Cell */
.user-cell {
    display: flex;
    align-items: center;
    gap: 12px;
}

.user-avatar {
    width: 36px;
    height: 36px;
    border-radius: 50%;
    background: rgba(93, 120, 255, 0.2);
    display: flex;
    align-items: center;
    justify-content: center;
    color: rgba(93, 120, 255, 0.9);
    font-weight: 600;
    font-size: 14px;
}

.user-info {
    display: flex;
    flex-direction: column;
}

.user-name {
    font-size: 14px;
    font-weight: 600;
}

.user-email {
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 12px;
    color: var(--muted);
}

/* Status Badges */
.status-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 4px 10px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 500;
}

.status-badge.active {
    background: rgba(49, 208, 124, 0.1);
    color: rgba(49, 208, 124, 0.9);
    border: 1px solid rgba(49, 208, 124, 0.3);
}

.status-badge.inactive {
    background: rgba(255, 85, 102, 0.1);
    color: rgba(255, 85, 102, 0.9);
    border: 1px solid rgba(255, 85, 102, 0.3);
}

/* Teams & Roles */
.teams-roles {
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.team-role-chip {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 4px 10px;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid var(--border);
    border-radius: 20px;
    font-size: 12px;
}

.team-name {
    color: var(--text);
}

.role-badge {
    display: flex;
    align-items: center;
    gap: 4px;
    color: var(--muted);
}

.no-teams {
    color: var(--muted2);
    font-size: 12px;
    font-style: italic;
}

/* Date Cell */
.date-cell {
    display: flex;
    align-items: center;
    gap: 6px;
    color: var(--muted);
    font-size: 13px;
}

/* Action Buttons */
.action-buttons {
    display: flex;
    gap: 8px;
}

/* Bulk Actions */
.bulk-actions-bar {
    background: rgba(93, 120, 255, 0.05);
    border: 1px solid rgba(93, 120, 255, 0.2);
    border-radius: var(--radius);
    padding: 12px 16px;
    margin-bottom: 16px;
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.bulk-info {
    font-size: 14px;
    color: var(--text);
}

.bulk-buttons {
    display: flex;
    gap: 8px;
}

/* Filters Bar */
.filters-bar {
    background: rgba(255, 255, 255, 0.02);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 16px;
    margin-bottom: 20px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 16px;
}

.search-box {
    flex: 1;
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 10px 14px;
    background: rgba(0, 0, 0, 0.18);
    border: 1px solid var(--border);
    border-radius: 12px;
}

.search-input {
    flex: 1;
    background: transparent;
    border: none;
    color: var(--text);
    font-size: 14px;
    outline: none;
}

.search-input::placeholder {
    color: var(--muted2);
}

.filter-buttons {
    display: flex;
    gap: 8px;
}

.filter-btn {
    padding: 8px 16px;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid var(--border);
    border-radius: 20px;
    color: var(--muted);
    font-size: 13px;
    cursor: pointer;
    transition: all 0.2s ease;
}

.filter-btn:hover {
    background: rgba(255, 255, 255, 0.1);
}

.filter-btn.active {
    background: rgba(93, 120, 255, 0.15);
    color: rgba(93, 120, 255, 0.9);
    border-color: rgba(93, 120, 255, 0.4);
}

/* Page Header */
.page-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 24px;
}

.header-content h1 {
    font-size: 24px;
    margin: 0 0 8px;
    display: flex;
    align-items: center;
    gap: 12px;
}

.header-content p {
    color: var(--muted);
    margin: 0;
    font-size: 14px;
}

.header-actions {
    display: flex;
    gap: 12px;
}

/* Empty State */
.empty-state {
    text-align: center;
    padding: 60px 20px;
    color: var(--muted);
}

.empty-state h3 {
    font-size: 18px;
    margin: 16px 0 8px;
    color: var(--text);
}

.empty-state p {
    margin-bottom: 24px;
}

/* Pagination */
.pagination {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 16px;
    border-top: 1px solid var(--border);
}

.pagination-info {
    font-size: 13px;
    color: var(--muted);
}

.pagination-controls {
    display: flex;
    align-items: center;
    gap: 16px;
}

.page-numbers {
    font-size: 13px;
    color: var(--text);
}

/* Loading States */
.loading {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 300px;
    gap: 16px;
}

.loading-spinner {
    width: 40px;
    height: 40px;
    border: 3px solid var(--border);
    border-top-color: rgba(93, 120, 255, 0.9);
    border-radius: 50%;
    animation: spin 1s linear infinite;
}

@keyframes spin {
    to { transform: rotate(360deg); }
}

/* Alerts */
.alert {
    padding: 12px 16px;
    border-radius: 12px;
    margin-bottom: 20px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
}

.alert-success {
    background: rgba(49, 208, 124, 0.1);
    border: 1px solid rgba(49, 208, 124, 0.3);
}

.alert-error {
    background: rgba(255, 85, 102, 0.1);
    border: 1px solid rgba(255, 85, 102, 0.3);
}

.alert-content {
    display: flex;
    align-items: center;
    gap: 10px;
    flex: 1;
}
```

### dashboard/frontend/src/admin.css

```css
/* ==================== */
/* Admin Panel Styles */
/* ==================== */

.admin-app {
    height: 100vh;
    display: grid;
    grid-template-columns: 280px 1fr;
    gap: 14px;
    padding: 14px;
}

.admin-main {
    display: flex;
    flex-direction: column;
    min-width: 0;
}

.admin-content {
    flex: 1;
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    box-shadow: var(--shadow);
    overflow: auto;
    padding: 20px;
}

/* Admin Sidebar */
.sidebar {
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    box-shadow: var(--shadow);
    overflow: hidden;
    display: flex;
    flex-direction: column;
}

.brand {
    padding: 20px;
    border-bottom: 1px solid var(--border);
    display: flex;
    gap: 12px;
    align-items: center;
}

.logo {
    width: 40px;
    height: 40px;
    border-radius: 12px;
    background: linear-gradient(135deg, rgba(93, 120, 255, 0.9), rgba(49, 208, 124, 0.9));
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-weight: bold;
    font-size: 18px;
}

.brand h1 {
    font-size: 16px;
    margin: 0;
    font-weight: 600;
}

.brand p {
    font-size: 12px;
    color: var(--muted);
    margin: 4px 0 0;
}

.nav {
    padding: 16px;
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.nav-link {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 12px 16px;
    border-radius: 12px;
    color: var(--muted);
    text-decoration: none;
    transition: all 0.2s ease;
}

.nav-link:hover {
    background: rgba(255, 255, 255, 0.05);
    color: var(--text);
}

.nav-link.active {
    background: rgba(93, 120, 255, 0.15);
    color: rgba(93, 120, 255, 0.9);
    border-left: 3px solid rgba(93, 120, 255, 0.9);
}

.nav-link-content {
    display: flex;
    align-items: center;
    gap: 12px;
}

.sideSection {
    margin-top: auto;
    padding: 16px;
    border-top: 1px solid var(--border);
}

.sideTitle {
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    color: var(--muted2);
    margin-bottom: 12px;
}

.chip {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 8px 12px;
    background: rgba(93, 120, 255, 0.1);
    border: 1px solid rgba(93, 120, 255, 0.3);
    border-radius: 20px;
    font-size: 12px;
    color: rgba(93, 120, 255, 0.9);
}

/* Admin Topbar */
.topbar {
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    box-shadow: var(--shadow);
    padding: 16px 20px;
    margin-bottom: 14px;
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.topLeft {
    display: flex;
    align-items: center;
    gap: 12px;
}

.crumbs {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 14px;
}

.crumb-link {
    color: var(--muted);
    text-decoration: none;
    transition: color 0.2s ease;
}

.crumb-link:hover {
    color: var(--text);
}

.crumb-link.current {
    color: var(--text);
    font-weight: 600;
}

.sep {
    color: var(--muted2);
}

.topRight {
    display: flex;
    align-items: center;
    gap: 16px;
}

.btn {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 10px 16px;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid var(--border);
    border-radius: 12px;
    color: var(--text);
    font-size: 14px;
    cursor: pointer;
    transition: all 0.2s ease;
    text-decoration: none;
}

.btn:hover {
    background: rgba(255, 255, 255, 0.1);
    transform: translateY(-1px);
}

.btn-primary {
    background: rgba(93, 120, 255, 0.2);
    border-color: rgba(93, 120, 255, 0.4);
    color: rgba(93, 120, 255, 0.9);
}

.btn-sm {
    padding: 6px 12px;
    font-size: 13px;
}

.btn-icon {
    padding: 8px;
    justify-content: center;
}

.btn-block {
    width: 100%;
    justify-content: center;
}

.btn-danger {
    background: rgba(255, 85, 102, 0.1);
    border-color: rgba(255, 85, 102, 0.3);
    color: rgba(255, 85, 102, 0.9);
}

.btn-success {
    background: rgba(49, 208, 124, 0.1);
    border-color: rgba(49, 208, 124, 0.3);
    color: rgba(49, 208, 124, 0.9);
}

.btn-warning {
    background: rgba(245, 200, 75, 0.1);
    border-color: rgba(245, 200, 75, 0.3);
    color: rgba(245, 200, 75, 0.9);
}

.user-menu {
    display: flex;
    align-items: center;
    gap: 12px;
}

.user-info {
    display: flex;
    align-items: center;
    gap: 12px;
}

.user-avatar {
    width: 36px;
    height: 36px;
    border-radius: 50%;
    background: rgba(93, 120, 255, 0.2);
    display: flex;
    align-items: center;
    justify-content: center;
    color: rgba(93, 120, 255, 0.9);
}

.user-details {
    display: flex;
    flex-direction: column;
}

.user-name {
    font-size: 14px;
    font-weight: 600;
}

.user-role {
    font-size: 12px;
    color: var(--muted);
}
```

### dashboard/frontend/src/components/AdminSidebar.tsx

```typescript
import React from 'react';
import { NavLink } from 'react-router-dom';
import { 
  Users, 
  UsersRound, 
  FolderKanban, 
  Shield, 
  Settings, 
  Key, 
  Brain, 
  GitBranch,
  BarChart3,
  FileText,
  Home
} from 'lucide-react';

interface AdminSidebarProps {
  className?: string;
}

const AdminSidebar: React.FC<AdminSidebarProps> = ({ className = '' }) => {
  const navItems = [
    { path: '/admin', icon: <Home size={18} />, label: 'Overview', exact: true },
    { path: '/admin/teams', icon: <UsersRound size={18} />, label: 'Teams' },
    { path: '/admin/users', icon: <Users size={18} />, label: 'Users' },
    { path: '/admin/projects', icon: <FolderKanban size={18} />, label: 'Projects' },
    { path: '/admin/roles', icon: <Shield size={18} />, label: 'Roles & Access' },
    { path: '/admin/integrations', icon: <Settings size={18} />, label: 'Integrations' },
    { path: '/admin/secrets', icon: <Key size={18} />, label: 'Secrets' },
    { path: '/admin/llm-configs', icon: <Brain size={18} />, label: 'LLM Configs' },
    { path: '/admin/repositories', icon: <GitBranch size={18} />, label: 'Repositories' },
    { path: '/admin/monitoring', icon: <BarChart3 size={18} />, label: 'Monitoring' },
    { path: '/admin/audit', icon: <FileText size={18} />, label: 'Audit Log' },
  ];

  return (
    <aside className={`sidebar ${className}`}>
      <div className="brand">
        <div className="logo"></div>
        <div>
          <h1>Admin Console</h1>
          <p>System Administration</p>
        </div>
      </div>

      <nav className="nav">
        {navItems.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            end={item.exact}
            className={({ isActive }) => 
              `nav-link ${isActive ? 'active' : ''}`
            }
          >
            <span className="nav-link-content">
              {item.icon}
              <span>{item.label}</span>
            </span>
          </NavLink>
        ))}
      </nav>

      <div className="sideSection">
        <div className="sideTitle">System</div>
        <div className="chip">
          <span>Admin Mode</span>
        </div>
      </div>
    </aside>
  );
};

export default AdminSidebar;
```

### dashboard/frontend/src/components/AdminTopbar.tsx

```typescript
import React from 'react';
import { useLocation, Link } from 'react-router-dom';
import { ChevronRight, Bell, User, LogOut, Globe } from 'lucide-react';

interface AdminTopbarProps {
  user?: {
    name: string;
    email: string;
    role: string;
  };
  onLogout?: () => void;
}

const AdminTopbar: React.FC<AdminTopbarProps> = ({ 
  user = { name: 'Admin User', email: 'admin@example.com', role: 'System Admin' },
  onLogout 
}) => {
  const location = useLocation();
  
  // Parse path for breadcrumbs
  const pathSegments = location.pathname.split('/').filter(Boolean);
  const breadcrumbs = pathSegments.map((segment, index) => {
    const path = '/' + pathSegments.slice(0, index + 1).join('/');
    const label = segment.charAt(0).toUpperCase() + segment.slice(1).replace(/-/g, ' ');
    
    return { path, label };
  });

  return (
    <div className="topbar">
      <div className="topLeft">
        <div className="crumbs">
          <Link to="/admin" className="crumb-link">
            Admin
          </Link>
          {breadcrumbs.map((crumb, index) => (
            <React.Fragment key={crumb.path}>
              <span className="sep">
                <ChevronRight size={14} />
              </span>
              <Link 
                to={crumb.path} 
                className={`crumb-link ${index === breadcrumbs.length - 1 ? 'current' : ''}`}
              >
                {crumb.label}
              </Link>
            </React.Fragment>
          ))}
        </div>
      </div>

      <div className="topRight">
        <button className="btn icon-btn" aria-label="Notifications">
          <Bell size={18} />
          <span className="badge">3</span>
        </button>

        <button className="btn icon-btn" aria-label="Language">
          <Globe size={18} />
          <span>EN</span>
        </button>

        <div className="user-menu">
          <div className="user-info">
            <div className="user-avatar">
              <User size={20} />
            </div>
            <div className="user-details">
              <div className="user-name">{user.name}</div>
              <div className="user-role">{user.role}</div>
            </div>
          </div>
          
          {onLogout && (
            <button 
              className="btn logout-btn" 
              onClick={onLogout}
              aria-label="Logout"
            >
              <LogOut size={16} />
            </button>
          )}
        </div>
      </div>
    </div>
  );
};

export default AdminTopbar;
```

### dashboard/frontend/src/components/EventDrawer.tsx

```typescript
import { LogChunk } from '../types';

interface EventDrawerProps {
    isOpen: boolean;
    onClose: () => void;
    title: string;
    logs: LogChunk[];
    loading: boolean;
}

export default function EventDrawer({ isOpen, onClose, title, logs, loading }: EventDrawerProps) {
    return (
        <>
            <div
                className={`drawer-backdrop ${isOpen ? 'open' : ''}`}
                onClick={onClose}
                aria-hidden="true"
            ></div>
            <div className={`drawer ${isOpen ? 'open' : ''}`} role="dialog" aria-modal="true">
                <div className="drawer-h">
                    <div>
                        <strong id="drawerTitle">{title}</strong>
                        <div className="meta">{logs.length} events</div>
                    </div>
                    <button className="x" onClick={onClose} aria-label="Close">✕</button>
                </div>

                <div className="drawer-controls">
                    <div className="seg" role="tablist">
                        <button type="button" className="active" role="tab">All</button>
                        <button type="button" role="tab">Warnings</button>
                        <button type="button" role="tab">Errors</button>
                    </div>
                </div>

                <div className="events">
                    {loading && <div className="p-4 text-center text-sm text-gray-400">Loading...</div>}
                    {!loading && logs.length === 0 && <div className="p-4 text-center text-sm text-gray-400">No events</div>}
                    {logs.map(log => (
                        <div key={log.id} className="ev ok">
                            <div className="t">
                                <span>{new Date(log.timestamp).toLocaleTimeString()}</span>
                                <code>ID: {log.id}</code>
                            </div>
                            <div className="d">{log.content}</div>
                        </div>
                    ))}
                </div>
            </div>
        </>
    );
}
```

### dashboard/frontend/src/components/LanguageSwitcher.tsx

```typescript
import React from 'react';
import { useI18n } from '../i18n/I18nProvider';

const LanguageSwitcher: React.FC = () => {
  const { locale, setLocale } = useI18n();

  const languages = [
    { code: 'ru', label: 'РУ', fullLabel: 'Русский' },
    { code: 'en', label: 'EN', fullLabel: 'English' }
  ];

  return (
    <div className="language-switcher">
      <div className="language-switcher-label">
        <span className="language-icon">🌐</span>
        <span className="language-current">{locale.toUpperCase()}</span>
      </div>
      <div className="language-dropdown">
        {languages.map((lang) => (
          <button
            key={lang.code}
            className={`language-option ${locale === lang.code ? 'active' : ''}`}
            onClick={() => setLocale(lang.code as 'ru' | 'en')}
            title={lang.fullLabel}
          >
            <span className="language-code">{lang.label}</span>
            <span className="language-name">{lang.fullLabel}</span>
          </button>
        ))}
      </div>
    </div>
  );
};

export default LanguageSwitcher;
```

### dashboard/frontend/src/components/Layout.tsx

```typescript
import { ReactNode } from 'react';
import { useNavigate } from 'react-router-dom';

interface LayoutProps {
  children: ReactNode;
}

export default function Layout({ children }: LayoutProps) {
  const navigate = useNavigate();

  return (
    <div className="app">
      <div className="sidebar">
        <div className="brand">
          <div className="logo"></div>
          <div>
            <h1>Orchestrator</h1>
            <p>AI Development Platform</p>
          </div>
        </div>
        
        <nav className="nav">
          <a href="/dashboard" className="nav-item">
            <span className="nav-icon">📊</span>
            <span className="nav-text">Dashboard</span>
          </a>
          <a href="/projects" className="nav-item active">
            <span className="nav-icon">📋</span>
            <span className="nav-text">Projects</span>
          </a>
          <a href="/cycles" className="nav-item">
            <span className="nav-icon">🔄</span>
            <span className="nav-text">Cycles</span>
          </a>
          <a href="/tasks" className="nav-item">
            <span className="nav-icon">📝</span>
            <span className="nav-text">Tasks</span>
          </a>
          <a href="/integrations" className="nav-item">
            <span className="nav-icon">🔗</span>
            <span className="nav-text">Integrations</span>
          </a>
        </nav>

        <div className="side-section">
          <div className="side-title">Settings</div>
          <a href="/admin" className="nav-item">
            <span className="nav-icon">⚙️</span>
            <span className="nav-text">Admin Panel</span>
          </a>
          <a href="/settings" className="nav-item">
            <span className="nav-icon">👤</span>
            <span className="nav-text">Profile</span>
          </a>
        </div>

        <div className="side-section">
          <div className="side-title">Language</div>
          <div className="language-switcher">
            <button className="lang-btn active">RU</button>
            <button className="lang-btn">EN</button>
          </div>
        </div>
      </div>

      <main className="main">
        {children}
      </main>
    </div>
  );
}
```

### dashboard/frontend/src/components/LogViewer.tsx

```typescript
import { useEffect, useState, useRef } from 'react'
import axios from 'axios'
import { LogChunk } from '../types'
import { Terminal, X } from 'lucide-react'

// LogViewer Component with Sidebar Mode Support
interface LogViewerProps {
    taskId: string;
    taskName: string;
    onClose: () => void;
    mode?: 'modal' | 'sidebar';
}

export default function LogViewer({ taskId, taskName, onClose, mode = 'modal' }: LogViewerProps) {
    const [logs, setLogs] = useState<LogChunk[]>([])
    const bottomRef = useRef<HTMLDivElement>(null)

    useEffect(() => {
        const fetchLogs = async () => {
            // ... same fetch logic ...
            try {
                const res = await axios.get(`/api/tasks/${taskId}/logs`)
                setLogs(res.data)
            } catch (e) {
                console.error(e)
            }
        }
        fetchLogs()
        const interval = setInterval(fetchLogs, 2000)
        return () => clearInterval(interval)
    }, [taskId])

    useEffect(() => {
        if (bottomRef.current) {
            bottomRef.current.scrollIntoView({ behavior: 'smooth' })
        }
    }, [logs])

    const containerClasses = mode === 'modal'
        ? "fixed inset-0 bg-black/80 backdrop-blur-sm flex items-center justify-center p-8 z-50 animate-fade-in"
        : "h-full w-full flex flex-col bg-[#020617]"

    const innerClasses = mode === 'modal'
        ? "bg-[#0f172a] w-full max-w-5xl h-[80vh] rounded-xl flex flex-col shadow-2xl border border-white/10 overflow-hidden text-sm font-mono"
        : "h-full flex flex-col overflow-hidden text-sm font-mono bg-[#020617]"

    return (
        <div className={containerClasses} onClick={mode === 'modal' ? (e) => {
            if (e.target === e.currentTarget) onClose()
        } : undefined}>
            <div className={innerClasses}>
                {/* Header */}
                <div className="flex items-center justify-between p-4 bg-[#1e293b] border-b border-[#334155] flex-shrink-0">
                    <div className="flex items-center gap-2 text-blue-400">
                        <Terminal size={18} />
                        <span className="font-bold truncate max-w-[300px]" title={taskName}>{taskName}</span>
                    </div>
                    <button onClick={onClose} className="p-1 hover:bg-[#334155] rounded text-slate-400 hover:text-white transition-colors">
                        <X size={20} />
                    </button>
                </div>

                {/* Logs Body */}
                <div className="flex-1 min-h-0 overflow-y-auto p-4 space-y-1 bg-[#020617] custom-scrollbar font-mono text-xs md:text-sm">
                    {logs.length === 0 && <div className="text-slate-600 italic px-2">Waiting for logs...</div>}
                    {logs.map((log) => (
                        <div key={log.id} className="text-slate-300 whitespace-pre-wrap break-words leading-tight hover:bg-white/5 px-2 py-0.5 rounded transition-colors group">
                            <span className="text-slate-600 text-[10px] mr-3 select-none w-14 inline-block opacity-50 group-hover:opacity-100 transition-opacity">
                                {new Date(log.timestamp).toLocaleTimeString()}
                            </span>
                            <span className={log.content.includes('ERROR') || log.content.includes('❌') ? 'text-red-400 font-semibold' :
                                Number(log.content.includes('WARN')) ? 'text-orange-400' :
                                    log.content.includes('SUCCESS') || log.content.includes('✔') ? 'text-emerald-400' : ''}>
                                {log.content}
                            </span>
                        </div>
                    ))}
                    <div ref={bottomRef} />
                </div>

                {/* Footer */}
                <div className="p-2 bg-[#1e293b] border-t border-[#334155] text-[10px] text-slate-500 flex justify-between flex-shrink-0">
                    <span className="truncate max-w-[200px] font-mono opacity-70">ID: {taskId}</span>
                    <span className="flex items-center gap-1.5 text-emerald-400">
                        <span className="relative flex h-2 w-2">
                            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                            <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-400"></span>
                        </span>
                        Live Connection
                    </span>
                </div>
            </div>
        </div>
    )
}
```

### dashboard/frontend/src/components/PipelineGraph.tsx

```typescript
import { Pipeline, Stage } from '../types';

interface PipelineGraphProps {
    pipeline?: Pipeline;
    onNodeClick: (title: string, stageId?: string) => void;
}

export default function PipelineGraph({ pipeline, onNodeClick }: PipelineGraphProps) {
    if (!pipeline) {
        return (
            <div className="graph-wrap flex items-center justify-center">
                <div style={{ color: 'var(--muted)' }}>Select a pipeline</div>
            </div>
        );
    }

    // Helper to find stage status
    const getStage = (namePartial: string): Stage | undefined =>
        pipeline.stages?.find(s => s.name.toLowerCase().includes(namePartial.toLowerCase()));

    const getStatus = (stage?: Stage) => {
        if (!stage) return 'pending'; // or 'idle'
        if (stage.status === 'RUNNING') return 'running';
        if (stage.status === 'COMPLETED' || stage.status === 'SUCCESS') return 'done';
        if (stage.status === 'FAILED') return 'error';
        return 'pending'; // PENDING
    };

    // Define Nodes with fixed positions (as per index_GPT.html)
    // We map real stages to these visual nodes
    const planStage = getStage('Planning');
    const execStage = getStage('Execution');
    const mergeStage = getStage('Merge');
    const reviewStage = getStage('Review'); // Matches Repo Review or Global Review

    // Determine final status
    const isSuccess = pipeline.status === 'SUCCESS';
    const isFailed = pipeline.status === 'FAILED';
    const doneStatus = isSuccess ? 'done' : isFailed ? 'error' : 'pending';

    const nodes = [
        { id: 'planner', title: 'Planner', x: 40, y: 70, status: getStatus(planStage), stageId: planStage?.id },
        { id: 'workers', title: 'Workers (Agents)', x: 320, y: 70, status: getStatus(execStage), stageId: execStage?.id },
        { id: 'merge', title: 'Merge (Runtime)', x: 600, y: 70, status: getStatus(mergeStage), stageId: mergeStage?.id },
        { id: 'review', title: 'Review', x: 600, y: 250, status: getStatus(reviewStage), stageId: reviewStage?.id },
        { id: 'done', title: 'Completion', x: 840, y: 160, status: doneStatus, stageId: undefined },
    ];

    // Edges
    const edges = [
        { from: 'planner', to: 'workers' },
        { from: 'workers', to: 'merge' },
        { from: 'merge', to: 'review' },
        { from: 'review', to: 'done' },
        { from: 'review', to: 'workers', kind: 'loop' }
    ];

    // Determine active edge based on first RUNNING node
    // Simple logic: if from is DONE and to is RUNNING/PENDING, might be active.
    // Better: if 'workers' is running, edge planner->workers is active? No, workers->merge.
    // Let's just highlight edge if source is DONE and target is RUNNING.
    const isEdgeActive = (fromId: string, toId: string) => {
        const fromNode = nodes.find(n => n.id === fromId);
        const toNode = nodes.find(n => n.id === toId);
        if (fromNode?.status === 'done' && (toNode?.status === 'running' || toNode?.status === 'pending')) return true;
        if (fromNode?.status === 'running') return true;
        return false;
    };

    return (
        <div className="graph-wrap">
            <div className="canvas" id="canvas">
                <svg className="edges">
                    <defs>
                        <marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto" markerUnits="strokeWidth">
                            <path d="M0,0 L0,6 L9,3 z" fill="rgba(255,255,255,.35)"></path>
                        </marker>
                    </defs>
                    {edges.map((edge, i) => {
                        const from = nodes.find(n => n.id === edge.from)!;
                        const to = nodes.find(n => n.id === edge.to)!;

                        // Simple straight lines or curves. 
                        // index_GPT.html didn't have JS for drawing lines in the provided snippet, 
                        // but assumed SVG lines. I'll implement basic paths.

                        const x1 = from.x + 220; // width
                        const y1 = from.y + 24; // mid height
                        const x2 = to.x;
                        const y2 = to.y + 24;

                        let d = `M${x1},${y1} L${x2},${y2}`;

                        // Handle loop (review -> workers)
                        if (edge.kind === 'loop') {
                            // Curve back
                            d = `M${from.x},${from.y + 24} C${from.x - 50},${from.y + 100} ${to.x + 50},${to.y + 100} ${to.x + 100},${to.y + 48}`;
                        } else if (y1 !== y2) {
                            // Curve
                            const mx = (x1 + x2) / 2;
                            d = `M${x1},${y1} C${mx},${y1} ${mx},${y2} ${x2},${y2}`;
                        }

                        // Check active
                        const active = isEdgeActive(from.id, to.id) ? 'active' : '';

                        return <path key={i} d={d} className={`edge ${active}`} />;
                    })}
                </svg>

                {nodes.map(node => (
                    <div
                        key={node.id}
                        className={`node ${node.status}`}
                        style={{ left: node.x, top: node.y }}
                        onClick={() => onNodeClick(node.title, node.stageId)}
                        tabIndex={0}
                    >
                        <div className="node-top">
                            <div className="node-title">{node.title}</div>
                            <div className="status-pill">{node.status.toUpperCase()}</div>
                        </div>
                        <div className="node-body">
                            <div className="mini">
                                <span>Stage ID: {(node.stageId || '---').slice(0, 8)}</span>
                                <div className="dot"></div>
                            </div>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
}
```

### dashboard/frontend/src/components/PipelineView.tsx

```typescript
import { useEffect, useState, useRef, useCallback } from 'react'
import { useParams } from 'react-router-dom'
import axios from 'axios'
import { Pipeline } from '../types'
import LogViewer from './LogViewer'
import {
    LayoutDashboard,
    CheckCircle2, GitBranch, PlayCircle, XCircle,
    MonitorPlay, ZoomIn, Maximize,
    ShieldCheck
} from 'lucide-react'

// --- Helpers ---

function getStatusColor(status: string) {
    if (status === 'RUNNING') return 'text-secondary' // Yellow for Running
    if (['COMPLETED', 'SUCCESS', 'APPROVED'].includes(status)) return 'text-success' // Green
    if (['FAILED', 'REJECTED', 'FAILED_FINAL'].includes(status)) return 'text-error' // Red
    return 'text-slate-500' // Gray
}

function getStatusBorder(status: string) {
    if (status === 'RUNNING') return 'border-secondary'
    if (['COMPLETED', 'SUCCESS', 'APPROVED'].includes(status)) return 'border-success'
    if (['FAILED', 'REJECTED', 'FAILED_FINAL'].includes(status)) return 'border-error'
    return 'border-border'
}

function getStageType(name: string): 'PLANNER' | 'WORKERS' | 'MERGER' | 'REVIEWER' | 'OTHER' {
    if (name.includes('PLANNING')) return 'PLANNER'
    if (name.includes('EXECUTION')) return 'WORKERS'
    if (name.includes('MERGE')) return 'MERGER'
    if (name.includes('REVIEW')) return 'REVIEWER'
    return 'OTHER'
}

// --- SVG Flow System ---

const IdeConnector = ({ start, end, status }: { start: { x: number, y: number }, end: { x: number, y: number }, status: string }) => {
    const midX = (start.x + end.x) / 2
    const path = `M ${start.x} ${start.y} C ${midX} ${start.y}, ${midX} ${end.y}, ${end.x} ${end.y}`
    const isActive = status === 'RUNNING' || status === 'SUCCESS' || status === 'COMPLETED'
    const color = isActive ? 'text-secondary' : 'text-slate-700' // Yellow/Purple for active, Dark Gray for idle

    return (
        <g className={`${color} transition-colors duration-300`}>
            <path
                d={path}
                fill="none"
                stroke="currentColor"
                strokeWidth={isActive ? "2" : "1"}
                className={isActive ? "opacity-100" : "opacity-30"}
            />
            {status === 'RUNNING' && (
                <circle r="3" fill="currentColor">
                    <animateMotion dur="1.5s" repeatCount="indefinite" path={path} />
                </circle>
            )}
        </g>
    )
}

// --- Components ---

const IdeCard = ({ title, name, icon: Icon, status, onClick, isActive, isWorker = false }: any) => {
    const isRunning = status === 'RUNNING'

    return (
        <div
            onClick={onClick}
            className={`
                relative transition-all duration-200 group cursor-pointer overflow-hidden
                bg-surfaceHighlight shadow-lg
                border-l-4 ${getStatusBorder(status)}
                ${isActive ? 'ring-2 ring-primary ring-offset-2 ring-offset-background' : ''}
                w-[320px] p-5 rounded-sm
                hover:bg-[#3a3a3c]
            `}
        >
            <div className="flex flex-col h-full justify-between relative z-10">
                <div className="flex items-start justify-between mb-3">
                    <div className="flex items-center gap-3">
                        <div className={`p-1.5 rounded-sm ${isRunning ? 'text-secondary' : 'text-slate-400'}`}>
                            <Icon size={20} />
                        </div>
                        <div className="text-xs font-bold uppercase tracking-wider text-slate-500">{title}</div>
                    </div>
                </div>

                <div className="font-mono text-sm text-slate-200 break-all leading-relaxed custom-scrollbar max-h-[100px] overflow-y-auto">
                    {name}
                </div>

                <div className="mt-3 flex items-center justify-between border-t border-white/5 pt-2">
                    <span className={`text-xs font-bold ${getStatusColor(status)}`}>
                        {status || 'PENDING'}
                    </span>
                    {isWorker && <span className="text-[10px] text-slate-600 font-mono">ID: {name.slice(-6)}</span>}
                </div>
            </div>
        </div>
    )
}

// --- Main View ---

export default function PipelineView() {
    const { id } = useParams()
    const [pipeline, setPipeline] = useState<Pipeline | null>(null)
    const [selectedTask, setSelectedTask] = useState<{ id: string, name: string } | null>(null)

    // Zoom/Pan State
    const [transform, setTransform] = useState({ x: 0, y: 0, k: 1 })
    const [isDragging, setIsDragging] = useState(false)
    const [lastPos, setLastPos] = useState({ x: 0, y: 0 })
    const containerRef = useRef<HTMLDivElement>(null)

    // Polling Logic
    useEffect(() => {
        if (!id) return
        const fetchDetails = async () => {
            try {
                const res = await axios.get(`/api/pipelines/${id}`)
                setPipeline(res.data)
            } catch (e) { console.error(e) }
        }
        fetchDetails()
        const interval = setInterval(fetchDetails, 2000)
        return () => clearInterval(interval)
    }, [id])

    // Zoom Handlers
    const handleWheel = useCallback((e: React.WheelEvent) => {
        if (e.ctrlKey || e.metaKey) {
            e.preventDefault()
            const scaleAmount = -e.deltaY * 0.001
            setTransform(t => ({
                ...t,
                k: Math.max(0.1, Math.min(4, t.k * (1 + scaleAmount)))
            }))
        } else {
            setTransform(t => ({ ...t, x: t.x - e.deltaX, y: t.y - e.deltaY }))
        }
    }, [])

    const handleMouseDown = (e: React.MouseEvent) => {
        if (e.button === 0) { // Left click
            setIsDragging(true)
            setLastPos({ x: e.clientX, y: e.clientY })
        }
    }

    const handleMouseMove = (e: React.MouseEvent) => {
        if (!isDragging) return
        const dx = e.clientX - lastPos.x
        const dy = e.clientY - lastPos.y
        setTransform(t => ({ ...t, x: t.x + dx, y: t.y + dy }))
        setLastPos({ x: e.clientX, y: e.clientY })
    }

    const handleMouseUp = () => setIsDragging(false)
    const handleMouseLeave = () => setIsDragging(false)

    if (!pipeline) return (
        <div className="flex items-center justify-center h-full text-slate-500 bg-background font-mono text-sm">
            INITIALIZING WORKSPACE...
        </div>
    )

    const stages = pipeline.stages || []
    const planner = stages.find(s => getStageType(s.name) === 'PLANNER')
    const workers = stages.find(s => getStageType(s.name) === 'WORKERS')?.tasks || []
    const merger = stages.find(s => getStageType(s.name) === 'MERGER')
    const reviewer = stages.find(s => getStageType(s.name) === 'REVIEWER')

    return (
        <div className="h-full flex flex-col bg-background text-slate-200 font-sans overflow-hidden select-none">

            {/* Header HUD */}
            <header className="flex-none h-12 border-b border-border bg-surface flex items-center justify-between px-4 z-30">
                <div className="flex items-center gap-4 text-sm">
                    <div className="font-bold text-slate-300 flex items-center gap-2">
                        <ZoomIn size={14} className="text-secondary" />
                        WORKSPACE
                    </div>
                    <span className="text-slate-500 font-mono text-xs hidden md:inline">{pipeline.objective}</span>
                </div>
                <div className="flex items-center gap-3">
                    <button onClick={() => setTransform({ x: 0, y: 0, k: 1 })} className="p-1 hover:bg-surfaceHighlight rounded text-slate-400" title="Reset View">
                        <Maximize size={14} />
                    </button>
                    <div className="text-xs font-mono text-slate-500">
                        {Math.round(transform.k * 100)}%
                    </div>
                    <div className={`px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider ${getStatusBorder(pipeline.status)} border text-slate-300`}>
                        {pipeline.status}
                    </div>
                </div>
            </header>

            {/* Infinite Canvas */}
            <main
                className="flex-1 relative overflow-hidden bg-background cursor-grab active:cursor-grabbing"
                onWheel={handleWheel}
                onMouseDown={handleMouseDown}
                onMouseMove={handleMouseMove}
                onMouseUp={handleMouseUp}
                onMouseLeave={handleMouseLeave}
            >
                {/* Transform Layer */}
                <div
                    className="absolute origin-top-left transition-transform duration-75 ease-linear"
                    style={{ transform: `translate(${transform.x}px, ${transform.y}px) scale(${transform.k})` }}
                >
                    <div className="w-[3000px] h-[2000px] relative pt-20 pl-20" ref={containerRef}>

                        {/* SVG Layer */}
                        <svg className="absolute inset-0 w-full h-full pointer-events-none z-0">
                            {/* Connectors */}
                            {workers.length > 0 ? (
                                <>
                                    {/* Planner -> Workers (Fan out) */}
                                    {workers.map((_, i) => (
                                        <IdeConnector
                                            key={`p-w-${i}`}
                                            start={{ x: 420, y: 400 }}
                                            end={{ x: 570, y: 400 + (workers.length * 180 / 2) - (workers.length * 180) + (i * 180) + 90 }}
                                            status={planner?.status || 'PENDING'}
                                        />
                                    ))}
                                    {/* Workers -> Merger (Fan in) */}
                                    {workers.map((w, i) => (
                                        <IdeConnector
                                            key={`w-m-${i}`}
                                            start={{ x: 890, y: 400 + (workers.length * 180 / 2) - (workers.length * 180) + (i * 180) + 90 }}
                                            end={{ x: 1040, y: 400 }}
                                            status={w.status === 'RUNNING' || w.status === 'COMPLETED' || w.status === 'SUCCESS' ? 'RUNNING' : 'PENDING'}
                                        />
                                    ))}
                                </>
                            ) : (
                                // No workers yet - direct line placeholder or broken
                                <IdeConnector start={{ x: 420, y: 400 }} end={{ x: 570, y: 400 }} status={planner?.status || 'PENDING'} />
                            )}

                            {/* Merger -> Reviewer */}
                            <IdeConnector start={{ x: 1360, y: 400 }} end={{ x: 1510, y: 400 }} status={merger?.status || 'PENDING'} />

                            {/* Reviewer -> Result */}
                            <IdeConnector start={{ x: 1830, y: 400 }} end={{ x: 1980, y: 416 }} status={reviewer?.status || 'PENDING'} />
                        </svg>

                        {/* --- NODES --- */}

                        {/* Planner (Centered at Y=400 -> Top ~320) */}
                        <div className="absolute top-[320px] left-[100px] z-10">
                            <IdeCard
                                title="Planner"
                                name={planner?.tasks?.[0]?.name || planner?.name || "Initializing..."}
                                icon={LayoutDashboard}
                                status={planner?.status}
                                isActive={selectedTask?.id === planner?.tasks?.[0]?.id}
                                onClick={() => planner?.tasks?.[0] && setSelectedTask({ id: planner.tasks[0].id, name: "Plan" })}
                            />
                        </div>

                        {/* Workers Grid (Dynamic Centering) */}
                        <div
                            className="absolute left-[570px] z-10 flex flex-col gap-[20px]"
                            style={{
                                top: workers.length > 0
                                    ? `${400 - (workers.length * 180 / 2)}px`
                                    : '320px'
                            }}
                        >
                            {workers.length > 0 ? workers.map(w => (
                                <IdeCard
                                    key={w.id}
                                    title="Worker Agent"
                                    name={w.name}
                                    icon={MonitorPlay}
                                    isWorker={true}
                                    status={w.status}
                                    isActive={selectedTask?.id === w.id}
                                    onClick={() => setSelectedTask({ id: w.id, name: w.name })}
                                />
                            )) : (
                                <div className="w-[320px] p-6 border border-dashed border-border text-slate-600 font-mono text-xs text-center glass-card">
                                    // Awaiting dispatch...
                                </div>
                            )}
                        </div>

                        {/* Merger (Centered at Y=400 -> Top ~320, X=1040) */}
                        <div className="absolute top-[320px] left-[1040px] z-10">
                            <IdeCard
                                title="Integrator"
                                name={merger?.name || "Merge Pending"}
                                icon={GitBranch}
                                status={merger?.status}
                                isActive={selectedTask?.id === merger?.tasks?.[0]?.id}
                                onClick={() => merger?.tasks?.[0] && setSelectedTask({ id: merger.tasks[0].id, name: "Merge" })}
                            />
                        </div>

                        {/* Reviewer (Centered at Y=400 -> Top ~320, X=1510) */}
                        <div className="absolute top-[320px] left-[1510px] z-10">
                            <IdeCard
                                title="Reviewer"
                                name={reviewer?.name || "Review Pending"}
                                icon={ShieldCheck}
                                status={reviewer?.status}
                                isActive={selectedTask?.id === reviewer?.tasks?.[0]?.id}
                                onClick={() => reviewer?.tasks?.[0] && setSelectedTask({ id: reviewer.tasks[0].id, name: "Review" })}
                            />
                        </div>

                        {/* Result (Centered at Y=400 -> Top ~350, X=1980) */}
                        <div className="absolute top-[350px] left-[1980px] z-10 flex items-center gap-4">
                            <div className={`
                                w-32 h-32 rounded-full border-4 flex items-center justify-center transition-all
                                ${pipeline.status === 'SUCCESS' ? 'border-success bg-background shadow-lg' :
                                    pipeline.status === 'FAILED' ? 'border-error bg-background shadow-lg' :
                                        'border-border bg-surfaceHighlight'}
                            `}>
                                {pipeline.status === 'SUCCESS' ? <CheckCircle2 size={48} className="text-success" /> :
                                    pipeline.status === 'FAILED' ? <XCircle size={48} className="text-error" /> :
                                        <PlayCircle size={48} className="text-secondary animate-pulse" />}
                            </div>
                            <div className="text-2xl font-bold tracking-tight text-slate-300">
                                {pipeline.status}
                            </div>
                        </div>

                    </div>
                </div>
            </main>

            {/* Sidebar Log Panel */}
            <div className={`fixed inset-y-0 right-0 w-[600px] bg-background border-l border-border shadow-2xl transition-transform duration-200 z-50 flex flex-col ${selectedTask ? 'translate-x-0' : 'translate-x-full'}`}>
                {selectedTask && (
                    <LogViewer
                        taskId={selectedTask.id}
                        taskName={selectedTask.name}
                        onClose={() => setSelectedTask(null)}
                        mode="sidebar"
                    />
                )}
            </div>
            {selectedTask && <div className="fixed inset-0 bg-black/50 z-40" onClick={() => setSelectedTask(null)} />}
        </div>
    )
}
```

### dashboard/frontend/src/components/ProjectTree.tsx

```typescript
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import {
  ChevronRight,
  ChevronDown,
  Folder,
  FolderOpen,
  FileText,
  CheckCircle,
  Circle,
  AlertCircle,
  Plus,
  Edit,
  Trash2,
  Play,
  Pause
} from 'lucide-react';

interface ProjectNode {
  id: string;
  name: string;
  type: 'project' | 'cycle' | 'epoch' | 'epic' | 'task';
  status: 'active' | 'completed' | 'paused' | 'planned';
  children?: ProjectNode[];
  description?: string;
  metadata?: Record<string, any>;
}

interface ProjectTreeProps {
  projectId?: string;
  onNodeSelect?: (node: ProjectNode) => void;
  onNodeAction?: (action: string, node: ProjectNode) => void;
  showActions?: boolean;
  expandedByDefault?: boolean;
}

const ProjectTree: React.FC<ProjectTreeProps> = ({
  projectId,
  onNodeSelect,
  onNodeAction,
  showActions = true,
  expandedByDefault = false
}) => {
  const [treeData, setTreeData] = useState<ProjectNode[]>([]);
  const [expandedNodes, setExpandedNodes] = useState<Set<string>>(new Set());
  const [selectedNode, setSelectedNode] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (projectId) {
      fetchProjectTree();
    } else {
      fetchAllProjects();
    }
  }, [projectId]);

  const fetchAllProjects = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await axios.get('/api/projects');
      const projects = response.data.map((project: any) => ({
        id: project.id,
        name: project.name,
        type: 'project' as const,
        status: project.status === 'active' ? 'active' : 
                project.status === 'completed' ? 'completed' : 'paused',
        description: project.description,
        metadata: {
          default_language: project.default_language,
          created_at: project.created_at,
          cycles_count: project.cycles_count || 0
        }
      }));
      setTreeData(projects);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to load projects');
      console.error('Error fetching projects:', err);
    } finally {
      setLoading(false);
    }
  };

  const fetchProjectTree = async () => {
    if (!projectId) return;
    
    setLoading(true);
    setError(null);
    try {
      const response = await axios.get(`/api/projects/${projectId}/tree`);
      const projectTree = transformApiResponse(response.data);
      setTreeData([projectTree]);
      
      // Expand first level by default
      if (expandedByDefault) {
        setExpandedNodes(new Set([projectTree.id]));
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to load project tree');
      console.error('Error fetching project tree:', err);
    } finally {
      setLoading(false);
    }
  };

  const transformApiResponse = (data: any): ProjectNode => {
    const transformNode = (node: any, type: ProjectNode['type']): ProjectNode => {
      const baseNode: ProjectNode = {
        id: node.id,
        name: node.name || node.title || `Untitled ${type}`,
        type,
        status: node.status === 'active' ? 'active' :
                node.status === 'completed' ? 'completed' :
                node.status === 'paused' ? 'paused' : 'planned',
        description: node.description,
        metadata: {
          ...node,
          created_at: node.created_at,
          updated_at: node.updated_at
        }
      };

      // Add children based on type
      if (type === 'project' && node.cycles) {
        baseNode.children = node.cycles.map((cycle: any) => transformNode(cycle, 'cycle'));
      } else if (type === 'cycle' && node.epochs) {
        baseNode.children = node.epochs.map((epoch: any) => transformNode(epoch, 'epoch'));
      } else if (type === 'epoch' && node.epics) {
        baseNode.children = node.epics.map((epic: any) => transformNode(epic, 'epic'));
      } else if (type === 'epic' && node.tasks) {
        baseNode.children = node.tasks.map((task: any) => transformNode(task, 'task'));
      }

      return baseNode;
    };

    return transformNode(data, 'project');
  };

  const toggleNode = (nodeId: string) => {
    const newExpanded = new Set(expandedNodes);
    if (newExpanded.has(nodeId)) {
      newExpanded.delete(nodeId);
    } else {
      newExpanded.add(nodeId);
    }
    setExpandedNodes(newExpanded);
  };

  const handleNodeClick = (node: ProjectNode) => {
    setSelectedNode(node.id);
    if (onNodeSelect) {
      onNodeSelect(node);
    }
    if (node.children && node.children.length > 0) {
      toggleNode(node.id);
    }
  };

  const handleAction = (action: string, node: ProjectNode, e: React.MouseEvent) => {
    e.stopPropagation();
    if (onNodeAction) {
      onNodeAction(action, node);
    }
  };

  const getStatusIcon = (status: ProjectNode['status']) => {
    switch (status) {
      case 'active':
        return <Play className="w-4 h-4 text-green-500" />;
      case 'completed':
        return <CheckCircle className="w-4 h-4 text-blue-500" />;
      case 'paused':
        return <Pause className="w-4 h-4 text-yellow-500" />;
      default:
        return <Circle className="w-4 h-4 text-gray-400" />;
    }
  };

  const getTypeIcon = (type: ProjectNode['type'], isExpanded: boolean) => {
    switch (type) {
      case 'project':
        return isExpanded ? 
          <FolderOpen className="w-4 h-4 text-blue-500" /> : 
          <Folder className="w-4 h-4 text-blue-400" />;
      case 'cycle':
        return <Folder className="w-4 h-4 text-green-400" />;
      case 'epoch':
        return <Folder className="w-4 h-4 text-purple-400" />;
      case 'epic':
        return <Folder className="w-4 h-4 text-orange-400" />;
      case 'task':
        return <FileText className="w-4 h-4 text-gray-400" />;
    }
  };

  const renderTreeNode = (node: ProjectNode, depth = 0) => {
    const isExpanded = expandedNodes.has(node.id);
    const isSelected = selectedNode === node.id;
    const hasChildren = node.children && node.children.length > 0;

    return (
      <div key={node.id}>
        <div
          className={`
            flex items-center px-2 py-1.5 rounded-md cursor-pointer transition-colors
            ${isSelected ? 'bg-blue-50 border border-blue-200' : 'hover:bg-gray-50'}
          `}
          style={{ paddingLeft: `${depth * 20 + 8}px` }}
          onClick={() => handleNodeClick(node)}
        >
          <div className="flex items-center space-x-2 flex-1">
            {hasChildren ? (
              <button
                className="p-0.5 hover:bg-gray-200 rounded"
                onClick={(e) => {
                  e.stopPropagation();
                  toggleNode(node.id);
                }}
              >
                {isExpanded ? (
                  <ChevronDown className="w-3 h-3 text-gray-500" />
                ) : (
                  <ChevronRight className="w-3 h-3 text-gray-500" />
                )}
              </button>
            ) : (
              <div className="w-5" /> // Spacer for alignment
            )}
            
            {getTypeIcon(node.type, isExpanded)}
            {getStatusIcon(node.status)}
            
            <span className={`font-medium ${isSelected ? 'text-blue-700' : 'text-gray-800'}`}>
              {node.name}
            </span>
            
            {node.description && (
              <span className="text-sm text-gray-500 truncate ml-2">
                {node.description}
              </span>
            )}
          </div>

          {showActions && (
            <div className="flex items-center space-x-1 ml-2">
              <button
                className="p-1 hover:bg-gray-200 rounded text-gray-600 hover:text-blue-600"
                onClick={(e) => handleAction('add', node, e)}
                title="Add child"
              >
                <Plus className="w-3 h-3" />
              </button>
              <button
                className="p-1 hover:bg-gray-200 rounded text-gray-600 hover:text-yellow-600"
                onClick={(e) => handleAction('edit', node, e)}
                title="Edit"
              >
                <Edit className="w-3 h-3" />
              </button>
              <button
                className="p-1 hover:bg-gray-200 rounded text-gray-600 hover:text-red-600"
                onClick={(e) => handleAction('delete', node, e)}
                title="Delete"
              >
                <Trash2 className="w-3 h-3" />
              </button>
            </div>
          )}
        </div>

        {isExpanded && hasChildren && node.children && (
          <div>
            {node.children.map(child => renderTreeNode(child, depth + 1))}
          </div>
        )}
      </div>
    );
  };

  if (loading) {
    return (
      <div className="p-4 text-center">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500 mx-auto"></div>
        <p className="mt-2 text-gray-600">Loading project tree...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-4 bg-red-50 border border-red-200 rounded-md">
        <div className="flex items-center">
          <AlertCircle className="w-5 h-5 text-red-500 mr-2" />
          <p className="text-red-700">{error}</p>
        </div>
      </div>
    );
  }

  if (treeData.length === 0) {
    return (
      <div className="p-4 text-center text-gray-500">
        <Folder className="w-12 h-12 mx-auto text-gray-300 mb-2" />
        <p>No projects found</p>
        <p className="text-sm mt-1">Create your first project to get started</p>
      </div>
    );
  }

  return (
    <div className="border rounded-lg bg-white">
      <div className="p-3 border-b bg-gray-50">
        <h3 className="font-semibold text-gray-800">
          {projectId ? 'Project Hierarchy' : 'All Projects'}
        </h3>
        <p className="text-sm text-gray-600">
          {projectId ? 'Project → Cycle → Epoch → Epic → Task' : 'Click on a project to view details'}
        </p>
      </div>
      <div className="p-2 max-h-96 overflow-y-auto">
        {treeData.map(node => renderTreeNode(node))}
      </div>
    </div>
  );
};

export default ProjectTree;
```

### dashboard/frontend/src/components/RuntimeList.tsx

```typescript
import { Task } from '../types';

interface RuntimeListProps {
    tasks: Task[];
}

export default function RuntimeList({ tasks }: RuntimeListProps) {
    // Filter tasks that actually used an agent
    const activeTasks = tasks.filter(t => t.agent_session_id);

    return (
        <div className="runtime-list" id="runtimeList">
            {activeTasks.length === 0 && (
                <div className="p-4 text-center" style={{ color: 'var(--muted)' }}>
                    No active runtimes
                </div>
            )}
            {activeTasks.map(task => {
                // Determine state class
                // "busy" if RUNNING or agent_state=='busy' or 'running'
                // "idle" if agent_state=='idle' or status=='COMPLETED'
                let stateClass = 'idle';
                let stateLabel = 'IDLE';

                const rawState = (task.agent_state || '').toLowerCase();
                const status = (task.status || '').toUpperCase();

                if (status === 'RUNNING') {
                    if (rawState === 'busy' || rawState === 'running') {
                        stateClass = 'busy';
                        stateLabel = 'BUSY';
                    } else if (rawState === 'idle' || rawState === 'awaiting_user_input') {
                        stateClass = 'idle';
                        stateLabel = 'IDLE';
                    } else {
                        // Fallback if no specific state but running
                        stateClass = 'busy';
                        stateLabel = 'RUNNING';
                    }
                } else if (status === 'FAILED' || status === 'FAILED_FINAL') {
                    stateClass = 'error';
                    stateLabel = 'ERROR';
                } else {
                    // Completed
                    stateClass = 'idle';
                    stateLabel = 'DONE';
                }

                return (
                    <div key={task.id} className="rt">
                        <div>
                            <strong>{task.name}</strong>
                            <small>{task.agent_session_id?.slice(0, 8)}...</small>
                        </div>
                        <div className={`state ${stateClass}`}>
                            {stateLabel}
                        </div>
                    </div>
                );
            })}
        </div>
    );
}
```

### dashboard/frontend/src/components/Sidebar.tsx

```typescript
import { Pipeline } from '../types';
import { NavLink } from 'react-router-dom';

interface SidebarProps {
    pipelines: Pipeline[];
}

export default function Sidebar({ pipelines }: SidebarProps) {
    return (
        <aside className="sidebar" aria-label="Sidebar">
            <div className="sb-header">
                <div className="logo" aria-hidden="true"></div>
                <div className="sb-title">
                    <strong>Orchestrator</strong>
                    <span>Dashboard</span>
                </div>
            </div>

            <div className="sb-search">
                <input id="q" type="search" placeholder="Search tasks..." aria-label="Search tasks" />
            </div>

            <div className="tasklist" role="listbox">
                {pipelines.map(p => (
                    <NavLink
                        key={p.id}
                        to={`/pipelines/${p.id}`}
                        className={({ isActive }) => `task ${isActive ? 'active' : ''}`}
                    >
                        {({ isActive }) => (
                            <>
                                <div className={`pulse ${p.status === 'RUNNING' ? 'on' : ''}`}></div>
                                <div className="task-main">
                                    <div className="task-top">
                                        <span className="task-key">PIPE-{p.id.slice(-4)}</span>
                                        <span className={`badge ${p.status === 'SUCCESS' ? 'done' : p.status === 'RUNNING' ? 'run' : ''}`}>
                                            {p.status}
                                        </span>
                                    </div>
                                    <div className="task-title">{p.objective || "Untitled Pipeline"}</div>
                                    <div className="task-meta">
                                        <span>{new Date(p.created_at).toLocaleTimeString()}</span>
                                    </div>
                                </div>
                            </>
                        )}
                    </NavLink>
                ))}
            </div>
        </aside>
    );
}
```

### dashboard/frontend/src/i18n/I18nProvider.tsx

```typescript
import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';

// Import translations
import ruTranslations from './locales/ru.json';
import enTranslations from './locales/en.json';

type Locale = 'ru' | 'en';
type Translations = typeof ruTranslations;

interface I18nContextType {
  locale: Locale;
  setLocale: (locale: Locale) => void;
  t: (key: string, params?: Record<string, any>) => string;
}

const translations: Record<Locale, Translations> = {
  ru: ruTranslations,
  en: enTranslations
};

const I18nContext = createContext<I18nContextType | undefined>(undefined);

interface I18nProviderProps {
  children: ReactNode;
  defaultLocale?: Locale;
}

export function I18nProvider({ children, defaultLocale = 'ru' }: I18nProviderProps) {
  const [locale, setLocale] = useState<Locale>(() => {
    // Try to get saved locale from localStorage
    const saved = localStorage.getItem('locale') as Locale;
    return saved && ['ru', 'en'].includes(saved) ? saved : defaultLocale;
  });

  // Save locale to localStorage when it changes
  useEffect(() => {
    localStorage.setItem('locale', locale);
    document.documentElement.lang = locale;
  }, [locale]);

  const t = (key: string, params?: Record<string, any>): string => {
    const keys = key.split('.');
    let value: any = translations[locale];
    
    for (const k of keys) {
      if (value && typeof value === 'object' && k in value) {
        value = value[k];
      } else {
        // Fallback to English if key not found
        value = translations.en;
        for (const k2 of keys) {
          if (value && typeof value === 'object' && k2 in value) {
            value = value[k2];
          } else {
            return key; // Return key if not found anywhere
          }
        }
      }
    }
    
    if (typeof value === 'string' && params) {
      return Object.entries(params).reduce((str, [param, val]) => {
        return str.replace(`{${param}}`, String(val));
      }, value);
    }
    
    return typeof value === 'string' ? value : key;
  };

  return (
    <I18nContext.Provider value={{ locale, setLocale, t }}>
      {children}
    </I18nContext.Provider>
  );
}

export function useI18n() {
  const context = useContext(I18nContext);
  if (context === undefined) {
    throw new Error('useI18n must be used within an I18nProvider');
  }
  return context;
}

// Helper hook for components
export function useTranslation() {
  const { t } = useI18n();
  return { t };
}
```

### dashboard/frontend/src/index.css

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

:root {
    --bg: #0b1020;
    --panel: rgba(255, 255, 255, .06);
    --panel-2: rgba(255, 255, 255, .09);
    --text: rgba(255, 255, 255, .92);
    --muted: rgba(255, 255, 255, .64);
    --muted2: rgba(255, 255, 255, .42);
    --border: rgba(255, 255, 255, .12);

    --ok: #31d07c;
    --run: #f5c84b;
    --idle: rgba(255, 255, 255, .18);
    --bad: #ff5566;
    --warn: #ffb020;

    --shadow: 0 14px 40px rgba(0, 0, 0, .35);
    --radius: 16px;
}

/* Import Admin Styles */
@import './admin.css';
@import './admin-dashboard.css';
@import './admin-tables.css';
@import './admin-login.css';

* {
    box-sizing: border-box;
}

/* html,body{ height:100%; } handled by tailwind/react root usually but good to keep */
body {
    margin: 0;
    font: 14px/1.35 system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif;
    color: var(--text);
    background:
        radial-gradient(1200px 600px at 20% -10%, rgba(93, 120, 255, .25), transparent 60%),
        radial-gradient(900px 500px at 85% 15%, rgba(49, 208, 124, .18), transparent 55%),
        radial-gradient(900px 600px at 30% 110%, rgba(245, 200, 75, .15), transparent 60%),
        var(--bg);
    overflow: hidden;
}

.app {
    height: 100vh;
    display: grid;
    grid-template-columns: 320px 1fr;
    gap: 14px;
    padding: 14px;
}

/* Sidebar */
.sidebar {
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    box-shadow: var(--shadow);
    overflow: hidden;
    display: flex;
    flex-direction: column;
    min-width: 280px;
}

.sb-header {
    padding: 16px 16px 12px;
    border-bottom: 1px solid var(--border);
    display: flex;
    gap: 10px;
    align-items: center;
}

.logo {
    width: 34px;
    height: 34px;
    border-radius: 12px;
    background:
        radial-gradient(circle at 30% 30%, rgba(255, 255, 255, .35), transparent 50%),
        linear-gradient(135deg, rgba(93, 120, 255, .9), rgba(49, 208, 124, .9));
    box-shadow: 0 10px 24px rgba(0, 0, 0, .25);
    flex: 0 0 auto;
}

.sb-title {
    display: flex;
    flex-direction: column;
    min-width: 0;
}

.sb-title strong {
    font-size: 14px;
    letter-spacing: .2px;
}

.sb-title span {
    font-size: 12px;
    color: var(--muted);
}

.sb-search {
    padding: 10px 16px 14px;
    border-bottom: 1px solid var(--border);
}

.sb-search input {
    width: 100%;
    padding: 10px 12px;
    border-radius: 12px;
    border: 1px solid var(--border);
    background: rgba(0, 0, 0, .18);
    color: var(--text);
    outline: none;
    transition: border-color .15s ease, transform .15s ease;
}

.sb-search input:focus {
    border-color: rgba(93, 120, 255, .65);
    transform: translateY(-1px);
}

.tasklist {
    padding: 12px;
    overflow: auto;
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.task {
    border: 1px solid var(--border);
    background: rgba(0, 0, 0, .16);
    border-radius: 14px;
    padding: 12px;
    cursor: pointer;
    transition: transform .12s ease, background .12s ease, border-color .12s ease;
    display: flex;
    gap: 10px;
    align-items: flex-start;
}

.task:hover {
    transform: translateY(-1px);
    background: rgba(0, 0, 0, .22);
}

.task.active {
    border-color: rgba(93, 120, 255, .75);
    background: rgba(93, 120, 255, .10);
}

.pulse {
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background: var(--idle);
    margin-top: 3px;
    flex: 0 0 auto;
    position: relative;
}

.pulse.on {
    background: var(--run);
    box-shadow: 0 0 0 0 rgba(245, 200, 75, .55);
    animation: pulse 1.2s infinite;
}

@keyframes pulse {
    0% {
        box-shadow: 0 0 0 0 rgba(245, 200, 75, .45);
    }

    70% {
        box-shadow: 0 0 0 12px rgba(245, 200, 75, 0);
    }

    100% {
        box-shadow: 0 0 0 0 rgba(245, 200, 75, 0);
    }
}

.task-main {
    min-width: 0;
    flex: 1;
}

.task-top {
    display: flex;
    gap: 8px;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 6px;
}

.task-key {
    font-weight: 650;
    letter-spacing: .2px;
    font-size: 12px;
    color: rgba(255, 255, 255, .86);
}

.badge {
    font-size: 11px;
    padding: 4px 8px;
    border-radius: 999px;
    border: 1px solid var(--border);
    color: var(--muted);
    background: rgba(255, 255, 255, .06);
    white-space: nowrap;
}

.badge.done {
    color: rgba(49, 208, 124, .95);
    border-color: rgba(49, 208, 124, .35);
    background: rgba(49, 208, 124, .10);
}

.badge.run {
    color: rgba(245, 200, 75, .95);
    border-color: rgba(245, 200, 75, .35);
    background: rgba(245, 200, 75, .10);
}

.task-title {
    color: rgba(255, 255, 255, .92);
    font-size: 13px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.task-meta {
    margin-top: 8px;
    color: var(--muted2);
    font-size: 12px;
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
}

/* Main area */
.main {
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    box-shadow: var(--shadow);
    overflow: hidden;
    display: flex;
    flex-direction: column;
    min-width: 0;
    position: relative;
}

.topbar {
    padding: 16px 16px 12px;
    border-bottom: 1px solid var(--border);
    display: flex;
    gap: 12px;
    align-items: flex-start;
    justify-content: space-between;
}

.headline {
    min-width: 0;
    display: flex;
    flex-direction: column;
    gap: 6px;
}

.headline .h1 {
    display: flex;
    gap: 10px;
    align-items: baseline;
    min-width: 0;
}

.headline .h1 strong {
    font-size: 16px;
    letter-spacing: .2px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    max-width: 64ch;
}

.headline .h1 code {
    font-size: 12px;
    color: rgba(255, 255, 255, .72);
    background: rgba(0, 0, 0, .18);
    border: 1px solid var(--border);
    padding: 2px 8px;
    border-radius: 999px;
}

.subline {
    color: var(--muted);
    font-size: 12px;
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
    align-items: center;
}

.progress {
    display: flex;
    align-items: center;
    gap: 8px;
}

.bar {
    width: 180px;
    height: 8px;
    border-radius: 999px;
    background: rgba(255, 255, 255, .08);
    border: 1px solid var(--border);
    overflow: hidden;
}

.bar>div {
    height: 100%;
    width: 0%;
    background: linear-gradient(90deg, rgba(93, 120, 255, .9), rgba(49, 208, 124, .9));
    transition: width .35s ease;
}

.actions {
    display: flex;
    gap: 10px;
    align-items: center;
    flex: 0 0 auto;
}

.btn {
    border: 1px solid var(--border);
    background: rgba(0, 0, 0, .18);
    color: var(--text);
    padding: 10px 12px;
    border-radius: 12px;
    cursor: pointer;
    transition: transform .12s ease, background .12s ease, border-color .12s ease;
    user-select: none;
}

.btn:hover {
    transform: translateY(-1px);
    background: rgba(0, 0, 0, .24);
}

.btn:active {
    transform: translateY(0px);
}

.btn.primary {
    border-color: rgba(93, 120, 255, .55);
    background: rgba(93, 120, 255, .16);
}

.content {
    position: relative;
    padding: 14px;
    display: grid;
    grid-template-columns: 1fr 320px;
    gap: 14px;
    height: 100%;
    overflow: hidden;
}

.graph-card,
.runtime-card {
    background: rgba(0, 0, 0, .16);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    overflow: hidden;
    position: relative;
    min-width: 0;
}

.card-h {
    padding: 12px 12px 10px;
    border-bottom: 1px solid var(--border);
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 10px;
}

.card-h strong {
    font-size: 13px;
}

.card-h span {
    color: var(--muted);
    font-size: 12px;
}

.graph-wrap {
    position: relative;
    height: calc(100% - 46px);
    overflow: auto;
    padding: 16px;
}

.canvas {
    position: relative;
    min-height: 420px;
    width: max(780px, 100%);
    padding: 10px;
}

svg.edges {
    position: absolute;
    inset: 0;
    pointer-events: none;
    overflow: visible;
}

.edge {
    stroke: rgba(255, 255, 255, .22);
    stroke-width: 2;
    fill: none;
    marker-end: url(#arrow);
}

.edge.active {
    stroke: rgba(245, 200, 75, .55);
    stroke-dasharray: 8 8;
    animation: dash 1s linear infinite;
}

@keyframes dash {
    to {
        stroke-dashoffset: -16;
    }
}

.node {
    position: absolute;
    width: 220px;
    border-radius: 16px;
    border: 1px solid var(--border);
    background: rgba(255, 255, 255, .04);
    padding: 12px;
    cursor: pointer;
    transition: transform .14s ease, border-color .14s ease, background .14s ease, box-shadow .14s ease;
    box-shadow: 0 10px 20px rgba(0, 0, 0, .18);
    outline: none;
}

.node:hover {
    transform: translateY(-2px);
    background: rgba(255, 255, 255, .06);
}

.node:focus {
    box-shadow: 0 0 0 3px rgba(93, 120, 255, .35), 0 10px 20px rgba(0, 0, 0, .18);
}

.node-top {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 10px;
    margin-bottom: 6px;
}

.node-title {
    font-weight: 700;
    font-size: 13px;
    letter-spacing: .2px;
}

.status-pill {
    font-size: 11px;
    padding: 3px 8px;
    border-radius: 999px;
    border: 1px solid var(--border);
    color: var(--muted);
    background: rgba(0, 0, 0, .18);
    white-space: nowrap;
}

.node-body {
    color: var(--muted);
    font-size: 12px;
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.mini {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 8px;
    color: var(--muted2);
}

.dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: var(--idle);
    box-shadow: 0 0 0 0 rgba(255, 255, 255, 0);
}

/* Status coloring */
.node.done {
    border-color: rgba(49, 208, 124, .40);
    background: rgba(49, 208, 124, .08);
}

.node.done .dot {
    background: var(--ok);
}

.node.done .status-pill {
    color: rgba(49, 208, 124, .95);
    border-color: rgba(49, 208, 124, .35);
    background: rgba(49, 208, 124, .10);
}

.node.running {
    border-color: rgba(245, 200, 75, .45);
    background: rgba(245, 200, 75, .08);
}

.node.running .dot {
    background: var(--run);
    box-shadow: 0 0 0 10px rgba(245, 200, 75, 0);
    animation: pulse 1.2s infinite;
}

.node.running .status-pill {
    color: rgba(245, 200, 75, .95);
    border-color: rgba(245, 200, 75, .35);
    background: rgba(245, 200, 75, .10);
}

.node.error {
    border-color: rgba(255, 85, 102, .55);
    background: rgba(255, 85, 102, .10);
}

.node.error .dot {
    background: var(--bad);
}

.node.error .status-pill {
    color: rgba(255, 85, 102, .95);
    border-color: rgba(255, 85, 102, .35);
    background: rgba(255, 85, 102, .12);
}

/* Runtime card */
.runtime-list {
    padding: 12px;
    display: flex;
    flex-direction: column;
    gap: 10px;
    overflow: auto;
    height: calc(100% - 46px);
}

.rt {
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 10px;
    background: rgba(0, 0, 0, .14);
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: 10px;
}

.rt strong {
    font-size: 12px;
}

.rt small {
    color: var(--muted2);
    display: block;
    margin-top: 4px;
    font-size: 11px;
}

.rt .state {
    font-size: 11px;
    padding: 3px 8px;
    border-radius: 999px;
    border: 1px solid var(--border);
    color: var(--muted);
    background: rgba(255, 255, 255, .04);
    white-space: nowrap;
}

.state.idle {
    border-color: rgba(255, 255, 255, .16);
    color: rgba(255, 255, 255, .65);
}

.state.busy {
    border-color: rgba(245, 200, 75, .35);
    color: rgba(245, 200, 75, .95);
    background: rgba(245, 200, 75, .10);
}

.state.error {
    border-color: rgba(255, 85, 102, .35);
    color: rgba(255, 85, 102, .95);
    background: rgba(255, 85, 102, .10);
}

.state.offline {
    border-color: rgba(255, 85, 102, .35);
    color: rgba(255, 85, 102, .95);
    background: rgba(0, 0, 0, .18);
}

/* Drawer */
.drawer-backdrop {
    position: absolute;
    inset: 0;
    background: rgba(0, 0, 0, .45);
    opacity: 0;
    pointer-events: none;
    transition: opacity .18s ease;
    z-index: 50;
}

.drawer {
    position: absolute;
    top: 0;
    right: 0;
    height: 100%;
    width: min(520px, 92vw);
    background: rgba(15, 18, 40, .92);
    border-left: 1px solid rgba(255, 255, 255, .12);
    box-shadow: -20px 0 50px rgba(0, 0, 0, .35);
    transform: translateX(105%);
    transition: transform .22s ease;
    display: flex;
    flex-direction: column;
    backdrop-filter: blur(10px);
    z-index: 51;
}

.drawer.open {
    transform: translateX(0%);
}

.drawer-backdrop.open {
    opacity: 1;
    pointer-events: auto;
}

.drawer-h {
    padding: 14px 14px 10px;
    border-bottom: 1px solid rgba(255, 255, 255, .12);
    display: flex;
    justify-content: space-between;
    gap: 10px;
    align-items: flex-start;
}

.drawer-h strong {
    font-size: 13px;
}

.drawer-h .meta {
    color: var(--muted);
    font-size: 12px;
    margin-top: 2px;
}

.x {
    border: 1px solid rgba(255, 255, 255, .12);
    background: rgba(0, 0, 0, .18);
    color: var(--text);
    width: 34px;
    height: 34px;
    border-radius: 12px;
    cursor: pointer;
    transition: transform .12s ease, background .12s ease;
    display: grid;
    place-items: center;
    flex: 0 0 auto;
}

.x:hover {
    transform: translateY(-1px);
    background: rgba(0, 0, 0, .26);
}

.drawer-controls {
    padding: 10px 14px;
    border-bottom: 1px solid rgba(255, 255, 255, .12);
    display: flex;
    gap: 10px;
    align-items: center;
    flex-wrap: wrap;
}

.seg {
    display: flex;
    border: 1px solid rgba(255, 255, 255, .14);
    border-radius: 999px;
    overflow: hidden;
}

.seg button {
    border: 0;
    background: transparent;
    color: rgba(255, 255, 255, .70);
    padding: 8px 10px;
    cursor: pointer;
}

.seg button.active {
    background: rgba(93, 120, 255, .16);
    color: rgba(255, 255, 255, .92);
}

.events {
    padding: 12px 14px 16px;
    overflow: auto;
}

.ev {
    border-left: 2px solid rgba(255, 255, 255, .14);
    padding-left: 10px;
    margin-left: 6px;
    padding-bottom: 12px;
    position: relative;
}

.ev:before {
    content: "";
    position: absolute;
    left: -6px;
    top: 4px;
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background: rgba(255, 255, 255, .18);
    border: 1px solid rgba(255, 255, 255, .18);
}

.ev.ok:before {
    background: rgba(49, 208, 124, .9);
    border-color: rgba(49, 208, 124, .45);
}

.ev.warn:before {
    background: rgba(245, 200, 75, .95);
    border-color: rgba(245, 200, 75, .45);
}

.ev.err:before {
    background: rgba(255, 85, 102, .95);
    border-color: rgba(255, 85, 102, .45);
}

.ev .t {
    color: rgba(255, 255, 255, .8);
    font-size: 12px;
    display: flex;
    gap: 8px;
    align-items: center;
}

.ev .t code {
    font-size: 11px;
    color: rgba(255, 255, 255, .7);
    background: rgba(0, 0, 0, .18);
    border: 1px solid rgba(255, 255, 255, .12);
    padding: 2px 6px;
    border-radius: 999px;
}

.ev .d {
    margin-top: 6px;
    color: rgba(255, 255, 255, .88);
    font-size: 13px;
}

.ev .m {
    margin-top: 4px;
    color: rgba(255, 255, 255, .55);
    font-size: 12px;
}

@media (max-width: 980px) {
    .app {
        grid-template-columns: 1fr;
    }

    .sidebar {
        height: 40vh;
    }

    .content {
        grid-template-columns: 1fr;
    }

    .runtime-card {
        height: 260px;
    }
}
```

### dashboard/frontend/src/main.tsx

```typescript
import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.tsx'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')!).render(
    <React.StrictMode>
        <App />
    </React.StrictMode>,
)
```

### dashboard/frontend/src/pages/AdminDashboard.tsx

```typescript
import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import { 
  Users, 
  UsersRound, 
  FolderKanban, 
  Shield, 
  Settings, 
  Key, 
  Brain, 
  GitBranch,
  BarChart3,
  FileText,
  AlertCircle,
  CheckCircle,
  Clock,
  TrendingUp
} from 'lucide-react';

interface SystemStats {
  totalUsers: number;
  totalTeams: number;
  totalProjects: number;
  activeSessions: number;
  pendingTasks: number;
  systemHealth: 'healthy' | 'warning' | 'critical';
}

const AdminDashboard: React.FC = () => {
  const [stats, setStats] = useState<SystemStats>({
    totalUsers: 0,
    totalTeams: 0,
    totalProjects: 0,
    activeSessions: 0,
    pendingTasks: 0,
    systemHealth: 'healthy'
  });
  const [loading, setLoading] = useState(true);
  const [recentActivity, setRecentActivity] = useState<any[]>([]);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      // Fetch system stats
      const [usersRes, teamsRes, projectsRes] = await Promise.all([
        axios.get('/api/auth/users'),
        axios.get('/api/teams'),
        axios.get('/api/projects')
      ]);

      setStats({
        totalUsers: usersRes.data.length || 0,
        totalTeams: teamsRes.data.length || 0,
        totalProjects: projectsRes.data.length || 0,
        activeSessions: 12, // Mock data
        pendingTasks: 5, // Mock data
        systemHealth: 'healthy'
      });

      // Fetch recent activity (mock for now)
      setRecentActivity([
        { id: 1, user: 'admin@example.com', action: 'Created new team', timestamp: '2024-01-19 10:30', type: 'create' },
        { id: 2, user: 'teamlead@example.com', action: 'Added user to project', timestamp: '2024-01-19 09:45', type: 'update' },
        { id: 3, user: 'system', action: 'System backup completed', timestamp: '2024-01-19 08:15', type: 'system' },
        { id: 4, user: 'admin@example.com', action: 'Updated LLM configuration', timestamp: '2024-01-19 07:30', type: 'update' },
        { id: 5, user: 'dev@example.com', action: 'Created new repository', timestamp: '2024-01-18 16:20', type: 'create' },
      ]);
    } catch (error) {
      console.error('Failed to fetch dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  const quickActions = [
    { icon: <Users size={20} />, label: 'Add User', path: '/admin/users/new', color: 'blue' },
    { icon: <UsersRound size={20} />, label: 'Create Team', path: '/admin/teams/new', color: 'green' },
    { icon: <FolderKanban size={20} />, label: 'New Project', path: '/admin/projects/new', color: 'purple' },
    { icon: <Brain size={20} />, label: 'LLM Config', path: '/admin/llm-configs/new', color: 'orange' },
    { icon: <GitBranch size={20} />, label: 'Add Repo', path: '/admin/repositories/new', color: 'red' },
    { icon: <Settings size={20} />, label: 'Integration', path: '/admin/integrations/new', color: 'teal' },
  ];

  const systemHealthItems = [
    { label: 'Authentication Service', status: 'healthy', lastCheck: '2 min ago' },
    { label: 'Database', status: 'healthy', lastCheck: '1 min ago' },
    { label: 'LLM Providers', status: 'warning', lastCheck: '5 min ago' },
    { label: 'VCS Integrations', status: 'healthy', lastCheck: '3 min ago' },
    { label: 'API Gateway', status: 'healthy', lastCheck: '1 min ago' },
  ];

  if (loading) {
    return (
      <div className="admin-dashboard loading">
        <div className="loading-spinner"></div>
        <p>Loading dashboard...</p>
      </div>
    );
  }

  return (
    <div className="admin-dashboard">
      <div className="dashboard-header">
        <h1>System Overview</h1>
        <p className="subtitle">Monitor and manage your multi-agent system</p>
      </div>

      {/* Stats Grid */}
      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-icon users">
            <Users size={24} />
          </div>
          <div className="stat-content">
            <div className="stat-value">{stats.totalUsers}</div>
            <div className="stat-label">Total Users</div>
          </div>
          <Link to="/admin/users" className="stat-link">View all →</Link>
        </div>

        <div className="stat-card">
          <div className="stat-icon teams">
            <UsersRound size={24} />
          </div>
          <div className="stat-content">
            <div className="stat-value">{stats.totalTeams}</div>
            <div className="stat-label">Teams</div>
          </div>
          <Link to="/admin/teams" className="stat-link">Manage →</Link>
        </div>

        <div className="stat-card">
          <div className="stat-icon projects">
            <FolderKanban size={24} />
          </div>
          <div className="stat-content">
            <div className="stat-value">{stats.totalProjects}</div>
            <div className="stat-label">Active Projects</div>
          </div>
          <Link to="/admin/projects" className="stat-link">Browse →</Link>
        </div>

        <div className="stat-card">
          <div className="stat-icon monitoring">
            <BarChart3 size={24} />
          </div>
          <div className="stat-content">
            <div className="stat-value">{stats.activeSessions}</div>
            <div className="stat-label">Active Sessions</div>
          </div>
          <Link to="/admin/monitoring" className="stat-link">Monitor →</Link>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="section">
        <div className="section-header">
          <h2>Quick Actions</h2>
          <p>Frequently used administrative tasks</p>
        </div>
        <div className="quick-actions-grid">
          {quickActions.map((action, index) => (
            <Link key={index} to={action.path} className="quick-action-card">
              <div className={`action-icon ${action.color}`}>
                {action.icon}
              </div>
              <div className="action-label">{action.label}</div>
            </Link>
          ))}
        </div>
      </div>

      <div className="two-column-grid">
        {/* Recent Activity */}
        <div className="section">
          <div className="section-header">
            <h2>Recent Activity</h2>
            <Link to="/admin/audit" className="view-all">View Audit Log →</Link>
          </div>
          <div className="activity-list">
            {recentActivity.map((activity) => (
              <div key={activity.id} className="activity-item">
                <div className="activity-icon">
                  {activity.type === 'create' && <CheckCircle size={16} />}
                  {activity.type === 'update' && <Clock size={16} />}
                  {activity.type === 'system' && <Settings size={16} />}
                </div>
                <div className="activity-content">
                  <div className="activity-action">{activity.action}</div>
                  <div className="activity-meta">
                    <span className="activity-user">{activity.user}</span>
                    <span className="activity-time">{activity.timestamp}</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* System Health */}
        <div className="section">
          <div className="section-header">
            <h2>System Health</h2>
            <div className={`health-status ${stats.systemHealth}`}>
              {stats.systemHealth === 'healthy' && 'All Systems Operational'}
              {stats.systemHealth === 'warning' && 'Minor Issues Detected'}
              {stats.systemHealth === 'critical' && 'Critical Issues'}
            </div>
          </div>
          <div className="health-list">
            {systemHealthItems.map((item, index) => (
              <div key={index} className="health-item">
                <div className="health-label">{item.label}</div>
                <div className="health-status-indicator">
                  <span className={`status-dot ${item.status}`}></span>
                  <span className="status-text">{item.status}</span>
                  <span className="last-check">{item.lastCheck}</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* System Alerts */}
      <div className="section alert-section">
        <div className="section-header">
          <h2>
            <AlertCircle size={20} />
            System Alerts
          </h2>
        </div>
        <div className="alert-list">
          <div className="alert-item warning">
            <div className="alert-icon">⚠️</div>
            <div className="alert-content">
              <div className="alert-title">LLM Provider Rate Limit</div>
              <div className="alert-description">
                OpenAI API approaching rate limit. Consider adding fallback providers.
              </div>
            </div>
            <button className="btn btn-sm">Configure</button>
          </div>
          <div className="alert-item info">
            <div className="alert-icon">ℹ️</div>
            <div className="alert-content">
              <div className="alert-title">Database Backup</div>
              <div className="alert-description">
                Scheduled backup completed successfully. 2.4GB of data backed up.
              </div>
            </div>
            <button className="btn btn-sm">View Logs</button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AdminDashboard;
```

### dashboard/frontend/src/pages/AdminIntegrations.tsx

```typescript
import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import AdminLayout from '../components/AdminLayout';

interface Integration {
  id: string;
  type: 'jira' | 'telegram' | 'webhook';
  name: string;
  config: Record<string, any>;
  team_id?: string;
  project_id?: string;
  enabled: boolean;
  created_at: string;
  updated_at: string;
}

interface IntegrationFormData {
  type: 'jira' | 'telegram' | 'webhook';
  name: string;
  config: Record<string, any>;
  team_id?: string;
  project_id?: string;
  enabled: boolean;
}

export default function AdminIntegrations() {
  const navigate = useNavigate();
  const [integrations, setIntegrations] = useState<Integration[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState<IntegrationFormData>({
    type: 'telegram',
    name: '',
    config: {},
    enabled: true
  });
  const [testing, setTesting] = useState(false);
  const [testResult, setTestResult] = useState<{ success: boolean; message: string } | null>(null);

  useEffect(() => {
    fetchIntegrations();
  }, []);

  const fetchIntegrations = async () => {
    try {
      setLoading(true);
      const response = await axios.get('/api/integrations');
      setIntegrations(response.data);
      setError(null);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to fetch integrations');
      console.error('Error fetching integrations:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
    const { name, value, type } = e.target;
    
    if (name.startsWith('config.')) {
      const configKey = name.replace('config.', '');
      setFormData(prev => ({
        ...prev,
        config: {
          ...prev.config,
          [configKey]: type === 'checkbox' ? (e.target as HTMLInputElement).checked : value
        }
      }));
    } else {
      setFormData(prev => ({
        ...prev,
        [name]: type === 'checkbox' ? (e.target as HTMLInputElement).checked : value
      }));
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await axios.post('/api/integrations', formData);
      setShowForm(false);
      setFormData({
        type: 'telegram',
        name: '',
        config: {},
        enabled: true
      });
      fetchIntegrations();
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to create integration');
    }
  };

  const handleTestTelegram = async () => {
    if (formData.type !== 'telegram' || !formData.config.bot_token || !formData.config.chat_id) {
      setTestResult({ success: false, message: 'Please fill in bot token and chat ID' });
      return;
    }

    setTesting(true);
    setTestResult(null);

    try {
      const response = await axios.post('/api/integrations/telegram/test', {
        bot_token: formData.config.bot_token,
        chat_id: formData.config.chat_id,
        message: 'Test notification from Orchestrator Bot Admin Panel'
      });

      setTestResult({
        success: response.data.success,
        message: response.data.message
      });
    } catch (err: any) {
      setTestResult({
        success: false,
        message: err.response?.data?.detail || 'Test failed'
      });
    } finally {
      setTesting(false);
    }
  };

  const toggleIntegration = async (id: string, enabled: boolean) => {
    try {
      // TODO: Implement update endpoint
      await axios.put(`/api/integrations/${id}`, { enabled: !enabled });
      fetchIntegrations();
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to update integration');
    }
  };

  const deleteIntegration = async (id: string) => {
    if (!confirm('Are you sure you want to delete this integration?')) return;
    
    try {
      // TODO: Implement delete endpoint
      await axios.delete(`/api/integrations/${id}`);
      fetchIntegrations();
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to delete integration');
    }
  };

  const getIntegrationIcon = (type: string) => {
    switch (type) {
      case 'jira': return '🔗';
      case 'telegram': return '📱';
      case 'webhook': return '🌐';
      default: return '⚙️';
    }
  };

  const getIntegrationConfigFields = () => {
    switch (formData.type) {
      case 'jira':
        return (
          <>
            <div className="form-group">
              <label>Base URL</label>
              <input
                type="url"
                name="config.base_url"
                value={formData.config.base_url || ''}
                onChange={handleInputChange}
                placeholder="https://company.atlassian.net"
                required
              />
            </div>
            <div className="form-group">
              <label>API Token</label>
              <input
                type="password"
                name="config.api_token"
                value={formData.config.api_token || ''}
                onChange={handleInputChange}
                placeholder="Your Jira API token"
                required
              />
            </div>
            <div className="form-group">
              <label>Username</label>
              <input
                type="text"
                name="config.username"
                value={formData.config.username || ''}
                onChange={handleInputChange}
                placeholder="email@example.com"
                required
              />
            </div>
            <div className="form-group">
              <label>Project Key</label>
              <input
                type="text"
                name="config.project_key"
                value={formData.config.project_key || ''}
                onChange={handleInputChange}
                placeholder="PROJ"
                required
              />
            </div>
          </>
        );
      
      case 'telegram':
        return (
          <>
            <div className="form-group">
              <label>Bot Token</label>
              <input
                type="password"
                name="config.bot_token"
                value={formData.config.bot_token || ''}
                onChange={handleInputChange}
                placeholder="1234567890:ABCdefGHIjklMNOpqrsTUVwxyz"
                required
              />
              <small className="text-muted">
                Get token from @BotFather on Telegram
              </small>
            </div>
            <div className="form-group">
              <label>Chat ID</label>
              <input
                type="text"
                name="config.chat_id"
                value={formData.config.chat_id || ''}
                onChange={handleInputChange}
                placeholder="-1001234567890 or user ID"
                required
              />
              <small className="text-muted">
                For channels: -100 + channel ID, for groups: group ID, for users: user ID
              </small>
            </div>
            <div className="form-group">
              <label>Thread ID (optional)</label>
              <input
                type="text"
                name="config.thread_id"
                value={formData.config.thread_id || ''}
                onChange={handleInputChange}
                placeholder="For forum topics"
              />
            </div>
            <div className="form-group">
              <label>Parse Mode</label>
              <select
                name="config.parse_mode"
                value={formData.config.parse_mode || 'HTML'}
                onChange={handleInputChange}
              >
                <option value="HTML">HTML</option>
                <option value="Markdown">Markdown</option>
              </select>
            </div>
            <div className="form-group">
              <button
                type="button"
                onClick={handleTestTelegram}
                disabled={testing || !formData.config.bot_token || !formData.config.chat_id}
                className="btn btn-secondary"
              >
                {testing ? 'Testing...' : 'Test Connection'}
              </button>
              {testResult && (
                <div className={`test-result ${testResult.success ? 'success' : 'error'}`}>
                  {testResult.message}
                </div>
              )}
            </div>
          </>
        );
      
      case 'webhook':
        return (
          <>
            <div className="form-group">
              <label>Webhook URL</label>
              <input
                type="url"
                name="config.url"
                value={formData.config.url || ''}
                onChange={handleInputChange}
                placeholder="https://example.com/webhook"
                required
              />
            </div>
            <div className="form-group">
              <label>Secret Token (optional)</label>
              <input
                type="password"
                name="config.secret"
                value={formData.config.secret || ''}
                onChange={handleInputChange}
                placeholder="Secret for verifying webhook requests"
              />
            </div>
            <div className="form-group">
              <label>Events</label>
              <div className="checkbox-group">
                <label>
                  <input
                    type="checkbox"
                    name="config.events.plan_ready"
                    checked={formData.config.events?.plan_ready || false}
                    onChange={handleInputChange}
                  />
                  Plan Ready
                </label>
                <label>
                  <input
                    type="checkbox"
                    name="config.events.plan_approved"
                    checked={formData.config.events?.plan_approved || false}
                    onChange={handleInputChange}
                  />
                  Plan Approved
                </label>
                <label>
                  <input
                    type="checkbox"
                    name="config.events.task_done"
                    checked={formData.config.events?.task_done || false}
                    onChange={handleInputChange}
                  />
                  Task Done
                </label>
                <label>
                  <input
                    type="checkbox"
                    name="config.events.merge_done"
                    checked={formData.config.events?.merge_done || false}
                    onChange={handleInputChange}
                  />
                  Merge Done
                </label>
              </div>
            </div>
          </>
        );
      
      default:
        return null;
    }
  };

  return (
    <AdminLayout>
      <div className="admin-page">
        <div className="page-header">
          <h1>Integrations</h1>
          <p>Configure external service integrations for notifications and data sync</p>
          <button
            className="btn btn-primary"
            onClick={() => setShowForm(true)}
          >
            + Add Integration
          </button>
        </div>

        {error && (
          <div className="alert alert-error">
            {error}
            <button onClick={() => setError(null)}>×</button>
          </div>
        )}

        {showForm && (
          <div className="modal-overlay">
            <div className="modal">
              <div className="modal-header">
                <h2>Add New Integration</h2>
                <button onClick={() => setShowForm(false)}>×</button>
              </div>
              <form onSubmit={handleSubmit}>
                <div className="modal-body">
                  <div className="form-group">
                    <label>Integration Type</label>
                    <select
                      name="type"
                      value={formData.type}
                      onChange={handleInputChange}
                      required
                    >
                      <option value="telegram">Telegram Bot</option>
                      <option value="jira">Jira</option>
                      <option value="webhook">Webhook</option>
                    </select>
                  </div>

                  <div className="form-group">
                    <label>Name</label>
                    <input
                      type="text"
                      name="name"
                      value={formData.name}
                      onChange={handleInputChange}
                      placeholder="e.g., Production Telegram Notifications"
                      required
                    />
                  </div>

                  {getIntegrationConfigFields()}

                  <div className="form-group">
                    <label>
                      <input
                        type="checkbox"
                        name="enabled"
                        checked={formData.enabled}
                        onChange={handleInputChange}
                      />
                      Enabled
                    </label>
                  </div>
                </div>
                <div className="modal-footer">
                  <button
                    type="button"
                    className="btn btn-secondary"
                    onClick={() => setShowForm(false)}
                  >
                    Cancel
                  </button>
                  <button type="submit" className="btn btn-primary">
                    Create Integration
                  </button>
                </div>
              </form>
            </div>
          </div>
        )}

        {loading ? (
          <div className="loading">Loading integrations...</div>
        ) : integrations.length === 0 ? (
          <div className="empty-state">
            <div className="empty-icon">🔗</div>
            <h3>No integrations configured</h3>
            <p>Add your first integration to enable notifications and external service connections.</p>
            <button
              className="btn btn-primary"
              onClick={() => setShowForm(true)}
            >
              Add Integration
            </button>
          </div>
        ) : (
          <div className="integrations-grid">
            {integrations.map(integration => (
              <div key={integration.id} className="integration-card">
                <div className="integration-header">
                  <div className="integration-icon">
                    {getIntegrationIcon(integration.type)}
                  </div>
                  <div className="integration-info">
                    <h3>{integration.name}</h3>
                    <div className="integration-meta">
                      <span className={`integration-type ${integration.type}`}>
                        {integration.type.toUpperCase()}
                      </span>
                      <span className={`integration-status ${integration.enabled ? 'enabled' : 'disabled'}`}>
                        {integration.enabled ? 'Enabled' : 'Disabled'}
                      </span>
                      {integration.team_id && (
                        <span className="integration-scope">Team</span>
                      )}
                      {integration.project_id && (
                        <span className="integration-scope">Project</span>
                      )}
                    </div>
                  </div>
                  <div className="integration-actions">
                    <button
                      className={`btn btn-sm ${integration.enabled ? 'btn-warning' : 'btn-success'}`}
                      onClick={() => toggleIntegration(integration.id, integration.enabled)}
                    >
                      {integration.enabled ? 'Disable' : 'Enable'}
                    </button>
                    <button
                      className="btn btn-sm btn-danger"
                      onClick={() => deleteIntegration(integration.id)}
                    >
                      Delete
                    </button>
                  </div>
                </div>
                
                <div className="integration-details">
                  <div className="detail-row">
                    <span className="detail-label">Created:</span>
                    <span className="detail-value">
                      {new Date(integration.created_at).toLocaleDateString()}
                    </span>
                  </div>
                  <div className="detail-row">
                    <span className="detail-label">Last Updated:</span>
                    <span className="detail-value">
                      {new Date(integration.updated_at).toLocaleDateString()}
                    </span>
                  </div>
                  
                  {integration.type === 'jira' && integration.config.base_url && (
                    <div className="detail-row">
                      <span className="detail-label">Jira URL:</span>
                      <span className="detail-value">
                        <a href={integration.config.base_url} target="_blank" rel="noopener noreferrer">
                          {integration.config.base_url}
                        </a>
                      </span>
                    </div>
                  )}
                  
                  {integration.type === 'telegram' && integration.config.chat_id && (
                    <div className="detail-row">
                      <span className="detail-label">Chat ID:</span>
                      <span className="detail-value">{integration.config.chat_id}</span>
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </AdminLayout>
  );
}
```

### dashboard/frontend/src/pages/AdminLLMConfigs.tsx

```typescript
import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import { 
  Brain, 
  Plus, 
  Search, 
  Filter, 
  Edit, 
  Trash2, 
  TestTube,
  CheckCircle,
  XCircle,
  Settings,
  Globe,
  Shield,
  Cpu
} from 'lucide-react';

interface LLMConfig {
  id: string;
  provider_type: string;
  model: string;
  api_key?: string;
  base_url?: string;
  timeout: number;
  max_retries: number;
  temperature: number;
  max_tokens?: number;
  extra_params?: Record<string, any>;
  team_id?: string;
  project_id?: string;
  is_default: boolean;
  created_at: string;
  updated_at: string;
  provider_id?: string;
}

const AdminLLMConfigs: React.FC = () => {
  const [configs, setConfigs] = useState<LLMConfig[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterScope, setFilterScope] = useState<'all' | 'global' | 'team' | 'project'>('all');
  const [testingConfig, setTestingConfig] = useState<string | null>(null);
  const [testResult, setTestResult] = useState<{success: boolean; message: string} | null>(null);

  useEffect(() => {
    fetchConfigs();
  }, []);

  const fetchConfigs = async () => {
    try {
      const response = await axios.get('/api/llm-configs');
      setConfigs(response.data);
    } catch (error) {
      console.error('Failed to fetch LLM configurations:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSearchTerm(e.target.value);
  };

  const handleFilterChange = (scope: 'all' | 'global' | 'team' | 'project') => {
    setFilterScope(scope);
  };

  const handleTestConfig = async (configId: string, providerId?: string) => {
    if (!providerId) {
      setTestResult({ success: false, message: 'No provider ID available' });
      return;
    }

    setTestingConfig(configId);
    setTestResult(null);

    try {
      const response = await axios.post('/api/llm-providers/test', {
        provider_id: providerId,
        test_message: 'Hello, are you working?'
      });
      
      setTestResult({ 
        success: true, 
        message: `Test successful: ${response.data.result || 'Provider responded correctly'}`
      });
    } catch (error: any) {
      setTestResult({ 
        success: false, 
        message: `Test failed: ${error.response?.data?.detail || error.message}`
      });
    } finally {
      setTestingConfig(null);
    }
  };

  const handleDeleteConfig = async (configId: string) => {
    if (!confirm('Are you sure you want to delete this LLM configuration?')) {
      return;
    }
    
    try {
      await axios.delete(`/api/llm-configs/${configId}`);
      fetchConfigs(); // Refresh list
    } catch (error) {
      console.error('Failed to delete configuration:', error);
      alert('Failed to delete configuration');
    }
  };

  const handleSetDefault = async (configId: string) => {
    try {
      await axios.put(`/api/llm-configs/${configId}`, { is_default: true });
      fetchConfigs(); // Refresh list
    } catch (error) {
      console.error('Failed to set default configuration:', error);
      alert('Failed to set default configuration');
    }
  };

  const filteredConfigs = configs.filter(config => {
    const matchesSearch = 
      config.provider_type.toLowerCase().includes(searchTerm.toLowerCase()) ||
      config.model.toLowerCase().includes(searchTerm.toLowerCase());
    
    const matchesFilter = 
      filterScope === 'all' ||
      (filterScope === 'global' && !config.team_id && !config.project_id) ||
      (filterScope === 'team' && config.team_id) ||
      (filterScope === 'project' && config.project_id);
    
    return matchesSearch && matchesFilter;
  });

  const getProviderIcon = (providerType: string) => {
    switch (providerType.toLowerCase()) {
      case 'openai':
        return <Cpu size={20} />;
      case 'anthropic':
        return <Brain size={20} />;
      case 'google':
        return <Globe size={20} />;
      case 'azure':
        return <Settings size={20} />;
      default:
        return <Brain size={20} />;
    }
  };

  const getScopeBadge = (config: LLMConfig) => {
    if (config.project_id) return { label: 'Project', color: 'purple' };
    if (config.team_id) return { label: 'Team', color: 'blue' };
    return { label: 'Global', color: 'green' };
  };

  if (loading) {
    return (
      <div className="admin-llm-configs loading">
        <div className="loading-spinner"></div>
        <p>Loading LLM configurations...</p>
      </div>
    );
  }

  return (
    <div className="admin-llm-configs">
      <div className="page-header">
        <div className="header-content">
          <h1>
            <Brain size={24} />
            LLM Configurations
          </h1>
          <p>Manage AI model providers and settings</p>
        </div>
        <div className="header-actions">
          <Link to="/admin/llm-configs/new" className="btn btn-primary">
            <Plus size={18} />
            Add Configuration
          </Link>
        </div>
      </div>

      {/* Test Result Alert */}
      {testResult && (
        <div className={`alert ${testResult.success ? 'alert-success' : 'alert-error'}`}>
          <div className="alert-content">
            {testResult.success ? <CheckCircle size={20} /> : <XCircle size={20} />}
            <span>{testResult.message}</span>
          </div>
          <button 
            className="btn btn-sm" 
            onClick={() => setTestResult(null)}
          >
            Dismiss
          </button>
        </div>
      )}

      {/* Filters and Search */}
      <div className="filters-bar">
        <div className="search-box">
          <Search size={18} />
          <input
            type="text"
            placeholder="Search by provider or model..."
            value={searchTerm}
            onChange={handleSearch}
            className="search-input"
          />
        </div>
        
        <div className="filter-buttons">
          <button
            className={`filter-btn ${filterScope === 'all' ? 'active' : ''}`}
            onClick={() => handleFilterChange('all')}
          >
            All ({configs.length})
          </button>
          <button
            className={`filter-btn ${filterScope === 'global' ? 'active' : ''}`}
            onClick={() => handleFilterChange('global')}
          >
            Global ({configs.filter(c => !c.team_id && !c.project_id).length})
          </button>
          <button
            className={`filter-btn ${filterScope === 'team' ? 'active' : ''}`}
            onClick={() => handleFilterChange('team')}
          >
            Team ({configs.filter(c => c.team_id).length})
          </button>
          <button
            className={`filter-btn ${filterScope === 'project' ? 'active' : ''}`}
            onClick={() => handleFilterChange('project')}
          >
            Project ({configs.filter(c => c.project_id).length})
          </button>
        </div>
      </div>

      {/* Configurations Grid */}
      <div className="configs-grid">
        {filteredConfigs.map((config) => {
          const scopeBadge = getScopeBadge(config);
          
          return (
            <div key={config.id} className="config-card">
              <div className="config-header">
                <div className="config-icon">
                  {getProviderIcon(config.provider_type)}
                </div>
                <div className="config-title">
                  <h3>{config.provider_type}</h3>
                  <div className="config-meta">
                    <span className="model-name">{config.model}</span>
                    <span className={`scope-badge ${scopeBadge.color}`}>
                      {scopeBadge.label}
                    </span>
                    {config.is_default && (
                      <span className="default-badge">
                        <Shield size={12} />
                        Default
                      </span>
                    )}
                  </div>
                </div>
              </div>

              <div className="config-details">
                <div className="detail-row">
                  <span className="detail-label">API Endpoint:</span>
                  <span className="detail-value">
                    {config.base_url || 'Default'}
                  </span>
                </div>
                <div className="detail-row">
                  <span className="detail-label">Timeout:</span>
                  <span className="detail-value">{config.timeout}s</span>
                </div>
                <div className="detail-row">
                  <span className="detail-label">Temperature:</span>
                  <span className="detail-value">{config.temperature}</span>
                </div>
                {config.max_tokens && (
                  <div className="detail-row">
                    <span className="detail-label">Max Tokens:</span>
                    <span className="detail-value">{config.max_tokens}</span>
                  </div>
                )}
                <div className="detail-row">
                  <span className="detail-label">Updated:</span>
                  <span className="detail-value">
                    {new Date(config.updated_at).toLocaleDateString()}
                  </span>
                </div>
              </div>

              <div className="config-actions">
                <button
                  className="btn btn-sm btn-icon"
                  onClick={() => handleTestConfig(config.id, config.provider_id)}
                  disabled={testingConfig === config.id}
                  aria-label="Test configuration"
                >
                  {testingConfig === config.id ? (
                    <div className="spinner"></div>
                  ) : (
                    <TestTube size={16} />
                  )}
                  Test
                </button>
                
                <Link 
                  to={`/admin/llm-configs/${config.id}/edit`}
                  className="btn btn-sm btn-icon"
                  aria-label="Edit configuration"
                >
                  <Edit size={16} />
                  Edit
                </Link>
                
                {!config.is_default && (
                  <button
                    className="btn btn-sm btn-icon"
                    onClick={() => handleSetDefault(config.id)}
                    aria-label="Set as default"
                  >
                    <Shield size={16} />
                    Set Default
                  </button>
                )}
                
                <button
                  className="btn btn-sm btn-icon btn-danger"
                  onClick={() => handleDeleteConfig(config.id)}
                  aria-label="Delete configuration"
                >
                  <Trash2 size={16} />
                  Delete
                </button>
              </div>
            </div>
          );
        })}
      </div>

      {filteredConfigs.length === 0 && (
        <div className="empty-state">
          <Brain size={48} />
          <h3>No LLM configurations found</h3>
          <p>Try adjusting your search or filter criteria</p>
          <Link to="/admin/llm-configs/new" className="btn btn-primary">
            <Plus size={18} />
            Add First Configuration
          </Link>
        </div>
      )}

      {/* Provider Stats */}
      {configs.length > 0 && (
        <div className="stats-section">
          <h3>Provider Statistics</h3>
          <div className="provider-stats">
            {Object.entries(
              configs.reduce((acc, config) => {
                acc[config.provider_type] = (acc[config.provider_type] || 0) + 1;
                return acc;
              }, {} as Record<string, number>)
            ).map(([provider, count]) => (
              <div key={provider} className="provider-stat">
                <div className="provider-icon">
                  {getProviderIcon(provider)}
                </div>
                <div className="stat-info">
                  <div className="stat-count">{count}</div>
                  <div className="stat-label">{provider}</div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default AdminLLMConfigs;
```

### dashboard/frontend/src/pages/AdminRepositories.tsx

```typescript
import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import { 
  GitBranch, 
  Plus, 
  Search, 
  Filter, 
  Edit, 
  Trash2, 
  ExternalLink,
  CheckCircle,
  XCircle,
  GitPullRequest,
  Code,
  Globe,
  Lock,
  RefreshCw
} from 'lucide-react';

interface Repository {
  id: string;
  project_id: string;
  repo_url: string;
  repo_name: string;
  branch: string;
  vcs_type: 'github' | 'gitlab' | 'gitea' | 'bitbucket';
  status: 'connected' | 'disconnected' | 'error';
  last_sync?: string;
  sync_status?: 'success' | 'failed' | 'pending';
  credentials_id?: string;
  created_at: string;
  updated_at: string;
  project_name?: string;
  team_name?: string;
}

interface Project {
  id: string;
  name: string;
  team_id: string;
  team_name?: string;
}

const AdminRepositories: React.FC = () => {
  const [repositories, setRepositories] = useState<Repository[]>([]);
  const [projects, setProjects] = useState<Project[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterProject, setFilterProject] = useState<string>('all');
  const [filterStatus, setFilterStatus] = useState<string>('all');
  const [syncingRepo, setSyncingRepo] = useState<string | null>(null);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [reposRes, projectsRes] = await Promise.all([
        axios.get('/api/project-repos'),
        axios.get('/api/projects')
      ]);

      // Mock data for now - replace with actual API response
      const mockRepos: Repository[] = [
        {
          id: '1',
          project_id: '1',
          repo_url: 'https://github.com/example/backend',
          repo_name: 'backend',
          branch: 'main',
          vcs_type: 'github',
          status: 'connected',
          last_sync: '2024-01-19T10:30:00Z',
          sync_status: 'success',
          created_at: '2024-01-18T14:20:00Z',
          updated_at: '2024-01-19T10:30:00Z',
          project_name: 'E-commerce Platform',
          team_name: 'Development Team'
        },
        {
          id: '2',
          project_id: '1',
          repo_url: 'https://github.com/example/frontend',
          repo_name: 'frontend',
          branch: 'develop',
          vcs_type: 'github',
          status: 'connected',
          last_sync: '2024-01-19T09:45:00Z',
          sync_status: 'success',
          created_at: '2024-01-18T15:30:00Z',
          updated_at: '2024-01-19T09:45:00Z',
          project_name: 'E-commerce Platform',
          team_name: 'Development Team'
        },
        {
          id: '3',
          project_id: '2',
          repo_url: 'https://gitlab.com/company/mobile-app',
          repo_name: 'mobile-app',
          branch: 'main',
          vcs_type: 'gitlab',
          status: 'error',
          last_sync: '2024-01-18T16:15:00Z',
          sync_status: 'failed',
          created_at: '2024-01-17T11:20:00Z',
          updated_at: '2024-01-18T16:15:00Z',
          project_name: 'Mobile Application',
          team_name: 'Mobile Team'
        },
        {
          id: '4',
          project_id: '3',
          repo_url: 'https://gitea.company.com/internal/tools',
          repo_name: 'tools',
          branch: 'master',
          vcs_type: 'gitea',
          status: 'disconnected',
          created_at: '2024-01-16T09:10:00Z',
          updated_at: '2024-01-16T09:10:00Z',
          project_name: 'Internal Tools',
          team_name: 'DevOps'
        }
      ];

      setRepositories(mockRepos);
      setProjects(projectsRes.data || []);
    } catch (error) {
      console.error('Failed to fetch data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSearchTerm(e.target.value);
  };

  const handleSyncRepository = async (repoId: string) => {
    setSyncingRepo(repoId);
    try {
      // TODO: Implement repository sync API
      console.log('Syncing repository:', repoId);
      await new Promise(resolve => setTimeout(resolve, 2000)); // Mock delay
      
      // Update repository status
      setRepositories(prev => prev.map(repo => 
        repo.id === repoId 
          ? { 
              ...repo, 
              status: 'connected', 
              sync_status: 'success',
              last_sync: new Date().toISOString()
            }
          : repo
      ));
    } catch (error) {
      console.error('Failed to sync repository:', error);
    } finally {
      setSyncingRepo(null);
    }
  };

  const handleDeleteRepository = async (repoId: string) => {
    if (!confirm('Are you sure you want to delete this repository?')) {
      return;
    }
    
    try {
      await axios.delete(`/api/project-repos/${repoId}`);
      setRepositories(prev => prev.filter(repo => repo.id !== repoId));
    } catch (error) {
      console.error('Failed to delete repository:', error);
      alert('Failed to delete repository');
    }
  };

  const getVCSIcon = (vcsType: string) => {
    switch (vcsType) {
      case 'github':
        return <Code size={20} />;
      case 'gitlab':
        return <GitPullRequest size={20} />;
      case 'gitea':
        return <GitBranch size={20} />;
      case 'bitbucket':
        return <Code size={20} />;
      default:
        return <GitBranch size={20} />;
    }
  };

  const getStatusBadge = (status: string) => {
    switch (status) {
      case 'connected':
        return { label: 'Connected', color: 'success', icon: <CheckCircle size={14} /> };
      case 'disconnected':
        return { label: 'Disconnected', color: 'warning', icon: <XCircle size={14} /> };
      case 'error':
        return { label: 'Error', color: 'error', icon: <XCircle size={14} /> };
      default:
        return { label: 'Unknown', color: 'neutral', icon: null };
    }
  };

  const getSyncStatusBadge = (syncStatus?: string) => {
    switch (syncStatus) {
      case 'success':
        return { label: 'Synced', color: 'success' };
      case 'failed':
        return { label: 'Sync Failed', color: 'error' };
      case 'pending':
        return { label: 'Syncing', color: 'warning' };
      default:
        return { label: 'Never Synced', color: 'neutral' };
    }
  };

  const filteredRepos = repositories.filter(repo => {
    const matchesSearch = 
      repo.repo_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      repo.repo_url.toLowerCase().includes(searchTerm.toLowerCase()) ||
      (repo.project_name && repo.project_name.toLowerCase().includes(searchTerm.toLowerCase()));
    
    const matchesProject = filterProject === 'all' || repo.project_id === filterProject;
    const matchesStatus = filterStatus === 'all' || repo.status === filterStatus;
    
    return matchesSearch && matchesProject && matchesStatus;
  });

  if (loading) {
    return (
      <div className="admin-repositories loading">
        <div className="loading-spinner"></div>
        <p>Loading repositories...</p>
      </div>
    );
  }

  return (
    <div className="admin-repositories">
      <div className="page-header">
        <div className="header-content">
          <h1>
            <GitBranch size={24} />
            Repository Management
          </h1>
          <p>Manage Git repositories for projects</p>
        </div>
        <div className="header-actions">
          <Link to="/admin/repositories/new" className="btn btn-primary">
            <Plus size={18} />
            Add Repository
          </Link>
        </div>
      </div>

      {/* Filters and Search */}
      <div className="filters-bar">
        <div className="search-box">
          <Search size={18} />
          <input
            type="text"
            placeholder="Search repositories..."
            value={searchTerm}
            onChange={handleSearch}
            className="search-input"
          />
        </div>
        
        <div className="filter-group">
          <select
            value={filterProject}
            onChange={(e) => setFilterProject(e.target.value)}
            className="filter-select"
          >
            <option value="all">All Projects</option>
            {projects.map(project => (
              <option key={project.id} value={project.id}>
                {project.name}
              </option>
            ))}
          </select>

          <select
            value={filterStatus}
            onChange={(e) => setFilterStatus(e.target.value)}
            className="filter-select"
          >
            <option value="all">All Statuses</option>
            <option value="connected">Connected</option>
            <option value="disconnected">Disconnected</option>
            <option value="error">Error</option>
          </select>
        </div>
      </div>

      {/* Repositories Table */}
      <div className="table-container">
        <table className="data-table">
          <thead>
            <tr>
              <th>Repository</th>
              <th>Project & Team</th>
              <th>VCS</th>
              <th>Status</th>
              <th>Last Sync</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {filteredRepos.map((repo) => {
              const statusBadge = getStatusBadge(repo.status);
              const syncBadge = getSyncStatusBadge(repo.sync_status);
              
              return (
                <tr key={repo.id}>
                  <td>
                    <div className="repo-cell">
                      <div className="repo-icon">
                        {getVCSIcon(repo.vcs_type)}
                      </div>
                      <div className="repo-info">
                        <div className="repo-name">
                          <a 
                            href={repo.repo_url} 
                            target="_blank" 
                            rel="noopener noreferrer"
                            className="repo-link"
                          >
                            {repo.repo_name}
                            <ExternalLink size={12} />
                          </a>
                        </div>
                        <div className="repo-url">
                          {repo.repo_url}
                        </div>
                        <div className="repo-branch">
                          <GitBranch size={12} />
                          {repo.branch}
                        </div>
                      </div>
                    </div>
                  </td>
                  <td>
                    <div className="project-cell">
                      <div className="project-name">{repo.project_name}</div>
                      <div className="team-name">
                        <Users size={12} />
                        {repo.team_name}
                      </div>
                    </div>
                  </td>
                  <td>
                    <span className="vcs-badge">
                      {repo.vcs_type.toUpperCase()}
                    </span>
                  </td>
                  <td>
                    <div className="status-cell">
                      <span className={`status-badge ${statusBadge.color}`}>
                        {statusBadge.icon}
                        {statusBadge.label}
                      </span>
                      {repo.sync_status && (
                        <span className={`sync-badge ${syncBadge.color}`}>
                          {syncBadge.label}
                        </span>
                      )}
                    </div>
                  </td>
                  <td>
                    <div className="date-cell">
                      {repo.last_sync ? (
                        <>
                          {new Date(repo.last_sync).toLocaleDateString()}
                          <br />
                          <small>{new Date(repo.last_sync).toLocaleTimeString()}</small>
                        </>
                      ) : (
                        'Never'
                      )}
                    </div>
                  </td>
                  <td>
                    <div className="action-buttons">
                      <button
                        className="btn btn-icon btn-sm"
                        onClick={() => handleSyncRepository(repo.id)}
                        disabled={syncingRepo === repo.id}
                        aria-label="Sync repository"
                      >
                        {syncingRepo === repo.id ? (
                          <div className="spinner"></div>
                        ) : (
                          <RefreshCw size={16} />
                        )}
                      </button>
                      
                      <Link 
                        to={`/admin/repositories/${repo.id}/edit`}
                        className="btn btn-icon btn-sm"
                        aria-label="Edit repository"
                      >
                        <Edit size={16} />
                      </Link>
                      
                      <button
                        className="btn btn-icon btn-sm btn-danger"
                        onClick={() => handleDeleteRepository(repo.id)}
                        aria-label="Delete repository"
                      >
                        <Trash2 size={16} />
                      </button>
                    </div>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>

        {filteredRepos.length === 0 && (
          <div className="empty-state">
            <GitBranch size={48} />
            <h3>No repositories found</h3>
            <p>Try adjusting your search or filter criteria</p>
            <Link to="/admin/repositories/new" className="btn btn-primary">
              <Plus size={18} />
              Add First Repository
            </Link>
          </div>
        )}
      </div>

      {/* Repository Stats */}
      {repositories.length > 0 && (
        <div className="stats-section">
          <h3>Repository Statistics</h3>
          <div className="stats-grid">
            <div className="stat-card">
              <div className="stat-icon">
                <GitBranch size={24} />
              </div>
              <div className="stat-content">
                <div className="stat-value">{repositories.length}</div>
                <div className="stat-label">Total Repositories</div>
              </div>
            </div>
            
            <div className="stat-card">
              <div className="stat-icon success">
                <CheckCircle size={24} />
              </div>
              <div className="stat-content">
                <div className="stat-value">
                  {repositories.filter(r => r.status === 'connected').length}
                </div>
                <div className="stat-label">Connected</div>
              </div>
            </div>
            
            <div className="stat-card">
              <div className="stat-icon warning">
                <XCircle size={24} />
              </div>
              <div className="stat-content">
                <div className="stat-value">
                  {repositories.filter(r => r.status === 'disconnected').length}
                </div>
                <div className="stat-label">Disconnected</div>
              </div>
            </div>
            
            <div className="stat-card">
              <div className="stat-icon">
                <Code size={24} />
              </div>
              <div className="stat-content">
                <div className="stat-value">
                  {new Set(repositories.map(r => r.vcs_type)).size}
                </div>
                <div className="stat-label">VCS Providers</div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* VCS Configuration Info */}
      <div className="info-section">
        <h3>VCS Configuration</h3>
        <div className="info-card">
          <div className="info-content">
            <p>
              Configure VCS providers (GitHub, GitLab, Gitea) in the 
              <Link to="/admin/integrations"> Integrations</Link> section.
            </p>
            <p className="text-sm text-muted">
              Ensure proper access tokens and permissions are set up for repository access.
            </p>
          </div>
          <div className="info-actions">
            <Link to="/admin/integrations" className="btn btn-sm">
              <Settings size={16} />
              Configure VCS
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AdminRepositories;
```

### dashboard/frontend/src/pages/AdminUsers.tsx

```typescript
import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import { 
  Users, 
  Plus, 
  Search, 
  Filter, 
  Edit, 
  Trash2, 
  UserCheck, 
  UserX,
  Mail,
  Calendar,
  Shield
} from 'lucide-react';

interface User {
  id: string;
  email: string;
  username: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
  teams?: Array<{
    team_id: string;
    team_name: string;
    role_id: string;
    role_name: string;
  }>;
}

const AdminUsers: React.FC = () => {
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterActive, setFilterActive] = useState<'all' | 'active' | 'inactive'>('all');
  const [selectedUsers, setSelectedUsers] = useState<string[]>([]);

  useEffect(() => {
    fetchUsers();
  }, []);

  const fetchUsers = async () => {
    try {
      const response = await axios.get('/api/auth/users');
      setUsers(response.data);
    } catch (error) {
      console.error('Failed to fetch users:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSearchTerm(e.target.value);
  };

  const handleFilterChange = (filter: 'all' | 'active' | 'inactive') => {
    setFilterActive(filter);
  };

  const toggleUserSelection = (userId: string) => {
    setSelectedUsers(prev => 
      prev.includes(userId) 
        ? prev.filter(id => id !== userId)
        : [...prev, userId]
    );
  };

  const toggleSelectAll = () => {
    if (selectedUsers.length === filteredUsers.length) {
      setSelectedUsers([]);
    } else {
      setSelectedUsers(filteredUsers.map(user => user.id));
    }
  };

  const handleActivateUsers = async (userIds: string[], activate: boolean) => {
    try {
      // TODO: Implement bulk activation/deactivation
      console.log(`${activate ? 'Activating' : 'Deactivating'} users:`, userIds);
      await Promise.all(
        userIds.map(id => 
          axios.put(`/api/auth/users/${id}`, { is_active: activate })
        )
      );
      fetchUsers(); // Refresh list
      setSelectedUsers([]);
    } catch (error) {
      console.error('Failed to update users:', error);
    }
  };

  const handleDeleteUsers = async (userIds: string[]) => {
    if (!confirm(`Are you sure you want to delete ${userIds.length} user(s)?`)) {
      return;
    }
    
    try {
      // TODO: Implement bulk deletion
      console.log('Deleting users:', userIds);
      await Promise.all(
        userIds.map(id => axios.delete(`/api/auth/users/${id}`))
      );
      fetchUsers(); // Refresh list
      setSelectedUsers([]);
    } catch (error) {
      console.error('Failed to delete users:', error);
    }
  };

  const filteredUsers = users.filter(user => {
    const matchesSearch = 
      user.email.toLowerCase().includes(searchTerm.toLowerCase()) ||
      user.username.toLowerCase().includes(searchTerm.toLowerCase());
    
    const matchesFilter = 
      filterActive === 'all' || 
      (filterActive === 'active' && user.is_active) ||
      (filterActive === 'inactive' && !user.is_active);
    
    return matchesSearch && matchesFilter;
  });

  if (loading) {
    return (
      <div className="admin-users loading">
        <div className="loading-spinner"></div>
        <p>Loading users...</p>
      </div>
    );
  }

  return (
    <div className="admin-users">
      <div className="page-header">
        <div className="header-content">
          <h1>
            <Users size={24} />
            User Management
          </h1>
          <p>Manage system users, permissions, and access</p>
        </div>
        <div className="header-actions">
          <Link to="/admin/users/new" className="btn btn-primary">
            <Plus size={18} />
            Add User
          </Link>
        </div>
      </div>

      {/* Bulk Actions Bar */}
      {selectedUsers.length > 0 && (
        <div className="bulk-actions-bar">
          <div className="bulk-info">
            <span>{selectedUsers.length} user(s) selected</span>
          </div>
          <div className="bulk-buttons">
            <button 
              className="btn btn-sm btn-success"
              onClick={() => handleActivateUsers(selectedUsers, true)}
            >
              <UserCheck size={16} />
              Activate
            </button>
            <button 
              className="btn btn-sm btn-warning"
              onClick={() => handleActivateUsers(selectedUsers, false)}
            >
              <UserX size={16} />
              Deactivate
            </button>
            <button 
              className="btn btn-sm btn-danger"
              onClick={() => handleDeleteUsers(selectedUsers)}
            >
              <Trash2 size={16} />
              Delete
            </button>
          </div>
        </div>
      )}

      {/* Filters and Search */}
      <div className="filters-bar">
        <div className="search-box">
          <Search size={18} />
          <input
            type="text"
            placeholder="Search users by email or username..."
            value={searchTerm}
            onChange={handleSearch}
            className="search-input"
          />
        </div>
        
        <div className="filter-buttons">
          <button
            className={`filter-btn ${filterActive === 'all' ? 'active' : ''}`}
            onClick={() => handleFilterChange('all')}
          >
            All ({users.length})
          </button>
          <button
            className={`filter-btn ${filterActive === 'active' ? 'active' : ''}`}
            onClick={() => handleFilterChange('active')}
          >
            Active ({users.filter(u => u.is_active).length})
          </button>
          <button
            className={`filter-btn ${filterActive === 'inactive' ? 'active' : ''}`}
            onClick={() => handleFilterChange('inactive')}
          >
            Inactive ({users.filter(u => !u.is_active).length})
          </button>
        </div>
      </div>

      {/* Users Table */}
      <div className="table-container">
        <table className="data-table">
          <thead>
            <tr>
              <th className="checkbox-cell">
                <input
                  type="checkbox"
                  checked={selectedUsers.length === filteredUsers.length && filteredUsers.length > 0}
                  onChange={toggleSelectAll}
                  aria-label="Select all users"
                />
              </th>
              <th>User</th>
              <th>Status</th>
              <th>Teams & Roles</th>
              <th>Created</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {filteredUsers.map((user) => (
              <tr key={user.id} className={!user.is_active ? 'inactive' : ''}>
                <td className="checkbox-cell">
                  <input
                    type="checkbox"
                    checked={selectedUsers.includes(user.id)}
                    onChange={() => toggleUserSelection(user.id)}
                    aria-label={`Select user ${user.email}`}
                  />
                </td>
                <td>
                  <div className="user-cell">
                    <div className="user-avatar">
                      {user.username.charAt(0).toUpperCase()}
                    </div>
                    <div className="user-info">
                      <div className="user-name">{user.username}</div>
                      <div className="user-email">
                        <Mail size={14} />
                        {user.email}
                      </div>
                    </div>
                  </div>
                </td>
                <td>
                  <span className={`status-badge ${user.is_active ? 'active' : 'inactive'}`}>
                    {user.is_active ? 'Active' : 'Inactive'}
                  </span>
                </td>
                <td>
                  <div className="teams-roles">
                    {user.teams && user.teams.length > 0 ? (
                      user.teams.map((team, index) => (
                        <div key={index} className="team-role-chip">
                          <span className="team-name">{team.team_name}</span>
                          <span className="role-badge">
                            <Shield size={12} />
                            {team.role_name}
                          </span>
                        </div>
                      ))
                    ) : (
                      <span className="no-teams">No teams assigned</span>
                    )}
                  </div>
                </td>
                <td>
                  <div className="date-cell">
                    <Calendar size={14} />
                    {new Date(user.created_at).toLocaleDateString()}
                  </div>
                </td>
                <td>
                  <div className="action-buttons">
                    <Link 
                      to={`/admin/users/${user.id}/edit`}
                      className="btn btn-icon btn-sm"
                      aria-label="Edit user"
                    >
                      <Edit size={16} />
                    </Link>
                    <button
                      className="btn btn-icon btn-sm"
                      onClick={() => handleActivateUsers([user.id], !user.is_active)}
                      aria-label={user.is_active ? 'Deactivate user' : 'Activate user'}
                    >
                      {user.is_active ? <UserX size={16} /> : <UserCheck size={16} />}
                    </button>
                    <button
                      className="btn btn-icon btn-sm btn-danger"
                      onClick={() => handleDeleteUsers([user.id])}
                      aria-label="Delete user"
                    >
                      <Trash2 size={16} />
                    </button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>

        {filteredUsers.length === 0 && (
          <div className="empty-state">
            <Users size={48} />
            <h3>No users found</h3>
            <p>Try adjusting your search or filter criteria</p>
            <Link to="/admin/users/new" className="btn btn-primary">
              <Plus size={18} />
              Add First User
            </Link>
          </div>
        )}
      </div>

      {/* Pagination */}
      {filteredUsers.length > 0 && (
        <div className="pagination">
          <div className="pagination-info">
            Showing {filteredUsers.length} of {users.length} users
          </div>
          <div className="pagination-controls">
            <button className="btn btn-sm" disabled>
              Previous
            </button>
            <span className="page-numbers">Page 1 of 1</span>
            <button className="btn btn-sm" disabled>
              Next
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default AdminUsers;
```

### dashboard/frontend/src/pages/Login.tsx

```typescript
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { LogIn, Mail, Lock, AlertCircle } from 'lucide-react';

const Login: React.FC = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const response = await axios.post('/api/auth/login', {
        email,
        password
      });

      // Store token
      localStorage.setItem('auth_token', response.data.access_token);
      
      // Redirect to admin panel
      navigate('/admin');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Login failed. Please check your credentials.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-page">
      <div className="login-container">
        <div className="login-header">
          <div className="logo">
            <div className="logo-icon">🤖</div>
            <h1>Orchestrator Bot</h1>
          </div>
          <p className="subtitle">Multi-Agent System Administration</p>
        </div>

        <div className="login-card">
          <div className="card-header">
            <h2>
              <LogIn size={24} />
              Admin Login
            </h2>
            <p>Enter your credentials to access the admin panel</p>
          </div>

          {error && (
            <div className="alert alert-error">
              <AlertCircle size={18} />
              <span>{error}</span>
            </div>
          )}

          <form onSubmit={handleSubmit} className="login-form">
            <div className="form-group">
              <label htmlFor="email">
                <Mail size={18} />
                Email Address
              </label>
              <input
                id="email"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="admin@example.com"
                required
                disabled={loading}
              />
            </div>

            <div className="form-group">
              <label htmlFor="password">
                <Lock size={18} />
                Password
              </label>
              <input
                id="password"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
                required
                disabled={loading}
              />
            </div>

            <div className="form-options">
              <label className="checkbox">
                <input type="checkbox" />
                <span>Remember me</span>
              </label>
              <a href="#" className="forgot-password">
                Forgot password?
              </a>
            </div>

            <button 
              type="submit" 
              className="btn btn-primary btn-block"
              disabled={loading}
            >
              {loading ? (
                <>
                  <div className="spinner"></div>
                  Signing in...
                </>
              ) : (
                <>
                  <LogIn size={18} />
                  Sign In
                </>
              )}
            </button>
          </form>

          <div className="login-footer">
            <p className="demo-credentials">
              <strong>Demo Credentials:</strong><br />
              Email: admin@example.com<br />
              Password: admin123
            </p>
            <p className="text-sm text-muted">
              Need access? Contact your system administrator.
            </p>
          </div>
        </div>

        <div className="login-info">
          <div className="info-card">
            <h3>System Access</h3>
            <ul>
              <li>• Full administrative control</li>
              <li>• User and team management</li>
              <li>• Project configuration</li>
              <li>• LLM provider settings</li>
              <li>• Repository management</li>
              <li>• System monitoring</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Login;
```

### dashboard/frontend/src/pages/ProjectDetails.tsx

```typescript
import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';
import Layout from '../components/Layout';
import ProjectTree from '../components/ProjectTree';

interface Project {
  id: string;
  name: string;
  description: string;
  status: string;
  default_language: string;
  created_at: string;
  updated_at: string;
  cycles_count: number;
  active_cycles_count: number;
}

interface Cycle {
  id: string;
  project_id: string;
  cycle_number: number;
  objective: string;
  objective_lang: string;
  status: string;
  source_type: string;
  source_ref?: string;
  created_at: string;
  updated_at: string;
  epochs_count: number;
  completed_epochs_count: number;
}

interface Epoch {
  id: string;
  cycle_id: string;
  title: string;
  description: string;
  order_index: number;
  status: string;
  created_at: string;
  updated_at: string;
  epics_count: number;
  completed_epics_count: number;
}

interface Epic {
  id: string;
  epoch_id: string;
  title: string;
  description: string;
  order_index: number;
  status: string;
  created_at: string;
  updated_at: string;
  work_items_count: number;
  completed_work_items_count: number;
}

interface WorkItem {
  id: string;
  epic_id: string;
  title: string;
  description: string;
  order_index: number;
  status: string;
  priority: number;
  worker_type: string;
  assignee_role: string;
  depends_on: string[];
  acceptance_criteria: any[];
  labels: string[];
  estimated_effort_minutes?: number;
  repo_id?: string;
  branch_name?: string;
  pr_url?: string;
  commit_sha?: string;
  agent_conversation_id?: string;
  agent_state?: string;
  last_error?: string;
  retry_count: number;
  created_at: string;
  updated_at: string;
}

export default function ProjectDetails() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [project, setProject] = useState<Project | null>(null);
  const [cycles, setCycles] = useState<Cycle[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState('overview');

  useEffect(() => {
    if (id) {
      fetchProjectData();
    }
  }, [id]);

  const fetchProjectData = async () => {
    try {
      setLoading(true);
      
      // Fetch project details
      const projectResponse = await axios.get(`/api/projects/${id}`);
      setProject(projectResponse.data);
      
      // Fetch cycles for this project
      const cyclesResponse = await axios.get(`/api/projects/${id}/cycles`);
      setCycles(cyclesResponse.data);
      
      setError(null);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to fetch project data');
      console.error('Error fetching project data:', err);
    } finally {
      setLoading(false);
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active':
      case 'in_progress':
      case 'completed':
      case 'done': return 'success';
      case 'pending':
      case 'queued': return 'warning';
      case 'failed':
      case 'error': return 'error';
      default: return 'neutral';
    }
  };

  const getStatusText = (status: string) => {
    return status.charAt(0).toUpperCase() + status.slice(1);
  };

  if (loading) {
    return (
      <Layout>
        <div className="page">
          <div className="loading">Loading project details...</div>
        </div>
      </Layout>
    );
  }

  if (error || !project) {
    return (
      <Layout>
        <div className="page">
          <div className="error-state">
            <div className="error-icon">⚠️</div>
            <h3>{error || 'Project not found'}</h3>
            <button
              className="btn btn-primary"
              onClick={() => navigate('/projects')}
            >
              Back to Projects
            </button>
          </div>
        </div>
      </Layout>
    );
  }

  return (
    <Layout>
      <div className="page">
        <div className="page-header">
          <div className="breadcrumbs">
            <button
              className="btn btn-link"
              onClick={() => navigate('/projects')}
            >
              Projects
            </button>
            <span className="separator">/</span>
            <span className="current">{project.name}</span>
          </div>
          <div className="header-main">
            <h1>{project.name}</h1>
            <p className="project-description">{project.description}</p>
            <div className="project-meta">
              <span className={`status-badge ${getStatusColor(project.status)}`}>
                {getStatusText(project.status)}
              </span>
              <span className="meta-item">
                <span className="meta-icon">🔄</span>
                {project.cycles_count} cycles
              </span>
              <span className="meta-item">
                <span className="meta-icon">⚡</span>
                {project.active_cycles_count} active
              </span>
              <span className="meta-item">
                <span className="meta-icon">🌐</span>
                {project.default_language.toUpperCase()}
              </span>
            </div>
          </div>
          <div className="header-actions">
            <button className="btn btn-secondary">Settings</button>
            <button className="btn btn-primary">New Cycle</button>
          </div>
        </div>

        <div className="tabs">
          <button
            className={`tab ${activeTab === 'overview' ? 'active' : ''}`}
            onClick={() => setActiveTab('overview')}
          >
            Overview
          </button>
          <button
            className={`tab ${activeTab === 'tree' ? 'active' : ''}`}
            onClick={() => setActiveTab('tree')}
          >
            Project Tree
          </button>
          <button
            className={`tab ${activeTab === 'cycles' ? 'active' : ''}`}
            onClick={() => setActiveTab('cycles')}
          >
            Cycles ({cycles.length})
          </button>
          <button
            className={`tab ${activeTab === 'settings' ? 'active' : ''}`}
            onClick={() => setActiveTab('settings')}
          >
            Settings
          </button>
        </div>

        {activeTab === 'overview' && (
          <div className="overview">
            <div className="stats-grid">
              <div className="stat-card">
                <div className="stat-value">{cycles.length}</div>
                <div className="stat-label">Development Cycles</div>
                <div className="stat-subtext">
                  {cycles.filter(c => c.status === 'completed').length} completed
                </div>
              </div>
              <div className="stat-card">
                <div className="stat-value">0</div>
                <div className="stat-label">Epochs</div>
                <div className="stat-subtext">0 completed</div>
              </div>
              <div className="stat-card">
                <div className="stat-value">0</div>
                <div className="stat-label">Epics</div>
                <div className="stat-subtext">0 completed</div>
              </div>
              <div className="stat-card">
                <div className="stat-value">0</div>
                <div className="stat-label">Work Items</div>
                <div className="stat-subtext">0 completed</div>
              </div>
            </div>

            <div className="recent-activity">
              <h3>Recent Activity</h3>
              <div className="activity-list">
                {cycles.slice(0, 5).map(cycle => (
                  <div key={cycle.id} className="activity-item">
                    <div className="activity-icon">🔄</div>
                    <div className="activity-content">
                      <div className="activity-title">
                        Cycle #{cycle.cycle_number}: {cycle.objective}
                      </div>
                      <div className="activity-meta">
                        <span className={`status-badge ${getStatusColor(cycle.status)}`}>
                          {getStatusText(cycle.status)}
                        </span>
                        <span className="activity-time">
                          Updated: {new Date(cycle.updated_at).toLocaleDateString()}
                        </span>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {activeTab === 'tree' && (
          <div className="project-tree">
            <div className="tree-header">
              <h3>Project Hierarchy</h3>
              <div className="tree-stats">
                <span>{cycles.length} cycles</span>
                <span>0 epochs</span>
                <span>0 epics</span>
                <span>0 work items</span>
              </div>
            </div>
            <ProjectTree
              projectId={id}
              onNodeSelect={(node) => {
                console.log('Selected node:', node);
                // Handle node selection - could navigate to details page
              }}
              onNodeAction={(action, node) => {
                console.log(`${action} action on node:`, node);
                // Handle actions like add, edit, delete
                if (action === 'add') {
                  // Show modal to add child
                  alert(`Add child to ${node.name}`);
                } else if (action === 'edit') {
                  // Show edit modal
                  alert(`Edit ${node.name}`);
                } else if (action === 'delete') {
                  // Show delete confirmation
                  if (confirm(`Delete ${node.name}?`)) {
                    console.log('Deleting node:', node);
                  }
                }
              }}
              showActions={true}
              expandedByDefault={true}
            />
          </div>
        )}

        {activeTab === 'cycles' && (
          <div className="cycles-list">
            <div className="list-header">
              <h3>Development Cycles</h3>
              <button className="btn btn-primary">New Cycle</button>
            </div>
            <div className="cycles-grid">
              {cycles.map(cycle => (
                <div key={cycle.id} className="cycle-card">
                  <div className="cycle-header">
                    <div className="cycle-icon">🔄</div>
                    <div className="cycle-info">
                      <h4>Cycle #{cycle.cycle_number}</h4>
                      <p className="cycle-objective">{cycle.objective}</p>
                      <div className="cycle-meta">
                        <span className={`status-badge ${getStatusColor(cycle.status)}`}>
                          {getStatusText(cycle.status)}
                        </span>
                        <span className="meta-item">
                          {cycle.epochs_count} epochs
                        </span>
                        <span className="meta-item">
                          {cycle.completed_epochs_count} completed
                        </span>
                      </div>
                    </div>
                  </div>
                  <div className="cycle-footer">
                    <div className="cycle-dates">
                      <div className="date-item">
                        <span className="date-label">Created:</span>
                        <span className="date-value">
                          {new Date(cycle.created_at).toLocaleDateString()}
                        </span>
                      </div>
                      <div className="date-item">
                        <span className="date-label">Updated:</span>
                        <span className="date-value">
                          {new Date(cycle.updated_at).toLocaleDateString()}
                        </span>
                      </div>
                    </div>
                    <div className="cycle-actions">
                      <button
                        className="btn btn-sm"
                        onClick={() => navigate(`/cycles/${cycle.id}`)}
                      >
                        View Details
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {activeTab === 'settings' && (
          <div className="settings">
            <h3>Project Settings</h3>
            <div className="settings-form">
              <div className="form-group">
                <label>Project Name</label>
                <input type="text" value={project.name} readOnly />
              </div>
              <div className="form-group">
                <label>Description</label>
                <textarea value={project.description} readOnly />
              </div>
              <div className="form-group">
                <label>Default Language</label>
                <select value={project.default_language} disabled>
                  <option value="ru">Russian (RU)</option>
                  <option value="en">English (EN)</option>
                </select>
              </div>
              <div className="form-group">
                <label>Status</label>
                <select value={project.status} disabled>
                  <option value="active">Active</option>
                  <option value="inactive">Inactive</option>
                  <option value="archived">Archived</option>
                </select>
              </div>
              <div className="form-actions">
                <button className="btn btn-primary">Save Changes</button>
                <button className="btn btn-secondary">Cancel</button>
              </div>
            </div>
          </div>
        )}
      </div>
    </Layout>
  );
}
```

### dashboard/frontend/src/pages/Projects.tsx

```typescript
import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import Layout from '../components/Layout';
import { useTranslation } from '../i18n/I18nProvider';

interface Project {
  id: string;
  name: string;
  description: string;
  status: string;
  default_language: string;
  created_at: string;
  updated_at: string;
  cycles_count: number;
  active_cycles_count: number;
  team_name?: string;
}

export default function Projects() {
  const navigate = useNavigate();
  const { t } = useTranslation();
  const [projects, setProjects] = useState<Project[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState('all');

  useEffect(() => {
    fetchProjects();
  }, []);

  const fetchProjects = async () => {
    try {
      setLoading(true);
      const response = await axios.get('/api/projects');
      setProjects(response.data);
      setError(null);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to fetch projects');
      console.error('Error fetching projects:', err);
    } finally {
      setLoading(false);
    }
  };

  const filteredProjects = projects.filter(project => {
    const matchesSearch = project.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         project.description.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesStatus = statusFilter === 'all' || project.status === statusFilter;
    return matchesSearch && matchesStatus;
  });

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active': return 'success';
      case 'inactive': return 'warning';
      case 'archived': return 'neutral';
      default: return 'neutral';
    }
  };

  const getStatusText = (status: string) => {
    switch (status) {
      case 'active': return t('status.active');
      case 'inactive': return t('status.inactive');
      case 'archived': return t('status.archived');
      default: return status;
    }
  };

  return (
    <Layout>
      <div className="page">
        <div className="page-header">
          <h1>{t('projects.title')}</h1>
          <p>{t('projects.subtitle')}</p>
          <div className="header-actions">
            <button
              className="btn btn-primary"
              onClick={() => navigate('/projects/new')}
            >
              + {t('projects.new_project')}
            </button>
          </div>
        </div>

        {error && (
          <div className="alert alert-error">
            {error}
            <button onClick={() => setError(null)}>×</button>
          </div>
        )}

        <div className="filters">
          <div className="search-box">
            <input
              type="text"
              placeholder={t('common.search')}
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
            <span className="search-icon">🔍</span>
          </div>
          <div className="filter-group">
            <select
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value)}
            >
              <option value="all">{t('common.all')} {t('common.status')}</option>
              <option value="active">{t('status.active')}</option>
              <option value="inactive">{t('status.inactive')}</option>
              <option value="archived">{t('status.archived')}</option>
            </select>
          </div>
        </div>

        {loading ? (
          <div className="loading">{t('common.loading')}</div>
        ) : filteredProjects.length === 0 ? (
          <div className="empty-state">
            <div className="empty-icon">📁</div>
            <h3>{t('projects.no_projects')}</h3>
            <p>{t('projects.create_first')}</p>
            <button
              className="btn btn-primary"
              onClick={() => navigate('/projects/new')}
            >
              {t('projects.create_project')}
            </button>
          </div>
        ) : (
          <div className="projects-grid">
            {filteredProjects.map(project => (
              <div
                key={project.id}
                className="project-card"
                onClick={() => navigate(`/projects/${project.id}`)}
              >
                <div className="project-header">
                  <div className="project-icon">
                    <span>📋</span>
                  </div>
                  <div className="project-info">
                    <h3>{project.name}</h3>
                    <p className="project-description">{project.description}</p>
                    <div className="project-meta">
                      <span className={`status-badge ${getStatusColor(project.status)}`}>
                        {getStatusText(project.status)}
                      </span>
                      <span className="meta-item">
                        <span className="meta-icon">🔄</span>
                        {project.cycles_count} {t('projects.cycles')}
                      </span>
                      <span className="meta-item">
                        <span className="meta-icon">⚡</span>
                        {project.active_cycles_count} {t('projects.active_cycles')}
                      </span>
                    </div>
                  </div>
                </div>
                
                <div className="project-footer">
                  <div className="project-dates">
                    <div className="date-item">
                      <span className="date-label">{t('common.created')}:</span>
                      <span className="date-value">
                        {new Date(project.created_at).toLocaleDateString()}
                      </span>
                    </div>
                    <div className="date-item">
                      <span className="date-label">{t('common.updated')}:</span>
                      <span className="date-value">
                        {new Date(project.updated_at).toLocaleDateString()}
                      </span>
                    </div>
                  </div>
                  <div className="project-language">
                    <span className="language-badge">
                      {project.default_language.toUpperCase()}
                    </span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </Layout>
  );
}
```

### dashboard/frontend/src/types.ts

```typescript
export interface LogChunk {
    id: number;
    task_id: string;
    content: string;
    timestamp: string;
}

export interface Task {
    id: string;
    stage_id: string;
    name: string;
    status: "PENDING" | "RUNNING" | "COMPLETED" | "FAILED" | "APPROVED" | "REJECTED" | "SUCCESS" | "FAILED_FINAL";
    agent_session_id?: string;
    branch_name?: string;
    agent_state?: string;
}

export interface Stage {
    id: string;
    pipeline_id: string;
    name: string;
    status: "PENDING" | "RUNNING" | "COMPLETED" | "FAILED" | "APPROVED" | "REJECTED" | "SUCCESS" | "FAILED_FINAL";
    start_time?: string;
    end_time?: string;
    tasks: Task[];
}

export interface Pipeline {
    id: string;
    status: "RUNNING" | "SUCCESS" | "FAILED";
    created_at: string;
    repo_url: string;
    objective: string;
    stages?: Stage[]; // Optional if fetched in list view
}
```

## Frontend

### dashboard/frontend/dist/assets/index-DJPa3AgC.css

```css
*,:before,:after{--tw-border-spacing-x: 0;--tw-border-spacing-y: 0;--tw-translate-x: 0;--tw-translate-y: 0;--tw-rotate: 0;--tw-skew-x: 0;--tw-skew-y: 0;--tw-scale-x: 1;--tw-scale-y: 1;--tw-pan-x: ;--tw-pan-y: ;--tw-pinch-zoom: ;--tw-scroll-snap-strictness: proximity;--tw-gradient-from-position: ;--tw-gradient-via-position: ;--tw-gradient-to-position: ;--tw-ordinal: ;--tw-slashed-zero: ;--tw-numeric-figure: ;--tw-numeric-spacing: ;--tw-numeric-fraction: ;--tw-ring-inset: ;--tw-ring-offset-width: 0px;--tw-ring-offset-color: #fff;--tw-ring-color: rgb(59 130 246 / .5);--tw-ring-offset-shadow: 0 0 #0000;--tw-ring-shadow: 0 0 #0000;--tw-shadow: 0 0 #0000;--tw-shadow-colored: 0 0 #0000;--tw-blur: ;--tw-brightness: ;--tw-contrast: ;--tw-grayscale: ;--tw-hue-rotate: ;--tw-invert: ;--tw-saturate: ;--tw-sepia: ;--tw-drop-shadow: ;--tw-backdrop-blur: ;--tw-backdrop-brightness: ;--tw-backdrop-contrast: ;--tw-backdrop-grayscale: ;--tw-backdrop-hue-rotate: ;--tw-backdrop-invert: ;--tw-backdrop-opacity: ;--tw-backdrop-saturate: ;--tw-backdrop-sepia: ;--tw-contain-size: ;--tw-contain-layout: ;--tw-contain-paint: ;--tw-contain-style: }::backdrop{--tw-border-spacing-x: 0;--tw-border-spacing-y: 0;--tw-translate-x: 0;--tw-translate-y: 0;--tw-rotate: 0;--tw-skew-x: 0;--tw-skew-y: 0;--tw-scale-x: 1;--tw-scale-y: 1;--tw-pan-x: ;--tw-pan-y: ;--tw-pinch-zoom: ;--tw-scroll-snap-strictness: proximity;--tw-gradient-from-position: ;--tw-gradient-via-position: ;--tw-gradient-to-position: ;--tw-ordinal: ;--tw-slashed-zero: ;--tw-numeric-figure: ;--tw-numeric-spacing: ;--tw-numeric-fraction: ;--tw-ring-inset: ;--tw-ring-offset-width: 0px;--tw-ring-offset-color: #fff;--tw-ring-color: rgb(59 130 246 / .5);--tw-ring-offset-shadow: 0 0 #0000;--tw-ring-shadow: 0 0 #0000;--tw-shadow: 0 0 #0000;--tw-shadow-colored: 0 0 #0000;--tw-blur: ;--tw-brightness: ;--tw-contrast: ;--tw-grayscale: ;--tw-hue-rotate: ;--tw-invert: ;--tw-saturate: ;--tw-sepia: ;--tw-drop-shadow: ;--tw-backdrop-blur: ;--tw-backdrop-brightness: ;--tw-backdrop-contrast: ;--tw-backdrop-grayscale: ;--tw-backdrop-hue-rotate: ;--tw-backdrop-invert: ;--tw-backdrop-opacity: ;--tw-backdrop-saturate: ;--tw-backdrop-sepia: ;--tw-contain-size: ;--tw-contain-layout: ;--tw-contain-paint: ;--tw-contain-style: }*,:before,:after{box-sizing:border-box;border-width:0;border-style:solid;border-color:#e5e7eb}:before,:after{--tw-content: ""}html,:host{line-height:1.5;-webkit-text-size-adjust:100%;-moz-tab-size:4;-o-tab-size:4;tab-size:4;font-family:Inter,system-ui,sans-serif;font-feature-settings:normal;font-variation-settings:normal;-webkit-tap-highlight-color:transparent}body{margin:0;line-height:inherit}hr{height:0;color:inherit;border-top-width:1px}abbr:where([title]){-webkit-text-decoration:underline dotted;text-decoration:underline dotted}h1,h2,h3,h4,h5,h6{font-size:inherit;font-weight:inherit}a{color:inherit;text-decoration:inherit}b,strong{font-weight:bolder}code,kbd,samp,pre{font-family:JetBrains Mono,monospace;font-feature-settings:normal;font-variation-settings:normal;font-size:1em}small{font-size:80%}sub,sup{font-size:75%;line-height:0;position:relative;vertical-align:baseline}sub{bottom:-.25em}sup{top:-.5em}table{text-indent:0;border-color:inherit;border-collapse:collapse}button,input,optgroup,select,textarea{font-family:inherit;font-feature-settings:inherit;font-variation-settings:inherit;font-size:100%;font-weight:inherit;line-height:inherit;letter-spacing:inherit;color:inherit;margin:0;padding:0}button,select{text-transform:none}button,input:where([type=button]),input:where([type=reset]),input:where([type=submit]){-webkit-appearance:button;background-color:transparent;background-image:none}:-moz-focusring{outline:auto}:-moz-ui-invalid{box-shadow:none}progress{vertical-align:baseline}::-webkit-inner-spin-button,::-webkit-outer-spin-button{height:auto}[type=search]{-webkit-appearance:textfield;outline-offset:-2px}::-webkit-search-decoration{-webkit-appearance:none}::-webkit-file-upload-button{-webkit-appearance:button;font:inherit}summary{display:list-item}blockquote,dl,dd,h1,h2,h3,h4,h5,h6,hr,figure,p,pre{margin:0}fieldset{margin:0;padding:0}legend{padding:0}ol,ul,menu{list-style:none;margin:0;padding:0}dialog{padding:0}textarea{resize:vertical}input::-moz-placeholder,textarea::-moz-placeholder{opacity:1;color:#9ca3af}input::placeholder,textarea::placeholder{opacity:1;color:#9ca3af}button,[role=button]{cursor:pointer}:disabled{cursor:default}img,svg,video,canvas,audio,iframe,embed,object{display:block;vertical-align:middle}img,video{max-width:100%;height:auto}[hidden]:where(:not([hidden=until-found])){display:none}.pointer-events-none{pointer-events:none}.fixed{position:fixed}.absolute{position:absolute}.relative{position:relative}.sticky{position:sticky}.inset-0{top:0;right:0;bottom:0;left:0}.inset-y-0{top:0;bottom:0}.-bottom-0\.5{bottom:-.125rem}.-right-0\.5{right:-.125rem}.bottom-\[-10\%\]{bottom:-10%}.left-0{left:0}.left-\[-10\%\]{left:-10%}.left-\[100px\]{left:100px}.left-\[1040px\]{left:1040px}.left-\[1510px\]{left:1510px}.left-\[1980px\]{left:1980px}.left-\[570px\]{left:570px}.right-0{right:0}.right-\[-10\%\]{right:-10%}.right-\[20\%\]{right:20%}.top-0{top:0}.top-\[-10\%\]{top:-10%}.top-\[320px\]{top:320px}.top-\[350px\]{top:350px}.top-\[40\%\]{top:40%}.-z-10{z-index:-10}.z-0{z-index:0}.z-10{z-index:10}.z-30{z-index:30}.z-40{z-index:40}.z-50{z-index:50}.mx-auto{margin-left:auto;margin-right:auto}.mb-1{margin-bottom:.25rem}.mb-12{margin-bottom:3rem}.mb-2{margin-bottom:.5rem}.mb-3{margin-bottom:.75rem}.mb-4{margin-bottom:1rem}.mb-6{margin-bottom:1.5rem}.mr-3{margin-right:.75rem}.mt-0\.5{margin-top:.125rem}.mt-3{margin-top:.75rem}.block{display:block}.inline-block{display:inline-block}.flex{display:flex}.inline-flex{display:inline-flex}.grid{display:grid}.hidden{display:none}.h-1\.5{height:.375rem}.h-10{height:2.5rem}.h-12{height:3rem}.h-16{height:4rem}.h-2{height:.5rem}.h-2\.5{height:.625rem}.h-32{height:8rem}.h-9{height:2.25rem}.h-\[20\%\]{height:20%}.h-\[2000px\]{height:2000px}.h-\[50\%\]{height:50%}.h-\[80vh\]{height:80vh}.h-full{height:100%}.h-px{height:1px}.h-screen{height:100vh}.max-h-\[100px\]{max-height:100px}.min-h-0{min-height:0px}.min-h-screen{min-height:100vh}.w-1\.5{width:.375rem}.w-10{width:2.5rem}.w-14{width:3.5rem}.w-2{width:.5rem}.w-2\.5{width:.625rem}.w-32{width:8rem}.w-72{width:18rem}.w-9{width:2.25rem}.w-\[20\%\]{width:20%}.w-\[3000px\]{width:3000px}.w-\[320px\]{width:320px}.w-\[50\%\]{width:50%}.w-\[600px\]{width:600px}.w-full{width:100%}.max-w-5xl{max-width:64rem}.max-w-\[200px\]{max-width:200px}.max-w-\[300px\]{max-width:300px}.max-w-xl{max-width:36rem}.flex-1{flex:1 1 0%}.flex-none{flex:none}.flex-shrink-0,.shrink-0{flex-shrink:0}.origin-top-left{transform-origin:top left}.-translate-x-full{--tw-translate-x: -100%;transform:translate(var(--tw-translate-x),var(--tw-translate-y)) rotate(var(--tw-rotate)) skew(var(--tw-skew-x)) skewY(var(--tw-skew-y)) scaleX(var(--tw-scale-x)) scaleY(var(--tw-scale-y))}.translate-x-0{--tw-translate-x: 0px;transform:translate(var(--tw-translate-x),var(--tw-translate-y)) rotate(var(--tw-rotate)) skew(var(--tw-skew-x)) skewY(var(--tw-skew-y)) scaleX(var(--tw-scale-x)) scaleY(var(--tw-scale-y))}.translate-x-full{--tw-translate-x: 100%;transform:translate(var(--tw-translate-x),var(--tw-translate-y)) rotate(var(--tw-rotate)) skew(var(--tw-skew-x)) skewY(var(--tw-skew-y)) scaleX(var(--tw-scale-x)) scaleY(var(--tw-scale-y))}.transform{transform:translate(var(--tw-translate-x),var(--tw-translate-y)) rotate(var(--tw-rotate)) skew(var(--tw-skew-x)) skewY(var(--tw-skew-y)) scaleX(var(--tw-scale-x)) scaleY(var(--tw-scale-y))}@keyframes fadeIn{0%{opacity:0;transform:translateY(10px)}to{opacity:1;transform:translateY(0)}}.animate-fade-in{animation:fadeIn .6s cubic-bezier(.16,1,.3,1)}@keyframes float{0%,to{transform:translateY(0)}50%{transform:translateY(-10px)}}.animate-float{animation:float 6s ease-in-out infinite}@keyframes ping{75%,to{transform:scale(2);opacity:0}}.animate-ping{animation:ping 1s cubic-bezier(0,0,.2,1) infinite}.animate-pulse{animation:pulse 2s cubic-bezier(.4,0,.6,1) infinite}@keyframes pulse{50%{opacity:.5}}.animate-pulse-slow{animation:pulse 4s cubic-bezier(.4,0,.6,1) infinite}.cursor-default{cursor:default}.cursor-grab{cursor:grab}.cursor-not-allowed{cursor:not-allowed}.cursor-pointer{cursor:pointer}.select-none{-webkit-user-select:none;-moz-user-select:none;user-select:none}.resize{resize:both}.grid-cols-1{grid-template-columns:repeat(1,minmax(0,1fr))}.flex-col{flex-direction:column}.items-start{align-items:flex-start}.items-center{align-items:center}.justify-center{justify-content:center}.justify-between{justify-content:space-between}.gap-1{gap:.25rem}.gap-1\.5{gap:.375rem}.gap-2{gap:.5rem}.gap-3{gap:.75rem}.gap-4{gap:1rem}.gap-6{gap:1.5rem}.gap-\[20px\]{gap:20px}.space-y-1>:not([hidden])~:not([hidden]){--tw-space-y-reverse: 0;margin-top:calc(.25rem * calc(1 - var(--tw-space-y-reverse)));margin-bottom:calc(.25rem * var(--tw-space-y-reverse))}.space-y-6>:not([hidden])~:not([hidden]){--tw-space-y-reverse: 0;margin-top:calc(1.5rem * calc(1 - var(--tw-space-y-reverse)));margin-bottom:calc(1.5rem * var(--tw-space-y-reverse))}.overflow-hidden{overflow:hidden}.overflow-y-auto{overflow-y:auto}.truncate{overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.whitespace-pre-wrap{white-space:pre-wrap}.break-words{overflow-wrap:break-word}.break-all{word-break:break-all}.rounded{border-radius:.25rem}.rounded-2xl{border-radius:1rem}.rounded-3xl{border-radius:1.5rem}.rounded-full{border-radius:9999px}.rounded-lg{border-radius:.5rem}.rounded-md{border-radius:.375rem}.rounded-sm{border-radius:.125rem}.rounded-xl{border-radius:.75rem}.border{border-width:1px}.border-2{border-width:2px}.border-4{border-width:4px}.border-b{border-bottom-width:1px}.border-l{border-left-width:1px}.border-l-2{border-left-width:2px}.border-l-4{border-left-width:4px}.border-r{border-right-width:1px}.border-t{border-top-width:1px}.border-dashed{border-style:dashed}.border-\[\#334155\]{--tw-border-opacity: 1;border-color:rgb(51 65 85 / var(--tw-border-opacity, 1))}.border-border{--tw-border-opacity: 1;border-color:rgb(30 41 59 / var(--tw-border-opacity, 1))}.border-error{--tw-border-opacity: 1;border-color:rgb(239 68 68 / var(--tw-border-opacity, 1))}.border-primary{--tw-border-opacity: 1;border-color:rgb(99 102 241 / var(--tw-border-opacity, 1))}.border-secondary{--tw-border-opacity: 1;border-color:rgb(139 92 246 / var(--tw-border-opacity, 1))}.border-success{--tw-border-opacity: 1;border-color:rgb(16 185 129 / var(--tw-border-opacity, 1))}.border-surface{--tw-border-opacity: 1;border-color:rgb(15 23 42 / var(--tw-border-opacity, 1))}.border-transparent{border-color:transparent}.border-white\/10{border-color:#ffffff1a}.border-white\/5{border-color:#ffffff0d}.bg-\[\#020617\]{--tw-bg-opacity: 1;background-color:rgb(2 6 23 / var(--tw-bg-opacity, 1))}.bg-\[\#0f172a\]{--tw-bg-opacity: 1;background-color:rgb(15 23 42 / var(--tw-bg-opacity, 1))}.bg-\[\#1e293b\]{--tw-bg-opacity: 1;background-color:rgb(30 41 59 / var(--tw-bg-opacity, 1))}.bg-accent\/10{background-color:#06b6d41a}.bg-amber-400\/10{background-color:#fbbf241a}.bg-background{--tw-bg-opacity: 1;background-color:rgb(3 7 18 / var(--tw-bg-opacity, 1))}.bg-black\/50{background-color:#00000080}.bg-black\/60{background-color:#0009}.bg-black\/80{background-color:#000c}.bg-blue-400\/10{background-color:#60a5fa1a}.bg-blue-500{--tw-bg-opacity: 1;background-color:rgb(59 130 246 / var(--tw-bg-opacity, 1))}.bg-emerald-400{--tw-bg-opacity: 1;background-color:rgb(52 211 153 / var(--tw-bg-opacity, 1))}.bg-emerald-400\/10{background-color:#34d3991a}.bg-emerald-500{--tw-bg-opacity: 1;background-color:rgb(16 185 129 / var(--tw-bg-opacity, 1))}.bg-primary{--tw-bg-opacity: 1;background-color:rgb(99 102 241 / var(--tw-bg-opacity, 1))}.bg-primary\/10{background-color:#6366f11a}.bg-primary\/20{background-color:#6366f133}.bg-red-500{--tw-bg-opacity: 1;background-color:rgb(239 68 68 / var(--tw-bg-opacity, 1))}.bg-secondary\/20{background-color:#8b5cf633}.bg-slate-600{--tw-bg-opacity: 1;background-color:rgb(71 85 105 / var(--tw-bg-opacity, 1))}.bg-surface{--tw-bg-opacity: 1;background-color:rgb(15 23 42 / var(--tw-bg-opacity, 1))}.bg-surface\/80{background-color:#0f172acc}.bg-surfaceHighlight{--tw-bg-opacity: 1;background-color:rgb(30 41 59 / var(--tw-bg-opacity, 1))}.bg-white\/5{background-color:#ffffff0d}.bg-\[url\(\'\/grid\.svg\'\)\]{background-image:url(/grid.svg)}.bg-gradient-to-br{background-image:linear-gradient(to bottom right,var(--tw-gradient-stops))}.bg-gradient-to-r{background-image:linear-gradient(to right,var(--tw-gradient-stops))}.bg-gradient-to-t{background-image:linear-gradient(to top,var(--tw-gradient-stops))}.from-black\/40{--tw-gradient-from: rgb(0 0 0 / .4) var(--tw-gradient-from-position);--tw-gradient-to: rgb(0 0 0 / 0) var(--tw-gradient-to-position);--tw-gradient-stops: var(--tw-gradient-from), var(--tw-gradient-to)}.from-primary{--tw-gradient-from: #6366f1 var(--tw-gradient-from-position);--tw-gradient-to: rgb(99 102 241 / 0) var(--tw-gradient-to-position);--tw-gradient-stops: var(--tw-gradient-from), var(--tw-gradient-to)}.from-primary\/10{--tw-gradient-from: rgb(99 102 241 / .1) var(--tw-gradient-from-position);--tw-gradient-to: rgb(99 102 241 / 0) var(--tw-gradient-to-position);--tw-gradient-stops: var(--tw-gradient-from), var(--tw-gradient-to)}.from-primary\/20{--tw-gradient-from: rgb(99 102 241 / .2) var(--tw-gradient-from-position);--tw-gradient-to: rgb(99 102 241 / 0) var(--tw-gradient-to-position);--tw-gradient-stops: var(--tw-gradient-from), var(--tw-gradient-to)}.from-transparent{--tw-gradient-from: transparent var(--tw-gradient-from-position);--tw-gradient-to: rgb(0 0 0 / 0) var(--tw-gradient-to-position);--tw-gradient-stops: var(--tw-gradient-from), var(--tw-gradient-to)}.via-white\/10{--tw-gradient-to: rgb(255 255 255 / 0) var(--tw-gradient-to-position);--tw-gradient-stops: var(--tw-gradient-from), rgb(255 255 255 / .1) var(--tw-gradient-via-position), var(--tw-gradient-to)}.to-secondary{--tw-gradient-to: #8b5cf6 var(--tw-gradient-to-position)}.to-secondary\/20{--tw-gradient-to: rgb(139 92 246 / .2) var(--tw-gradient-to-position)}.to-transparent{--tw-gradient-to: transparent var(--tw-gradient-to-position)}.bg-\[length\:32px_32px\]{background-size:32px 32px}.fill-emerald-400{fill:#34d399}.p-1{padding:.25rem}.p-1\.5{padding:.375rem}.p-2{padding:.5rem}.p-3{padding:.75rem}.p-4{padding:1rem}.p-5{padding:1.25rem}.p-6{padding:1.5rem}.p-8{padding:2rem}.px-1\.5{padding-left:.375rem;padding-right:.375rem}.px-2{padding-left:.5rem;padding-right:.5rem}.px-3{padding-left:.75rem;padding-right:.75rem}.px-4{padding-left:1rem;padding-right:1rem}.px-6{padding-left:1.5rem;padding-right:1.5rem}.py-0\.5{padding-top:.125rem;padding-bottom:.125rem}.py-1\.5{padding-top:.375rem;padding-bottom:.375rem}.py-10{padding-top:2.5rem;padding-bottom:2.5rem}.py-2\.5{padding-top:.625rem;padding-bottom:.625rem}.pl-20{padding-left:5rem}.pr-2{padding-right:.5rem}.pt-2{padding-top:.5rem}.pt-20{padding-top:5rem}.text-center{text-align:center}.font-mono{font-family:JetBrains Mono,monospace}.font-sans{font-family:Inter,system-ui,sans-serif}.text-2xl{font-size:1.5rem;line-height:2rem}.text-3xl{font-size:1.875rem;line-height:2.25rem}.text-4xl{font-size:2.25rem;line-height:2.5rem}.text-\[10px\]{font-size:10px}.text-lg{font-size:1.125rem;line-height:1.75rem}.text-sm{font-size:.875rem;line-height:1.25rem}.text-xs{font-size:.75rem;line-height:1rem}.font-bold{font-weight:700}.font-medium{font-weight:500}.font-semibold{font-weight:600}.uppercase{text-transform:uppercase}.italic{font-style:italic}.leading-none{line-height:1}.leading-relaxed{line-height:1.625}.leading-tight{line-height:1.25}.tracking-tight{letter-spacing:-.025em}.tracking-wider{letter-spacing:.05em}.tracking-widest{letter-spacing:.1em}.text-amber-400{--tw-text-opacity: 1;color:rgb(251 191 36 / var(--tw-text-opacity, 1))}.text-blue-400{--tw-text-opacity: 1;color:rgb(96 165 250 / var(--tw-text-opacity, 1))}.text-emerald-400{--tw-text-opacity: 1;color:rgb(52 211 153 / var(--tw-text-opacity, 1))}.text-error{--tw-text-opacity: 1;color:rgb(239 68 68 / var(--tw-text-opacity, 1))}.text-orange-400{--tw-text-opacity: 1;color:rgb(251 146 60 / var(--tw-text-opacity, 1))}.text-primary{--tw-text-opacity: 1;color:rgb(99 102 241 / var(--tw-text-opacity, 1))}.text-primary-foreground{--tw-text-opacity: 1;color:rgb(255 255 255 / var(--tw-text-opacity, 1))}.text-red-400{--tw-text-opacity: 1;color:rgb(248 113 113 / var(--tw-text-opacity, 1))}.text-secondary{--tw-text-opacity: 1;color:rgb(139 92 246 / var(--tw-text-opacity, 1))}.text-slate-200{--tw-text-opacity: 1;color:rgb(226 232 240 / var(--tw-text-opacity, 1))}.text-slate-300{--tw-text-opacity: 1;color:rgb(203 213 225 / var(--tw-text-opacity, 1))}.text-slate-400{--tw-text-opacity: 1;color:rgb(148 163 184 / var(--tw-text-opacity, 1))}.text-slate-500{--tw-text-opacity: 1;color:rgb(100 116 139 / var(--tw-text-opacity, 1))}.text-slate-600{--tw-text-opacity: 1;color:rgb(71 85 105 / var(--tw-text-opacity, 1))}.text-slate-700{--tw-text-opacity: 1;color:rgb(51 65 85 / var(--tw-text-opacity, 1))}.text-success{--tw-text-opacity: 1;color:rgb(16 185 129 / var(--tw-text-opacity, 1))}.text-white{--tw-text-opacity: 1;color:rgb(255 255 255 / var(--tw-text-opacity, 1))}.opacity-0{opacity:0}.opacity-100{opacity:1}.opacity-30{opacity:.3}.opacity-50{opacity:.5}.opacity-60{opacity:.6}.opacity-70{opacity:.7}.opacity-75{opacity:.75}.opacity-\[0\.03\]{opacity:.03}.mix-blend-screen{mix-blend-mode:screen}.shadow-2xl{--tw-shadow: 0 25px 50px -12px rgb(0 0 0 / .25);--tw-shadow-colored: 0 25px 50px -12px var(--tw-shadow-color);box-shadow:var(--tw-ring-offset-shadow, 0 0 #0000),var(--tw-ring-shadow, 0 0 #0000),var(--tw-shadow)}.shadow-\[0_0_8px_rgba\(16\,185\,129\,0\.6\)\]{--tw-shadow: 0 0 8px rgba(16,185,129,.6);--tw-shadow-colored: 0 0 8px var(--tw-shadow-color);box-shadow:var(--tw-ring-offset-shadow, 0 0 #0000),var(--tw-ring-shadow, 0 0 #0000),var(--tw-shadow)}.shadow-\[0_0_8px_rgba\(239\,68\,68\,0\.6\)\]{--tw-shadow: 0 0 8px rgba(239,68,68,.6);--tw-shadow-colored: 0 0 8px var(--tw-shadow-color);box-shadow:var(--tw-ring-offset-shadow, 0 0 #0000),var(--tw-ring-shadow, 0 0 #0000),var(--tw-shadow)}.shadow-\[0_0_8px_rgba\(59\,130\,246\,0\.6\)\]{--tw-shadow: 0 0 8px rgba(59,130,246,.6);--tw-shadow-colored: 0 0 8px var(--tw-shadow-color);box-shadow:var(--tw-ring-offset-shadow, 0 0 #0000),var(--tw-ring-shadow, 0 0 #0000),var(--tw-shadow)}.shadow-\[0_0_8px_rgba\(99\,102\,241\,0\.6\)\]{--tw-shadow: 0 0 8px rgba(99,102,241,.6);--tw-shadow-colored: 0 0 8px var(--tw-shadow-color);box-shadow:var(--tw-ring-offset-shadow, 0 0 #0000),var(--tw-ring-shadow, 0 0 #0000),var(--tw-shadow)}.shadow-lg{--tw-shadow: 0 10px 15px -3px rgb(0 0 0 / .1), 0 4px 6px -4px rgb(0 0 0 / .1);--tw-shadow-colored: 0 10px 15px -3px var(--tw-shadow-color), 0 4px 6px -4px var(--tw-shadow-color);box-shadow:var(--tw-ring-offset-shadow, 0 0 #0000),var(--tw-ring-shadow, 0 0 #0000),var(--tw-shadow)}.shadow-sm{--tw-shadow: 0 1px 2px 0 rgb(0 0 0 / .05);--tw-shadow-colored: 0 1px 2px 0 var(--tw-shadow-color);box-shadow:var(--tw-ring-offset-shadow, 0 0 #0000),var(--tw-ring-shadow, 0 0 #0000),var(--tw-shadow)}.shadow-primary\/20{--tw-shadow-color: rgb(99 102 241 / .2);--tw-shadow: var(--tw-shadow-colored)}.ring-1{--tw-ring-offset-shadow: var(--tw-ring-inset) 0 0 0 var(--tw-ring-offset-width) var(--tw-ring-offset-color);--tw-ring-shadow: var(--tw-ring-inset) 0 0 0 calc(1px + var(--tw-ring-offset-width)) var(--tw-ring-color);box-shadow:var(--tw-ring-offset-shadow),var(--tw-ring-shadow),var(--tw-shadow, 0 0 #0000)}.ring-2{--tw-ring-offset-shadow: var(--tw-ring-inset) 0 0 0 var(--tw-ring-offset-width) var(--tw-ring-offset-color);--tw-ring-shadow: var(--tw-ring-inset) 0 0 0 calc(2px + var(--tw-ring-offset-width)) var(--tw-ring-color);box-shadow:var(--tw-ring-offset-shadow),var(--tw-ring-shadow),var(--tw-shadow, 0 0 #0000)}.ring-primary{--tw-ring-opacity: 1;--tw-ring-color: rgb(99 102 241 / var(--tw-ring-opacity, 1))}.ring-primary\/20{--tw-ring-color: rgb(99 102 241 / .2)}.ring-offset-2{--tw-ring-offset-width: 2px}.ring-offset-background{--tw-ring-offset-color: #030712}.blur-\[100px\]{--tw-blur: blur(100px);filter:var(--tw-blur) var(--tw-brightness) var(--tw-contrast) var(--tw-grayscale) var(--tw-hue-rotate) var(--tw-invert) var(--tw-saturate) var(--tw-sepia) var(--tw-drop-shadow)}.blur-\[120px\]{--tw-blur: blur(120px);filter:var(--tw-blur) var(--tw-brightness) var(--tw-contrast) var(--tw-grayscale) var(--tw-hue-rotate) var(--tw-invert) var(--tw-saturate) var(--tw-sepia) var(--tw-drop-shadow)}.blur-xl{--tw-blur: blur(24px);filter:var(--tw-blur) var(--tw-brightness) var(--tw-contrast) var(--tw-grayscale) var(--tw-hue-rotate) var(--tw-invert) var(--tw-saturate) var(--tw-sepia) var(--tw-drop-shadow)}.backdrop-blur-md{--tw-backdrop-blur: blur(12px);-webkit-backdrop-filter:var(--tw-backdrop-blur) var(--tw-backdrop-brightness) var(--tw-backdrop-contrast) var(--tw-backdrop-grayscale) var(--tw-backdrop-hue-rotate) var(--tw-backdrop-invert) var(--tw-backdrop-opacity) var(--tw-backdrop-saturate) var(--tw-backdrop-sepia);backdrop-filter:var(--tw-backdrop-blur) var(--tw-backdrop-brightness) var(--tw-backdrop-contrast) var(--tw-backdrop-grayscale) var(--tw-backdrop-hue-rotate) var(--tw-backdrop-invert) var(--tw-backdrop-opacity) var(--tw-backdrop-saturate) var(--tw-backdrop-sepia)}.backdrop-blur-sm{--tw-backdrop-blur: blur(4px);-webkit-backdrop-filter:var(--tw-backdrop-blur) var(--tw-backdrop-brightness) var(--tw-backdrop-contrast) var(--tw-backdrop-grayscale) var(--tw-backdrop-hue-rotate) var(--tw-backdrop-invert) var(--tw-backdrop-opacity) var(--tw-backdrop-saturate) var(--tw-backdrop-sepia);backdrop-filter:var(--tw-backdrop-blur) var(--tw-backdrop-brightness) var(--tw-backdrop-contrast) var(--tw-backdrop-grayscale) var(--tw-backdrop-hue-rotate) var(--tw-backdrop-invert) var(--tw-backdrop-opacity) var(--tw-backdrop-saturate) var(--tw-backdrop-sepia)}.backdrop-blur-xl{--tw-backdrop-blur: blur(24px);-webkit-backdrop-filter:var(--tw-backdrop-blur) var(--tw-backdrop-brightness) var(--tw-backdrop-contrast) var(--tw-backdrop-grayscale) var(--tw-backdrop-hue-rotate) var(--tw-backdrop-invert) var(--tw-backdrop-opacity) var(--tw-backdrop-saturate) var(--tw-backdrop-sepia);backdrop-filter:var(--tw-backdrop-blur) var(--tw-backdrop-brightness) var(--tw-backdrop-contrast) var(--tw-backdrop-grayscale) var(--tw-backdrop-hue-rotate) var(--tw-backdrop-invert) var(--tw-backdrop-opacity) var(--tw-backdrop-saturate) var(--tw-backdrop-sepia)}.transition-all{transition-property:all;transition-timing-function:cubic-bezier(.4,0,.2,1);transition-duration:.15s}.transition-colors{transition-property:color,background-color,border-color,text-decoration-color,fill,stroke;transition-timing-function:cubic-bezier(.4,0,.2,1);transition-duration:.15s}.transition-opacity{transition-property:opacity;transition-timing-function:cubic-bezier(.4,0,.2,1);transition-duration:.15s}.transition-transform{transition-property:transform;transition-timing-function:cubic-bezier(.4,0,.2,1);transition-duration:.15s}.duration-200{transition-duration:.2s}.duration-300{transition-duration:.3s}.duration-500{transition-duration:.5s}.duration-75{transition-duration:75ms}.ease-in-out{transition-timing-function:cubic-bezier(.4,0,.2,1)}.ease-linear{transition-timing-function:linear}:root{--font-sans: "Inter", system-ui, -apple-system, sans-serif}body{margin:0;min-height:100vh;font-family:var(--font-sans);background-color:#030712;background-image:radial-gradient(circle at 50% 0%,rgba(99,102,241,.15) 0%,transparent 50%),radial-gradient(circle at 80% 50%,rgba(139,92,246,.15) 0%,transparent 40%);color:#f8fafc;overflow:hidden}::-webkit-scrollbar{width:6px;height:6px}::-webkit-scrollbar-track{background:transparent}::-webkit-scrollbar-thumb{background:#94a3b833;border-radius:9999px;-webkit-transition:background .2s;transition:background .2s}::-webkit-scrollbar-thumb:hover{background:#94a3b866}.glass{background:#0f172aa6;backdrop-filter:blur(20px);-webkit-backdrop-filter:blur(20px);border:1px solid rgba(255,255,255,.08);box-shadow:0 4px 6px -1px #0000001a,0 2px 4px -1px #0000000f}.glass-panel{background:#1e293bb3;backdrop-filter:blur(16px);-webkit-backdrop-filter:blur(16px);border:1px solid rgba(255,255,255,.05);box-shadow:0 8px 32px #00000040}.glass-card{background:linear-gradient(180deg,#1e293b66,#0f172a66);border:1px solid rgba(255,255,255,.05);box-shadow:0 4px 6px -1px #0000001a;transition:all .3s cubic-bezier(.4,0,.2,1)}.glass-card:hover{background:linear-gradient(180deg,#1e293b99,#0f172a99);border-color:#6366f14d;box-shadow:0 10px 15px -3px #0000001a,0 0 0 1px #6366f11a}.text-gradient{background:linear-gradient(to right,#818cf8,#c4b5fd,#67e8f9);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}.text-gradient-primary{background:linear-gradient(to right,#6366f1,#a855f7);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}.hover\:scale-\[1\.02\]:hover{--tw-scale-x: 1.02;--tw-scale-y: 1.02;transform:translate(var(--tw-translate-x),var(--tw-translate-y)) rotate(var(--tw-rotate)) skew(var(--tw-skew-x)) skewY(var(--tw-skew-y)) scaleX(var(--tw-scale-x)) scaleY(var(--tw-scale-y))}.hover\:bg-\[\#334155\]:hover{--tw-bg-opacity: 1;background-color:rgb(51 65 85 / var(--tw-bg-opacity, 1))}.hover\:bg-\[\#3a3a3c\]:hover{--tw-bg-opacity: 1;background-color:rgb(58 58 60 / var(--tw-bg-opacity, 1))}.hover\:bg-surfaceHighlight:hover{--tw-bg-opacity: 1;background-color:rgb(30 41 59 / var(--tw-bg-opacity, 1))}.hover\:bg-white\/5:hover{background-color:#ffffff0d}.hover\:text-slate-200:hover{--tw-text-opacity: 1;color:rgb(226 232 240 / var(--tw-text-opacity, 1))}.hover\:text-white:hover{--tw-text-opacity: 1;color:rgb(255 255 255 / var(--tw-text-opacity, 1))}.active\:cursor-grabbing:active{cursor:grabbing}.group:hover .group-hover\:bg-primary\/30{background-color:#6366f14d}.group:hover .group-hover\:opacity-100{opacity:1}@media (min-width: 768px){.md\:ml-72{margin-left:18rem}.md\:inline{display:inline}.md\:hidden{display:none}.md\:grid-cols-3{grid-template-columns:repeat(3,minmax(0,1fr))}.md\:text-5xl{font-size:3rem;line-height:1}.md\:text-sm{font-size:.875rem;line-height:1.25rem}}
```

### dashboard/frontend/dist/assets/index-E3jWGKad.js

```javascript
function jd(e,t){for(var n=0;n<t.length;n++){const r=t[n];if(typeof r!="string"&&!Array.isArray(r)){for(const l in r)if(l!=="default"&&!(l in e)){const i=Object.getOwnPropertyDescriptor(r,l);i&&Object.defineProperty(e,l,i.get?i:{enumerable:!0,get:()=>r[l]})}}}return Object.freeze(Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}))}(function(){const t=document.createElement("link").relList;if(t&&t.supports&&t.supports("modulepreload"))return;for(const l of document.querySelectorAll('link[rel="modulepreload"]'))r(l);new MutationObserver(l=>{for(const i of l)if(i.type==="childList")for(const o of i.addedNodes)o.tagName==="LINK"&&o.rel==="modulepreload"&&r(o)}).observe(document,{childList:!0,subtree:!0});function n(l){const i={};return l.integrity&&(i.integrity=l.integrity),l.referrerPolicy&&(i.referrerPolicy=l.referrerPolicy),l.crossOrigin==="use-credentials"?i.credentials="include":l.crossOrigin==="anonymous"?i.credentials="omit":i.credentials="same-origin",i}function r(l){if(l.ep)return;l.ep=!0;const i=n(l);fetch(l.href,i)}})();function Td(e){return e&&e.__esModule&&Object.prototype.hasOwnProperty.call(e,"default")?e.default:e}var ja={exports:{}},Gl={},Ta={exports:{}},D={};/**
 * @license React
 * react.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */var Pr=Symbol.for("react.element"),Od=Symbol.for("react.portal"),Ld=Symbol.for("react.fragment"),zd=Symbol.for("react.strict_mode"),Ad=Symbol.for("react.profiler"),Id=Symbol.for("react.provider"),Dd=Symbol.for("react.context"),Fd=Symbol.for("react.forward_ref"),Md=Symbol.for("react.suspense"),Ud=Symbol.for("react.memo"),Bd=Symbol.for("react.lazy"),Js=Symbol.iterator;function $d(e){return e===null||typeof e!="object"?null:(e=Js&&e[Js]||e["@@iterator"],typeof e=="function"?e:null)}var Oa={isMounted:function(){return!1},enqueueForceUpdate:function(){},enqueueReplaceState:function(){},enqueueSetState:function(){}},La=Object.assign,za={};function Ln(e,t,n){this.props=e,this.context=t,this.refs=za,this.updater=n||Oa}Ln.prototype.isReactComponent={};Ln.prototype.setState=function(e,t){if(typeof e!="object"&&typeof e!="function"&&e!=null)throw Error("setState(...): takes an object of state variables to update or a function which returns an object of state variables.");this.updater.enqueueSetState(this,e,t,"setState")};Ln.prototype.forceUpdate=function(e){this.updater.enqueueForceUpdate(this,e,"forceUpdate")};function Aa(){}Aa.prototype=Ln.prototype;function Jo(e,t,n){this.props=e,this.context=t,this.refs=za,this.updater=n||Oa}var Yo=Jo.prototype=new Aa;Yo.constructor=Jo;La(Yo,Ln.prototype);Yo.isPureReactComponent=!0;var Ys=Array.isArray,Ia=Object.prototype.hasOwnProperty,bo={current:null},Da={key:!0,ref:!0,__self:!0,__source:!0};function Fa(e,t,n){var r,l={},i=null,o=null;if(t!=null)for(r in t.ref!==void 0&&(o=t.ref),t.key!==void 0&&(i=""+t.key),t)Ia.call(t,r)&&!Da.hasOwnProperty(r)&&(l[r]=t[r]);var s=arguments.length-2;if(s===1)l.children=n;else if(1<s){for(var u=Array(s),a=0;a<s;a++)u[a]=arguments[a+2];l.children=u}if(e&&e.defaultProps)for(r in s=e.defaultProps,s)l[r]===void 0&&(l[r]=s[r]);return{$$typeof:Pr,type:e,key:i,ref:o,props:l,_owner:bo.current}}function Vd(e,t){return{$$typeof:Pr,type:e.type,key:t,ref:e.ref,props:e.props,_owner:e._owner}}function Zo(e){return typeof e=="object"&&e!==null&&e.$$typeof===Pr}function Wd(e){var t={"=":"=0",":":"=2"};return"$"+e.replace(/[=:]/g,function(n){return t[n]})}var bs=/\/+/g;function vi(e,t){return typeof e=="object"&&e!==null&&e.key!=null?Wd(""+e.key):t.toString(36)}function il(e,t,n,r,l){var i=typeof e;(i==="undefined"||i==="boolean")&&(e=null);var o=!1;if(e===null)o=!0;else switch(i){case"string":case"number":o=!0;break;case"object":switch(e.$$typeof){case Pr:case Od:o=!0}}if(o)return o=e,l=l(o),e=r===""?"."+vi(o,0):r,Ys(l)?(n="",e!=null&&(n=e.replace(bs,"$&/")+"/"),il(l,t,n,"",function(a){return a})):l!=null&&(Zo(l)&&(l=Vd(l,n+(!l.key||o&&o.key===l.key?"":(""+l.key).replace(bs,"$&/")+"/")+e)),t.push(l)),1;if(o=0,r=r===""?".":r+":",Ys(e))for(var s=0;s<e.length;s++){i=e[s];var u=r+vi(i,s);o+=il(i,t,n,u,l)}else if(u=$d(e),typeof u=="function")for(e=u.call(e),s=0;!(i=e.next()).done;)i=i.value,u=r+vi(i,s++),o+=il(i,t,n,u,l);else if(i==="object")throw t=String(e),Error("Objects are not valid as a React child (found: "+(t==="[object Object]"?"object with keys {"+Object.keys(e).join(", ")+"}":t)+"). If you meant to render a collection of children, use an array instead.");return o}function Mr(e,t,n){if(e==null)return e;var r=[],l=0;return il(e,r,"","",function(i){return t.call(n,i,l++)}),r}function Hd(e){if(e._status===-1){var t=e._result;t=t(),t.then(function(n){(e._status===0||e._status===-1)&&(e._status=1,e._result=n)},function(n){(e._status===0||e._status===-1)&&(e._status=2,e._result=n)}),e._status===-1&&(e._status=0,e._result=t)}if(e._status===1)return e._result.default;throw e._result}var ge={current:null},ol={transition:null},Qd={ReactCurrentDispatcher:ge,ReactCurrentBatchConfig:ol,ReactCurrentOwner:bo};function Ma(){throw Error("act(...) is not supported in production builds of React.")}D.Children={map:Mr,forEach:function(e,t,n){Mr(e,function(){t.apply(this,arguments)},n)},count:function(e){var t=0;return Mr(e,function(){t++}),t},toArray:function(e){return Mr(e,function(t){return t})||[]},only:function(e){if(!Zo(e))throw Error("React.Children.only expected to receive a single React element child.");return e}};D.Component=Ln;D.Fragment=Ld;D.Profiler=Ad;D.PureComponent=Jo;D.StrictMode=zd;D.Suspense=Md;D.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED=Qd;D.act=Ma;D.cloneElement=function(e,t,n){if(e==null)throw Error("React.cloneElement(...): The argument must be a React element, but you passed "+e+".");var r=La({},e.props),l=e.key,i=e.ref,o=e._owner;if(t!=null){if(t.ref!==void 0&&(i=t.ref,o=bo.current),t.key!==void 0&&(l=""+t.key),e.type&&e.type.defaultProps)var s=e.type.defaultProps;for(u in t)Ia.call(t,u)&&!Da.hasOwnProperty(u)&&(r[u]=t[u]===void 0&&s!==void 0?s[u]:t[u])}var u=arguments.length-2;if(u===1)r.children=n;else if(1<u){s=Array(u);for(var a=0;a<u;a++)s[a]=arguments[a+2];r.children=s}return{$$typeof:Pr,type:e.type,key:l,ref:i,props:r,_owner:o}};D.createContext=function(e){return e={$$typeof:Dd,_currentValue:e,_currentValue2:e,_threadCount:0,Provider:null,Consumer:null,_defaultValue:null,_globalName:null},e.Provider={$$typeof:Id,_context:e},e.Consumer=e};D.createElement=Fa;D.createFactory=function(e){var t=Fa.bind(null,e);return t.type=e,t};D.createRef=function(){return{current:null}};D.forwardRef=function(e){return{$$typeof:Fd,render:e}};D.isValidElement=Zo;D.lazy=function(e){return{$$typeof:Bd,_payload:{_status:-1,_result:e},_init:Hd}};D.memo=function(e,t){return{$$typeof:Ud,type:e,compare:t===void 0?null:t}};D.startTransition=function(e){var t=ol.transition;ol.transition={};try{e()}finally{ol.transition=t}};D.unstable_act=Ma;D.useCallback=function(e,t){return ge.current.useCallback(e,t)};D.useContext=function(e){return ge.current.useContext(e)};D.useDebugValue=function(){};D.useDeferredValue=function(e){return ge.current.useDeferredValue(e)};D.useEffect=function(e,t){return ge.current.useEffect(e,t)};D.useId=function(){return ge.current.useId()};D.useImperativeHandle=function(e,t,n){return ge.current.useImperativeHandle(e,t,n)};D.useInsertionEffect=function(e,t){return ge.current.useInsertionEffect(e,t)};D.useLayoutEffect=function(e,t){return ge.current.useLayoutEffect(e,t)};D.useMemo=function(e,t){return ge.current.useMemo(e,t)};D.useReducer=function(e,t,n){return ge.current.useReducer(e,t,n)};D.useRef=function(e){return ge.current.useRef(e)};D.useState=function(e){return ge.current.useState(e)};D.useSyncExternalStore=function(e,t,n){return ge.current.useSyncExternalStore(e,t,n)};D.useTransition=function(){return ge.current.useTransition()};D.version="18.3.1";Ta.exports=D;var N=Ta.exports;const Ua=Td(N),Kd=jd({__proto__:null,default:Ua},[N]);/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */var Gd=N,Xd=Symbol.for("react.element"),qd=Symbol.for("react.fragment"),Jd=Object.prototype.hasOwnProperty,Yd=Gd.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner,bd={key:!0,ref:!0,__self:!0,__source:!0};function Ba(e,t,n){var r,l={},i=null,o=null;n!==void 0&&(i=""+n),t.key!==void 0&&(i=""+t.key),t.ref!==void 0&&(o=t.ref);for(r in t)Jd.call(t,r)&&!bd.hasOwnProperty(r)&&(l[r]=t[r]);if(e&&e.defaultProps)for(r in t=e.defaultProps,t)l[r]===void 0&&(l[r]=t[r]);return{$$typeof:Xd,type:e,key:i,ref:o,props:l,_owner:Yd.current}}Gl.Fragment=qd;Gl.jsx=Ba;Gl.jsxs=Ba;ja.exports=Gl;var v=ja.exports,Gi={},$a={exports:{}},Ae={},Va={exports:{}},Wa={};/**
 * @license React
 * scheduler.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */(function(e){function t(R,z){var I=R.length;R.push(z);e:for(;0<I;){var B=I-1>>>1,W=R[B];if(0<l(W,z))R[B]=z,R[I]=W,I=B;else break e}}function n(R){return R.length===0?null:R[0]}function r(R){if(R.length===0)return null;var z=R[0],I=R.pop();if(I!==z){R[0]=I;e:for(var B=0,W=R.length,pt=W>>>1;B<pt;){var De=2*(B+1)-1,nn=R[De],Mt=De+1,Fr=R[Mt];if(0>l(nn,I))Mt<W&&0>l(Fr,nn)?(R[B]=Fr,R[Mt]=I,B=Mt):(R[B]=nn,R[De]=I,B=De);else if(Mt<W&&0>l(Fr,I))R[B]=Fr,R[Mt]=I,B=Mt;else break e}}return z}function l(R,z){var I=R.sortIndex-z.sortIndex;return I!==0?I:R.id-z.id}if(typeof performance=="object"&&typeof performance.now=="function"){var i=performance;e.unstable_now=function(){return i.now()}}else{var o=Date,s=o.now();e.unstable_now=function(){return o.now()-s}}var u=[],a=[],f=1,d=null,y=3,E=!1,m=!1,x=!1,S=typeof setTimeout=="function"?setTimeout:null,h=typeof clearTimeout=="function"?clearTimeout:null,c=typeof setImmediate<"u"?setImmediate:null;typeof navigator<"u"&&navigator.scheduling!==void 0&&navigator.scheduling.isInputPending!==void 0&&navigator.scheduling.isInputPending.bind(navigator.scheduling);function p(R){for(var z=n(a);z!==null;){if(z.callback===null)r(a);else if(z.startTime<=R)r(a),z.sortIndex=z.expirationTime,t(u,z);else break;z=n(a)}}function g(R){if(x=!1,p(R),!m)if(n(u)!==null)m=!0,U(k);else{var z=n(a);z!==null&&me(g,z.startTime-R)}}function k(R,z){m=!1,x&&(x=!1,h(T),T=-1),E=!0;var I=y;try{for(p(z),d=n(u);d!==null&&(!(d.expirationTime>z)||R&&!te());){var B=d.callback;if(typeof B=="function"){d.callback=null,y=d.priorityLevel;var W=B(d.expirationTime<=z);z=e.unstable_now(),typeof W=="function"?d.callback=W:d===n(u)&&r(u),p(z)}else r(u);d=n(u)}if(d!==null)var pt=!0;else{var De=n(a);De!==null&&me(g,De.startTime-z),pt=!1}return pt}finally{d=null,y=I,E=!1}}var _=!1,P=null,T=-1,M=5,L=-1;function te(){return!(e.unstable_now()-L<M)}function _e(){if(P!==null){var R=e.unstable_now();L=R;var z=!0;try{z=P(!0,R)}finally{z?we():(_=!1,P=null)}}else _=!1}var we;if(typeof c=="function")we=function(){c(_e)};else if(typeof MessageChannel<"u"){var je=new MessageChannel,O=je.port2;je.port1.onmessage=_e,we=function(){O.postMessage(null)}}else we=function(){S(_e,0)};function U(R){P=R,_||(_=!0,we())}function me(R,z){T=S(function(){R(e.unstable_now())},z)}e.unstable_IdlePriority=5,e.unstable_ImmediatePriority=1,e.unstable_LowPriority=4,e.unstable_NormalPriority=3,e.unstable_Profiling=null,e.unstable_UserBlockingPriority=2,e.unstable_cancelCallback=function(R){R.callback=null},e.unstable_continueExecution=function(){m||E||(m=!0,U(k))},e.unstable_forceFrameRate=function(R){0>R||125<R?console.error("forceFrameRate takes a positive int between 0 and 125, forcing frame rates higher than 125 fps is not supported"):M=0<R?Math.floor(1e3/R):5},e.unstable_getCurrentPriorityLevel=function(){return y},e.unstable_getFirstCallbackNode=function(){return n(u)},e.unstable_next=function(R){switch(y){case 1:case 2:case 3:var z=3;break;default:z=y}var I=y;y=z;try{return R()}finally{y=I}},e.unstable_pauseExecution=function(){},e.unstable_requestPaint=function(){},e.unstable_runWithPriority=function(R,z){switch(R){case 1:case 2:case 3:case 4:case 5:break;default:R=3}var I=y;y=R;try{return z()}finally{y=I}},e.unstable_scheduleCallback=function(R,z,I){var B=e.unstable_now();switch(typeof I=="object"&&I!==null?(I=I.delay,I=typeof I=="number"&&0<I?B+I:B):I=B,R){case 1:var W=-1;break;case 2:W=250;break;case 5:W=1073741823;break;case 4:W=1e4;break;default:W=5e3}return W=I+W,R={id:f++,callback:z,priorityLevel:R,startTime:I,expirationTime:W,sortIndex:-1},I>B?(R.sortIndex=I,t(a,R),n(u)===null&&R===n(a)&&(x?(h(T),T=-1):x=!0,me(g,I-B))):(R.sortIndex=W,t(u,R),m||E||(m=!0,U(k))),R},e.unstable_shouldYield=te,e.unstable_wrapCallback=function(R){var z=y;return function(){var I=y;y=z;try{return R.apply(this,arguments)}finally{y=I}}}})(Wa);Va.exports=Wa;var Zd=Va.exports;/**
 * @license React
 * react-dom.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */var ep=N,ze=Zd;function C(e){for(var t="https://reactjs.org/docs/error-decoder.html?invariant="+e,n=1;n<arguments.length;n++)t+="&args[]="+encodeURIComponent(arguments[n]);return"Minified React error #"+e+"; visit "+t+" for the full message or use the non-minified dev environment for full errors and additional helpful warnings."}var Ha=new Set,ur={};function en(e,t){kn(e,t),kn(e+"Capture",t)}function kn(e,t){for(ur[e]=t,e=0;e<t.length;e++)Ha.add(t[e])}var ut=!(typeof window>"u"||typeof window.document>"u"||typeof window.document.createElement>"u"),Xi=Object.prototype.hasOwnProperty,tp=/^[:A-Z_a-z\u00C0-\u00D6\u00D8-\u00F6\u00F8-\u02FF\u0370-\u037D\u037F-\u1FFF\u200C-\u200D\u2070-\u218F\u2C00-\u2FEF\u3001-\uD7FF\uF900-\uFDCF\uFDF0-\uFFFD][:A-Z_a-z\u00C0-\u00D6\u00D8-\u00F6\u00F8-\u02FF\u0370-\u037D\u037F-\u1FFF\u200C-\u200D\u2070-\u218F\u2C00-\u2FEF\u3001-\uD7FF\uF900-\uFDCF\uFDF0-\uFFFD\-.0-9\u00B7\u0300-\u036F\u203F-\u2040]*$/,Zs={},eu={};function np(e){return Xi.call(eu,e)?!0:Xi.call(Zs,e)?!1:tp.test(e)?eu[e]=!0:(Zs[e]=!0,!1)}function rp(e,t,n,r){if(n!==null&&n.type===0)return!1;switch(typeof t){case"function":case"symbol":return!0;case"boolean":return r?!1:n!==null?!n.acceptsBooleans:(e=e.toLowerCase().slice(0,5),e!=="data-"&&e!=="aria-");default:return!1}}function lp(e,t,n,r){if(t===null||typeof t>"u"||rp(e,t,n,r))return!0;if(r)return!1;if(n!==null)switch(n.type){case 3:return!t;case 4:return t===!1;case 5:return isNaN(t);case 6:return isNaN(t)||1>t}return!1}function xe(e,t,n,r,l,i,o){this.acceptsBooleans=t===2||t===3||t===4,this.attributeName=r,this.attributeNamespace=l,this.mustUseProperty=n,this.propertyName=e,this.type=t,this.sanitizeURL=i,this.removeEmptyString=o}var ae={};"children dangerouslySetInnerHTML defaultValue defaultChecked innerHTML suppressContentEditableWarning suppressHydrationWarning style".split(" ").forEach(function(e){ae[e]=new xe(e,0,!1,e,null,!1,!1)});[["acceptCharset","accept-charset"],["className","class"],["htmlFor","for"],["httpEquiv","http-equiv"]].forEach(function(e){var t=e[0];ae[t]=new xe(t,1,!1,e[1],null,!1,!1)});["contentEditable","draggable","spellCheck","value"].forEach(function(e){ae[e]=new xe(e,2,!1,e.toLowerCase(),null,!1,!1)});["autoReverse","externalResourcesRequired","focusable","preserveAlpha"].forEach(function(e){ae[e]=new xe(e,2,!1,e,null,!1,!1)});"allowFullScreen async autoFocus autoPlay controls default defer disabled disablePictureInPicture disableRemotePlayback formNoValidate hidden loop noModule noValidate open playsInline readOnly required reversed scoped seamless itemScope".split(" ").forEach(function(e){ae[e]=new xe(e,3,!1,e.toLowerCase(),null,!1,!1)});["checked","multiple","muted","selected"].forEach(function(e){ae[e]=new xe(e,3,!0,e,null,!1,!1)});["capture","download"].forEach(function(e){ae[e]=new xe(e,4,!1,e,null,!1,!1)});["cols","rows","size","span"].forEach(function(e){ae[e]=new xe(e,6,!1,e,null,!1,!1)});["rowSpan","start"].forEach(function(e){ae[e]=new xe(e,5,!1,e.toLowerCase(),null,!1,!1)});var es=/[\-:]([a-z])/g;function ts(e){return e[1].toUpperCase()}"accent-height alignment-baseline arabic-form baseline-shift cap-height clip-path clip-rule color-interpolation color-interpolation-filters color-profile color-rendering dominant-baseline enable-background fill-opacity fill-rule flood-color flood-opacity font-family font-size font-size-adjust font-stretch font-style font-variant font-weight glyph-name glyph-orientation-horizontal glyph-orientation-vertical horiz-adv-x horiz-origin-x image-rendering letter-spacing lighting-color marker-end marker-mid marker-start overline-position overline-thickness paint-order panose-1 pointer-events rendering-intent shape-rendering stop-color stop-opacity strikethrough-position strikethrough-thickness stroke-dasharray stroke-dashoffset stroke-linecap stroke-linejoin stroke-miterlimit stroke-opacity stroke-width text-anchor text-decoration text-rendering underline-position underline-thickness unicode-bidi unicode-range units-per-em v-alphabetic v-hanging v-ideographic v-mathematical vector-effect vert-adv-y vert-origin-x vert-origin-y word-spacing writing-mode xmlns:xlink x-height".split(" ").forEach(function(e){var t=e.replace(es,ts);ae[t]=new xe(t,1,!1,e,null,!1,!1)});"xlink:actuate xlink:arcrole xlink:role xlink:show xlink:title xlink:type".split(" ").forEach(function(e){var t=e.replace(es,ts);ae[t]=new xe(t,1,!1,e,"http://www.w3.org/1999/xlink",!1,!1)});["xml:base","xml:lang","xml:space"].forEach(function(e){var t=e.replace(es,ts);ae[t]=new xe(t,1,!1,e,"http://www.w3.org/XML/1998/namespace",!1,!1)});["tabIndex","crossOrigin"].forEach(function(e){ae[e]=new xe(e,1,!1,e.toLowerCase(),null,!1,!1)});ae.xlinkHref=new xe("xlinkHref",1,!1,"xlink:href","http://www.w3.org/1999/xlink",!0,!1);["src","href","action","formAction"].forEach(function(e){ae[e]=new xe(e,1,!1,e.toLowerCase(),null,!0,!0)});function ns(e,t,n,r){var l=ae.hasOwnProperty(t)?ae[t]:null;(l!==null?l.type!==0:r||!(2<t.length)||t[0]!=="o"&&t[0]!=="O"||t[1]!=="n"&&t[1]!=="N")&&(lp(t,n,l,r)&&(n=null),r||l===null?np(t)&&(n===null?e.removeAttribute(t):e.setAttribute(t,""+n)):l.mustUseProperty?e[l.propertyName]=n===null?l.type===3?!1:"":n:(t=l.attributeName,r=l.attributeNamespace,n===null?e.removeAttribute(t):(l=l.type,n=l===3||l===4&&n===!0?"":""+n,r?e.setAttributeNS(r,t,n):e.setAttribute(t,n))))}var dt=ep.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED,Ur=Symbol.for("react.element"),ln=Symbol.for("react.portal"),on=Symbol.for("react.fragment"),rs=Symbol.for("react.strict_mode"),qi=Symbol.for("react.profiler"),Qa=Symbol.for("react.provider"),Ka=Symbol.for("react.context"),ls=Symbol.for("react.forward_ref"),Ji=Symbol.for("react.suspense"),Yi=Symbol.for("react.suspense_list"),is=Symbol.for("react.memo"),mt=Symbol.for("react.lazy"),Ga=Symbol.for("react.offscreen"),tu=Symbol.iterator;function Un(e){return e===null||typeof e!="object"?null:(e=tu&&e[tu]||e["@@iterator"],typeof e=="function"?e:null)}var q=Object.assign,gi;function qn(e){if(gi===void 0)try{throw Error()}catch(n){var t=n.stack.trim().match(/\n( *(at )?)/);gi=t&&t[1]||""}return`
`+gi+e}var xi=!1;function wi(e,t){if(!e||xi)return"";xi=!0;var n=Error.prepareStackTrace;Error.prepareStackTrace=void 0;try{if(t)if(t=function(){throw Error()},Object.defineProperty(t.prototype,"props",{set:function(){throw Error()}}),typeof Reflect=="object"&&Reflect.construct){try{Reflect.construct(t,[])}catch(a){var r=a}Reflect.construct(e,[],t)}else{try{t.call()}catch(a){r=a}e.call(t.prototype)}else{try{throw Error()}catch(a){r=a}e()}}catch(a){if(a&&r&&typeof a.stack=="string"){for(var l=a.stack.split(`
`),i=r.stack.split(`
`),o=l.length-1,s=i.length-1;1<=o&&0<=s&&l[o]!==i[s];)s--;for(;1<=o&&0<=s;o--,s--)if(l[o]!==i[s]){if(o!==1||s!==1)do if(o--,s--,0>s||l[o]!==i[s]){var u=`
`+l[o].replace(" at new "," at ");return e.displayName&&u.includes("<anonymous>")&&(u=u.replace("<anonymous>",e.displayName)),u}while(1<=o&&0<=s);break}}}finally{xi=!1,Error.prepareStackTrace=n}return(e=e?e.displayName||e.name:"")?qn(e):""}function ip(e){switch(e.tag){case 5:return qn(e.type);case 16:return qn("Lazy");case 13:return qn("Suspense");case 19:return qn("SuspenseList");case 0:case 2:case 15:return e=wi(e.type,!1),e;case 11:return e=wi(e.type.render,!1),e;case 1:return e=wi(e.type,!0),e;default:return""}}function bi(e){if(e==null)return null;if(typeof e=="function")return e.displayName||e.name||null;if(typeof e=="string")return e;switch(e){case on:return"Fragment";case ln:return"Portal";case qi:return"Profiler";case rs:return"StrictMode";case Ji:return"Suspense";case Yi:return"SuspenseList"}if(typeof e=="object")switch(e.$$typeof){case Ka:return(e.displayName||"Context")+".Consumer";case Qa:return(e._context.displayName||"Context")+".Provider";case ls:var t=e.render;return e=e.displayName,e||(e=t.displayName||t.name||"",e=e!==""?"ForwardRef("+e+")":"ForwardRef"),e;case is:return t=e.displayName||null,t!==null?t:bi(e.type)||"Memo";case mt:t=e._payload,e=e._init;try{return bi(e(t))}catch{}}return null}function op(e){var t=e.type;switch(e.tag){case 24:return"Cache";case 9:return(t.displayName||"Context")+".Consumer";case 10:return(t._context.displayName||"Context")+".Provider";case 18:return"DehydratedFragment";case 11:return e=t.render,e=e.displayName||e.name||"",t.displayName||(e!==""?"ForwardRef("+e+")":"ForwardRef");case 7:return"Fragment";case 5:return t;case 4:return"Portal";case 3:return"Root";case 6:return"Text";case 16:return bi(t);case 8:return t===rs?"StrictMode":"Mode";case 22:return"Offscreen";case 12:return"Profiler";case 21:return"Scope";case 13:return"Suspense";case 19:return"SuspenseList";case 25:return"TracingMarker";case 1:case 0:case 17:case 2:case 14:case 15:if(typeof t=="function")return t.displayName||t.name||null;if(typeof t=="string")return t}return null}function Ot(e){switch(typeof e){case"boolean":case"number":case"string":case"undefined":return e;case"object":return e;default:return""}}function Xa(e){var t=e.type;return(e=e.nodeName)&&e.toLowerCase()==="input"&&(t==="checkbox"||t==="radio")}function sp(e){var t=Xa(e)?"checked":"value",n=Object.getOwnPropertyDescriptor(e.constructor.prototype,t),r=""+e[t];if(!e.hasOwnProperty(t)&&typeof n<"u"&&typeof n.get=="function"&&typeof n.set=="function"){var l=n.get,i=n.set;return Object.defineProperty(e,t,{configurable:!0,get:function(){return l.call(this)},set:function(o){r=""+o,i.call(this,o)}}),Object.defineProperty(e,t,{enumerable:n.enumerable}),{getValue:function(){return r},setValue:function(o){r=""+o},stopTracking:function(){e._valueTracker=null,delete e[t]}}}}function Br(e){e._valueTracker||(e._valueTracker=sp(e))}function qa(e){if(!e)return!1;var t=e._valueTracker;if(!t)return!0;var n=t.getValue(),r="";return e&&(r=Xa(e)?e.checked?"true":"false":e.value),e=r,e!==n?(t.setValue(e),!0):!1}function wl(e){if(e=e||(typeof document<"u"?document:void 0),typeof e>"u")return null;try{return e.activeElement||e.body}catch{return e.body}}function Zi(e,t){var n=t.checked;return q({},t,{defaultChecked:void 0,defaultValue:void 0,value:void 0,checked:n??e._wrapperState.initialChecked})}function nu(e,t){var n=t.defaultValue==null?"":t.defaultValue,r=t.checked!=null?t.checked:t.defaultChecked;n=Ot(t.value!=null?t.value:n),e._wrapperState={initialChecked:r,initialValue:n,controlled:t.type==="checkbox"||t.type==="radio"?t.checked!=null:t.value!=null}}function Ja(e,t){t=t.checked,t!=null&&ns(e,"checked",t,!1)}function eo(e,t){Ja(e,t);var n=Ot(t.value),r=t.type;if(n!=null)r==="number"?(n===0&&e.value===""||e.value!=n)&&(e.value=""+n):e.value!==""+n&&(e.value=""+n);else if(r==="submit"||r==="reset"){e.removeAttribute("value");return}t.hasOwnProperty("value")?to(e,t.type,n):t.hasOwnProperty("defaultValue")&&to(e,t.type,Ot(t.defaultValue)),t.checked==null&&t.defaultChecked!=null&&(e.defaultChecked=!!t.defaultChecked)}function ru(e,t,n){if(t.hasOwnProperty("value")||t.hasOwnProperty("defaultValue")){var r=t.type;if(!(r!=="submit"&&r!=="reset"||t.value!==void 0&&t.value!==null))return;t=""+e._wrapperState.initialValue,n||t===e.value||(e.value=t),e.defaultValue=t}n=e.name,n!==""&&(e.name=""),e.defaultChecked=!!e._wrapperState.initialChecked,n!==""&&(e.name=n)}function to(e,t,n){(t!=="number"||wl(e.ownerDocument)!==e)&&(n==null?e.defaultValue=""+e._wrapperState.initialValue:e.defaultValue!==""+n&&(e.defaultValue=""+n))}var Jn=Array.isArray;function vn(e,t,n,r){if(e=e.options,t){t={};for(var l=0;l<n.length;l++)t["$"+n[l]]=!0;for(n=0;n<e.length;n++)l=t.hasOwnProperty("$"+e[n].value),e[n].selected!==l&&(e[n].selected=l),l&&r&&(e[n].defaultSelected=!0)}else{for(n=""+Ot(n),t=null,l=0;l<e.length;l++){if(e[l].value===n){e[l].selected=!0,r&&(e[l].defaultSelected=!0);return}t!==null||e[l].disabled||(t=e[l])}t!==null&&(t.selected=!0)}}function no(e,t){if(t.dangerouslySetInnerHTML!=null)throw Error(C(91));return q({},t,{value:void 0,defaultValue:void 0,children:""+e._wrapperState.initialValue})}function lu(e,t){var n=t.value;if(n==null){if(n=t.children,t=t.defaultValue,n!=null){if(t!=null)throw Error(C(92));if(Jn(n)){if(1<n.length)throw Error(C(93));n=n[0]}t=n}t==null&&(t=""),n=t}e._wrapperState={initialValue:Ot(n)}}function Ya(e,t){var n=Ot(t.value),r=Ot(t.defaultValue);n!=null&&(n=""+n,n!==e.value&&(e.value=n),t.defaultValue==null&&e.defaultValue!==n&&(e.defaultValue=n)),r!=null&&(e.defaultValue=""+r)}function iu(e){var t=e.textContent;t===e._wrapperState.initialValue&&t!==""&&t!==null&&(e.value=t)}function ba(e){switch(e){case"svg":return"http://www.w3.org/2000/svg";case"math":return"http://www.w3.org/1998/Math/MathML";default:return"http://www.w3.org/1999/xhtml"}}function ro(e,t){return e==null||e==="http://www.w3.org/1999/xhtml"?ba(t):e==="http://www.w3.org/2000/svg"&&t==="foreignObject"?"http://www.w3.org/1999/xhtml":e}var $r,Za=function(e){return typeof MSApp<"u"&&MSApp.execUnsafeLocalFunction?function(t,n,r,l){MSApp.execUnsafeLocalFunction(function(){return e(t,n,r,l)})}:e}(function(e,t){if(e.namespaceURI!=="http://www.w3.org/2000/svg"||"innerHTML"in e)e.innerHTML=t;else{for($r=$r||document.createElement("div"),$r.innerHTML="<svg>"+t.valueOf().toString()+"</svg>",t=$r.firstChild;e.firstChild;)e.removeChild(e.firstChild);for(;t.firstChild;)e.appendChild(t.firstChild)}});function ar(e,t){if(t){var n=e.firstChild;if(n&&n===e.lastChild&&n.nodeType===3){n.nodeValue=t;return}}e.textContent=t}var Zn={animationIterationCount:!0,aspectRatio:!0,borderImageOutset:!0,borderImageSlice:!0,borderImageWidth:!0,boxFlex:!0,boxFlexGroup:!0,boxOrdinalGroup:!0,columnCount:!0,columns:!0,flex:!0,flexGrow:!0,flexPositive:!0,flexShrink:!0,flexNegative:!0,flexOrder:!0,gridArea:!0,gridRow:!0,gridRowEnd:!0,gridRowSpan:!0,gridRowStart:!0,gridColumn:!0,gridColumnEnd:!0,gridColumnSpan:!0,gridColumnStart:!0,fontWeight:!0,lineClamp:!0,lineHeight:!0,opacity:!0,order:!0,orphans:!0,tabSize:!0,widows:!0,zIndex:!0,zoom:!0,fillOpacity:!0,floodOpacity:!0,stopOpacity:!0,strokeDasharray:!0,strokeDashoffset:!0,strokeMiterlimit:!0,strokeOpacity:!0,strokeWidth:!0},up=["Webkit","ms","Moz","O"];Object.keys(Zn).forEach(function(e){up.forEach(function(t){t=t+e.charAt(0).toUpperCase()+e.substring(1),Zn[t]=Zn[e]})});function ec(e,t,n){return t==null||typeof t=="boolean"||t===""?"":n||typeof t!="number"||t===0||Zn.hasOwnProperty(e)&&Zn[e]?(""+t).trim():t+"px"}function tc(e,t){e=e.style;for(var n in t)if(t.hasOwnProperty(n)){var r=n.indexOf("--")===0,l=ec(n,t[n],r);n==="float"&&(n="cssFloat"),r?e.setProperty(n,l):e[n]=l}}var ap=q({menuitem:!0},{area:!0,base:!0,br:!0,col:!0,embed:!0,hr:!0,img:!0,input:!0,keygen:!0,link:!0,meta:!0,param:!0,source:!0,track:!0,wbr:!0});function lo(e,t){if(t){if(ap[e]&&(t.children!=null||t.dangerouslySetInnerHTML!=null))throw Error(C(137,e));if(t.dangerouslySetInnerHTML!=null){if(t.children!=null)throw Error(C(60));if(typeof t.dangerouslySetInnerHTML!="object"||!("__html"in t.dangerouslySetInnerHTML))throw Error(C(61))}if(t.style!=null&&typeof t.style!="object")throw Error(C(62))}}function io(e,t){if(e.indexOf("-")===-1)return typeof t.is=="string";switch(e){case"annotation-xml":case"color-profile":case"font-face":case"font-face-src":case"font-face-uri":case"font-face-format":case"font-face-name":case"missing-glyph":return!1;default:return!0}}var oo=null;function os(e){return e=e.target||e.srcElement||window,e.correspondingUseElement&&(e=e.correspondingUseElement),e.nodeType===3?e.parentNode:e}var so=null,gn=null,xn=null;function ou(e){if(e=Tr(e)){if(typeof so!="function")throw Error(C(280));var t=e.stateNode;t&&(t=bl(t),so(e.stateNode,e.type,t))}}function nc(e){gn?xn?xn.push(e):xn=[e]:gn=e}function rc(){if(gn){var e=gn,t=xn;if(xn=gn=null,ou(e),t)for(e=0;e<t.length;e++)ou(t[e])}}function lc(e,t){return e(t)}function ic(){}var Si=!1;function oc(e,t,n){if(Si)return e(t,n);Si=!0;try{return lc(e,t,n)}finally{Si=!1,(gn!==null||xn!==null)&&(ic(),rc())}}function cr(e,t){var n=e.stateNode;if(n===null)return null;var r=bl(n);if(r===null)return null;n=r[t];e:switch(t){case"onClick":case"onClickCapture":case"onDoubleClick":case"onDoubleClickCapture":case"onMouseDown":case"onMouseDownCapture":case"onMouseMove":case"onMouseMoveCapture":case"onMouseUp":case"onMouseUpCapture":case"onMouseEnter":(r=!r.disabled)||(e=e.type,r=!(e==="button"||e==="input"||e==="select"||e==="textarea")),e=!r;break e;default:e=!1}if(e)return null;if(n&&typeof n!="function")throw Error(C(231,t,typeof n));return n}var uo=!1;if(ut)try{var Bn={};Object.defineProperty(Bn,"passive",{get:function(){uo=!0}}),window.addEventListener("test",Bn,Bn),window.removeEventListener("test",Bn,Bn)}catch{uo=!1}function cp(e,t,n,r,l,i,o,s,u){var a=Array.prototype.slice.call(arguments,3);try{t.apply(n,a)}catch(f){this.onError(f)}}var er=!1,Sl=null,El=!1,ao=null,fp={onError:function(e){er=!0,Sl=e}};function dp(e,t,n,r,l,i,o,s,u){er=!1,Sl=null,cp.apply(fp,arguments)}function pp(e,t,n,r,l,i,o,s,u){if(dp.apply(this,arguments),er){if(er){var a=Sl;er=!1,Sl=null}else throw Error(C(198));El||(El=!0,ao=a)}}function tn(e){var t=e,n=e;if(e.alternate)for(;t.return;)t=t.return;else{e=t;do t=e,t.flags&4098&&(n=t.return),e=t.return;while(e)}return t.tag===3?n:null}function sc(e){if(e.tag===13){var t=e.memoizedState;if(t===null&&(e=e.alternate,e!==null&&(t=e.memoizedState)),t!==null)return t.dehydrated}return null}function su(e){if(tn(e)!==e)throw Error(C(188))}function hp(e){var t=e.alternate;if(!t){if(t=tn(e),t===null)throw Error(C(188));return t!==e?null:e}for(var n=e,r=t;;){var l=n.return;if(l===null)break;var i=l.alternate;if(i===null){if(r=l.return,r!==null){n=r;continue}break}if(l.child===i.child){for(i=l.child;i;){if(i===n)return su(l),e;if(i===r)return su(l),t;i=i.sibling}throw Error(C(188))}if(n.return!==r.return)n=l,r=i;else{for(var o=!1,s=l.child;s;){if(s===n){o=!0,n=l,r=i;break}if(s===r){o=!0,r=l,n=i;break}s=s.sibling}if(!o){for(s=i.child;s;){if(s===n){o=!0,n=i,r=l;break}if(s===r){o=!0,r=i,n=l;break}s=s.sibling}if(!o)throw Error(C(189))}}if(n.alternate!==r)throw Error(C(190))}if(n.tag!==3)throw Error(C(188));return n.stateNode.current===n?e:t}function uc(e){return e=hp(e),e!==null?ac(e):null}function ac(e){if(e.tag===5||e.tag===6)return e;for(e=e.child;e!==null;){var t=ac(e);if(t!==null)return t;e=e.sibling}return null}var cc=ze.unstable_scheduleCallback,uu=ze.unstable_cancelCallback,mp=ze.unstable_shouldYield,yp=ze.unstable_requestPaint,Z=ze.unstable_now,vp=ze.unstable_getCurrentPriorityLevel,ss=ze.unstable_ImmediatePriority,fc=ze.unstable_UserBlockingPriority,kl=ze.unstable_NormalPriority,gp=ze.unstable_LowPriority,dc=ze.unstable_IdlePriority,Xl=null,tt=null;function xp(e){if(tt&&typeof tt.onCommitFiberRoot=="function")try{tt.onCommitFiberRoot(Xl,e,void 0,(e.current.flags&128)===128)}catch{}}var Ge=Math.clz32?Math.clz32:Ep,wp=Math.log,Sp=Math.LN2;function Ep(e){return e>>>=0,e===0?32:31-(wp(e)/Sp|0)|0}var Vr=64,Wr=4194304;function Yn(e){switch(e&-e){case 1:return 1;case 2:return 2;case 4:return 4;case 8:return 8;case 16:return 16;case 32:return 32;case 64:case 128:case 256:case 512:case 1024:case 2048:case 4096:case 8192:case 16384:case 32768:case 65536:case 131072:case 262144:case 524288:case 1048576:case 2097152:return e&4194240;case 4194304:case 8388608:case 16777216:case 33554432:case 67108864:return e&130023424;case 134217728:return 134217728;case 268435456:return 268435456;case 536870912:return 536870912;case 1073741824:return 1073741824;default:return e}}function Cl(e,t){var n=e.pendingLanes;if(n===0)return 0;var r=0,l=e.suspendedLanes,i=e.pingedLanes,o=n&268435455;if(o!==0){var s=o&~l;s!==0?r=Yn(s):(i&=o,i!==0&&(r=Yn(i)))}else o=n&~l,o!==0?r=Yn(o):i!==0&&(r=Yn(i));if(r===0)return 0;if(t!==0&&t!==r&&!(t&l)&&(l=r&-r,i=t&-t,l>=i||l===16&&(i&4194240)!==0))return t;if(r&4&&(r|=n&16),t=e.entangledLanes,t!==0)for(e=e.entanglements,t&=r;0<t;)n=31-Ge(t),l=1<<n,r|=e[n],t&=~l;return r}function kp(e,t){switch(e){case 1:case 2:case 4:return t+250;case 8:case 16:case 32:case 64:case 128:case 256:case 512:case 1024:case 2048:case 4096:case 8192:case 16384:case 32768:case 65536:case 131072:case 262144:case 524288:case 1048576:case 2097152:return t+5e3;case 4194304:case 8388608:case 16777216:case 33554432:case 67108864:return-1;case 134217728:case 268435456:case 536870912:case 1073741824:return-1;default:return-1}}function Cp(e,t){for(var n=e.suspendedLanes,r=e.pingedLanes,l=e.expirationTimes,i=e.pendingLanes;0<i;){var o=31-Ge(i),s=1<<o,u=l[o];u===-1?(!(s&n)||s&r)&&(l[o]=kp(s,t)):u<=t&&(e.expiredLanes|=s),i&=~s}}function co(e){return e=e.pendingLanes&-1073741825,e!==0?e:e&1073741824?1073741824:0}function pc(){var e=Vr;return Vr<<=1,!(Vr&4194240)&&(Vr=64),e}function Ei(e){for(var t=[],n=0;31>n;n++)t.push(e);return t}function _r(e,t,n){e.pendingLanes|=t,t!==536870912&&(e.suspendedLanes=0,e.pingedLanes=0),e=e.eventTimes,t=31-Ge(t),e[t]=n}function Np(e,t){var n=e.pendingLanes&~t;e.pendingLanes=t,e.suspendedLanes=0,e.pingedLanes=0,e.expiredLanes&=t,e.mutableReadLanes&=t,e.entangledLanes&=t,t=e.entanglements;var r=e.eventTimes;for(e=e.expirationTimes;0<n;){var l=31-Ge(n),i=1<<l;t[l]=0,r[l]=-1,e[l]=-1,n&=~i}}function us(e,t){var n=e.entangledLanes|=t;for(e=e.entanglements;n;){var r=31-Ge(n),l=1<<r;l&t|e[r]&t&&(e[r]|=t),n&=~l}}var $=0;function hc(e){return e&=-e,1<e?4<e?e&268435455?16:536870912:4:1}var mc,as,yc,vc,gc,fo=!1,Hr=[],Et=null,kt=null,Ct=null,fr=new Map,dr=new Map,vt=[],Rp="mousedown mouseup touchcancel touchend touchstart auxclick dblclick pointercancel pointerdown pointerup dragend dragstart drop compositionend compositionstart keydown keypress keyup input textInput copy cut paste click change contextmenu reset submit".split(" ");function au(e,t){switch(e){case"focusin":case"focusout":Et=null;break;case"dragenter":case"dragleave":kt=null;break;case"mouseover":case"mouseout":Ct=null;break;case"pointerover":case"pointerout":fr.delete(t.pointerId);break;case"gotpointercapture":case"lostpointercapture":dr.delete(t.pointerId)}}function $n(e,t,n,r,l,i){return e===null||e.nativeEvent!==i?(e={blockedOn:t,domEventName:n,eventSystemFlags:r,nativeEvent:i,targetContainers:[l]},t!==null&&(t=Tr(t),t!==null&&as(t)),e):(e.eventSystemFlags|=r,t=e.targetContainers,l!==null&&t.indexOf(l)===-1&&t.push(l),e)}function Pp(e,t,n,r,l){switch(t){case"focusin":return Et=$n(Et,e,t,n,r,l),!0;case"dragenter":return kt=$n(kt,e,t,n,r,l),!0;case"mouseover":return Ct=$n(Ct,e,t,n,r,l),!0;case"pointerover":var i=l.pointerId;return fr.set(i,$n(fr.get(i)||null,e,t,n,r,l)),!0;case"gotpointercapture":return i=l.pointerId,dr.set(i,$n(dr.get(i)||null,e,t,n,r,l)),!0}return!1}function xc(e){var t=$t(e.target);if(t!==null){var n=tn(t);if(n!==null){if(t=n.tag,t===13){if(t=sc(n),t!==null){e.blockedOn=t,gc(e.priority,function(){yc(n)});return}}else if(t===3&&n.stateNode.current.memoizedState.isDehydrated){e.blockedOn=n.tag===3?n.stateNode.containerInfo:null;return}}}e.blockedOn=null}function sl(e){if(e.blockedOn!==null)return!1;for(var t=e.targetContainers;0<t.length;){var n=po(e.domEventName,e.eventSystemFlags,t[0],e.nativeEvent);if(n===null){n=e.nativeEvent;var r=new n.constructor(n.type,n);oo=r,n.target.dispatchEvent(r),oo=null}else return t=Tr(n),t!==null&&as(t),e.blockedOn=n,!1;t.shift()}return!0}function cu(e,t,n){sl(e)&&n.delete(t)}function _p(){fo=!1,Et!==null&&sl(Et)&&(Et=null),kt!==null&&sl(kt)&&(kt=null),Ct!==null&&sl(Ct)&&(Ct=null),fr.forEach(cu),dr.forEach(cu)}function Vn(e,t){e.blockedOn===t&&(e.blockedOn=null,fo||(fo=!0,ze.unstable_scheduleCallback(ze.unstable_NormalPriority,_p)))}function pr(e){function t(l){return Vn(l,e)}if(0<Hr.length){Vn(Hr[0],e);for(var n=1;n<Hr.length;n++){var r=Hr[n];r.blockedOn===e&&(r.blockedOn=null)}}for(Et!==null&&Vn(Et,e),kt!==null&&Vn(kt,e),Ct!==null&&Vn(Ct,e),fr.forEach(t),dr.forEach(t),n=0;n<vt.length;n++)r=vt[n],r.blockedOn===e&&(r.blockedOn=null);for(;0<vt.length&&(n=vt[0],n.blockedOn===null);)xc(n),n.blockedOn===null&&vt.shift()}var wn=dt.ReactCurrentBatchConfig,Nl=!0;function jp(e,t,n,r){var l=$,i=wn.transition;wn.transition=null;try{$=1,cs(e,t,n,r)}finally{$=l,wn.transition=i}}function Tp(e,t,n,r){var l=$,i=wn.transition;wn.transition=null;try{$=4,cs(e,t,n,r)}finally{$=l,wn.transition=i}}function cs(e,t,n,r){if(Nl){var l=po(e,t,n,r);if(l===null)Li(e,t,r,Rl,n),au(e,r);else if(Pp(l,e,t,n,r))r.stopPropagation();else if(au(e,r),t&4&&-1<Rp.indexOf(e)){for(;l!==null;){var i=Tr(l);if(i!==null&&mc(i),i=po(e,t,n,r),i===null&&Li(e,t,r,Rl,n),i===l)break;l=i}l!==null&&r.stopPropagation()}else Li(e,t,r,null,n)}}var Rl=null;function po(e,t,n,r){if(Rl=null,e=os(r),e=$t(e),e!==null)if(t=tn(e),t===null)e=null;else if(n=t.tag,n===13){if(e=sc(t),e!==null)return e;e=null}else if(n===3){if(t.stateNode.current.memoizedState.isDehydrated)return t.tag===3?t.stateNode.containerInfo:null;e=null}else t!==e&&(e=null);return Rl=e,null}function wc(e){switch(e){case"cancel":case"click":case"close":case"contextmenu":case"copy":case"cut":case"auxclick":case"dblclick":case"dragend":case"dragstart":case"drop":case"focusin":case"focusout":case"input":case"invalid":case"keydown":case"keypress":case"keyup":case"mousedown":case"mouseup":case"paste":case"pause":case"play":case"pointercancel":case"pointerdown":case"pointerup":case"ratechange":case"reset":case"resize":case"seeked":case"submit":case"touchcancel":case"touchend":case"touchstart":case"volumechange":case"change":case"selectionchange":case"textInput":case"compositionstart":case"compositionend":case"compositionupdate":case"beforeblur":case"afterblur":case"beforeinput":case"blur":case"fullscreenchange":case"focus":case"hashchange":case"popstate":case"select":case"selectstart":return 1;case"drag":case"dragenter":case"dragexit":case"dragleave":case"dragover":case"mousemove":case"mouseout":case"mouseover":case"pointermove":case"pointerout":case"pointerover":case"scroll":case"toggle":case"touchmove":case"wheel":case"mouseenter":case"mouseleave":case"pointerenter":case"pointerleave":return 4;case"message":switch(vp()){case ss:return 1;case fc:return 4;case kl:case gp:return 16;case dc:return 536870912;default:return 16}default:return 16}}var xt=null,fs=null,ul=null;function Sc(){if(ul)return ul;var e,t=fs,n=t.length,r,l="value"in xt?xt.value:xt.textContent,i=l.length;for(e=0;e<n&&t[e]===l[e];e++);var o=n-e;for(r=1;r<=o&&t[n-r]===l[i-r];r++);return ul=l.slice(e,1<r?1-r:void 0)}function al(e){var t=e.keyCode;return"charCode"in e?(e=e.charCode,e===0&&t===13&&(e=13)):e=t,e===10&&(e=13),32<=e||e===13?e:0}function Qr(){return!0}function fu(){return!1}function Ie(e){function t(n,r,l,i,o){this._reactName=n,this._targetInst=l,this.type=r,this.nativeEvent=i,this.target=o,this.currentTarget=null;for(var s in e)e.hasOwnProperty(s)&&(n=e[s],this[s]=n?n(i):i[s]);return this.isDefaultPrevented=(i.defaultPrevented!=null?i.defaultPrevented:i.returnValue===!1)?Qr:fu,this.isPropagationStopped=fu,this}return q(t.prototype,{preventDefault:function(){this.defaultPrevented=!0;var n=this.nativeEvent;n&&(n.preventDefault?n.preventDefault():typeof n.returnValue!="unknown"&&(n.returnValue=!1),this.isDefaultPrevented=Qr)},stopPropagation:function(){var n=this.nativeEvent;n&&(n.stopPropagation?n.stopPropagation():typeof n.cancelBubble!="unknown"&&(n.cancelBubble=!0),this.isPropagationStopped=Qr)},persist:function(){},isPersistent:Qr}),t}var zn={eventPhase:0,bubbles:0,cancelable:0,timeStamp:function(e){return e.timeStamp||Date.now()},defaultPrevented:0,isTrusted:0},ds=Ie(zn),jr=q({},zn,{view:0,detail:0}),Op=Ie(jr),ki,Ci,Wn,ql=q({},jr,{screenX:0,screenY:0,clientX:0,clientY:0,pageX:0,pageY:0,ctrlKey:0,shiftKey:0,altKey:0,metaKey:0,getModifierState:ps,button:0,buttons:0,relatedTarget:function(e){return e.relatedTarget===void 0?e.fromElement===e.srcElement?e.toElement:e.fromElement:e.relatedTarget},movementX:function(e){return"movementX"in e?e.movementX:(e!==Wn&&(Wn&&e.type==="mousemove"?(ki=e.screenX-Wn.screenX,Ci=e.screenY-Wn.screenY):Ci=ki=0,Wn=e),ki)},movementY:function(e){return"movementY"in e?e.movementY:Ci}}),du=Ie(ql),Lp=q({},ql,{dataTransfer:0}),zp=Ie(Lp),Ap=q({},jr,{relatedTarget:0}),Ni=Ie(Ap),Ip=q({},zn,{animationName:0,elapsedTime:0,pseudoElement:0}),Dp=Ie(Ip),Fp=q({},zn,{clipboardData:function(e){return"clipboardData"in e?e.clipboardData:window.clipboardData}}),Mp=Ie(Fp),Up=q({},zn,{data:0}),pu=Ie(Up),Bp={Esc:"Escape",Spacebar:" ",Left:"ArrowLeft",Up:"ArrowUp",Right:"ArrowRight",Down:"ArrowDown",Del:"Delete",Win:"OS",Menu:"ContextMenu",Apps:"ContextMenu",Scroll:"ScrollLock",MozPrintableKey:"Unidentified"},$p={8:"Backspace",9:"Tab",12:"Clear",13:"Enter",16:"Shift",17:"Control",18:"Alt",19:"Pause",20:"CapsLock",27:"Escape",32:" ",33:"PageUp",34:"PageDown",35:"End",36:"Home",37:"ArrowLeft",38:"ArrowUp",39:"ArrowRight",40:"ArrowDown",45:"Insert",46:"Delete",112:"F1",113:"F2",114:"F3",115:"F4",116:"F5",117:"F6",118:"F7",119:"F8",120:"F9",121:"F10",122:"F11",123:"F12",144:"NumLock",145:"ScrollLock",224:"Meta"},Vp={Alt:"altKey",Control:"ctrlKey",Meta:"metaKey",Shift:"shiftKey"};function Wp(e){var t=this.nativeEvent;return t.getModifierState?t.getModifierState(e):(e=Vp[e])?!!t[e]:!1}function ps(){return Wp}var Hp=q({},jr,{key:function(e){if(e.key){var t=Bp[e.key]||e.key;if(t!=="Unidentified")return t}return e.type==="keypress"?(e=al(e),e===13?"Enter":String.fromCharCode(e)):e.type==="keydown"||e.type==="keyup"?$p[e.keyCode]||"Unidentified":""},code:0,location:0,ctrlKey:0,shiftKey:0,altKey:0,metaKey:0,repeat:0,locale:0,getModifierState:ps,charCode:function(e){return e.type==="keypress"?al(e):0},keyCode:function(e){return e.type==="keydown"||e.type==="keyup"?e.keyCode:0},which:function(e){return e.type==="keypress"?al(e):e.type==="keydown"||e.type==="keyup"?e.keyCode:0}}),Qp=Ie(Hp),Kp=q({},ql,{pointerId:0,width:0,height:0,pressure:0,tangentialPressure:0,tiltX:0,tiltY:0,twist:0,pointerType:0,isPrimary:0}),hu=Ie(Kp),Gp=q({},jr,{touches:0,targetTouches:0,changedTouches:0,altKey:0,metaKey:0,ctrlKey:0,shiftKey:0,getModifierState:ps}),Xp=Ie(Gp),qp=q({},zn,{propertyName:0,elapsedTime:0,pseudoElement:0}),Jp=Ie(qp),Yp=q({},ql,{deltaX:function(e){return"deltaX"in e?e.deltaX:"wheelDeltaX"in e?-e.wheelDeltaX:0},deltaY:function(e){return"deltaY"in e?e.deltaY:"wheelDeltaY"in e?-e.wheelDeltaY:"wheelDelta"in e?-e.wheelDelta:0},deltaZ:0,deltaMode:0}),bp=Ie(Yp),Zp=[9,13,27,32],hs=ut&&"CompositionEvent"in window,tr=null;ut&&"documentMode"in document&&(tr=document.documentMode);var eh=ut&&"TextEvent"in window&&!tr,Ec=ut&&(!hs||tr&&8<tr&&11>=tr),mu=" ",yu=!1;function kc(e,t){switch(e){case"keyup":return Zp.indexOf(t.keyCode)!==-1;case"keydown":return t.keyCode!==229;case"keypress":case"mousedown":case"focusout":return!0;default:return!1}}function Cc(e){return e=e.detail,typeof e=="object"&&"data"in e?e.data:null}var sn=!1;function th(e,t){switch(e){case"compositionend":return Cc(t);case"keypress":return t.which!==32?null:(yu=!0,mu);case"textInput":return e=t.data,e===mu&&yu?null:e;default:return null}}function nh(e,t){if(sn)return e==="compositionend"||!hs&&kc(e,t)?(e=Sc(),ul=fs=xt=null,sn=!1,e):null;switch(e){case"paste":return null;case"keypress":if(!(t.ctrlKey||t.altKey||t.metaKey)||t.ctrlKey&&t.altKey){if(t.char&&1<t.char.length)return t.char;if(t.which)return String.fromCharCode(t.which)}return null;case"compositionend":return Ec&&t.locale!=="ko"?null:t.data;default:return null}}var rh={color:!0,date:!0,datetime:!0,"datetime-local":!0,email:!0,month:!0,number:!0,password:!0,range:!0,search:!0,tel:!0,text:!0,time:!0,url:!0,week:!0};function vu(e){var t=e&&e.nodeName&&e.nodeName.toLowerCase();return t==="input"?!!rh[e.type]:t==="textarea"}function Nc(e,t,n,r){nc(r),t=Pl(t,"onChange"),0<t.length&&(n=new ds("onChange","change",null,n,r),e.push({event:n,listeners:t}))}var nr=null,hr=null;function lh(e){Dc(e,0)}function Jl(e){var t=cn(e);if(qa(t))return e}function ih(e,t){if(e==="change")return t}var Rc=!1;if(ut){var Ri;if(ut){var Pi="oninput"in document;if(!Pi){var gu=document.createElement("div");gu.setAttribute("oninput","return;"),Pi=typeof gu.oninput=="function"}Ri=Pi}else Ri=!1;Rc=Ri&&(!document.documentMode||9<document.documentMode)}function xu(){nr&&(nr.detachEvent("onpropertychange",Pc),hr=nr=null)}function Pc(e){if(e.propertyName==="value"&&Jl(hr)){var t=[];Nc(t,hr,e,os(e)),oc(lh,t)}}function oh(e,t,n){e==="focusin"?(xu(),nr=t,hr=n,nr.attachEvent("onpropertychange",Pc)):e==="focusout"&&xu()}function sh(e){if(e==="selectionchange"||e==="keyup"||e==="keydown")return Jl(hr)}function uh(e,t){if(e==="click")return Jl(t)}function ah(e,t){if(e==="input"||e==="change")return Jl(t)}function ch(e,t){return e===t&&(e!==0||1/e===1/t)||e!==e&&t!==t}var qe=typeof Object.is=="function"?Object.is:ch;function mr(e,t){if(qe(e,t))return!0;if(typeof e!="object"||e===null||typeof t!="object"||t===null)return!1;var n=Object.keys(e),r=Object.keys(t);if(n.length!==r.length)return!1;for(r=0;r<n.length;r++){var l=n[r];if(!Xi.call(t,l)||!qe(e[l],t[l]))return!1}return!0}function wu(e){for(;e&&e.firstChild;)e=e.firstChild;return e}function Su(e,t){var n=wu(e);e=0;for(var r;n;){if(n.nodeType===3){if(r=e+n.textContent.length,e<=t&&r>=t)return{node:n,offset:t-e};e=r}e:{for(;n;){if(n.nextSibling){n=n.nextSibling;break e}n=n.parentNode}n=void 0}n=wu(n)}}function _c(e,t){return e&&t?e===t?!0:e&&e.nodeType===3?!1:t&&t.nodeType===3?_c(e,t.parentNode):"contains"in e?e.contains(t):e.compareDocumentPosition?!!(e.compareDocumentPosition(t)&16):!1:!1}function jc(){for(var e=window,t=wl();t instanceof e.HTMLIFrameElement;){try{var n=typeof t.contentWindow.location.href=="string"}catch{n=!1}if(n)e=t.contentWindow;else break;t=wl(e.document)}return t}function ms(e){var t=e&&e.nodeName&&e.nodeName.toLowerCase();return t&&(t==="input"&&(e.type==="text"||e.type==="search"||e.type==="tel"||e.type==="url"||e.type==="password")||t==="textarea"||e.contentEditable==="true")}function fh(e){var t=jc(),n=e.focusedElem,r=e.selectionRange;if(t!==n&&n&&n.ownerDocument&&_c(n.ownerDocument.documentElement,n)){if(r!==null&&ms(n)){if(t=r.start,e=r.end,e===void 0&&(e=t),"selectionStart"in n)n.selectionStart=t,n.selectionEnd=Math.min(e,n.value.length);else if(e=(t=n.ownerDocument||document)&&t.defaultView||window,e.getSelection){e=e.getSelection();var l=n.textContent.length,i=Math.min(r.start,l);r=r.end===void 0?i:Math.min(r.end,l),!e.extend&&i>r&&(l=r,r=i,i=l),l=Su(n,i);var o=Su(n,r);l&&o&&(e.rangeCount!==1||e.anchorNode!==l.node||e.anchorOffset!==l.offset||e.focusNode!==o.node||e.focusOffset!==o.offset)&&(t=t.createRange(),t.setStart(l.node,l.offset),e.removeAllRanges(),i>r?(e.addRange(t),e.extend(o.node,o.offset)):(t.setEnd(o.node,o.offset),e.addRange(t)))}}for(t=[],e=n;e=e.parentNode;)e.nodeType===1&&t.push({element:e,left:e.scrollLeft,top:e.scrollTop});for(typeof n.focus=="function"&&n.focus(),n=0;n<t.length;n++)e=t[n],e.element.scrollLeft=e.left,e.element.scrollTop=e.top}}var dh=ut&&"documentMode"in document&&11>=document.documentMode,un=null,ho=null,rr=null,mo=!1;function Eu(e,t,n){var r=n.window===n?n.document:n.nodeType===9?n:n.ownerDocument;mo||un==null||un!==wl(r)||(r=un,"selectionStart"in r&&ms(r)?r={start:r.selectionStart,end:r.selectionEnd}:(r=(r.ownerDocument&&r.ownerDocument.defaultView||window).getSelection(),r={anchorNode:r.anchorNode,anchorOffset:r.anchorOffset,focusNode:r.focusNode,focusOffset:r.focusOffset}),rr&&mr(rr,r)||(rr=r,r=Pl(ho,"onSelect"),0<r.length&&(t=new ds("onSelect","select",null,t,n),e.push({event:t,listeners:r}),t.target=un)))}function Kr(e,t){var n={};return n[e.toLowerCase()]=t.toLowerCase(),n["Webkit"+e]="webkit"+t,n["Moz"+e]="moz"+t,n}var an={animationend:Kr("Animation","AnimationEnd"),animationiteration:Kr("Animation","AnimationIteration"),animationstart:Kr("Animation","AnimationStart"),transitionend:Kr("Transition","TransitionEnd")},_i={},Tc={};ut&&(Tc=document.createElement("div").style,"AnimationEvent"in window||(delete an.animationend.animation,delete an.animationiteration.animation,delete an.animationstart.animation),"TransitionEvent"in window||delete an.transitionend.transition);function Yl(e){if(_i[e])return _i[e];if(!an[e])return e;var t=an[e],n;for(n in t)if(t.hasOwnProperty(n)&&n in Tc)return _i[e]=t[n];return e}var Oc=Yl("animationend"),Lc=Yl("animationiteration"),zc=Yl("animationstart"),Ac=Yl("transitionend"),Ic=new Map,ku="abort auxClick cancel canPlay canPlayThrough click close contextMenu copy cut drag dragEnd dragEnter dragExit dragLeave dragOver dragStart drop durationChange emptied encrypted ended error gotPointerCapture input invalid keyDown keyPress keyUp load loadedData loadedMetadata loadStart lostPointerCapture mouseDown mouseMove mouseOut mouseOver mouseUp paste pause play playing pointerCancel pointerDown pointerMove pointerOut pointerOver pointerUp progress rateChange reset resize seeked seeking stalled submit suspend timeUpdate touchCancel touchEnd touchStart volumeChange scroll toggle touchMove waiting wheel".split(" ");function zt(e,t){Ic.set(e,t),en(t,[e])}for(var ji=0;ji<ku.length;ji++){var Ti=ku[ji],ph=Ti.toLowerCase(),hh=Ti[0].toUpperCase()+Ti.slice(1);zt(ph,"on"+hh)}zt(Oc,"onAnimationEnd");zt(Lc,"onAnimationIteration");zt(zc,"onAnimationStart");zt("dblclick","onDoubleClick");zt("focusin","onFocus");zt("focusout","onBlur");zt(Ac,"onTransitionEnd");kn("onMouseEnter",["mouseout","mouseover"]);kn("onMouseLeave",["mouseout","mouseover"]);kn("onPointerEnter",["pointerout","pointerover"]);kn("onPointerLeave",["pointerout","pointerover"]);en("onChange","change click focusin focusout input keydown keyup selectionchange".split(" "));en("onSelect","focusout contextmenu dragend focusin keydown keyup mousedown mouseup selectionchange".split(" "));en("onBeforeInput",["compositionend","keypress","textInput","paste"]);en("onCompositionEnd","compositionend focusout keydown keypress keyup mousedown".split(" "));en("onCompositionStart","compositionstart focusout keydown keypress keyup mousedown".split(" "));en("onCompositionUpdate","compositionupdate focusout keydown keypress keyup mousedown".split(" "));var bn="abort canplay canplaythrough durationchange emptied encrypted ended error loadeddata loadedmetadata loadstart pause play playing progress ratechange resize seeked seeking stalled suspend timeupdate volumechange waiting".split(" "),mh=new Set("cancel close invalid load scroll toggle".split(" ").concat(bn));function Cu(e,t,n){var r=e.type||"unknown-event";e.currentTarget=n,pp(r,t,void 0,e),e.currentTarget=null}function Dc(e,t){t=(t&4)!==0;for(var n=0;n<e.length;n++){var r=e[n],l=r.event;r=r.listeners;e:{var i=void 0;if(t)for(var o=r.length-1;0<=o;o--){var s=r[o],u=s.instance,a=s.currentTarget;if(s=s.listener,u!==i&&l.isPropagationStopped())break e;Cu(l,s,a),i=u}else for(o=0;o<r.length;o++){if(s=r[o],u=s.instance,a=s.currentTarget,s=s.listener,u!==i&&l.isPropagationStopped())break e;Cu(l,s,a),i=u}}}if(El)throw e=ao,El=!1,ao=null,e}function H(e,t){var n=t[wo];n===void 0&&(n=t[wo]=new Set);var r=e+"__bubble";n.has(r)||(Fc(t,e,2,!1),n.add(r))}function Oi(e,t,n){var r=0;t&&(r|=4),Fc(n,e,r,t)}var Gr="_reactListening"+Math.random().toString(36).slice(2);function yr(e){if(!e[Gr]){e[Gr]=!0,Ha.forEach(function(n){n!=="selectionchange"&&(mh.has(n)||Oi(n,!1,e),Oi(n,!0,e))});var t=e.nodeType===9?e:e.ownerDocument;t===null||t[Gr]||(t[Gr]=!0,Oi("selectionchange",!1,t))}}function Fc(e,t,n,r){switch(wc(t)){case 1:var l=jp;break;case 4:l=Tp;break;default:l=cs}n=l.bind(null,t,n,e),l=void 0,!uo||t!=="touchstart"&&t!=="touchmove"&&t!=="wheel"||(l=!0),r?l!==void 0?e.addEventListener(t,n,{capture:!0,passive:l}):e.addEventListener(t,n,!0):l!==void 0?e.addEventListener(t,n,{passive:l}):e.addEventListener(t,n,!1)}function Li(e,t,n,r,l){var i=r;if(!(t&1)&&!(t&2)&&r!==null)e:for(;;){if(r===null)return;var o=r.tag;if(o===3||o===4){var s=r.stateNode.containerInfo;if(s===l||s.nodeType===8&&s.parentNode===l)break;if(o===4)for(o=r.return;o!==null;){var u=o.tag;if((u===3||u===4)&&(u=o.stateNode.containerInfo,u===l||u.nodeType===8&&u.parentNode===l))return;o=o.return}for(;s!==null;){if(o=$t(s),o===null)return;if(u=o.tag,u===5||u===6){r=i=o;continue e}s=s.parentNode}}r=r.return}oc(function(){var a=i,f=os(n),d=[];e:{var y=Ic.get(e);if(y!==void 0){var E=ds,m=e;switch(e){case"keypress":if(al(n)===0)break e;case"keydown":case"keyup":E=Qp;break;case"focusin":m="focus",E=Ni;break;case"focusout":m="blur",E=Ni;break;case"beforeblur":case"afterblur":E=Ni;break;case"click":if(n.button===2)break e;case"auxclick":case"dblclick":case"mousedown":case"mousemove":case"mouseup":case"mouseout":case"mouseover":case"contextmenu":E=du;break;case"drag":case"dragend":case"dragenter":case"dragexit":case"dragleave":case"dragover":case"dragstart":case"drop":E=zp;break;case"touchcancel":case"touchend":case"touchmove":case"touchstart":E=Xp;break;case Oc:case Lc:case zc:E=Dp;break;case Ac:E=Jp;break;case"scroll":E=Op;break;case"wheel":E=bp;break;case"copy":case"cut":case"paste":E=Mp;break;case"gotpointercapture":case"lostpointercapture":case"pointercancel":case"pointerdown":case"pointermove":case"pointerout":case"pointerover":case"pointerup":E=hu}var x=(t&4)!==0,S=!x&&e==="scroll",h=x?y!==null?y+"Capture":null:y;x=[];for(var c=a,p;c!==null;){p=c;var g=p.stateNode;if(p.tag===5&&g!==null&&(p=g,h!==null&&(g=cr(c,h),g!=null&&x.push(vr(c,g,p)))),S)break;c=c.return}0<x.length&&(y=new E(y,m,null,n,f),d.push({event:y,listeners:x}))}}if(!(t&7)){e:{if(y=e==="mouseover"||e==="pointerover",E=e==="mouseout"||e==="pointerout",y&&n!==oo&&(m=n.relatedTarget||n.fromElement)&&($t(m)||m[at]))break e;if((E||y)&&(y=f.window===f?f:(y=f.ownerDocument)?y.defaultView||y.parentWindow:window,E?(m=n.relatedTarget||n.toElement,E=a,m=m?$t(m):null,m!==null&&(S=tn(m),m!==S||m.tag!==5&&m.tag!==6)&&(m=null)):(E=null,m=a),E!==m)){if(x=du,g="onMouseLeave",h="onMouseEnter",c="mouse",(e==="pointerout"||e==="pointerover")&&(x=hu,g="onPointerLeave",h="onPointerEnter",c="pointer"),S=E==null?y:cn(E),p=m==null?y:cn(m),y=new x(g,c+"leave",E,n,f),y.target=S,y.relatedTarget=p,g=null,$t(f)===a&&(x=new x(h,c+"enter",m,n,f),x.target=p,x.relatedTarget=S,g=x),S=g,E&&m)t:{for(x=E,h=m,c=0,p=x;p;p=rn(p))c++;for(p=0,g=h;g;g=rn(g))p++;for(;0<c-p;)x=rn(x),c--;for(;0<p-c;)h=rn(h),p--;for(;c--;){if(x===h||h!==null&&x===h.alternate)break t;x=rn(x),h=rn(h)}x=null}else x=null;E!==null&&Nu(d,y,E,x,!1),m!==null&&S!==null&&Nu(d,S,m,x,!0)}}e:{if(y=a?cn(a):window,E=y.nodeName&&y.nodeName.toLowerCase(),E==="select"||E==="input"&&y.type==="file")var k=ih;else if(vu(y))if(Rc)k=ah;else{k=sh;var _=oh}else(E=y.nodeName)&&E.toLowerCase()==="input"&&(y.type==="checkbox"||y.type==="radio")&&(k=uh);if(k&&(k=k(e,a))){Nc(d,k,n,f);break e}_&&_(e,y,a),e==="focusout"&&(_=y._wrapperState)&&_.controlled&&y.type==="number"&&to(y,"number",y.value)}switch(_=a?cn(a):window,e){case"focusin":(vu(_)||_.contentEditable==="true")&&(un=_,ho=a,rr=null);break;case"focusout":rr=ho=un=null;break;case"mousedown":mo=!0;break;case"contextmenu":case"mouseup":case"dragend":mo=!1,Eu(d,n,f);break;case"selectionchange":if(dh)break;case"keydown":case"keyup":Eu(d,n,f)}var P;if(hs)e:{switch(e){case"compositionstart":var T="onCompositionStart";break e;case"compositionend":T="onCompositionEnd";break e;case"compositionupdate":T="onCompositionUpdate";break e}T=void 0}else sn?kc(e,n)&&(T="onCompositionEnd"):e==="keydown"&&n.keyCode===229&&(T="onCompositionStart");T&&(Ec&&n.locale!=="ko"&&(sn||T!=="onCompositionStart"?T==="onCompositionEnd"&&sn&&(P=Sc()):(xt=f,fs="value"in xt?xt.value:xt.textContent,sn=!0)),_=Pl(a,T),0<_.length&&(T=new pu(T,e,null,n,f),d.push({event:T,listeners:_}),P?T.data=P:(P=Cc(n),P!==null&&(T.data=P)))),(P=eh?th(e,n):nh(e,n))&&(a=Pl(a,"onBeforeInput"),0<a.length&&(f=new pu("onBeforeInput","beforeinput",null,n,f),d.push({event:f,listeners:a}),f.data=P))}Dc(d,t)})}function vr(e,t,n){return{instance:e,listener:t,currentTarget:n}}function Pl(e,t){for(var n=t+"Capture",r=[];e!==null;){var l=e,i=l.stateNode;l.tag===5&&i!==null&&(l=i,i=cr(e,n),i!=null&&r.unshift(vr(e,i,l)),i=cr(e,t),i!=null&&r.push(vr(e,i,l))),e=e.return}return r}function rn(e){if(e===null)return null;do e=e.return;while(e&&e.tag!==5);return e||null}function Nu(e,t,n,r,l){for(var i=t._reactName,o=[];n!==null&&n!==r;){var s=n,u=s.alternate,a=s.stateNode;if(u!==null&&u===r)break;s.tag===5&&a!==null&&(s=a,l?(u=cr(n,i),u!=null&&o.unshift(vr(n,u,s))):l||(u=cr(n,i),u!=null&&o.push(vr(n,u,s)))),n=n.return}o.length!==0&&e.push({event:t,listeners:o})}var yh=/\r\n?/g,vh=/\u0000|\uFFFD/g;function Ru(e){return(typeof e=="string"?e:""+e).replace(yh,`
`).replace(vh,"")}function Xr(e,t,n){if(t=Ru(t),Ru(e)!==t&&n)throw Error(C(425))}function _l(){}var yo=null,vo=null;function go(e,t){return e==="textarea"||e==="noscript"||typeof t.children=="string"||typeof t.children=="number"||typeof t.dangerouslySetInnerHTML=="object"&&t.dangerouslySetInnerHTML!==null&&t.dangerouslySetInnerHTML.__html!=null}var xo=typeof setTimeout=="function"?setTimeout:void 0,gh=typeof clearTimeout=="function"?clearTimeout:void 0,Pu=typeof Promise=="function"?Promise:void 0,xh=typeof queueMicrotask=="function"?queueMicrotask:typeof Pu<"u"?function(e){return Pu.resolve(null).then(e).catch(wh)}:xo;function wh(e){setTimeout(function(){throw e})}function zi(e,t){var n=t,r=0;do{var l=n.nextSibling;if(e.removeChild(n),l&&l.nodeType===8)if(n=l.data,n==="/$"){if(r===0){e.removeChild(l),pr(t);return}r--}else n!=="$"&&n!=="$?"&&n!=="$!"||r++;n=l}while(n);pr(t)}function Nt(e){for(;e!=null;e=e.nextSibling){var t=e.nodeType;if(t===1||t===3)break;if(t===8){if(t=e.data,t==="$"||t==="$!"||t==="$?")break;if(t==="/$")return null}}return e}function _u(e){e=e.previousSibling;for(var t=0;e;){if(e.nodeType===8){var n=e.data;if(n==="$"||n==="$!"||n==="$?"){if(t===0)return e;t--}else n==="/$"&&t++}e=e.previousSibling}return null}var An=Math.random().toString(36).slice(2),et="__reactFiber$"+An,gr="__reactProps$"+An,at="__reactContainer$"+An,wo="__reactEvents$"+An,Sh="__reactListeners$"+An,Eh="__reactHandles$"+An;function $t(e){var t=e[et];if(t)return t;for(var n=e.parentNode;n;){if(t=n[at]||n[et]){if(n=t.alternate,t.child!==null||n!==null&&n.child!==null)for(e=_u(e);e!==null;){if(n=e[et])return n;e=_u(e)}return t}e=n,n=e.parentNode}return null}function Tr(e){return e=e[et]||e[at],!e||e.tag!==5&&e.tag!==6&&e.tag!==13&&e.tag!==3?null:e}function cn(e){if(e.tag===5||e.tag===6)return e.stateNode;throw Error(C(33))}function bl(e){return e[gr]||null}var So=[],fn=-1;function At(e){return{current:e}}function Q(e){0>fn||(e.current=So[fn],So[fn]=null,fn--)}function V(e,t){fn++,So[fn]=e.current,e.current=t}var Lt={},he=At(Lt),ke=At(!1),Xt=Lt;function Cn(e,t){var n=e.type.contextTypes;if(!n)return Lt;var r=e.stateNode;if(r&&r.__reactInternalMemoizedUnmaskedChildContext===t)return r.__reactInternalMemoizedMaskedChildContext;var l={},i;for(i in n)l[i]=t[i];return r&&(e=e.stateNode,e.__reactInternalMemoizedUnmaskedChildContext=t,e.__reactInternalMemoizedMaskedChildContext=l),l}function Ce(e){return e=e.childContextTypes,e!=null}function jl(){Q(ke),Q(he)}function ju(e,t,n){if(he.current!==Lt)throw Error(C(168));V(he,t),V(ke,n)}function Mc(e,t,n){var r=e.stateNode;if(t=t.childContextTypes,typeof r.getChildContext!="function")return n;r=r.getChildContext();for(var l in r)if(!(l in t))throw Error(C(108,op(e)||"Unknown",l));return q({},n,r)}function Tl(e){return e=(e=e.stateNode)&&e.__reactInternalMemoizedMergedChildContext||Lt,Xt=he.current,V(he,e),V(ke,ke.current),!0}function Tu(e,t,n){var r=e.stateNode;if(!r)throw Error(C(169));n?(e=Mc(e,t,Xt),r.__reactInternalMemoizedMergedChildContext=e,Q(ke),Q(he),V(he,e)):Q(ke),V(ke,n)}var lt=null,Zl=!1,Ai=!1;function Uc(e){lt===null?lt=[e]:lt.push(e)}function kh(e){Zl=!0,Uc(e)}function It(){if(!Ai&&lt!==null){Ai=!0;var e=0,t=$;try{var n=lt;for($=1;e<n.length;e++){var r=n[e];do r=r(!0);while(r!==null)}lt=null,Zl=!1}catch(l){throw lt!==null&&(lt=lt.slice(e+1)),cc(ss,It),l}finally{$=t,Ai=!1}}return null}var dn=[],pn=0,Ol=null,Ll=0,Fe=[],Me=0,qt=null,it=1,ot="";function Ut(e,t){dn[pn++]=Ll,dn[pn++]=Ol,Ol=e,Ll=t}function Bc(e,t,n){Fe[Me++]=it,Fe[Me++]=ot,Fe[Me++]=qt,qt=e;var r=it;e=ot;var l=32-Ge(r)-1;r&=~(1<<l),n+=1;var i=32-Ge(t)+l;if(30<i){var o=l-l%5;i=(r&(1<<o)-1).toString(32),r>>=o,l-=o,it=1<<32-Ge(t)+l|n<<l|r,ot=i+e}else it=1<<i|n<<l|r,ot=e}function ys(e){e.return!==null&&(Ut(e,1),Bc(e,1,0))}function vs(e){for(;e===Ol;)Ol=dn[--pn],dn[pn]=null,Ll=dn[--pn],dn[pn]=null;for(;e===qt;)qt=Fe[--Me],Fe[Me]=null,ot=Fe[--Me],Fe[Me]=null,it=Fe[--Me],Fe[Me]=null}var Le=null,Oe=null,K=!1,Ke=null;function $c(e,t){var n=Ue(5,null,null,0);n.elementType="DELETED",n.stateNode=t,n.return=e,t=e.deletions,t===null?(e.deletions=[n],e.flags|=16):t.push(n)}function Ou(e,t){switch(e.tag){case 5:var n=e.type;return t=t.nodeType!==1||n.toLowerCase()!==t.nodeName.toLowerCase()?null:t,t!==null?(e.stateNode=t,Le=e,Oe=Nt(t.firstChild),!0):!1;case 6:return t=e.pendingProps===""||t.nodeType!==3?null:t,t!==null?(e.stateNode=t,Le=e,Oe=null,!0):!1;case 13:return t=t.nodeType!==8?null:t,t!==null?(n=qt!==null?{id:it,overflow:ot}:null,e.memoizedState={dehydrated:t,treeContext:n,retryLane:1073741824},n=Ue(18,null,null,0),n.stateNode=t,n.return=e,e.child=n,Le=e,Oe=null,!0):!1;default:return!1}}function Eo(e){return(e.mode&1)!==0&&(e.flags&128)===0}function ko(e){if(K){var t=Oe;if(t){var n=t;if(!Ou(e,t)){if(Eo(e))throw Error(C(418));t=Nt(n.nextSibling);var r=Le;t&&Ou(e,t)?$c(r,n):(e.flags=e.flags&-4097|2,K=!1,Le=e)}}else{if(Eo(e))throw Error(C(418));e.flags=e.flags&-4097|2,K=!1,Le=e}}}function Lu(e){for(e=e.return;e!==null&&e.tag!==5&&e.tag!==3&&e.tag!==13;)e=e.return;Le=e}function qr(e){if(e!==Le)return!1;if(!K)return Lu(e),K=!0,!1;var t;if((t=e.tag!==3)&&!(t=e.tag!==5)&&(t=e.type,t=t!=="head"&&t!=="body"&&!go(e.type,e.memoizedProps)),t&&(t=Oe)){if(Eo(e))throw Vc(),Error(C(418));for(;t;)$c(e,t),t=Nt(t.nextSibling)}if(Lu(e),e.tag===13){if(e=e.memoizedState,e=e!==null?e.dehydrated:null,!e)throw Error(C(317));e:{for(e=e.nextSibling,t=0;e;){if(e.nodeType===8){var n=e.data;if(n==="/$"){if(t===0){Oe=Nt(e.nextSibling);break e}t--}else n!=="$"&&n!=="$!"&&n!=="$?"||t++}e=e.nextSibling}Oe=null}}else Oe=Le?Nt(e.stateNode.nextSibling):null;return!0}function Vc(){for(var e=Oe;e;)e=Nt(e.nextSibling)}function Nn(){Oe=Le=null,K=!1}function gs(e){Ke===null?Ke=[e]:Ke.push(e)}var Ch=dt.ReactCurrentBatchConfig;function Hn(e,t,n){if(e=n.ref,e!==null&&typeof e!="function"&&typeof e!="object"){if(n._owner){if(n=n._owner,n){if(n.tag!==1)throw Error(C(309));var r=n.stateNode}if(!r)throw Error(C(147,e));var l=r,i=""+e;return t!==null&&t.ref!==null&&typeof t.ref=="function"&&t.ref._stringRef===i?t.ref:(t=function(o){var s=l.refs;o===null?delete s[i]:s[i]=o},t._stringRef=i,t)}if(typeof e!="string")throw Error(C(284));if(!n._owner)throw Error(C(290,e))}return e}function Jr(e,t){throw e=Object.prototype.toString.call(t),Error(C(31,e==="[object Object]"?"object with keys {"+Object.keys(t).join(", ")+"}":e))}function zu(e){var t=e._init;return t(e._payload)}function Wc(e){function t(h,c){if(e){var p=h.deletions;p===null?(h.deletions=[c],h.flags|=16):p.push(c)}}function n(h,c){if(!e)return null;for(;c!==null;)t(h,c),c=c.sibling;return null}function r(h,c){for(h=new Map;c!==null;)c.key!==null?h.set(c.key,c):h.set(c.index,c),c=c.sibling;return h}function l(h,c){return h=jt(h,c),h.index=0,h.sibling=null,h}function i(h,c,p){return h.index=p,e?(p=h.alternate,p!==null?(p=p.index,p<c?(h.flags|=2,c):p):(h.flags|=2,c)):(h.flags|=1048576,c)}function o(h){return e&&h.alternate===null&&(h.flags|=2),h}function s(h,c,p,g){return c===null||c.tag!==6?(c=$i(p,h.mode,g),c.return=h,c):(c=l(c,p),c.return=h,c)}function u(h,c,p,g){var k=p.type;return k===on?f(h,c,p.props.children,g,p.key):c!==null&&(c.elementType===k||typeof k=="object"&&k!==null&&k.$$typeof===mt&&zu(k)===c.type)?(g=l(c,p.props),g.ref=Hn(h,c,p),g.return=h,g):(g=yl(p.type,p.key,p.props,null,h.mode,g),g.ref=Hn(h,c,p),g.return=h,g)}function a(h,c,p,g){return c===null||c.tag!==4||c.stateNode.containerInfo!==p.containerInfo||c.stateNode.implementation!==p.implementation?(c=Vi(p,h.mode,g),c.return=h,c):(c=l(c,p.children||[]),c.return=h,c)}function f(h,c,p,g,k){return c===null||c.tag!==7?(c=Kt(p,h.mode,g,k),c.return=h,c):(c=l(c,p),c.return=h,c)}function d(h,c,p){if(typeof c=="string"&&c!==""||typeof c=="number")return c=$i(""+c,h.mode,p),c.return=h,c;if(typeof c=="object"&&c!==null){switch(c.$$typeof){case Ur:return p=yl(c.type,c.key,c.props,null,h.mode,p),p.ref=Hn(h,null,c),p.return=h,p;case ln:return c=Vi(c,h.mode,p),c.return=h,c;case mt:var g=c._init;return d(h,g(c._payload),p)}if(Jn(c)||Un(c))return c=Kt(c,h.mode,p,null),c.return=h,c;Jr(h,c)}return null}function y(h,c,p,g){var k=c!==null?c.key:null;if(typeof p=="string"&&p!==""||typeof p=="number")return k!==null?null:s(h,c,""+p,g);if(typeof p=="object"&&p!==null){switch(p.$$typeof){case Ur:return p.key===k?u(h,c,p,g):null;case ln:return p.key===k?a(h,c,p,g):null;case mt:return k=p._init,y(h,c,k(p._payload),g)}if(Jn(p)||Un(p))return k!==null?null:f(h,c,p,g,null);Jr(h,p)}return null}function E(h,c,p,g,k){if(typeof g=="string"&&g!==""||typeof g=="number")return h=h.get(p)||null,s(c,h,""+g,k);if(typeof g=="object"&&g!==null){switch(g.$$typeof){case Ur:return h=h.get(g.key===null?p:g.key)||null,u(c,h,g,k);case ln:return h=h.get(g.key===null?p:g.key)||null,a(c,h,g,k);case mt:var _=g._init;return E(h,c,p,_(g._payload),k)}if(Jn(g)||Un(g))return h=h.get(p)||null,f(c,h,g,k,null);Jr(c,g)}return null}function m(h,c,p,g){for(var k=null,_=null,P=c,T=c=0,M=null;P!==null&&T<p.length;T++){P.index>T?(M=P,P=null):M=P.sibling;var L=y(h,P,p[T],g);if(L===null){P===null&&(P=M);break}e&&P&&L.alternate===null&&t(h,P),c=i(L,c,T),_===null?k=L:_.sibling=L,_=L,P=M}if(T===p.length)return n(h,P),K&&Ut(h,T),k;if(P===null){for(;T<p.length;T++)P=d(h,p[T],g),P!==null&&(c=i(P,c,T),_===null?k=P:_.sibling=P,_=P);return K&&Ut(h,T),k}for(P=r(h,P);T<p.length;T++)M=E(P,h,T,p[T],g),M!==null&&(e&&M.alternate!==null&&P.delete(M.key===null?T:M.key),c=i(M,c,T),_===null?k=M:_.sibling=M,_=M);return e&&P.forEach(function(te){return t(h,te)}),K&&Ut(h,T),k}function x(h,c,p,g){var k=Un(p);if(typeof k!="function")throw Error(C(150));if(p=k.call(p),p==null)throw Error(C(151));for(var _=k=null,P=c,T=c=0,M=null,L=p.next();P!==null&&!L.done;T++,L=p.next()){P.index>T?(M=P,P=null):M=P.sibling;var te=y(h,P,L.value,g);if(te===null){P===null&&(P=M);break}e&&P&&te.alternate===null&&t(h,P),c=i(te,c,T),_===null?k=te:_.sibling=te,_=te,P=M}if(L.done)return n(h,P),K&&Ut(h,T),k;if(P===null){for(;!L.done;T++,L=p.next())L=d(h,L.value,g),L!==null&&(c=i(L,c,T),_===null?k=L:_.sibling=L,_=L);return K&&Ut(h,T),k}for(P=r(h,P);!L.done;T++,L=p.next())L=E(P,h,T,L.value,g),L!==null&&(e&&L.alternate!==null&&P.delete(L.key===null?T:L.key),c=i(L,c,T),_===null?k=L:_.sibling=L,_=L);return e&&P.forEach(function(_e){return t(h,_e)}),K&&Ut(h,T),k}function S(h,c,p,g){if(typeof p=="object"&&p!==null&&p.type===on&&p.key===null&&(p=p.props.children),typeof p=="object"&&p!==null){switch(p.$$typeof){case Ur:e:{for(var k=p.key,_=c;_!==null;){if(_.key===k){if(k=p.type,k===on){if(_.tag===7){n(h,_.sibling),c=l(_,p.props.children),c.return=h,h=c;break e}}else if(_.elementType===k||typeof k=="object"&&k!==null&&k.$$typeof===mt&&zu(k)===_.type){n(h,_.sibling),c=l(_,p.props),c.ref=Hn(h,_,p),c.return=h,h=c;break e}n(h,_);break}else t(h,_);_=_.sibling}p.type===on?(c=Kt(p.props.children,h.mode,g,p.key),c.return=h,h=c):(g=yl(p.type,p.key,p.props,null,h.mode,g),g.ref=Hn(h,c,p),g.return=h,h=g)}return o(h);case ln:e:{for(_=p.key;c!==null;){if(c.key===_)if(c.tag===4&&c.stateNode.containerInfo===p.containerInfo&&c.stateNode.implementation===p.implementation){n(h,c.sibling),c=l(c,p.children||[]),c.return=h,h=c;break e}else{n(h,c);break}else t(h,c);c=c.sibling}c=Vi(p,h.mode,g),c.return=h,h=c}return o(h);case mt:return _=p._init,S(h,c,_(p._payload),g)}if(Jn(p))return m(h,c,p,g);if(Un(p))return x(h,c,p,g);Jr(h,p)}return typeof p=="string"&&p!==""||typeof p=="number"?(p=""+p,c!==null&&c.tag===6?(n(h,c.sibling),c=l(c,p),c.return=h,h=c):(n(h,c),c=$i(p,h.mode,g),c.return=h,h=c),o(h)):n(h,c)}return S}var Rn=Wc(!0),Hc=Wc(!1),zl=At(null),Al=null,hn=null,xs=null;function ws(){xs=hn=Al=null}function Ss(e){var t=zl.current;Q(zl),e._currentValue=t}function Co(e,t,n){for(;e!==null;){var r=e.alternate;if((e.childLanes&t)!==t?(e.childLanes|=t,r!==null&&(r.childLanes|=t)):r!==null&&(r.childLanes&t)!==t&&(r.childLanes|=t),e===n)break;e=e.return}}function Sn(e,t){Al=e,xs=hn=null,e=e.dependencies,e!==null&&e.firstContext!==null&&(e.lanes&t&&(Ee=!0),e.firstContext=null)}function $e(e){var t=e._currentValue;if(xs!==e)if(e={context:e,memoizedValue:t,next:null},hn===null){if(Al===null)throw Error(C(308));hn=e,Al.dependencies={lanes:0,firstContext:e}}else hn=hn.next=e;return t}var Vt=null;function Es(e){Vt===null?Vt=[e]:Vt.push(e)}function Qc(e,t,n,r){var l=t.interleaved;return l===null?(n.next=n,Es(t)):(n.next=l.next,l.next=n),t.interleaved=n,ct(e,r)}function ct(e,t){e.lanes|=t;var n=e.alternate;for(n!==null&&(n.lanes|=t),n=e,e=e.return;e!==null;)e.childLanes|=t,n=e.alternate,n!==null&&(n.childLanes|=t),n=e,e=e.return;return n.tag===3?n.stateNode:null}var yt=!1;function ks(e){e.updateQueue={baseState:e.memoizedState,firstBaseUpdate:null,lastBaseUpdate:null,shared:{pending:null,interleaved:null,lanes:0},effects:null}}function Kc(e,t){e=e.updateQueue,t.updateQueue===e&&(t.updateQueue={baseState:e.baseState,firstBaseUpdate:e.firstBaseUpdate,lastBaseUpdate:e.lastBaseUpdate,shared:e.shared,effects:e.effects})}function st(e,t){return{eventTime:e,lane:t,tag:0,payload:null,callback:null,next:null}}function Rt(e,t,n){var r=e.updateQueue;if(r===null)return null;if(r=r.shared,F&2){var l=r.pending;return l===null?t.next=t:(t.next=l.next,l.next=t),r.pending=t,ct(e,n)}return l=r.interleaved,l===null?(t.next=t,Es(r)):(t.next=l.next,l.next=t),r.interleaved=t,ct(e,n)}function cl(e,t,n){if(t=t.updateQueue,t!==null&&(t=t.shared,(n&4194240)!==0)){var r=t.lanes;r&=e.pendingLanes,n|=r,t.lanes=n,us(e,n)}}function Au(e,t){var n=e.updateQueue,r=e.alternate;if(r!==null&&(r=r.updateQueue,n===r)){var l=null,i=null;if(n=n.firstBaseUpdate,n!==null){do{var o={eventTime:n.eventTime,lane:n.lane,tag:n.tag,payload:n.payload,callback:n.callback,next:null};i===null?l=i=o:i=i.next=o,n=n.next}while(n!==null);i===null?l=i=t:i=i.next=t}else l=i=t;n={baseState:r.baseState,firstBaseUpdate:l,lastBaseUpdate:i,shared:r.shared,effects:r.effects},e.updateQueue=n;return}e=n.lastBaseUpdate,e===null?n.firstBaseUpdate=t:e.next=t,n.lastBaseUpdate=t}function Il(e,t,n,r){var l=e.updateQueue;yt=!1;var i=l.firstBaseUpdate,o=l.lastBaseUpdate,s=l.shared.pending;if(s!==null){l.shared.pending=null;var u=s,a=u.next;u.next=null,o===null?i=a:o.next=a,o=u;var f=e.alternate;f!==null&&(f=f.updateQueue,s=f.lastBaseUpdate,s!==o&&(s===null?f.firstBaseUpdate=a:s.next=a,f.lastBaseUpdate=u))}if(i!==null){var d=l.baseState;o=0,f=a=u=null,s=i;do{var y=s.lane,E=s.eventTime;if((r&y)===y){f!==null&&(f=f.next={eventTime:E,lane:0,tag:s.tag,payload:s.payload,callback:s.callback,next:null});e:{var m=e,x=s;switch(y=t,E=n,x.tag){case 1:if(m=x.payload,typeof m=="function"){d=m.call(E,d,y);break e}d=m;break e;case 3:m.flags=m.flags&-65537|128;case 0:if(m=x.payload,y=typeof m=="function"?m.call(E,d,y):m,y==null)break e;d=q({},d,y);break e;case 2:yt=!0}}s.callback!==null&&s.lane!==0&&(e.flags|=64,y=l.effects,y===null?l.effects=[s]:y.push(s))}else E={eventTime:E,lane:y,tag:s.tag,payload:s.payload,callback:s.callback,next:null},f===null?(a=f=E,u=d):f=f.next=E,o|=y;if(s=s.next,s===null){if(s=l.shared.pending,s===null)break;y=s,s=y.next,y.next=null,l.lastBaseUpdate=y,l.shared.pending=null}}while(!0);if(f===null&&(u=d),l.baseState=u,l.firstBaseUpdate=a,l.lastBaseUpdate=f,t=l.shared.interleaved,t!==null){l=t;do o|=l.lane,l=l.next;while(l!==t)}else i===null&&(l.shared.lanes=0);Yt|=o,e.lanes=o,e.memoizedState=d}}function Iu(e,t,n){if(e=t.effects,t.effects=null,e!==null)for(t=0;t<e.length;t++){var r=e[t],l=r.callback;if(l!==null){if(r.callback=null,r=n,typeof l!="function")throw Error(C(191,l));l.call(r)}}}var Or={},nt=At(Or),xr=At(Or),wr=At(Or);function Wt(e){if(e===Or)throw Error(C(174));return e}function Cs(e,t){switch(V(wr,t),V(xr,e),V(nt,Or),e=t.nodeType,e){case 9:case 11:t=(t=t.documentElement)?t.namespaceURI:ro(null,"");break;default:e=e===8?t.parentNode:t,t=e.namespaceURI||null,e=e.tagName,t=ro(t,e)}Q(nt),V(nt,t)}function Pn(){Q(nt),Q(xr),Q(wr)}function Gc(e){Wt(wr.current);var t=Wt(nt.current),n=ro(t,e.type);t!==n&&(V(xr,e),V(nt,n))}function Ns(e){xr.current===e&&(Q(nt),Q(xr))}var G=At(0);function Dl(e){for(var t=e;t!==null;){if(t.tag===13){var n=t.memoizedState;if(n!==null&&(n=n.dehydrated,n===null||n.data==="$?"||n.data==="$!"))return t}else if(t.tag===19&&t.memoizedProps.revealOrder!==void 0){if(t.flags&128)return t}else if(t.child!==null){t.child.return=t,t=t.child;continue}if(t===e)break;for(;t.sibling===null;){if(t.return===null||t.return===e)return null;t=t.return}t.sibling.return=t.return,t=t.sibling}return null}var Ii=[];function Rs(){for(var e=0;e<Ii.length;e++)Ii[e]._workInProgressVersionPrimary=null;Ii.length=0}var fl=dt.ReactCurrentDispatcher,Di=dt.ReactCurrentBatchConfig,Jt=0,X=null,ne=null,le=null,Fl=!1,lr=!1,Sr=0,Nh=0;function ce(){throw Error(C(321))}function Ps(e,t){if(t===null)return!1;for(var n=0;n<t.length&&n<e.length;n++)if(!qe(e[n],t[n]))return!1;return!0}function _s(e,t,n,r,l,i){if(Jt=i,X=t,t.memoizedState=null,t.updateQueue=null,t.lanes=0,fl.current=e===null||e.memoizedState===null?jh:Th,e=n(r,l),lr){i=0;do{if(lr=!1,Sr=0,25<=i)throw Error(C(301));i+=1,le=ne=null,t.updateQueue=null,fl.current=Oh,e=n(r,l)}while(lr)}if(fl.current=Ml,t=ne!==null&&ne.next!==null,Jt=0,le=ne=X=null,Fl=!1,t)throw Error(C(300));return e}function js(){var e=Sr!==0;return Sr=0,e}function Ze(){var e={memoizedState:null,baseState:null,baseQueue:null,queue:null,next:null};return le===null?X.memoizedState=le=e:le=le.next=e,le}function Ve(){if(ne===null){var e=X.alternate;e=e!==null?e.memoizedState:null}else e=ne.next;var t=le===null?X.memoizedState:le.next;if(t!==null)le=t,ne=e;else{if(e===null)throw Error(C(310));ne=e,e={memoizedState:ne.memoizedState,baseState:ne.baseState,baseQueue:ne.baseQueue,queue:ne.queue,next:null},le===null?X.memoizedState=le=e:le=le.next=e}return le}function Er(e,t){return typeof t=="function"?t(e):t}function Fi(e){var t=Ve(),n=t.queue;if(n===null)throw Error(C(311));n.lastRenderedReducer=e;var r=ne,l=r.baseQueue,i=n.pending;if(i!==null){if(l!==null){var o=l.next;l.next=i.next,i.next=o}r.baseQueue=l=i,n.pending=null}if(l!==null){i=l.next,r=r.baseState;var s=o=null,u=null,a=i;do{var f=a.lane;if((Jt&f)===f)u!==null&&(u=u.next={lane:0,action:a.action,hasEagerState:a.hasEagerState,eagerState:a.eagerState,next:null}),r=a.hasEagerState?a.eagerState:e(r,a.action);else{var d={lane:f,action:a.action,hasEagerState:a.hasEagerState,eagerState:a.eagerState,next:null};u===null?(s=u=d,o=r):u=u.next=d,X.lanes|=f,Yt|=f}a=a.next}while(a!==null&&a!==i);u===null?o=r:u.next=s,qe(r,t.memoizedState)||(Ee=!0),t.memoizedState=r,t.baseState=o,t.baseQueue=u,n.lastRenderedState=r}if(e=n.interleaved,e!==null){l=e;do i=l.lane,X.lanes|=i,Yt|=i,l=l.next;while(l!==e)}else l===null&&(n.lanes=0);return[t.memoizedState,n.dispatch]}function Mi(e){var t=Ve(),n=t.queue;if(n===null)throw Error(C(311));n.lastRenderedReducer=e;var r=n.dispatch,l=n.pending,i=t.memoizedState;if(l!==null){n.pending=null;var o=l=l.next;do i=e(i,o.action),o=o.next;while(o!==l);qe(i,t.memoizedState)||(Ee=!0),t.memoizedState=i,t.baseQueue===null&&(t.baseState=i),n.lastRenderedState=i}return[i,r]}function Xc(){}function qc(e,t){var n=X,r=Ve(),l=t(),i=!qe(r.memoizedState,l);if(i&&(r.memoizedState=l,Ee=!0),r=r.queue,Ts(bc.bind(null,n,r,e),[e]),r.getSnapshot!==t||i||le!==null&&le.memoizedState.tag&1){if(n.flags|=2048,kr(9,Yc.bind(null,n,r,l,t),void 0,null),ie===null)throw Error(C(349));Jt&30||Jc(n,t,l)}return l}function Jc(e,t,n){e.flags|=16384,e={getSnapshot:t,value:n},t=X.updateQueue,t===null?(t={lastEffect:null,stores:null},X.updateQueue=t,t.stores=[e]):(n=t.stores,n===null?t.stores=[e]:n.push(e))}function Yc(e,t,n,r){t.value=n,t.getSnapshot=r,Zc(t)&&ef(e)}function bc(e,t,n){return n(function(){Zc(t)&&ef(e)})}function Zc(e){var t=e.getSnapshot;e=e.value;try{var n=t();return!qe(e,n)}catch{return!0}}function ef(e){var t=ct(e,1);t!==null&&Xe(t,e,1,-1)}function Du(e){var t=Ze();return typeof e=="function"&&(e=e()),t.memoizedState=t.baseState=e,e={pending:null,interleaved:null,lanes:0,dispatch:null,lastRenderedReducer:Er,lastRenderedState:e},t.queue=e,e=e.dispatch=_h.bind(null,X,e),[t.memoizedState,e]}function kr(e,t,n,r){return e={tag:e,create:t,destroy:n,deps:r,next:null},t=X.updateQueue,t===null?(t={lastEffect:null,stores:null},X.updateQueue=t,t.lastEffect=e.next=e):(n=t.lastEffect,n===null?t.lastEffect=e.next=e:(r=n.next,n.next=e,e.next=r,t.lastEffect=e)),e}function tf(){return Ve().memoizedState}function dl(e,t,n,r){var l=Ze();X.flags|=e,l.memoizedState=kr(1|t,n,void 0,r===void 0?null:r)}function ei(e,t,n,r){var l=Ve();r=r===void 0?null:r;var i=void 0;if(ne!==null){var o=ne.memoizedState;if(i=o.destroy,r!==null&&Ps(r,o.deps)){l.memoizedState=kr(t,n,i,r);return}}X.flags|=e,l.memoizedState=kr(1|t,n,i,r)}function Fu(e,t){return dl(8390656,8,e,t)}function Ts(e,t){return ei(2048,8,e,t)}function nf(e,t){return ei(4,2,e,t)}function rf(e,t){return ei(4,4,e,t)}function lf(e,t){if(typeof t=="function")return e=e(),t(e),function(){t(null)};if(t!=null)return e=e(),t.current=e,function(){t.current=null}}function of(e,t,n){return n=n!=null?n.concat([e]):null,ei(4,4,lf.bind(null,t,e),n)}function Os(){}function sf(e,t){var n=Ve();t=t===void 0?null:t;var r=n.memoizedState;return r!==null&&t!==null&&Ps(t,r[1])?r[0]:(n.memoizedState=[e,t],e)}function uf(e,t){var n=Ve();t=t===void 0?null:t;var r=n.memoizedState;return r!==null&&t!==null&&Ps(t,r[1])?r[0]:(e=e(),n.memoizedState=[e,t],e)}function af(e,t,n){return Jt&21?(qe(n,t)||(n=pc(),X.lanes|=n,Yt|=n,e.baseState=!0),t):(e.baseState&&(e.baseState=!1,Ee=!0),e.memoizedState=n)}function Rh(e,t){var n=$;$=n!==0&&4>n?n:4,e(!0);var r=Di.transition;Di.transition={};try{e(!1),t()}finally{$=n,Di.transition=r}}function cf(){return Ve().memoizedState}function Ph(e,t,n){var r=_t(e);if(n={lane:r,action:n,hasEagerState:!1,eagerState:null,next:null},ff(e))df(t,n);else if(n=Qc(e,t,n,r),n!==null){var l=ve();Xe(n,e,r,l),pf(n,t,r)}}function _h(e,t,n){var r=_t(e),l={lane:r,action:n,hasEagerState:!1,eagerState:null,next:null};if(ff(e))df(t,l);else{var i=e.alternate;if(e.lanes===0&&(i===null||i.lanes===0)&&(i=t.lastRenderedReducer,i!==null))try{var o=t.lastRenderedState,s=i(o,n);if(l.hasEagerState=!0,l.eagerState=s,qe(s,o)){var u=t.interleaved;u===null?(l.next=l,Es(t)):(l.next=u.next,u.next=l),t.interleaved=l;return}}catch{}finally{}n=Qc(e,t,l,r),n!==null&&(l=ve(),Xe(n,e,r,l),pf(n,t,r))}}function ff(e){var t=e.alternate;return e===X||t!==null&&t===X}function df(e,t){lr=Fl=!0;var n=e.pending;n===null?t.next=t:(t.next=n.next,n.next=t),e.pending=t}function pf(e,t,n){if(n&4194240){var r=t.lanes;r&=e.pendingLanes,n|=r,t.lanes=n,us(e,n)}}var Ml={readContext:$e,useCallback:ce,useContext:ce,useEffect:ce,useImperativeHandle:ce,useInsertionEffect:ce,useLayoutEffect:ce,useMemo:ce,useReducer:ce,useRef:ce,useState:ce,useDebugValue:ce,useDeferredValue:ce,useTransition:ce,useMutableSource:ce,useSyncExternalStore:ce,useId:ce,unstable_isNewReconciler:!1},jh={readContext:$e,useCallback:function(e,t){return Ze().memoizedState=[e,t===void 0?null:t],e},useContext:$e,useEffect:Fu,useImperativeHandle:function(e,t,n){return n=n!=null?n.concat([e]):null,dl(4194308,4,lf.bind(null,t,e),n)},useLayoutEffect:function(e,t){return dl(4194308,4,e,t)},useInsertionEffect:function(e,t){return dl(4,2,e,t)},useMemo:function(e,t){var n=Ze();return t=t===void 0?null:t,e=e(),n.memoizedState=[e,t],e},useReducer:function(e,t,n){var r=Ze();return t=n!==void 0?n(t):t,r.memoizedState=r.baseState=t,e={pending:null,interleaved:null,lanes:0,dispatch:null,lastRenderedReducer:e,lastRenderedState:t},r.queue=e,e=e.dispatch=Ph.bind(null,X,e),[r.memoizedState,e]},useRef:function(e){var t=Ze();return e={current:e},t.memoizedState=e},useState:Du,useDebugValue:Os,useDeferredValue:function(e){return Ze().memoizedState=e},useTransition:function(){var e=Du(!1),t=e[0];return e=Rh.bind(null,e[1]),Ze().memoizedState=e,[t,e]},useMutableSource:function(){},useSyncExternalStore:function(e,t,n){var r=X,l=Ze();if(K){if(n===void 0)throw Error(C(407));n=n()}else{if(n=t(),ie===null)throw Error(C(349));Jt&30||Jc(r,t,n)}l.memoizedState=n;var i={value:n,getSnapshot:t};return l.queue=i,Fu(bc.bind(null,r,i,e),[e]),r.flags|=2048,kr(9,Yc.bind(null,r,i,n,t),void 0,null),n},useId:function(){var e=Ze(),t=ie.identifierPrefix;if(K){var n=ot,r=it;n=(r&~(1<<32-Ge(r)-1)).toString(32)+n,t=":"+t+"R"+n,n=Sr++,0<n&&(t+="H"+n.toString(32)),t+=":"}else n=Nh++,t=":"+t+"r"+n.toString(32)+":";return e.memoizedState=t},unstable_isNewReconciler:!1},Th={readContext:$e,useCallback:sf,useContext:$e,useEffect:Ts,useImperativeHandle:of,useInsertionEffect:nf,useLayoutEffect:rf,useMemo:uf,useReducer:Fi,useRef:tf,useState:function(){return Fi(Er)},useDebugValue:Os,useDeferredValue:function(e){var t=Ve();return af(t,ne.memoizedState,e)},useTransition:function(){var e=Fi(Er)[0],t=Ve().memoizedState;return[e,t]},useMutableSource:Xc,useSyncExternalStore:qc,useId:cf,unstable_isNewReconciler:!1},Oh={readContext:$e,useCallback:sf,useContext:$e,useEffect:Ts,useImperativeHandle:of,useInsertionEffect:nf,useLayoutEffect:rf,useMemo:uf,useReducer:Mi,useRef:tf,useState:function(){return Mi(Er)},useDebugValue:Os,useDeferredValue:function(e){var t=Ve();return ne===null?t.memoizedState=e:af(t,ne.memoizedState,e)},useTransition:function(){var e=Mi(Er)[0],t=Ve().memoizedState;return[e,t]},useMutableSource:Xc,useSyncExternalStore:qc,useId:cf,unstable_isNewReconciler:!1};function He(e,t){if(e&&e.defaultProps){t=q({},t),e=e.defaultProps;for(var n in e)t[n]===void 0&&(t[n]=e[n]);return t}return t}function No(e,t,n,r){t=e.memoizedState,n=n(r,t),n=n==null?t:q({},t,n),e.memoizedState=n,e.lanes===0&&(e.updateQueue.baseState=n)}var ti={isMounted:function(e){return(e=e._reactInternals)?tn(e)===e:!1},enqueueSetState:function(e,t,n){e=e._reactInternals;var r=ve(),l=_t(e),i=st(r,l);i.payload=t,n!=null&&(i.callback=n),t=Rt(e,i,l),t!==null&&(Xe(t,e,l,r),cl(t,e,l))},enqueueReplaceState:function(e,t,n){e=e._reactInternals;var r=ve(),l=_t(e),i=st(r,l);i.tag=1,i.payload=t,n!=null&&(i.callback=n),t=Rt(e,i,l),t!==null&&(Xe(t,e,l,r),cl(t,e,l))},enqueueForceUpdate:function(e,t){e=e._reactInternals;var n=ve(),r=_t(e),l=st(n,r);l.tag=2,t!=null&&(l.callback=t),t=Rt(e,l,r),t!==null&&(Xe(t,e,r,n),cl(t,e,r))}};function Mu(e,t,n,r,l,i,o){return e=e.stateNode,typeof e.shouldComponentUpdate=="function"?e.shouldComponentUpdate(r,i,o):t.prototype&&t.prototype.isPureReactComponent?!mr(n,r)||!mr(l,i):!0}function hf(e,t,n){var r=!1,l=Lt,i=t.contextType;return typeof i=="object"&&i!==null?i=$e(i):(l=Ce(t)?Xt:he.current,r=t.contextTypes,i=(r=r!=null)?Cn(e,l):Lt),t=new t(n,i),e.memoizedState=t.state!==null&&t.state!==void 0?t.state:null,t.updater=ti,e.stateNode=t,t._reactInternals=e,r&&(e=e.stateNode,e.__reactInternalMemoizedUnmaskedChildContext=l,e.__reactInternalMemoizedMaskedChildContext=i),t}function Uu(e,t,n,r){e=t.state,typeof t.componentWillReceiveProps=="function"&&t.componentWillReceiveProps(n,r),typeof t.UNSAFE_componentWillReceiveProps=="function"&&t.UNSAFE_componentWillReceiveProps(n,r),t.state!==e&&ti.enqueueReplaceState(t,t.state,null)}function Ro(e,t,n,r){var l=e.stateNode;l.props=n,l.state=e.memoizedState,l.refs={},ks(e);var i=t.contextType;typeof i=="object"&&i!==null?l.context=$e(i):(i=Ce(t)?Xt:he.current,l.context=Cn(e,i)),l.state=e.memoizedState,i=t.getDerivedStateFromProps,typeof i=="function"&&(No(e,t,i,n),l.state=e.memoizedState),typeof t.getDerivedStateFromProps=="function"||typeof l.getSnapshotBeforeUpdate=="function"||typeof l.UNSAFE_componentWillMount!="function"&&typeof l.componentWillMount!="function"||(t=l.state,typeof l.componentWillMount=="function"&&l.componentWillMount(),typeof l.UNSAFE_componentWillMount=="function"&&l.UNSAFE_componentWillMount(),t!==l.state&&ti.enqueueReplaceState(l,l.state,null),Il(e,n,l,r),l.state=e.memoizedState),typeof l.componentDidMount=="function"&&(e.flags|=4194308)}function _n(e,t){try{var n="",r=t;do n+=ip(r),r=r.return;while(r);var l=n}catch(i){l=`
Error generating stack: `+i.message+`
`+i.stack}return{value:e,source:t,stack:l,digest:null}}function Ui(e,t,n){return{value:e,source:null,stack:n??null,digest:t??null}}function Po(e,t){try{console.error(t.value)}catch(n){setTimeout(function(){throw n})}}var Lh=typeof WeakMap=="function"?WeakMap:Map;function mf(e,t,n){n=st(-1,n),n.tag=3,n.payload={element:null};var r=t.value;return n.callback=function(){Bl||(Bl=!0,Fo=r),Po(e,t)},n}function yf(e,t,n){n=st(-1,n),n.tag=3;var r=e.type.getDerivedStateFromError;if(typeof r=="function"){var l=t.value;n.payload=function(){return r(l)},n.callback=function(){Po(e,t)}}var i=e.stateNode;return i!==null&&typeof i.componentDidCatch=="function"&&(n.callback=function(){Po(e,t),typeof r!="function"&&(Pt===null?Pt=new Set([this]):Pt.add(this));var o=t.stack;this.componentDidCatch(t.value,{componentStack:o!==null?o:""})}),n}function Bu(e,t,n){var r=e.pingCache;if(r===null){r=e.pingCache=new Lh;var l=new Set;r.set(t,l)}else l=r.get(t),l===void 0&&(l=new Set,r.set(t,l));l.has(n)||(l.add(n),e=Kh.bind(null,e,t,n),t.then(e,e))}function $u(e){do{var t;if((t=e.tag===13)&&(t=e.memoizedState,t=t!==null?t.dehydrated!==null:!0),t)return e;e=e.return}while(e!==null);return null}function Vu(e,t,n,r,l){return e.mode&1?(e.flags|=65536,e.lanes=l,e):(e===t?e.flags|=65536:(e.flags|=128,n.flags|=131072,n.flags&=-52805,n.tag===1&&(n.alternate===null?n.tag=17:(t=st(-1,1),t.tag=2,Rt(n,t,1))),n.lanes|=1),e)}var zh=dt.ReactCurrentOwner,Ee=!1;function ye(e,t,n,r){t.child=e===null?Hc(t,null,n,r):Rn(t,e.child,n,r)}function Wu(e,t,n,r,l){n=n.render;var i=t.ref;return Sn(t,l),r=_s(e,t,n,r,i,l),n=js(),e!==null&&!Ee?(t.updateQueue=e.updateQueue,t.flags&=-2053,e.lanes&=~l,ft(e,t,l)):(K&&n&&ys(t),t.flags|=1,ye(e,t,r,l),t.child)}function Hu(e,t,n,r,l){if(e===null){var i=n.type;return typeof i=="function"&&!Us(i)&&i.defaultProps===void 0&&n.compare===null&&n.defaultProps===void 0?(t.tag=15,t.type=i,vf(e,t,i,r,l)):(e=yl(n.type,null,r,t,t.mode,l),e.ref=t.ref,e.return=t,t.child=e)}if(i=e.child,!(e.lanes&l)){var o=i.memoizedProps;if(n=n.compare,n=n!==null?n:mr,n(o,r)&&e.ref===t.ref)return ft(e,t,l)}return t.flags|=1,e=jt(i,r),e.ref=t.ref,e.return=t,t.child=e}function vf(e,t,n,r,l){if(e!==null){var i=e.memoizedProps;if(mr(i,r)&&e.ref===t.ref)if(Ee=!1,t.pendingProps=r=i,(e.lanes&l)!==0)e.flags&131072&&(Ee=!0);else return t.lanes=e.lanes,ft(e,t,l)}return _o(e,t,n,r,l)}function gf(e,t,n){var r=t.pendingProps,l=r.children,i=e!==null?e.memoizedState:null;if(r.mode==="hidden")if(!(t.mode&1))t.memoizedState={baseLanes:0,cachePool:null,transitions:null},V(yn,Te),Te|=n;else{if(!(n&1073741824))return e=i!==null?i.baseLanes|n:n,t.lanes=t.childLanes=1073741824,t.memoizedState={baseLanes:e,cachePool:null,transitions:null},t.updateQueue=null,V(yn,Te),Te|=e,null;t.memoizedState={baseLanes:0,cachePool:null,transitions:null},r=i!==null?i.baseLanes:n,V(yn,Te),Te|=r}else i!==null?(r=i.baseLanes|n,t.memoizedState=null):r=n,V(yn,Te),Te|=r;return ye(e,t,l,n),t.child}function xf(e,t){var n=t.ref;(e===null&&n!==null||e!==null&&e.ref!==n)&&(t.flags|=512,t.flags|=2097152)}function _o(e,t,n,r,l){var i=Ce(n)?Xt:he.current;return i=Cn(t,i),Sn(t,l),n=_s(e,t,n,r,i,l),r=js(),e!==null&&!Ee?(t.updateQueue=e.updateQueue,t.flags&=-2053,e.lanes&=~l,ft(e,t,l)):(K&&r&&ys(t),t.flags|=1,ye(e,t,n,l),t.child)}function Qu(e,t,n,r,l){if(Ce(n)){var i=!0;Tl(t)}else i=!1;if(Sn(t,l),t.stateNode===null)pl(e,t),hf(t,n,r),Ro(t,n,r,l),r=!0;else if(e===null){var o=t.stateNode,s=t.memoizedProps;o.props=s;var u=o.context,a=n.contextType;typeof a=="object"&&a!==null?a=$e(a):(a=Ce(n)?Xt:he.current,a=Cn(t,a));var f=n.getDerivedStateFromProps,d=typeof f=="function"||typeof o.getSnapshotBeforeUpdate=="function";d||typeof o.UNSAFE_componentWillReceiveProps!="function"&&typeof o.componentWillReceiveProps!="function"||(s!==r||u!==a)&&Uu(t,o,r,a),yt=!1;var y=t.memoizedState;o.state=y,Il(t,r,o,l),u=t.memoizedState,s!==r||y!==u||ke.current||yt?(typeof f=="function"&&(No(t,n,f,r),u=t.memoizedState),(s=yt||Mu(t,n,s,r,y,u,a))?(d||typeof o.UNSAFE_componentWillMount!="function"&&typeof o.componentWillMount!="function"||(typeof o.componentWillMount=="function"&&o.componentWillMount(),typeof o.UNSAFE_componentWillMount=="function"&&o.UNSAFE_componentWillMount()),typeof o.componentDidMount=="function"&&(t.flags|=4194308)):(typeof o.componentDidMount=="function"&&(t.flags|=4194308),t.memoizedProps=r,t.memoizedState=u),o.props=r,o.state=u,o.context=a,r=s):(typeof o.componentDidMount=="function"&&(t.flags|=4194308),r=!1)}else{o=t.stateNode,Kc(e,t),s=t.memoizedProps,a=t.type===t.elementType?s:He(t.type,s),o.props=a,d=t.pendingProps,y=o.context,u=n.contextType,typeof u=="object"&&u!==null?u=$e(u):(u=Ce(n)?Xt:he.current,u=Cn(t,u));var E=n.getDerivedStateFromProps;(f=typeof E=="function"||typeof o.getSnapshotBeforeUpdate=="function")||typeof o.UNSAFE_componentWillReceiveProps!="function"&&typeof o.componentWillReceiveProps!="function"||(s!==d||y!==u)&&Uu(t,o,r,u),yt=!1,y=t.memoizedState,o.state=y,Il(t,r,o,l);var m=t.memoizedState;s!==d||y!==m||ke.current||yt?(typeof E=="function"&&(No(t,n,E,r),m=t.memoizedState),(a=yt||Mu(t,n,a,r,y,m,u)||!1)?(f||typeof o.UNSAFE_componentWillUpdate!="function"&&typeof o.componentWillUpdate!="function"||(typeof o.componentWillUpdate=="function"&&o.componentWillUpdate(r,m,u),typeof o.UNSAFE_componentWillUpdate=="function"&&o.UNSAFE_componentWillUpdate(r,m,u)),typeof o.componentDidUpdate=="function"&&(t.flags|=4),typeof o.getSnapshotBeforeUpdate=="function"&&(t.flags|=1024)):(typeof o.componentDidUpdate!="function"||s===e.memoizedProps&&y===e.memoizedState||(t.flags|=4),typeof o.getSnapshotBeforeUpdate!="function"||s===e.memoizedProps&&y===e.memoizedState||(t.flags|=1024),t.memoizedProps=r,t.memoizedState=m),o.props=r,o.state=m,o.context=u,r=a):(typeof o.componentDidUpdate!="function"||s===e.memoizedProps&&y===e.memoizedState||(t.flags|=4),typeof o.getSnapshotBeforeUpdate!="function"||s===e.memoizedProps&&y===e.memoizedState||(t.flags|=1024),r=!1)}return jo(e,t,n,r,i,l)}function jo(e,t,n,r,l,i){xf(e,t);var o=(t.flags&128)!==0;if(!r&&!o)return l&&Tu(t,n,!1),ft(e,t,i);r=t.stateNode,zh.current=t;var s=o&&typeof n.getDerivedStateFromError!="function"?null:r.render();return t.flags|=1,e!==null&&o?(t.child=Rn(t,e.child,null,i),t.child=Rn(t,null,s,i)):ye(e,t,s,i),t.memoizedState=r.state,l&&Tu(t,n,!0),t.child}function wf(e){var t=e.stateNode;t.pendingContext?ju(e,t.pendingContext,t.pendingContext!==t.context):t.context&&ju(e,t.context,!1),Cs(e,t.containerInfo)}function Ku(e,t,n,r,l){return Nn(),gs(l),t.flags|=256,ye(e,t,n,r),t.child}var To={dehydrated:null,treeContext:null,retryLane:0};function Oo(e){return{baseLanes:e,cachePool:null,transitions:null}}function Sf(e,t,n){var r=t.pendingProps,l=G.current,i=!1,o=(t.flags&128)!==0,s;if((s=o)||(s=e!==null&&e.memoizedState===null?!1:(l&2)!==0),s?(i=!0,t.flags&=-129):(e===null||e.memoizedState!==null)&&(l|=1),V(G,l&1),e===null)return ko(t),e=t.memoizedState,e!==null&&(e=e.dehydrated,e!==null)?(t.mode&1?e.data==="$!"?t.lanes=8:t.lanes=1073741824:t.lanes=1,null):(o=r.children,e=r.fallback,i?(r=t.mode,i=t.child,o={mode:"hidden",children:o},!(r&1)&&i!==null?(i.childLanes=0,i.pendingProps=o):i=li(o,r,0,null),e=Kt(e,r,n,null),i.return=t,e.return=t,i.sibling=e,t.child=i,t.child.memoizedState=Oo(n),t.memoizedState=To,e):Ls(t,o));if(l=e.memoizedState,l!==null&&(s=l.dehydrated,s!==null))return Ah(e,t,o,r,s,l,n);if(i){i=r.fallback,o=t.mode,l=e.child,s=l.sibling;var u={mode:"hidden",children:r.children};return!(o&1)&&t.child!==l?(r=t.child,r.childLanes=0,r.pendingProps=u,t.deletions=null):(r=jt(l,u),r.subtreeFlags=l.subtreeFlags&14680064),s!==null?i=jt(s,i):(i=Kt(i,o,n,null),i.flags|=2),i.return=t,r.return=t,r.sibling=i,t.child=r,r=i,i=t.child,o=e.child.memoizedState,o=o===null?Oo(n):{baseLanes:o.baseLanes|n,cachePool:null,transitions:o.transitions},i.memoizedState=o,i.childLanes=e.childLanes&~n,t.memoizedState=To,r}return i=e.child,e=i.sibling,r=jt(i,{mode:"visible",children:r.children}),!(t.mode&1)&&(r.lanes=n),r.return=t,r.sibling=null,e!==null&&(n=t.deletions,n===null?(t.deletions=[e],t.flags|=16):n.push(e)),t.child=r,t.memoizedState=null,r}function Ls(e,t){return t=li({mode:"visible",children:t},e.mode,0,null),t.return=e,e.child=t}function Yr(e,t,n,r){return r!==null&&gs(r),Rn(t,e.child,null,n),e=Ls(t,t.pendingProps.children),e.flags|=2,t.memoizedState=null,e}function Ah(e,t,n,r,l,i,o){if(n)return t.flags&256?(t.flags&=-257,r=Ui(Error(C(422))),Yr(e,t,o,r)):t.memoizedState!==null?(t.child=e.child,t.flags|=128,null):(i=r.fallback,l=t.mode,r=li({mode:"visible",children:r.children},l,0,null),i=Kt(i,l,o,null),i.flags|=2,r.return=t,i.return=t,r.sibling=i,t.child=r,t.mode&1&&Rn(t,e.child,null,o),t.child.memoizedState=Oo(o),t.memoizedState=To,i);if(!(t.mode&1))return Yr(e,t,o,null);if(l.data==="$!"){if(r=l.nextSibling&&l.nextSibling.dataset,r)var s=r.dgst;return r=s,i=Error(C(419)),r=Ui(i,r,void 0),Yr(e,t,o,r)}if(s=(o&e.childLanes)!==0,Ee||s){if(r=ie,r!==null){switch(o&-o){case 4:l=2;break;case 16:l=8;break;case 64:case 128:case 256:case 512:case 1024:case 2048:case 4096:case 8192:case 16384:case 32768:case 65536:case 131072:case 262144:case 524288:case 1048576:case 2097152:case 4194304:case 8388608:case 16777216:case 33554432:case 67108864:l=32;break;case 536870912:l=268435456;break;default:l=0}l=l&(r.suspendedLanes|o)?0:l,l!==0&&l!==i.retryLane&&(i.retryLane=l,ct(e,l),Xe(r,e,l,-1))}return Ms(),r=Ui(Error(C(421))),Yr(e,t,o,r)}return l.data==="$?"?(t.flags|=128,t.child=e.child,t=Gh.bind(null,e),l._reactRetry=t,null):(e=i.treeContext,Oe=Nt(l.nextSibling),Le=t,K=!0,Ke=null,e!==null&&(Fe[Me++]=it,Fe[Me++]=ot,Fe[Me++]=qt,it=e.id,ot=e.overflow,qt=t),t=Ls(t,r.children),t.flags|=4096,t)}function Gu(e,t,n){e.lanes|=t;var r=e.alternate;r!==null&&(r.lanes|=t),Co(e.return,t,n)}function Bi(e,t,n,r,l){var i=e.memoizedState;i===null?e.memoizedState={isBackwards:t,rendering:null,renderingStartTime:0,last:r,tail:n,tailMode:l}:(i.isBackwards=t,i.rendering=null,i.renderingStartTime=0,i.last=r,i.tail=n,i.tailMode=l)}function Ef(e,t,n){var r=t.pendingProps,l=r.revealOrder,i=r.tail;if(ye(e,t,r.children,n),r=G.current,r&2)r=r&1|2,t.flags|=128;else{if(e!==null&&e.flags&128)e:for(e=t.child;e!==null;){if(e.tag===13)e.memoizedState!==null&&Gu(e,n,t);else if(e.tag===19)Gu(e,n,t);else if(e.child!==null){e.child.return=e,e=e.child;continue}if(e===t)break e;for(;e.sibling===null;){if(e.return===null||e.return===t)break e;e=e.return}e.sibling.return=e.return,e=e.sibling}r&=1}if(V(G,r),!(t.mode&1))t.memoizedState=null;else switch(l){case"forwards":for(n=t.child,l=null;n!==null;)e=n.alternate,e!==null&&Dl(e)===null&&(l=n),n=n.sibling;n=l,n===null?(l=t.child,t.child=null):(l=n.sibling,n.sibling=null),Bi(t,!1,l,n,i);break;case"backwards":for(n=null,l=t.child,t.child=null;l!==null;){if(e=l.alternate,e!==null&&Dl(e)===null){t.child=l;break}e=l.sibling,l.sibling=n,n=l,l=e}Bi(t,!0,n,null,i);break;case"together":Bi(t,!1,null,null,void 0);break;default:t.memoizedState=null}return t.child}function pl(e,t){!(t.mode&1)&&e!==null&&(e.alternate=null,t.alternate=null,t.flags|=2)}function ft(e,t,n){if(e!==null&&(t.dependencies=e.dependencies),Yt|=t.lanes,!(n&t.childLanes))return null;if(e!==null&&t.child!==e.child)throw Error(C(153));if(t.child!==null){for(e=t.child,n=jt(e,e.pendingProps),t.child=n,n.return=t;e.sibling!==null;)e=e.sibling,n=n.sibling=jt(e,e.pendingProps),n.return=t;n.sibling=null}return t.child}function Ih(e,t,n){switch(t.tag){case 3:wf(t),Nn();break;case 5:Gc(t);break;case 1:Ce(t.type)&&Tl(t);break;case 4:Cs(t,t.stateNode.containerInfo);break;case 10:var r=t.type._context,l=t.memoizedProps.value;V(zl,r._currentValue),r._currentValue=l;break;case 13:if(r=t.memoizedState,r!==null)return r.dehydrated!==null?(V(G,G.current&1),t.flags|=128,null):n&t.child.childLanes?Sf(e,t,n):(V(G,G.current&1),e=ft(e,t,n),e!==null?e.sibling:null);V(G,G.current&1);break;case 19:if(r=(n&t.childLanes)!==0,e.flags&128){if(r)return Ef(e,t,n);t.flags|=128}if(l=t.memoizedState,l!==null&&(l.rendering=null,l.tail=null,l.lastEffect=null),V(G,G.current),r)break;return null;case 22:case 23:return t.lanes=0,gf(e,t,n)}return ft(e,t,n)}var kf,Lo,Cf,Nf;kf=function(e,t){for(var n=t.child;n!==null;){if(n.tag===5||n.tag===6)e.appendChild(n.stateNode);else if(n.tag!==4&&n.child!==null){n.child.return=n,n=n.child;continue}if(n===t)break;for(;n.sibling===null;){if(n.return===null||n.return===t)return;n=n.return}n.sibling.return=n.return,n=n.sibling}};Lo=function(){};Cf=function(e,t,n,r){var l=e.memoizedProps;if(l!==r){e=t.stateNode,Wt(nt.current);var i=null;switch(n){case"input":l=Zi(e,l),r=Zi(e,r),i=[];break;case"select":l=q({},l,{value:void 0}),r=q({},r,{value:void 0}),i=[];break;case"textarea":l=no(e,l),r=no(e,r),i=[];break;default:typeof l.onClick!="function"&&typeof r.onClick=="function"&&(e.onclick=_l)}lo(n,r);var o;n=null;for(a in l)if(!r.hasOwnProperty(a)&&l.hasOwnProperty(a)&&l[a]!=null)if(a==="style"){var s=l[a];for(o in s)s.hasOwnProperty(o)&&(n||(n={}),n[o]="")}else a!=="dangerouslySetInnerHTML"&&a!=="children"&&a!=="suppressContentEditableWarning"&&a!=="suppressHydrationWarning"&&a!=="autoFocus"&&(ur.hasOwnProperty(a)?i||(i=[]):(i=i||[]).push(a,null));for(a in r){var u=r[a];if(s=l!=null?l[a]:void 0,r.hasOwnProperty(a)&&u!==s&&(u!=null||s!=null))if(a==="style")if(s){for(o in s)!s.hasOwnProperty(o)||u&&u.hasOwnProperty(o)||(n||(n={}),n[o]="");for(o in u)u.hasOwnProperty(o)&&s[o]!==u[o]&&(n||(n={}),n[o]=u[o])}else n||(i||(i=[]),i.push(a,n)),n=u;else a==="dangerouslySetInnerHTML"?(u=u?u.__html:void 0,s=s?s.__html:void 0,u!=null&&s!==u&&(i=i||[]).push(a,u)):a==="children"?typeof u!="string"&&typeof u!="number"||(i=i||[]).push(a,""+u):a!=="suppressContentEditableWarning"&&a!=="suppressHydrationWarning"&&(ur.hasOwnProperty(a)?(u!=null&&a==="onScroll"&&H("scroll",e),i||s===u||(i=[])):(i=i||[]).push(a,u))}n&&(i=i||[]).push("style",n);var a=i;(t.updateQueue=a)&&(t.flags|=4)}};Nf=function(e,t,n,r){n!==r&&(t.flags|=4)};function Qn(e,t){if(!K)switch(e.tailMode){case"hidden":t=e.tail;for(var n=null;t!==null;)t.alternate!==null&&(n=t),t=t.sibling;n===null?e.tail=null:n.sibling=null;break;case"collapsed":n=e.tail;for(var r=null;n!==null;)n.alternate!==null&&(r=n),n=n.sibling;r===null?t||e.tail===null?e.tail=null:e.tail.sibling=null:r.sibling=null}}function fe(e){var t=e.alternate!==null&&e.alternate.child===e.child,n=0,r=0;if(t)for(var l=e.child;l!==null;)n|=l.lanes|l.childLanes,r|=l.subtreeFlags&14680064,r|=l.flags&14680064,l.return=e,l=l.sibling;else for(l=e.child;l!==null;)n|=l.lanes|l.childLanes,r|=l.subtreeFlags,r|=l.flags,l.return=e,l=l.sibling;return e.subtreeFlags|=r,e.childLanes=n,t}function Dh(e,t,n){var r=t.pendingProps;switch(vs(t),t.tag){case 2:case 16:case 15:case 0:case 11:case 7:case 8:case 12:case 9:case 14:return fe(t),null;case 1:return Ce(t.type)&&jl(),fe(t),null;case 3:return r=t.stateNode,Pn(),Q(ke),Q(he),Rs(),r.pendingContext&&(r.context=r.pendingContext,r.pendingContext=null),(e===null||e.child===null)&&(qr(t)?t.flags|=4:e===null||e.memoizedState.isDehydrated&&!(t.flags&256)||(t.flags|=1024,Ke!==null&&(Bo(Ke),Ke=null))),Lo(e,t),fe(t),null;case 5:Ns(t);var l=Wt(wr.current);if(n=t.type,e!==null&&t.stateNode!=null)Cf(e,t,n,r,l),e.ref!==t.ref&&(t.flags|=512,t.flags|=2097152);else{if(!r){if(t.stateNode===null)throw Error(C(166));return fe(t),null}if(e=Wt(nt.current),qr(t)){r=t.stateNode,n=t.type;var i=t.memoizedProps;switch(r[et]=t,r[gr]=i,e=(t.mode&1)!==0,n){case"dialog":H("cancel",r),H("close",r);break;case"iframe":case"object":case"embed":H("load",r);break;case"video":case"audio":for(l=0;l<bn.length;l++)H(bn[l],r);break;case"source":H("error",r);break;case"img":case"image":case"link":H("error",r),H("load",r);break;case"details":H("toggle",r);break;case"input":nu(r,i),H("invalid",r);break;case"select":r._wrapperState={wasMultiple:!!i.multiple},H("invalid",r);break;case"textarea":lu(r,i),H("invalid",r)}lo(n,i),l=null;for(var o in i)if(i.hasOwnProperty(o)){var s=i[o];o==="children"?typeof s=="string"?r.textContent!==s&&(i.suppressHydrationWarning!==!0&&Xr(r.textContent,s,e),l=["children",s]):typeof s=="number"&&r.textContent!==""+s&&(i.suppressHydrationWarning!==!0&&Xr(r.textContent,s,e),l=["children",""+s]):ur.hasOwnProperty(o)&&s!=null&&o==="onScroll"&&H("scroll",r)}switch(n){case"input":Br(r),ru(r,i,!0);break;case"textarea":Br(r),iu(r);break;case"select":case"option":break;default:typeof i.onClick=="function"&&(r.onclick=_l)}r=l,t.updateQueue=r,r!==null&&(t.flags|=4)}else{o=l.nodeType===9?l:l.ownerDocument,e==="http://www.w3.org/1999/xhtml"&&(e=ba(n)),e==="http://www.w3.org/1999/xhtml"?n==="script"?(e=o.createElement("div"),e.innerHTML="<script><\/script>",e=e.removeChild(e.firstChild)):typeof r.is=="string"?e=o.createElement(n,{is:r.is}):(e=o.createElement(n),n==="select"&&(o=e,r.multiple?o.multiple=!0:r.size&&(o.size=r.size))):e=o.createElementNS(e,n),e[et]=t,e[gr]=r,kf(e,t,!1,!1),t.stateNode=e;e:{switch(o=io(n,r),n){case"dialog":H("cancel",e),H("close",e),l=r;break;case"iframe":case"object":case"embed":H("load",e),l=r;break;case"video":case"audio":for(l=0;l<bn.length;l++)H(bn[l],e);l=r;break;case"source":H("error",e),l=r;break;case"img":case"image":case"link":H("error",e),H("load",e),l=r;break;case"details":H("toggle",e),l=r;break;case"input":nu(e,r),l=Zi(e,r),H("invalid",e);break;case"option":l=r;break;case"select":e._wrapperState={wasMultiple:!!r.multiple},l=q({},r,{value:void 0}),H("invalid",e);break;case"textarea":lu(e,r),l=no(e,r),H("invalid",e);break;default:l=r}lo(n,l),s=l;for(i in s)if(s.hasOwnProperty(i)){var u=s[i];i==="style"?tc(e,u):i==="dangerouslySetInnerHTML"?(u=u?u.__html:void 0,u!=null&&Za(e,u)):i==="children"?typeof u=="string"?(n!=="textarea"||u!=="")&&ar(e,u):typeof u=="number"&&ar(e,""+u):i!=="suppressContentEditableWarning"&&i!=="suppressHydrationWarning"&&i!=="autoFocus"&&(ur.hasOwnProperty(i)?u!=null&&i==="onScroll"&&H("scroll",e):u!=null&&ns(e,i,u,o))}switch(n){case"input":Br(e),ru(e,r,!1);break;case"textarea":Br(e),iu(e);break;case"option":r.value!=null&&e.setAttribute("value",""+Ot(r.value));break;case"select":e.multiple=!!r.multiple,i=r.value,i!=null?vn(e,!!r.multiple,i,!1):r.defaultValue!=null&&vn(e,!!r.multiple,r.defaultValue,!0);break;default:typeof l.onClick=="function"&&(e.onclick=_l)}switch(n){case"button":case"input":case"select":case"textarea":r=!!r.autoFocus;break e;case"img":r=!0;break e;default:r=!1}}r&&(t.flags|=4)}t.ref!==null&&(t.flags|=512,t.flags|=2097152)}return fe(t),null;case 6:if(e&&t.stateNode!=null)Nf(e,t,e.memoizedProps,r);else{if(typeof r!="string"&&t.stateNode===null)throw Error(C(166));if(n=Wt(wr.current),Wt(nt.current),qr(t)){if(r=t.stateNode,n=t.memoizedProps,r[et]=t,(i=r.nodeValue!==n)&&(e=Le,e!==null))switch(e.tag){case 3:Xr(r.nodeValue,n,(e.mode&1)!==0);break;case 5:e.memoizedProps.suppressHydrationWarning!==!0&&Xr(r.nodeValue,n,(e.mode&1)!==0)}i&&(t.flags|=4)}else r=(n.nodeType===9?n:n.ownerDocument).createTextNode(r),r[et]=t,t.stateNode=r}return fe(t),null;case 13:if(Q(G),r=t.memoizedState,e===null||e.memoizedState!==null&&e.memoizedState.dehydrated!==null){if(K&&Oe!==null&&t.mode&1&&!(t.flags&128))Vc(),Nn(),t.flags|=98560,i=!1;else if(i=qr(t),r!==null&&r.dehydrated!==null){if(e===null){if(!i)throw Error(C(318));if(i=t.memoizedState,i=i!==null?i.dehydrated:null,!i)throw Error(C(317));i[et]=t}else Nn(),!(t.flags&128)&&(t.memoizedState=null),t.flags|=4;fe(t),i=!1}else Ke!==null&&(Bo(Ke),Ke=null),i=!0;if(!i)return t.flags&65536?t:null}return t.flags&128?(t.lanes=n,t):(r=r!==null,r!==(e!==null&&e.memoizedState!==null)&&r&&(t.child.flags|=8192,t.mode&1&&(e===null||G.current&1?re===0&&(re=3):Ms())),t.updateQueue!==null&&(t.flags|=4),fe(t),null);case 4:return Pn(),Lo(e,t),e===null&&yr(t.stateNode.containerInfo),fe(t),null;case 10:return Ss(t.type._context),fe(t),null;case 17:return Ce(t.type)&&jl(),fe(t),null;case 19:if(Q(G),i=t.memoizedState,i===null)return fe(t),null;if(r=(t.flags&128)!==0,o=i.rendering,o===null)if(r)Qn(i,!1);else{if(re!==0||e!==null&&e.flags&128)for(e=t.child;e!==null;){if(o=Dl(e),o!==null){for(t.flags|=128,Qn(i,!1),r=o.updateQueue,r!==null&&(t.updateQueue=r,t.flags|=4),t.subtreeFlags=0,r=n,n=t.child;n!==null;)i=n,e=r,i.flags&=14680066,o=i.alternate,o===null?(i.childLanes=0,i.lanes=e,i.child=null,i.subtreeFlags=0,i.memoizedProps=null,i.memoizedState=null,i.updateQueue=null,i.dependencies=null,i.stateNode=null):(i.childLanes=o.childLanes,i.lanes=o.lanes,i.child=o.child,i.subtreeFlags=0,i.deletions=null,i.memoizedProps=o.memoizedProps,i.memoizedState=o.memoizedState,i.updateQueue=o.updateQueue,i.type=o.type,e=o.dependencies,i.dependencies=e===null?null:{lanes:e.lanes,firstContext:e.firstContext}),n=n.sibling;return V(G,G.current&1|2),t.child}e=e.sibling}i.tail!==null&&Z()>jn&&(t.flags|=128,r=!0,Qn(i,!1),t.lanes=4194304)}else{if(!r)if(e=Dl(o),e!==null){if(t.flags|=128,r=!0,n=e.updateQueue,n!==null&&(t.updateQueue=n,t.flags|=4),Qn(i,!0),i.tail===null&&i.tailMode==="hidden"&&!o.alternate&&!K)return fe(t),null}else 2*Z()-i.renderingStartTime>jn&&n!==1073741824&&(t.flags|=128,r=!0,Qn(i,!1),t.lanes=4194304);i.isBackwards?(o.sibling=t.child,t.child=o):(n=i.last,n!==null?n.sibling=o:t.child=o,i.last=o)}return i.tail!==null?(t=i.tail,i.rendering=t,i.tail=t.sibling,i.renderingStartTime=Z(),t.sibling=null,n=G.current,V(G,r?n&1|2:n&1),t):(fe(t),null);case 22:case 23:return Fs(),r=t.memoizedState!==null,e!==null&&e.memoizedState!==null!==r&&(t.flags|=8192),r&&t.mode&1?Te&1073741824&&(fe(t),t.subtreeFlags&6&&(t.flags|=8192)):fe(t),null;case 24:return null;case 25:return null}throw Error(C(156,t.tag))}function Fh(e,t){switch(vs(t),t.tag){case 1:return Ce(t.type)&&jl(),e=t.flags,e&65536?(t.flags=e&-65537|128,t):null;case 3:return Pn(),Q(ke),Q(he),Rs(),e=t.flags,e&65536&&!(e&128)?(t.flags=e&-65537|128,t):null;case 5:return Ns(t),null;case 13:if(Q(G),e=t.memoizedState,e!==null&&e.dehydrated!==null){if(t.alternate===null)throw Error(C(340));Nn()}return e=t.flags,e&65536?(t.flags=e&-65537|128,t):null;case 19:return Q(G),null;case 4:return Pn(),null;case 10:return Ss(t.type._context),null;case 22:case 23:return Fs(),null;case 24:return null;default:return null}}var br=!1,de=!1,Mh=typeof WeakSet=="function"?WeakSet:Set,j=null;function mn(e,t){var n=e.ref;if(n!==null)if(typeof n=="function")try{n(null)}catch(r){Y(e,t,r)}else n.current=null}function zo(e,t,n){try{n()}catch(r){Y(e,t,r)}}var Xu=!1;function Uh(e,t){if(yo=Nl,e=jc(),ms(e)){if("selectionStart"in e)var n={start:e.selectionStart,end:e.selectionEnd};else e:{n=(n=e.ownerDocument)&&n.defaultView||window;var r=n.getSelection&&n.getSelection();if(r&&r.rangeCount!==0){n=r.anchorNode;var l=r.anchorOffset,i=r.focusNode;r=r.focusOffset;try{n.nodeType,i.nodeType}catch{n=null;break e}var o=0,s=-1,u=-1,a=0,f=0,d=e,y=null;t:for(;;){for(var E;d!==n||l!==0&&d.nodeType!==3||(s=o+l),d!==i||r!==0&&d.nodeType!==3||(u=o+r),d.nodeType===3&&(o+=d.nodeValue.length),(E=d.firstChild)!==null;)y=d,d=E;for(;;){if(d===e)break t;if(y===n&&++a===l&&(s=o),y===i&&++f===r&&(u=o),(E=d.nextSibling)!==null)break;d=y,y=d.parentNode}d=E}n=s===-1||u===-1?null:{start:s,end:u}}else n=null}n=n||{start:0,end:0}}else n=null;for(vo={focusedElem:e,selectionRange:n},Nl=!1,j=t;j!==null;)if(t=j,e=t.child,(t.subtreeFlags&1028)!==0&&e!==null)e.return=t,j=e;else for(;j!==null;){t=j;try{var m=t.alternate;if(t.flags&1024)switch(t.tag){case 0:case 11:case 15:break;case 1:if(m!==null){var x=m.memoizedProps,S=m.memoizedState,h=t.stateNode,c=h.getSnapshotBeforeUpdate(t.elementType===t.type?x:He(t.type,x),S);h.__reactInternalSnapshotBeforeUpdate=c}break;case 3:var p=t.stateNode.containerInfo;p.nodeType===1?p.textContent="":p.nodeType===9&&p.documentElement&&p.removeChild(p.documentElement);break;case 5:case 6:case 4:case 17:break;default:throw Error(C(163))}}catch(g){Y(t,t.return,g)}if(e=t.sibling,e!==null){e.return=t.return,j=e;break}j=t.return}return m=Xu,Xu=!1,m}function ir(e,t,n){var r=t.updateQueue;if(r=r!==null?r.lastEffect:null,r!==null){var l=r=r.next;do{if((l.tag&e)===e){var i=l.destroy;l.destroy=void 0,i!==void 0&&zo(t,n,i)}l=l.next}while(l!==r)}}function ni(e,t){if(t=t.updateQueue,t=t!==null?t.lastEffect:null,t!==null){var n=t=t.next;do{if((n.tag&e)===e){var r=n.create;n.destroy=r()}n=n.next}while(n!==t)}}function Ao(e){var t=e.ref;if(t!==null){var n=e.stateNode;switch(e.tag){case 5:e=n;break;default:e=n}typeof t=="function"?t(e):t.current=e}}function Rf(e){var t=e.alternate;t!==null&&(e.alternate=null,Rf(t)),e.child=null,e.deletions=null,e.sibling=null,e.tag===5&&(t=e.stateNode,t!==null&&(delete t[et],delete t[gr],delete t[wo],delete t[Sh],delete t[Eh])),e.stateNode=null,e.return=null,e.dependencies=null,e.memoizedProps=null,e.memoizedState=null,e.pendingProps=null,e.stateNode=null,e.updateQueue=null}function Pf(e){return e.tag===5||e.tag===3||e.tag===4}function qu(e){e:for(;;){for(;e.sibling===null;){if(e.return===null||Pf(e.return))return null;e=e.return}for(e.sibling.return=e.return,e=e.sibling;e.tag!==5&&e.tag!==6&&e.tag!==18;){if(e.flags&2||e.child===null||e.tag===4)continue e;e.child.return=e,e=e.child}if(!(e.flags&2))return e.stateNode}}function Io(e,t,n){var r=e.tag;if(r===5||r===6)e=e.stateNode,t?n.nodeType===8?n.parentNode.insertBefore(e,t):n.insertBefore(e,t):(n.nodeType===8?(t=n.parentNode,t.insertBefore(e,n)):(t=n,t.appendChild(e)),n=n._reactRootContainer,n!=null||t.onclick!==null||(t.onclick=_l));else if(r!==4&&(e=e.child,e!==null))for(Io(e,t,n),e=e.sibling;e!==null;)Io(e,t,n),e=e.sibling}function Do(e,t,n){var r=e.tag;if(r===5||r===6)e=e.stateNode,t?n.insertBefore(e,t):n.appendChild(e);else if(r!==4&&(e=e.child,e!==null))for(Do(e,t,n),e=e.sibling;e!==null;)Do(e,t,n),e=e.sibling}var se=null,Qe=!1;function ht(e,t,n){for(n=n.child;n!==null;)_f(e,t,n),n=n.sibling}function _f(e,t,n){if(tt&&typeof tt.onCommitFiberUnmount=="function")try{tt.onCommitFiberUnmount(Xl,n)}catch{}switch(n.tag){case 5:de||mn(n,t);case 6:var r=se,l=Qe;se=null,ht(e,t,n),se=r,Qe=l,se!==null&&(Qe?(e=se,n=n.stateNode,e.nodeType===8?e.parentNode.removeChild(n):e.removeChild(n)):se.removeChild(n.stateNode));break;case 18:se!==null&&(Qe?(e=se,n=n.stateNode,e.nodeType===8?zi(e.parentNode,n):e.nodeType===1&&zi(e,n),pr(e)):zi(se,n.stateNode));break;case 4:r=se,l=Qe,se=n.stateNode.containerInfo,Qe=!0,ht(e,t,n),se=r,Qe=l;break;case 0:case 11:case 14:case 15:if(!de&&(r=n.updateQueue,r!==null&&(r=r.lastEffect,r!==null))){l=r=r.next;do{var i=l,o=i.destroy;i=i.tag,o!==void 0&&(i&2||i&4)&&zo(n,t,o),l=l.next}while(l!==r)}ht(e,t,n);break;case 1:if(!de&&(mn(n,t),r=n.stateNode,typeof r.componentWillUnmount=="function"))try{r.props=n.memoizedProps,r.state=n.memoizedState,r.componentWillUnmount()}catch(s){Y(n,t,s)}ht(e,t,n);break;case 21:ht(e,t,n);break;case 22:n.mode&1?(de=(r=de)||n.memoizedState!==null,ht(e,t,n),de=r):ht(e,t,n);break;default:ht(e,t,n)}}function Ju(e){var t=e.updateQueue;if(t!==null){e.updateQueue=null;var n=e.stateNode;n===null&&(n=e.stateNode=new Mh),t.forEach(function(r){var l=Xh.bind(null,e,r);n.has(r)||(n.add(r),r.then(l,l))})}}function We(e,t){var n=t.deletions;if(n!==null)for(var r=0;r<n.length;r++){var l=n[r];try{var i=e,o=t,s=o;e:for(;s!==null;){switch(s.tag){case 5:se=s.stateNode,Qe=!1;break e;case 3:se=s.stateNode.containerInfo,Qe=!0;break e;case 4:se=s.stateNode.containerInfo,Qe=!0;break e}s=s.return}if(se===null)throw Error(C(160));_f(i,o,l),se=null,Qe=!1;var u=l.alternate;u!==null&&(u.return=null),l.return=null}catch(a){Y(l,t,a)}}if(t.subtreeFlags&12854)for(t=t.child;t!==null;)jf(t,e),t=t.sibling}function jf(e,t){var n=e.alternate,r=e.flags;switch(e.tag){case 0:case 11:case 14:case 15:if(We(t,e),Ye(e),r&4){try{ir(3,e,e.return),ni(3,e)}catch(x){Y(e,e.return,x)}try{ir(5,e,e.return)}catch(x){Y(e,e.return,x)}}break;case 1:We(t,e),Ye(e),r&512&&n!==null&&mn(n,n.return);break;case 5:if(We(t,e),Ye(e),r&512&&n!==null&&mn(n,n.return),e.flags&32){var l=e.stateNode;try{ar(l,"")}catch(x){Y(e,e.return,x)}}if(r&4&&(l=e.stateNode,l!=null)){var i=e.memoizedProps,o=n!==null?n.memoizedProps:i,s=e.type,u=e.updateQueue;if(e.updateQueue=null,u!==null)try{s==="input"&&i.type==="radio"&&i.name!=null&&Ja(l,i),io(s,o);var a=io(s,i);for(o=0;o<u.length;o+=2){var f=u[o],d=u[o+1];f==="style"?tc(l,d):f==="dangerouslySetInnerHTML"?Za(l,d):f==="children"?ar(l,d):ns(l,f,d,a)}switch(s){case"input":eo(l,i);break;case"textarea":Ya(l,i);break;case"select":var y=l._wrapperState.wasMultiple;l._wrapperState.wasMultiple=!!i.multiple;var E=i.value;E!=null?vn(l,!!i.multiple,E,!1):y!==!!i.multiple&&(i.defaultValue!=null?vn(l,!!i.multiple,i.defaultValue,!0):vn(l,!!i.multiple,i.multiple?[]:"",!1))}l[gr]=i}catch(x){Y(e,e.return,x)}}break;case 6:if(We(t,e),Ye(e),r&4){if(e.stateNode===null)throw Error(C(162));l=e.stateNode,i=e.memoizedProps;try{l.nodeValue=i}catch(x){Y(e,e.return,x)}}break;case 3:if(We(t,e),Ye(e),r&4&&n!==null&&n.memoizedState.isDehydrated)try{pr(t.containerInfo)}catch(x){Y(e,e.return,x)}break;case 4:We(t,e),Ye(e);break;case 13:We(t,e),Ye(e),l=e.child,l.flags&8192&&(i=l.memoizedState!==null,l.stateNode.isHidden=i,!i||l.alternate!==null&&l.alternate.memoizedState!==null||(Is=Z())),r&4&&Ju(e);break;case 22:if(f=n!==null&&n.memoizedState!==null,e.mode&1?(de=(a=de)||f,We(t,e),de=a):We(t,e),Ye(e),r&8192){if(a=e.memoizedState!==null,(e.stateNode.isHidden=a)&&!f&&e.mode&1)for(j=e,f=e.child;f!==null;){for(d=j=f;j!==null;){switch(y=j,E=y.child,y.tag){case 0:case 11:case 14:case 15:ir(4,y,y.return);break;case 1:mn(y,y.return);var m=y.stateNode;if(typeof m.componentWillUnmount=="function"){r=y,n=y.return;try{t=r,m.props=t.memoizedProps,m.state=t.memoizedState,m.componentWillUnmount()}catch(x){Y(r,n,x)}}break;case 5:mn(y,y.return);break;case 22:if(y.memoizedState!==null){bu(d);continue}}E!==null?(E.return=y,j=E):bu(d)}f=f.sibling}e:for(f=null,d=e;;){if(d.tag===5){if(f===null){f=d;try{l=d.stateNode,a?(i=l.style,typeof i.setProperty=="function"?i.setProperty("display","none","important"):i.display="none"):(s=d.stateNode,u=d.memoizedProps.style,o=u!=null&&u.hasOwnProperty("display")?u.display:null,s.style.display=ec("display",o))}catch(x){Y(e,e.return,x)}}}else if(d.tag===6){if(f===null)try{d.stateNode.nodeValue=a?"":d.memoizedProps}catch(x){Y(e,e.return,x)}}else if((d.tag!==22&&d.tag!==23||d.memoizedState===null||d===e)&&d.child!==null){d.child.return=d,d=d.child;continue}if(d===e)break e;for(;d.sibling===null;){if(d.return===null||d.return===e)break e;f===d&&(f=null),d=d.return}f===d&&(f=null),d.sibling.return=d.return,d=d.sibling}}break;case 19:We(t,e),Ye(e),r&4&&Ju(e);break;case 21:break;default:We(t,e),Ye(e)}}function Ye(e){var t=e.flags;if(t&2){try{e:{for(var n=e.return;n!==null;){if(Pf(n)){var r=n;break e}n=n.return}throw Error(C(160))}switch(r.tag){case 5:var l=r.stateNode;r.flags&32&&(ar(l,""),r.flags&=-33);var i=qu(e);Do(e,i,l);break;case 3:case 4:var o=r.stateNode.containerInfo,s=qu(e);Io(e,s,o);break;default:throw Error(C(161))}}catch(u){Y(e,e.return,u)}e.flags&=-3}t&4096&&(e.flags&=-4097)}function Bh(e,t,n){j=e,Tf(e)}function Tf(e,t,n){for(var r=(e.mode&1)!==0;j!==null;){var l=j,i=l.child;if(l.tag===22&&r){var o=l.memoizedState!==null||br;if(!o){var s=l.alternate,u=s!==null&&s.memoizedState!==null||de;s=br;var a=de;if(br=o,(de=u)&&!a)for(j=l;j!==null;)o=j,u=o.child,o.tag===22&&o.memoizedState!==null?Zu(l):u!==null?(u.return=o,j=u):Zu(l);for(;i!==null;)j=i,Tf(i),i=i.sibling;j=l,br=s,de=a}Yu(e)}else l.subtreeFlags&8772&&i!==null?(i.return=l,j=i):Yu(e)}}function Yu(e){for(;j!==null;){var t=j;if(t.flags&8772){var n=t.alternate;try{if(t.flags&8772)switch(t.tag){case 0:case 11:case 15:de||ni(5,t);break;case 1:var r=t.stateNode;if(t.flags&4&&!de)if(n===null)r.componentDidMount();else{var l=t.elementType===t.type?n.memoizedProps:He(t.type,n.memoizedProps);r.componentDidUpdate(l,n.memoizedState,r.__reactInternalSnapshotBeforeUpdate)}var i=t.updateQueue;i!==null&&Iu(t,i,r);break;case 3:var o=t.updateQueue;if(o!==null){if(n=null,t.child!==null)switch(t.child.tag){case 5:n=t.child.stateNode;break;case 1:n=t.child.stateNode}Iu(t,o,n)}break;case 5:var s=t.stateNode;if(n===null&&t.flags&4){n=s;var u=t.memoizedProps;switch(t.type){case"button":case"input":case"select":case"textarea":u.autoFocus&&n.focus();break;case"img":u.src&&(n.src=u.src)}}break;case 6:break;case 4:break;case 12:break;case 13:if(t.memoizedState===null){var a=t.alternate;if(a!==null){var f=a.memoizedState;if(f!==null){var d=f.dehydrated;d!==null&&pr(d)}}}break;case 19:case 17:case 21:case 22:case 23:case 25:break;default:throw Error(C(163))}de||t.flags&512&&Ao(t)}catch(y){Y(t,t.return,y)}}if(t===e){j=null;break}if(n=t.sibling,n!==null){n.return=t.return,j=n;break}j=t.return}}function bu(e){for(;j!==null;){var t=j;if(t===e){j=null;break}var n=t.sibling;if(n!==null){n.return=t.return,j=n;break}j=t.return}}function Zu(e){for(;j!==null;){var t=j;try{switch(t.tag){case 0:case 11:case 15:var n=t.return;try{ni(4,t)}catch(u){Y(t,n,u)}break;case 1:var r=t.stateNode;if(typeof r.componentDidMount=="function"){var l=t.return;try{r.componentDidMount()}catch(u){Y(t,l,u)}}var i=t.return;try{Ao(t)}catch(u){Y(t,i,u)}break;case 5:var o=t.return;try{Ao(t)}catch(u){Y(t,o,u)}}}catch(u){Y(t,t.return,u)}if(t===e){j=null;break}var s=t.sibling;if(s!==null){s.return=t.return,j=s;break}j=t.return}}var $h=Math.ceil,Ul=dt.ReactCurrentDispatcher,zs=dt.ReactCurrentOwner,Be=dt.ReactCurrentBatchConfig,F=0,ie=null,ee=null,ue=0,Te=0,yn=At(0),re=0,Cr=null,Yt=0,ri=0,As=0,or=null,Se=null,Is=0,jn=1/0,rt=null,Bl=!1,Fo=null,Pt=null,Zr=!1,wt=null,$l=0,sr=0,Mo=null,hl=-1,ml=0;function ve(){return F&6?Z():hl!==-1?hl:hl=Z()}function _t(e){return e.mode&1?F&2&&ue!==0?ue&-ue:Ch.transition!==null?(ml===0&&(ml=pc()),ml):(e=$,e!==0||(e=window.event,e=e===void 0?16:wc(e.type)),e):1}function Xe(e,t,n,r){if(50<sr)throw sr=0,Mo=null,Error(C(185));_r(e,n,r),(!(F&2)||e!==ie)&&(e===ie&&(!(F&2)&&(ri|=n),re===4&&gt(e,ue)),Ne(e,r),n===1&&F===0&&!(t.mode&1)&&(jn=Z()+500,Zl&&It()))}function Ne(e,t){var n=e.callbackNode;Cp(e,t);var r=Cl(e,e===ie?ue:0);if(r===0)n!==null&&uu(n),e.callbackNode=null,e.callbackPriority=0;else if(t=r&-r,e.callbackPriority!==t){if(n!=null&&uu(n),t===1)e.tag===0?kh(ea.bind(null,e)):Uc(ea.bind(null,e)),xh(function(){!(F&6)&&It()}),n=null;else{switch(hc(r)){case 1:n=ss;break;case 4:n=fc;break;case 16:n=kl;break;case 536870912:n=dc;break;default:n=kl}n=Mf(n,Of.bind(null,e))}e.callbackPriority=t,e.callbackNode=n}}function Of(e,t){if(hl=-1,ml=0,F&6)throw Error(C(327));var n=e.callbackNode;if(En()&&e.callbackNode!==n)return null;var r=Cl(e,e===ie?ue:0);if(r===0)return null;if(r&30||r&e.expiredLanes||t)t=Vl(e,r);else{t=r;var l=F;F|=2;var i=zf();(ie!==e||ue!==t)&&(rt=null,jn=Z()+500,Qt(e,t));do try{Hh();break}catch(s){Lf(e,s)}while(!0);ws(),Ul.current=i,F=l,ee!==null?t=0:(ie=null,ue=0,t=re)}if(t!==0){if(t===2&&(l=co(e),l!==0&&(r=l,t=Uo(e,l))),t===1)throw n=Cr,Qt(e,0),gt(e,r),Ne(e,Z()),n;if(t===6)gt(e,r);else{if(l=e.current.alternate,!(r&30)&&!Vh(l)&&(t=Vl(e,r),t===2&&(i=co(e),i!==0&&(r=i,t=Uo(e,i))),t===1))throw n=Cr,Qt(e,0),gt(e,r),Ne(e,Z()),n;switch(e.finishedWork=l,e.finishedLanes=r,t){case 0:case 1:throw Error(C(345));case 2:Bt(e,Se,rt);break;case 3:if(gt(e,r),(r&130023424)===r&&(t=Is+500-Z(),10<t)){if(Cl(e,0)!==0)break;if(l=e.suspendedLanes,(l&r)!==r){ve(),e.pingedLanes|=e.suspendedLanes&l;break}e.timeoutHandle=xo(Bt.bind(null,e,Se,rt),t);break}Bt(e,Se,rt);break;case 4:if(gt(e,r),(r&4194240)===r)break;for(t=e.eventTimes,l=-1;0<r;){var o=31-Ge(r);i=1<<o,o=t[o],o>l&&(l=o),r&=~i}if(r=l,r=Z()-r,r=(120>r?120:480>r?480:1080>r?1080:1920>r?1920:3e3>r?3e3:4320>r?4320:1960*$h(r/1960))-r,10<r){e.timeoutHandle=xo(Bt.bind(null,e,Se,rt),r);break}Bt(e,Se,rt);break;case 5:Bt(e,Se,rt);break;default:throw Error(C(329))}}}return Ne(e,Z()),e.callbackNode===n?Of.bind(null,e):null}function Uo(e,t){var n=or;return e.current.memoizedState.isDehydrated&&(Qt(e,t).flags|=256),e=Vl(e,t),e!==2&&(t=Se,Se=n,t!==null&&Bo(t)),e}function Bo(e){Se===null?Se=e:Se.push.apply(Se,e)}function Vh(e){for(var t=e;;){if(t.flags&16384){var n=t.updateQueue;if(n!==null&&(n=n.stores,n!==null))for(var r=0;r<n.length;r++){var l=n[r],i=l.getSnapshot;l=l.value;try{if(!qe(i(),l))return!1}catch{return!1}}}if(n=t.child,t.subtreeFlags&16384&&n!==null)n.return=t,t=n;else{if(t===e)break;for(;t.sibling===null;){if(t.return===null||t.return===e)return!0;t=t.return}t.sibling.return=t.return,t=t.sibling}}return!0}function gt(e,t){for(t&=~As,t&=~ri,e.suspendedLanes|=t,e.pingedLanes&=~t,e=e.expirationTimes;0<t;){var n=31-Ge(t),r=1<<n;e[n]=-1,t&=~r}}function ea(e){if(F&6)throw Error(C(327));En();var t=Cl(e,0);if(!(t&1))return Ne(e,Z()),null;var n=Vl(e,t);if(e.tag!==0&&n===2){var r=co(e);r!==0&&(t=r,n=Uo(e,r))}if(n===1)throw n=Cr,Qt(e,0),gt(e,t),Ne(e,Z()),n;if(n===6)throw Error(C(345));return e.finishedWork=e.current.alternate,e.finishedLanes=t,Bt(e,Se,rt),Ne(e,Z()),null}function Ds(e,t){var n=F;F|=1;try{return e(t)}finally{F=n,F===0&&(jn=Z()+500,Zl&&It())}}function bt(e){wt!==null&&wt.tag===0&&!(F&6)&&En();var t=F;F|=1;var n=Be.transition,r=$;try{if(Be.transition=null,$=1,e)return e()}finally{$=r,Be.transition=n,F=t,!(F&6)&&It()}}function Fs(){Te=yn.current,Q(yn)}function Qt(e,t){e.finishedWork=null,e.finishedLanes=0;var n=e.timeoutHandle;if(n!==-1&&(e.timeoutHandle=-1,gh(n)),ee!==null)for(n=ee.return;n!==null;){var r=n;switch(vs(r),r.tag){case 1:r=r.type.childContextTypes,r!=null&&jl();break;case 3:Pn(),Q(ke),Q(he),Rs();break;case 5:Ns(r);break;case 4:Pn();break;case 13:Q(G);break;case 19:Q(G);break;case 10:Ss(r.type._context);break;case 22:case 23:Fs()}n=n.return}if(ie=e,ee=e=jt(e.current,null),ue=Te=t,re=0,Cr=null,As=ri=Yt=0,Se=or=null,Vt!==null){for(t=0;t<Vt.length;t++)if(n=Vt[t],r=n.interleaved,r!==null){n.interleaved=null;var l=r.next,i=n.pending;if(i!==null){var o=i.next;i.next=l,r.next=o}n.pending=r}Vt=null}return e}function Lf(e,t){do{var n=ee;try{if(ws(),fl.current=Ml,Fl){for(var r=X.memoizedState;r!==null;){var l=r.queue;l!==null&&(l.pending=null),r=r.next}Fl=!1}if(Jt=0,le=ne=X=null,lr=!1,Sr=0,zs.current=null,n===null||n.return===null){re=1,Cr=t,ee=null;break}e:{var i=e,o=n.return,s=n,u=t;if(t=ue,s.flags|=32768,u!==null&&typeof u=="object"&&typeof u.then=="function"){var a=u,f=s,d=f.tag;if(!(f.mode&1)&&(d===0||d===11||d===15)){var y=f.alternate;y?(f.updateQueue=y.updateQueue,f.memoizedState=y.memoizedState,f.lanes=y.lanes):(f.updateQueue=null,f.memoizedState=null)}var E=$u(o);if(E!==null){E.flags&=-257,Vu(E,o,s,i,t),E.mode&1&&Bu(i,a,t),t=E,u=a;var m=t.updateQueue;if(m===null){var x=new Set;x.add(u),t.updateQueue=x}else m.add(u);break e}else{if(!(t&1)){Bu(i,a,t),Ms();break e}u=Error(C(426))}}else if(K&&s.mode&1){var S=$u(o);if(S!==null){!(S.flags&65536)&&(S.flags|=256),Vu(S,o,s,i,t),gs(_n(u,s));break e}}i=u=_n(u,s),re!==4&&(re=2),or===null?or=[i]:or.push(i),i=o;do{switch(i.tag){case 3:i.flags|=65536,t&=-t,i.lanes|=t;var h=mf(i,u,t);Au(i,h);break e;case 1:s=u;var c=i.type,p=i.stateNode;if(!(i.flags&128)&&(typeof c.getDerivedStateFromError=="function"||p!==null&&typeof p.componentDidCatch=="function"&&(Pt===null||!Pt.has(p)))){i.flags|=65536,t&=-t,i.lanes|=t;var g=yf(i,s,t);Au(i,g);break e}}i=i.return}while(i!==null)}If(n)}catch(k){t=k,ee===n&&n!==null&&(ee=n=n.return);continue}break}while(!0)}function zf(){var e=Ul.current;return Ul.current=Ml,e===null?Ml:e}function Ms(){(re===0||re===3||re===2)&&(re=4),ie===null||!(Yt&268435455)&&!(ri&268435455)||gt(ie,ue)}function Vl(e,t){var n=F;F|=2;var r=zf();(ie!==e||ue!==t)&&(rt=null,Qt(e,t));do try{Wh();break}catch(l){Lf(e,l)}while(!0);if(ws(),F=n,Ul.current=r,ee!==null)throw Error(C(261));return ie=null,ue=0,re}function Wh(){for(;ee!==null;)Af(ee)}function Hh(){for(;ee!==null&&!mp();)Af(ee)}function Af(e){var t=Ff(e.alternate,e,Te);e.memoizedProps=e.pendingProps,t===null?If(e):ee=t,zs.current=null}function If(e){var t=e;do{var n=t.alternate;if(e=t.return,t.flags&32768){if(n=Fh(n,t),n!==null){n.flags&=32767,ee=n;return}if(e!==null)e.flags|=32768,e.subtreeFlags=0,e.deletions=null;else{re=6,ee=null;return}}else if(n=Dh(n,t,Te),n!==null){ee=n;return}if(t=t.sibling,t!==null){ee=t;return}ee=t=e}while(t!==null);re===0&&(re=5)}function Bt(e,t,n){var r=$,l=Be.transition;try{Be.transition=null,$=1,Qh(e,t,n,r)}finally{Be.transition=l,$=r}return null}function Qh(e,t,n,r){do En();while(wt!==null);if(F&6)throw Error(C(327));n=e.finishedWork;var l=e.finishedLanes;if(n===null)return null;if(e.finishedWork=null,e.finishedLanes=0,n===e.current)throw Error(C(177));e.callbackNode=null,e.callbackPriority=0;var i=n.lanes|n.childLanes;if(Np(e,i),e===ie&&(ee=ie=null,ue=0),!(n.subtreeFlags&2064)&&!(n.flags&2064)||Zr||(Zr=!0,Mf(kl,function(){return En(),null})),i=(n.flags&15990)!==0,n.subtreeFlags&15990||i){i=Be.transition,Be.transition=null;var o=$;$=1;var s=F;F|=4,zs.current=null,Uh(e,n),jf(n,e),fh(vo),Nl=!!yo,vo=yo=null,e.current=n,Bh(n),yp(),F=s,$=o,Be.transition=i}else e.current=n;if(Zr&&(Zr=!1,wt=e,$l=l),i=e.pendingLanes,i===0&&(Pt=null),xp(n.stateNode),Ne(e,Z()),t!==null)for(r=e.onRecoverableError,n=0;n<t.length;n++)l=t[n],r(l.value,{componentStack:l.stack,digest:l.digest});if(Bl)throw Bl=!1,e=Fo,Fo=null,e;return $l&1&&e.tag!==0&&En(),i=e.pendingLanes,i&1?e===Mo?sr++:(sr=0,Mo=e):sr=0,It(),null}function En(){if(wt!==null){var e=hc($l),t=Be.transition,n=$;try{if(Be.transition=null,$=16>e?16:e,wt===null)var r=!1;else{if(e=wt,wt=null,$l=0,F&6)throw Error(C(331));var l=F;for(F|=4,j=e.current;j!==null;){var i=j,o=i.child;if(j.flags&16){var s=i.deletions;if(s!==null){for(var u=0;u<s.length;u++){var a=s[u];for(j=a;j!==null;){var f=j;switch(f.tag){case 0:case 11:case 15:ir(8,f,i)}var d=f.child;if(d!==null)d.return=f,j=d;else for(;j!==null;){f=j;var y=f.sibling,E=f.return;if(Rf(f),f===a){j=null;break}if(y!==null){y.return=E,j=y;break}j=E}}}var m=i.alternate;if(m!==null){var x=m.child;if(x!==null){m.child=null;do{var S=x.sibling;x.sibling=null,x=S}while(x!==null)}}j=i}}if(i.subtreeFlags&2064&&o!==null)o.return=i,j=o;else e:for(;j!==null;){if(i=j,i.flags&2048)switch(i.tag){case 0:case 11:case 15:ir(9,i,i.return)}var h=i.sibling;if(h!==null){h.return=i.return,j=h;break e}j=i.return}}var c=e.current;for(j=c;j!==null;){o=j;var p=o.child;if(o.subtreeFlags&2064&&p!==null)p.return=o,j=p;else e:for(o=c;j!==null;){if(s=j,s.flags&2048)try{switch(s.tag){case 0:case 11:case 15:ni(9,s)}}catch(k){Y(s,s.return,k)}if(s===o){j=null;break e}var g=s.sibling;if(g!==null){g.return=s.return,j=g;break e}j=s.return}}if(F=l,It(),tt&&typeof tt.onPostCommitFiberRoot=="function")try{tt.onPostCommitFiberRoot(Xl,e)}catch{}r=!0}return r}finally{$=n,Be.transition=t}}return!1}function ta(e,t,n){t=_n(n,t),t=mf(e,t,1),e=Rt(e,t,1),t=ve(),e!==null&&(_r(e,1,t),Ne(e,t))}function Y(e,t,n){if(e.tag===3)ta(e,e,n);else for(;t!==null;){if(t.tag===3){ta(t,e,n);break}else if(t.tag===1){var r=t.stateNode;if(typeof t.type.getDerivedStateFromError=="function"||typeof r.componentDidCatch=="function"&&(Pt===null||!Pt.has(r))){e=_n(n,e),e=yf(t,e,1),t=Rt(t,e,1),e=ve(),t!==null&&(_r(t,1,e),Ne(t,e));break}}t=t.return}}function Kh(e,t,n){var r=e.pingCache;r!==null&&r.delete(t),t=ve(),e.pingedLanes|=e.suspendedLanes&n,ie===e&&(ue&n)===n&&(re===4||re===3&&(ue&130023424)===ue&&500>Z()-Is?Qt(e,0):As|=n),Ne(e,t)}function Df(e,t){t===0&&(e.mode&1?(t=Wr,Wr<<=1,!(Wr&130023424)&&(Wr=4194304)):t=1);var n=ve();e=ct(e,t),e!==null&&(_r(e,t,n),Ne(e,n))}function Gh(e){var t=e.memoizedState,n=0;t!==null&&(n=t.retryLane),Df(e,n)}function Xh(e,t){var n=0;switch(e.tag){case 13:var r=e.stateNode,l=e.memoizedState;l!==null&&(n=l.retryLane);break;case 19:r=e.stateNode;break;default:throw Error(C(314))}r!==null&&r.delete(t),Df(e,n)}var Ff;Ff=function(e,t,n){if(e!==null)if(e.memoizedProps!==t.pendingProps||ke.current)Ee=!0;else{if(!(e.lanes&n)&&!(t.flags&128))return Ee=!1,Ih(e,t,n);Ee=!!(e.flags&131072)}else Ee=!1,K&&t.flags&1048576&&Bc(t,Ll,t.index);switch(t.lanes=0,t.tag){case 2:var r=t.type;pl(e,t),e=t.pendingProps;var l=Cn(t,he.current);Sn(t,n),l=_s(null,t,r,e,l,n);var i=js();return t.flags|=1,typeof l=="object"&&l!==null&&typeof l.render=="function"&&l.$$typeof===void 0?(t.tag=1,t.memoizedState=null,t.updateQueue=null,Ce(r)?(i=!0,Tl(t)):i=!1,t.memoizedState=l.state!==null&&l.state!==void 0?l.state:null,ks(t),l.updater=ti,t.stateNode=l,l._reactInternals=t,Ro(t,r,e,n),t=jo(null,t,r,!0,i,n)):(t.tag=0,K&&i&&ys(t),ye(null,t,l,n),t=t.child),t;case 16:r=t.elementType;e:{switch(pl(e,t),e=t.pendingProps,l=r._init,r=l(r._payload),t.type=r,l=t.tag=Jh(r),e=He(r,e),l){case 0:t=_o(null,t,r,e,n);break e;case 1:t=Qu(null,t,r,e,n);break e;case 11:t=Wu(null,t,r,e,n);break e;case 14:t=Hu(null,t,r,He(r.type,e),n);break e}throw Error(C(306,r,""))}return t;case 0:return r=t.type,l=t.pendingProps,l=t.elementType===r?l:He(r,l),_o(e,t,r,l,n);case 1:return r=t.type,l=t.pendingProps,l=t.elementType===r?l:He(r,l),Qu(e,t,r,l,n);case 3:e:{if(wf(t),e===null)throw Error(C(387));r=t.pendingProps,i=t.memoizedState,l=i.element,Kc(e,t),Il(t,r,null,n);var o=t.memoizedState;if(r=o.element,i.isDehydrated)if(i={element:r,isDehydrated:!1,cache:o.cache,pendingSuspenseBoundaries:o.pendingSuspenseBoundaries,transitions:o.transitions},t.updateQueue.baseState=i,t.memoizedState=i,t.flags&256){l=_n(Error(C(423)),t),t=Ku(e,t,r,n,l);break e}else if(r!==l){l=_n(Error(C(424)),t),t=Ku(e,t,r,n,l);break e}else for(Oe=Nt(t.stateNode.containerInfo.firstChild),Le=t,K=!0,Ke=null,n=Hc(t,null,r,n),t.child=n;n;)n.flags=n.flags&-3|4096,n=n.sibling;else{if(Nn(),r===l){t=ft(e,t,n);break e}ye(e,t,r,n)}t=t.child}return t;case 5:return Gc(t),e===null&&ko(t),r=t.type,l=t.pendingProps,i=e!==null?e.memoizedProps:null,o=l.children,go(r,l)?o=null:i!==null&&go(r,i)&&(t.flags|=32),xf(e,t),ye(e,t,o,n),t.child;case 6:return e===null&&ko(t),null;case 13:return Sf(e,t,n);case 4:return Cs(t,t.stateNode.containerInfo),r=t.pendingProps,e===null?t.child=Rn(t,null,r,n):ye(e,t,r,n),t.child;case 11:return r=t.type,l=t.pendingProps,l=t.elementType===r?l:He(r,l),Wu(e,t,r,l,n);case 7:return ye(e,t,t.pendingProps,n),t.child;case 8:return ye(e,t,t.pendingProps.children,n),t.child;case 12:return ye(e,t,t.pendingProps.children,n),t.child;case 10:e:{if(r=t.type._context,l=t.pendingProps,i=t.memoizedProps,o=l.value,V(zl,r._currentValue),r._currentValue=o,i!==null)if(qe(i.value,o)){if(i.children===l.children&&!ke.current){t=ft(e,t,n);break e}}else for(i=t.child,i!==null&&(i.return=t);i!==null;){var s=i.dependencies;if(s!==null){o=i.child;for(var u=s.firstContext;u!==null;){if(u.context===r){if(i.tag===1){u=st(-1,n&-n),u.tag=2;var a=i.updateQueue;if(a!==null){a=a.shared;var f=a.pending;f===null?u.next=u:(u.next=f.next,f.next=u),a.pending=u}}i.lanes|=n,u=i.alternate,u!==null&&(u.lanes|=n),Co(i.return,n,t),s.lanes|=n;break}u=u.next}}else if(i.tag===10)o=i.type===t.type?null:i.child;else if(i.tag===18){if(o=i.return,o===null)throw Error(C(341));o.lanes|=n,s=o.alternate,s!==null&&(s.lanes|=n),Co(o,n,t),o=i.sibling}else o=i.child;if(o!==null)o.return=i;else for(o=i;o!==null;){if(o===t){o=null;break}if(i=o.sibling,i!==null){i.return=o.return,o=i;break}o=o.return}i=o}ye(e,t,l.children,n),t=t.child}return t;case 9:return l=t.type,r=t.pendingProps.children,Sn(t,n),l=$e(l),r=r(l),t.flags|=1,ye(e,t,r,n),t.child;case 14:return r=t.type,l=He(r,t.pendingProps),l=He(r.type,l),Hu(e,t,r,l,n);case 15:return vf(e,t,t.type,t.pendingProps,n);case 17:return r=t.type,l=t.pendingProps,l=t.elementType===r?l:He(r,l),pl(e,t),t.tag=1,Ce(r)?(e=!0,Tl(t)):e=!1,Sn(t,n),hf(t,r,l),Ro(t,r,l,n),jo(null,t,r,!0,e,n);case 19:return Ef(e,t,n);case 22:return gf(e,t,n)}throw Error(C(156,t.tag))};function Mf(e,t){return cc(e,t)}function qh(e,t,n,r){this.tag=e,this.key=n,this.sibling=this.child=this.return=this.stateNode=this.type=this.elementType=null,this.index=0,this.ref=null,this.pendingProps=t,this.dependencies=this.memoizedState=this.updateQueue=this.memoizedProps=null,this.mode=r,this.subtreeFlags=this.flags=0,this.deletions=null,this.childLanes=this.lanes=0,this.alternate=null}function Ue(e,t,n,r){return new qh(e,t,n,r)}function Us(e){return e=e.prototype,!(!e||!e.isReactComponent)}function Jh(e){if(typeof e=="function")return Us(e)?1:0;if(e!=null){if(e=e.$$typeof,e===ls)return 11;if(e===is)return 14}return 2}function jt(e,t){var n=e.alternate;return n===null?(n=Ue(e.tag,t,e.key,e.mode),n.elementType=e.elementType,n.type=e.type,n.stateNode=e.stateNode,n.alternate=e,e.alternate=n):(n.pendingProps=t,n.type=e.type,n.flags=0,n.subtreeFlags=0,n.deletions=null),n.flags=e.flags&14680064,n.childLanes=e.childLanes,n.lanes=e.lanes,n.child=e.child,n.memoizedProps=e.memoizedProps,n.memoizedState=e.memoizedState,n.updateQueue=e.updateQueue,t=e.dependencies,n.dependencies=t===null?null:{lanes:t.lanes,firstContext:t.firstContext},n.sibling=e.sibling,n.index=e.index,n.ref=e.ref,n}function yl(e,t,n,r,l,i){var o=2;if(r=e,typeof e=="function")Us(e)&&(o=1);else if(typeof e=="string")o=5;else e:switch(e){case on:return Kt(n.children,l,i,t);case rs:o=8,l|=8;break;case qi:return e=Ue(12,n,t,l|2),e.elementType=qi,e.lanes=i,e;case Ji:return e=Ue(13,n,t,l),e.elementType=Ji,e.lanes=i,e;case Yi:return e=Ue(19,n,t,l),e.elementType=Yi,e.lanes=i,e;case Ga:return li(n,l,i,t);default:if(typeof e=="object"&&e!==null)switch(e.$$typeof){case Qa:o=10;break e;case Ka:o=9;break e;case ls:o=11;break e;case is:o=14;break e;case mt:o=16,r=null;break e}throw Error(C(130,e==null?e:typeof e,""))}return t=Ue(o,n,t,l),t.elementType=e,t.type=r,t.lanes=i,t}function Kt(e,t,n,r){return e=Ue(7,e,r,t),e.lanes=n,e}function li(e,t,n,r){return e=Ue(22,e,r,t),e.elementType=Ga,e.lanes=n,e.stateNode={isHidden:!1},e}function $i(e,t,n){return e=Ue(6,e,null,t),e.lanes=n,e}function Vi(e,t,n){return t=Ue(4,e.children!==null?e.children:[],e.key,t),t.lanes=n,t.stateNode={containerInfo:e.containerInfo,pendingChildren:null,implementation:e.implementation},t}function Yh(e,t,n,r,l){this.tag=t,this.containerInfo=e,this.finishedWork=this.pingCache=this.current=this.pendingChildren=null,this.timeoutHandle=-1,this.callbackNode=this.pendingContext=this.context=null,this.callbackPriority=0,this.eventTimes=Ei(0),this.expirationTimes=Ei(-1),this.entangledLanes=this.finishedLanes=this.mutableReadLanes=this.expiredLanes=this.pingedLanes=this.suspendedLanes=this.pendingLanes=0,this.entanglements=Ei(0),this.identifierPrefix=r,this.onRecoverableError=l,this.mutableSourceEagerHydrationData=null}function Bs(e,t,n,r,l,i,o,s,u){return e=new Yh(e,t,n,s,u),t===1?(t=1,i===!0&&(t|=8)):t=0,i=Ue(3,null,null,t),e.current=i,i.stateNode=e,i.memoizedState={element:r,isDehydrated:n,cache:null,transitions:null,pendingSuspenseBoundaries:null},ks(i),e}function bh(e,t,n){var r=3<arguments.length&&arguments[3]!==void 0?arguments[3]:null;return{$$typeof:ln,key:r==null?null:""+r,children:e,containerInfo:t,implementation:n}}function Uf(e){if(!e)return Lt;e=e._reactInternals;e:{if(tn(e)!==e||e.tag!==1)throw Error(C(170));var t=e;do{switch(t.tag){case 3:t=t.stateNode.context;break e;case 1:if(Ce(t.type)){t=t.stateNode.__reactInternalMemoizedMergedChildContext;break e}}t=t.return}while(t!==null);throw Error(C(171))}if(e.tag===1){var n=e.type;if(Ce(n))return Mc(e,n,t)}return t}function Bf(e,t,n,r,l,i,o,s,u){return e=Bs(n,r,!0,e,l,i,o,s,u),e.context=Uf(null),n=e.current,r=ve(),l=_t(n),i=st(r,l),i.callback=t??null,Rt(n,i,l),e.current.lanes=l,_r(e,l,r),Ne(e,r),e}function ii(e,t,n,r){var l=t.current,i=ve(),o=_t(l);return n=Uf(n),t.context===null?t.context=n:t.pendingContext=n,t=st(i,o),t.payload={element:e},r=r===void 0?null:r,r!==null&&(t.callback=r),e=Rt(l,t,o),e!==null&&(Xe(e,l,o,i),cl(e,l,o)),o}function Wl(e){if(e=e.current,!e.child)return null;switch(e.child.tag){case 5:return e.child.stateNode;default:return e.child.stateNode}}function na(e,t){if(e=e.memoizedState,e!==null&&e.dehydrated!==null){var n=e.retryLane;e.retryLane=n!==0&&n<t?n:t}}function $s(e,t){na(e,t),(e=e.alternate)&&na(e,t)}function Zh(){return null}var $f=typeof reportError=="function"?reportError:function(e){console.error(e)};function Vs(e){this._internalRoot=e}oi.prototype.render=Vs.prototype.render=function(e){var t=this._internalRoot;if(t===null)throw Error(C(409));ii(e,t,null,null)};oi.prototype.unmount=Vs.prototype.unmount=function(){var e=this._internalRoot;if(e!==null){this._internalRoot=null;var t=e.containerInfo;bt(function(){ii(null,e,null,null)}),t[at]=null}};function oi(e){this._internalRoot=e}oi.prototype.unstable_scheduleHydration=function(e){if(e){var t=vc();e={blockedOn:null,target:e,priority:t};for(var n=0;n<vt.length&&t!==0&&t<vt[n].priority;n++);vt.splice(n,0,e),n===0&&xc(e)}};function Ws(e){return!(!e||e.nodeType!==1&&e.nodeType!==9&&e.nodeType!==11)}function si(e){return!(!e||e.nodeType!==1&&e.nodeType!==9&&e.nodeType!==11&&(e.nodeType!==8||e.nodeValue!==" react-mount-point-unstable "))}function ra(){}function em(e,t,n,r,l){if(l){if(typeof r=="function"){var i=r;r=function(){var a=Wl(o);i.call(a)}}var o=Bf(t,r,e,0,null,!1,!1,"",ra);return e._reactRootContainer=o,e[at]=o.current,yr(e.nodeType===8?e.parentNode:e),bt(),o}for(;l=e.lastChild;)e.removeChild(l);if(typeof r=="function"){var s=r;r=function(){var a=Wl(u);s.call(a)}}var u=Bs(e,0,!1,null,null,!1,!1,"",ra);return e._reactRootContainer=u,e[at]=u.current,yr(e.nodeType===8?e.parentNode:e),bt(function(){ii(t,u,n,r)}),u}function ui(e,t,n,r,l){var i=n._reactRootContainer;if(i){var o=i;if(typeof l=="function"){var s=l;l=function(){var u=Wl(o);s.call(u)}}ii(t,o,e,l)}else o=em(n,t,e,l,r);return Wl(o)}mc=function(e){switch(e.tag){case 3:var t=e.stateNode;if(t.current.memoizedState.isDehydrated){var n=Yn(t.pendingLanes);n!==0&&(us(t,n|1),Ne(t,Z()),!(F&6)&&(jn=Z()+500,It()))}break;case 13:bt(function(){var r=ct(e,1);if(r!==null){var l=ve();Xe(r,e,1,l)}}),$s(e,1)}};as=function(e){if(e.tag===13){var t=ct(e,134217728);if(t!==null){var n=ve();Xe(t,e,134217728,n)}$s(e,134217728)}};yc=function(e){if(e.tag===13){var t=_t(e),n=ct(e,t);if(n!==null){var r=ve();Xe(n,e,t,r)}$s(e,t)}};vc=function(){return $};gc=function(e,t){var n=$;try{return $=e,t()}finally{$=n}};so=function(e,t,n){switch(t){case"input":if(eo(e,n),t=n.name,n.type==="radio"&&t!=null){for(n=e;n.parentNode;)n=n.parentNode;for(n=n.querySelectorAll("input[name="+JSON.stringify(""+t)+'][type="radio"]'),t=0;t<n.length;t++){var r=n[t];if(r!==e&&r.form===e.form){var l=bl(r);if(!l)throw Error(C(90));qa(r),eo(r,l)}}}break;case"textarea":Ya(e,n);break;case"select":t=n.value,t!=null&&vn(e,!!n.multiple,t,!1)}};lc=Ds;ic=bt;var tm={usingClientEntryPoint:!1,Events:[Tr,cn,bl,nc,rc,Ds]},Kn={findFiberByHostInstance:$t,bundleType:0,version:"18.3.1",rendererPackageName:"react-dom"},nm={bundleType:Kn.bundleType,version:Kn.version,rendererPackageName:Kn.rendererPackageName,rendererConfig:Kn.rendererConfig,overrideHookState:null,overrideHookStateDeletePath:null,overrideHookStateRenamePath:null,overrideProps:null,overridePropsDeletePath:null,overridePropsRenamePath:null,setErrorHandler:null,setSuspenseHandler:null,scheduleUpdate:null,currentDispatcherRef:dt.ReactCurrentDispatcher,findHostInstanceByFiber:function(e){return e=uc(e),e===null?null:e.stateNode},findFiberByHostInstance:Kn.findFiberByHostInstance||Zh,findHostInstancesForRefresh:null,scheduleRefresh:null,scheduleRoot:null,setRefreshHandler:null,getCurrentFiber:null,reconcilerVersion:"18.3.1-next-f1338f8080-20240426"};if(typeof __REACT_DEVTOOLS_GLOBAL_HOOK__<"u"){var el=__REACT_DEVTOOLS_GLOBAL_HOOK__;if(!el.isDisabled&&el.supportsFiber)try{Xl=el.inject(nm),tt=el}catch{}}Ae.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED=tm;Ae.createPortal=function(e,t){var n=2<arguments.length&&arguments[2]!==void 0?arguments[2]:null;if(!Ws(t))throw Error(C(200));return bh(e,t,null,n)};Ae.createRoot=function(e,t){if(!Ws(e))throw Error(C(299));var n=!1,r="",l=$f;return t!=null&&(t.unstable_strictMode===!0&&(n=!0),t.identifierPrefix!==void 0&&(r=t.identifierPrefix),t.onRecoverableError!==void 0&&(l=t.onRecoverableError)),t=Bs(e,1,!1,null,null,n,!1,r,l),e[at]=t.current,yr(e.nodeType===8?e.parentNode:e),new Vs(t)};Ae.findDOMNode=function(e){if(e==null)return null;if(e.nodeType===1)return e;var t=e._reactInternals;if(t===void 0)throw typeof e.render=="function"?Error(C(188)):(e=Object.keys(e).join(","),Error(C(268,e)));return e=uc(t),e=e===null?null:e.stateNode,e};Ae.flushSync=function(e){return bt(e)};Ae.hydrate=function(e,t,n){if(!si(t))throw Error(C(200));return ui(null,e,t,!0,n)};Ae.hydrateRoot=function(e,t,n){if(!Ws(e))throw Error(C(405));var r=n!=null&&n.hydratedSources||null,l=!1,i="",o=$f;if(n!=null&&(n.unstable_strictMode===!0&&(l=!0),n.identifierPrefix!==void 0&&(i=n.identifierPrefix),n.onRecoverableError!==void 0&&(o=n.onRecoverableError)),t=Bf(t,null,e,1,n??null,l,!1,i,o),e[at]=t.current,yr(e),r)for(e=0;e<r.length;e++)n=r[e],l=n._getVersion,l=l(n._source),t.mutableSourceEagerHydrationData==null?t.mutableSourceEagerHydrationData=[n,l]:t.mutableSourceEagerHydrationData.push(n,l);return new oi(t)};Ae.render=function(e,t,n){if(!si(t))throw Error(C(200));return ui(null,e,t,!1,n)};Ae.unmountComponentAtNode=function(e){if(!si(e))throw Error(C(40));return e._reactRootContainer?(bt(function(){ui(null,null,e,!1,function(){e._reactRootContainer=null,e[at]=null})}),!0):!1};Ae.unstable_batchedUpdates=Ds;Ae.unstable_renderSubtreeIntoContainer=function(e,t,n,r){if(!si(n))throw Error(C(200));if(e==null||e._reactInternals===void 0)throw Error(C(38));return ui(e,t,n,!1,r)};Ae.version="18.3.1-next-f1338f8080-20240426";function Vf(){if(!(typeof __REACT_DEVTOOLS_GLOBAL_HOOK__>"u"||typeof __REACT_DEVTOOLS_GLOBAL_HOOK__.checkDCE!="function"))try{__REACT_DEVTOOLS_GLOBAL_HOOK__.checkDCE(Vf)}catch(e){console.error(e)}}Vf(),$a.exports=Ae;var rm=$a.exports,la=rm;Gi.createRoot=la.createRoot,Gi.hydrateRoot=la.hydrateRoot;/**
 * @remix-run/router v1.23.2
 *
 * Copyright (c) Remix Software Inc.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE.md file in the root directory of this source tree.
 *
 * @license MIT
 */function Nr(){return Nr=Object.assign?Object.assign.bind():function(e){for(var t=1;t<arguments.length;t++){var n=arguments[t];for(var r in n)Object.prototype.hasOwnProperty.call(n,r)&&(e[r]=n[r])}return e},Nr.apply(this,arguments)}var St;(function(e){e.Pop="POP",e.Push="PUSH",e.Replace="REPLACE"})(St||(St={}));const ia="popstate";function lm(e){e===void 0&&(e={});function t(r,l){let{pathname:i,search:o,hash:s}=r.location;return $o("",{pathname:i,search:o,hash:s},l.state&&l.state.usr||null,l.state&&l.state.key||"default")}function n(r,l){return typeof l=="string"?l:Hl(l)}return om(t,n,null,e)}function b(e,t){if(e===!1||e===null||typeof e>"u")throw new Error(t)}function Hs(e,t){if(!e){typeof console<"u"&&console.warn(t);try{throw new Error(t)}catch{}}}function im(){return Math.random().toString(36).substr(2,8)}function oa(e,t){return{usr:e.state,key:e.key,idx:t}}function $o(e,t,n,r){return n===void 0&&(n=null),Nr({pathname:typeof e=="string"?e:e.pathname,search:"",hash:""},typeof t=="string"?In(t):t,{state:n,key:t&&t.key||r||im()})}function Hl(e){let{pathname:t="/",search:n="",hash:r=""}=e;return n&&n!=="?"&&(t+=n.charAt(0)==="?"?n:"?"+n),r&&r!=="#"&&(t+=r.charAt(0)==="#"?r:"#"+r),t}function In(e){let t={};if(e){let n=e.indexOf("#");n>=0&&(t.hash=e.substr(n),e=e.substr(0,n));let r=e.indexOf("?");r>=0&&(t.search=e.substr(r),e=e.substr(0,r)),e&&(t.pathname=e)}return t}function om(e,t,n,r){r===void 0&&(r={});let{window:l=document.defaultView,v5Compat:i=!1}=r,o=l.history,s=St.Pop,u=null,a=f();a==null&&(a=0,o.replaceState(Nr({},o.state,{idx:a}),""));function f(){return(o.state||{idx:null}).idx}function d(){s=St.Pop;let S=f(),h=S==null?null:S-a;a=S,u&&u({action:s,location:x.location,delta:h})}function y(S,h){s=St.Push;let c=$o(x.location,S,h);a=f()+1;let p=oa(c,a),g=x.createHref(c);try{o.pushState(p,"",g)}catch(k){if(k instanceof DOMException&&k.name==="DataCloneError")throw k;l.location.assign(g)}i&&u&&u({action:s,location:x.location,delta:1})}function E(S,h){s=St.Replace;let c=$o(x.location,S,h);a=f();let p=oa(c,a),g=x.createHref(c);o.replaceState(p,"",g),i&&u&&u({action:s,location:x.location,delta:0})}function m(S){let h=l.location.origin!=="null"?l.location.origin:l.location.href,c=typeof S=="string"?S:Hl(S);return c=c.replace(/ $/,"%20"),b(h,"No window.location.(origin|href) available to create URL for href: "+c),new URL(c,h)}let x={get action(){return s},get location(){return e(l,o)},listen(S){if(u)throw new Error("A history only accepts one active listener");return l.addEventListener(ia,d),u=S,()=>{l.removeEventListener(ia,d),u=null}},createHref(S){return t(l,S)},createURL:m,encodeLocation(S){let h=m(S);return{pathname:h.pathname,search:h.search,hash:h.hash}},push:y,replace:E,go(S){return o.go(S)}};return x}var sa;(function(e){e.data="data",e.deferred="deferred",e.redirect="redirect",e.error="error"})(sa||(sa={}));function sm(e,t,n){return n===void 0&&(n="/"),um(e,t,n)}function um(e,t,n,r){let l=typeof t=="string"?In(t):t,i=Tn(l.pathname||"/",n);if(i==null)return null;let o=Wf(e);am(o);let s=null;for(let u=0;s==null&&u<o.length;++u){let a=wm(i);s=gm(o[u],a)}return s}function Wf(e,t,n,r){t===void 0&&(t=[]),n===void 0&&(n=[]),r===void 0&&(r="");let l=(i,o,s)=>{let u={relativePath:s===void 0?i.path||"":s,caseSensitive:i.caseSensitive===!0,childrenIndex:o,route:i};u.relativePath.startsWith("/")&&(b(u.relativePath.startsWith(r),'Absolute route path "'+u.relativePath+'" nested under path '+('"'+r+'" is not valid. An absolute child route path ')+"must start with the combined path of all its parent routes."),u.relativePath=u.relativePath.slice(r.length));let a=Tt([r,u.relativePath]),f=n.concat(u);i.children&&i.children.length>0&&(b(i.index!==!0,"Index routes must not have child routes. Please remove "+('all child routes from route path "'+a+'".')),Wf(i.children,t,f,a)),!(i.path==null&&!i.index)&&t.push({path:a,score:ym(a,i.index),routesMeta:f})};return e.forEach((i,o)=>{var s;if(i.path===""||!((s=i.path)!=null&&s.includes("?")))l(i,o);else for(let u of Hf(i.path))l(i,o,u)}),t}function Hf(e){let t=e.split("/");if(t.length===0)return[];let[n,...r]=t,l=n.endsWith("?"),i=n.replace(/\?$/,"");if(r.length===0)return l?[i,""]:[i];let o=Hf(r.join("/")),s=[];return s.push(...o.map(u=>u===""?i:[i,u].join("/"))),l&&s.push(...o),s.map(u=>e.startsWith("/")&&u===""?"/":u)}function am(e){e.sort((t,n)=>t.score!==n.score?n.score-t.score:vm(t.routesMeta.map(r=>r.childrenIndex),n.routesMeta.map(r=>r.childrenIndex)))}const cm=/^:[\w-]+$/,fm=3,dm=2,pm=1,hm=10,mm=-2,ua=e=>e==="*";function ym(e,t){let n=e.split("/"),r=n.length;return n.some(ua)&&(r+=mm),t&&(r+=dm),n.filter(l=>!ua(l)).reduce((l,i)=>l+(cm.test(i)?fm:i===""?pm:hm),r)}function vm(e,t){return e.length===t.length&&e.slice(0,-1).every((r,l)=>r===t[l])?e[e.length-1]-t[t.length-1]:0}function gm(e,t,n){let{routesMeta:r}=e,l={},i="/",o=[];for(let s=0;s<r.length;++s){let u=r[s],a=s===r.length-1,f=i==="/"?t:t.slice(i.length)||"/",d=Vo({path:u.relativePath,caseSensitive:u.caseSensitive,end:a},f),y=u.route;if(!d)return null;Object.assign(l,d.params),o.push({params:l,pathname:Tt([i,d.pathname]),pathnameBase:Nm(Tt([i,d.pathnameBase])),route:y}),d.pathnameBase!=="/"&&(i=Tt([i,d.pathnameBase]))}return o}function Vo(e,t){typeof e=="string"&&(e={path:e,caseSensitive:!1,end:!0});let[n,r]=xm(e.path,e.caseSensitive,e.end),l=t.match(n);if(!l)return null;let i=l[0],o=i.replace(/(.)\/+$/,"$1"),s=l.slice(1);return{params:r.reduce((a,f,d)=>{let{paramName:y,isOptional:E}=f;if(y==="*"){let x=s[d]||"";o=i.slice(0,i.length-x.length).replace(/(.)\/+$/,"$1")}const m=s[d];return E&&!m?a[y]=void 0:a[y]=(m||"").replace(/%2F/g,"/"),a},{}),pathname:i,pathnameBase:o,pattern:e}}function xm(e,t,n){t===void 0&&(t=!1),n===void 0&&(n=!0),Hs(e==="*"||!e.endsWith("*")||e.endsWith("/*"),'Route path "'+e+'" will be treated as if it were '+('"'+e.replace(/\*$/,"/*")+'" because the `*` character must ')+"always follow a `/` in the pattern. To get rid of this warning, "+('please change the route path to "'+e.replace(/\*$/,"/*")+'".'));let r=[],l="^"+e.replace(/\/*\*?$/,"").replace(/^\/*/,"/").replace(/[\\.*+^${}|()[\]]/g,"\\$&").replace(/\/:([\w-]+)(\?)?/g,(o,s,u)=>(r.push({paramName:s,isOptional:u!=null}),u?"/?([^\\/]+)?":"/([^\\/]+)"));return e.endsWith("*")?(r.push({paramName:"*"}),l+=e==="*"||e==="/*"?"(.*)$":"(?:\\/(.+)|\\/*)$"):n?l+="\\/*$":e!==""&&e!=="/"&&(l+="(?:(?=\\/|$))"),[new RegExp(l,t?void 0:"i"),r]}function wm(e){try{return e.split("/").map(t=>decodeURIComponent(t).replace(/\//g,"%2F")).join("/")}catch(t){return Hs(!1,'The URL path "'+e+'" could not be decoded because it is is a malformed URL segment. This is probably due to a bad percent '+("encoding ("+t+").")),e}}function Tn(e,t){if(t==="/")return e;if(!e.toLowerCase().startsWith(t.toLowerCase()))return null;let n=t.endsWith("/")?t.length-1:t.length,r=e.charAt(n);return r&&r!=="/"?null:e.slice(n)||"/"}const Sm=/^(?:[a-z][a-z0-9+.-]*:|\/\/)/i,Em=e=>Sm.test(e);function km(e,t){t===void 0&&(t="/");let{pathname:n,search:r="",hash:l=""}=typeof e=="string"?In(e):e,i;if(n)if(Em(n))i=n;else{if(n.includes("//")){let o=n;n=n.replace(/\/\/+/g,"/"),Hs(!1,"Pathnames cannot have embedded double slashes - normalizing "+(o+" -> "+n))}n.startsWith("/")?i=aa(n.substring(1),"/"):i=aa(n,t)}else i=t;return{pathname:i,search:Rm(r),hash:Pm(l)}}function aa(e,t){let n=t.replace(/\/+$/,"").split("/");return e.split("/").forEach(l=>{l===".."?n.length>1&&n.pop():l!=="."&&n.push(l)}),n.length>1?n.join("/"):"/"}function Wi(e,t,n,r){return"Cannot include a '"+e+"' character in a manually specified "+("`to."+t+"` field ["+JSON.stringify(r)+"].  Please separate it out to the ")+("`to."+n+"` field. Alternatively you may provide the full path as ")+'a string in <Link to="..."> and the router will parse it for you.'}function Cm(e){return e.filter((t,n)=>n===0||t.route.path&&t.route.path.length>0)}function Qf(e,t){let n=Cm(e);return t?n.map((r,l)=>l===n.length-1?r.pathname:r.pathnameBase):n.map(r=>r.pathnameBase)}function Kf(e,t,n,r){r===void 0&&(r=!1);let l;typeof e=="string"?l=In(e):(l=Nr({},e),b(!l.pathname||!l.pathname.includes("?"),Wi("?","pathname","search",l)),b(!l.pathname||!l.pathname.includes("#"),Wi("#","pathname","hash",l)),b(!l.search||!l.search.includes("#"),Wi("#","search","hash",l)));let i=e===""||l.pathname==="",o=i?"/":l.pathname,s;if(o==null)s=n;else{let d=t.length-1;if(!r&&o.startsWith("..")){let y=o.split("/");for(;y[0]==="..";)y.shift(),d-=1;l.pathname=y.join("/")}s=d>=0?t[d]:"/"}let u=km(l,s),a=o&&o!=="/"&&o.endsWith("/"),f=(i||o===".")&&n.endsWith("/");return!u.pathname.endsWith("/")&&(a||f)&&(u.pathname+="/"),u}const Tt=e=>e.join("/").replace(/\/\/+/g,"/"),Nm=e=>e.replace(/\/+$/,"").replace(/^\/*/,"/"),Rm=e=>!e||e==="?"?"":e.startsWith("?")?e:"?"+e,Pm=e=>!e||e==="#"?"":e.startsWith("#")?e:"#"+e;function _m(e){return e!=null&&typeof e.status=="number"&&typeof e.statusText=="string"&&typeof e.internal=="boolean"&&"data"in e}const Gf=["post","put","patch","delete"];new Set(Gf);const jm=["get",...Gf];new Set(jm);/**
 * React Router v6.30.3
 *
 * Copyright (c) Remix Software Inc.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE.md file in the root directory of this source tree.
 *
 * @license MIT
 */function Rr(){return Rr=Object.assign?Object.assign.bind():function(e){for(var t=1;t<arguments.length;t++){var n=arguments[t];for(var r in n)Object.prototype.hasOwnProperty.call(n,r)&&(e[r]=n[r])}return e},Rr.apply(this,arguments)}const ai=N.createContext(null),Xf=N.createContext(null),Dt=N.createContext(null),ci=N.createContext(null),Ft=N.createContext({outlet:null,matches:[],isDataRoute:!1}),qf=N.createContext(null);function Tm(e,t){let{relative:n}=t===void 0?{}:t;Lr()||b(!1);let{basename:r,navigator:l}=N.useContext(Dt),{hash:i,pathname:o,search:s}=fi(e,{relative:n}),u=o;return r!=="/"&&(u=o==="/"?r:Tt([r,o])),l.createHref({pathname:u,search:s,hash:i})}function Lr(){return N.useContext(ci)!=null}function Dn(){return Lr()||b(!1),N.useContext(ci).location}function Jf(e){N.useContext(Dt).static||N.useLayoutEffect(e)}function Om(){let{isDataRoute:e}=N.useContext(Ft);return e?Qm():Lm()}function Lm(){Lr()||b(!1);let e=N.useContext(ai),{basename:t,future:n,navigator:r}=N.useContext(Dt),{matches:l}=N.useContext(Ft),{pathname:i}=Dn(),o=JSON.stringify(Qf(l,n.v7_relativeSplatPath)),s=N.useRef(!1);return Jf(()=>{s.current=!0}),N.useCallback(function(a,f){if(f===void 0&&(f={}),!s.current)return;if(typeof a=="number"){r.go(a);return}let d=Kf(a,JSON.parse(o),i,f.relative==="path");e==null&&t!=="/"&&(d.pathname=d.pathname==="/"?t:Tt([t,d.pathname])),(f.replace?r.replace:r.push)(d,f.state,f)},[t,r,o,i,e])}function zm(){let{matches:e}=N.useContext(Ft),t=e[e.length-1];return t?t.params:{}}function fi(e,t){let{relative:n}=t===void 0?{}:t,{future:r}=N.useContext(Dt),{matches:l}=N.useContext(Ft),{pathname:i}=Dn(),o=JSON.stringify(Qf(l,r.v7_relativeSplatPath));return N.useMemo(()=>Kf(e,JSON.parse(o),i,n==="path"),[e,o,i,n])}function Am(e,t){return Im(e,t)}function Im(e,t,n,r){Lr()||b(!1);let{navigator:l}=N.useContext(Dt),{matches:i}=N.useContext(Ft),o=i[i.length-1],s=o?o.params:{};o&&o.pathname;let u=o?o.pathnameBase:"/";o&&o.route;let a=Dn(),f;if(t){var d;let S=typeof t=="string"?In(t):t;u==="/"||(d=S.pathname)!=null&&d.startsWith(u)||b(!1),f=S}else f=a;let y=f.pathname||"/",E=y;if(u!=="/"){let S=u.replace(/^\//,"").split("/");E="/"+y.replace(/^\//,"").split("/").slice(S.length).join("/")}let m=sm(e,{pathname:E}),x=Bm(m&&m.map(S=>Object.assign({},S,{params:Object.assign({},s,S.params),pathname:Tt([u,l.encodeLocation?l.encodeLocation(S.pathname).pathname:S.pathname]),pathnameBase:S.pathnameBase==="/"?u:Tt([u,l.encodeLocation?l.encodeLocation(S.pathnameBase).pathname:S.pathnameBase])})),i,n,r);return t&&x?N.createElement(ci.Provider,{value:{location:Rr({pathname:"/",search:"",hash:"",state:null,key:"default"},f),navigationType:St.Pop}},x):x}function Dm(){let e=Hm(),t=_m(e)?e.status+" "+e.statusText:e instanceof Error?e.message:JSON.stringify(e),n=e instanceof Error?e.stack:null,l={padding:"0.5rem",backgroundColor:"rgba(200,200,200, 0.5)"};return N.createElement(N.Fragment,null,N.createElement("h2",null,"Unexpected Application Error!"),N.createElement("h3",{style:{fontStyle:"italic"}},t),n?N.createElement("pre",{style:l},n):null,null)}const Fm=N.createElement(Dm,null);class Mm extends N.Component{constructor(t){super(t),this.state={location:t.location,revalidation:t.revalidation,error:t.error}}static getDerivedStateFromError(t){return{error:t}}static getDerivedStateFromProps(t,n){return n.location!==t.location||n.revalidation!=="idle"&&t.revalidation==="idle"?{error:t.error,location:t.location,revalidation:t.revalidation}:{error:t.error!==void 0?t.error:n.error,location:n.location,revalidation:t.revalidation||n.revalidation}}componentDidCatch(t,n){console.error("React Router caught the following error during render",t,n)}render(){return this.state.error!==void 0?N.createElement(Ft.Provider,{value:this.props.routeContext},N.createElement(qf.Provider,{value:this.state.error,children:this.props.component})):this.props.children}}function Um(e){let{routeContext:t,match:n,children:r}=e,l=N.useContext(ai);return l&&l.static&&l.staticContext&&(n.route.errorElement||n.route.ErrorBoundary)&&(l.staticContext._deepestRenderedBoundaryId=n.route.id),N.createElement(Ft.Provider,{value:t},r)}function Bm(e,t,n,r){var l;if(t===void 0&&(t=[]),n===void 0&&(n=null),r===void 0&&(r=null),e==null){var i;if(!n)return null;if(n.errors)e=n.matches;else if((i=r)!=null&&i.v7_partialHydration&&t.length===0&&!n.initialized&&n.matches.length>0)e=n.matches;else return null}let o=e,s=(l=n)==null?void 0:l.errors;if(s!=null){let f=o.findIndex(d=>d.route.id&&(s==null?void 0:s[d.route.id])!==void 0);f>=0||b(!1),o=o.slice(0,Math.min(o.length,f+1))}let u=!1,a=-1;if(n&&r&&r.v7_partialHydration)for(let f=0;f<o.length;f++){let d=o[f];if((d.route.HydrateFallback||d.route.hydrateFallbackElement)&&(a=f),d.route.id){let{loaderData:y,errors:E}=n,m=d.route.loader&&y[d.route.id]===void 0&&(!E||E[d.route.id]===void 0);if(d.route.lazy||m){u=!0,a>=0?o=o.slice(0,a+1):o=[o[0]];break}}}return o.reduceRight((f,d,y)=>{let E,m=!1,x=null,S=null;n&&(E=s&&d.route.id?s[d.route.id]:void 0,x=d.route.errorElement||Fm,u&&(a<0&&y===0?(Km("route-fallback"),m=!0,S=null):a===y&&(m=!0,S=d.route.hydrateFallbackElement||null)));let h=t.concat(o.slice(0,y+1)),c=()=>{let p;return E?p=x:m?p=S:d.route.Component?p=N.createElement(d.route.Component,null):d.route.element?p=d.route.element:p=f,N.createElement(Um,{match:d,routeContext:{outlet:f,matches:h,isDataRoute:n!=null},children:p})};return n&&(d.route.ErrorBoundary||d.route.errorElement||y===0)?N.createElement(Mm,{location:n.location,revalidation:n.revalidation,component:x,error:E,children:c(),routeContext:{outlet:null,matches:h,isDataRoute:!0}}):c()},null)}var Yf=function(e){return e.UseBlocker="useBlocker",e.UseRevalidator="useRevalidator",e.UseNavigateStable="useNavigate",e}(Yf||{}),bf=function(e){return e.UseBlocker="useBlocker",e.UseLoaderData="useLoaderData",e.UseActionData="useActionData",e.UseRouteError="useRouteError",e.UseNavigation="useNavigation",e.UseRouteLoaderData="useRouteLoaderData",e.UseMatches="useMatches",e.UseRevalidator="useRevalidator",e.UseNavigateStable="useNavigate",e.UseRouteId="useRouteId",e}(bf||{});function $m(e){let t=N.useContext(ai);return t||b(!1),t}function Vm(e){let t=N.useContext(Xf);return t||b(!1),t}function Wm(e){let t=N.useContext(Ft);return t||b(!1),t}function Zf(e){let t=Wm(),n=t.matches[t.matches.length-1];return n.route.id||b(!1),n.route.id}function Hm(){var e;let t=N.useContext(qf),n=Vm(),r=Zf();return t!==void 0?t:(e=n.errors)==null?void 0:e[r]}function Qm(){let{router:e}=$m(Yf.UseNavigateStable),t=Zf(bf.UseNavigateStable),n=N.useRef(!1);return Jf(()=>{n.current=!0}),N.useCallback(function(l,i){i===void 0&&(i={}),n.current&&(typeof l=="number"?e.navigate(l):e.navigate(l,Rr({fromRouteId:t},i)))},[e,t])}const ca={};function Km(e,t,n){ca[e]||(ca[e]=!0)}function Gm(e,t){e==null||e.v7_startTransition,e==null||e.v7_relativeSplatPath}function Wo(e){b(!1)}function Xm(e){let{basename:t="/",children:n=null,location:r,navigationType:l=St.Pop,navigator:i,static:o=!1,future:s}=e;Lr()&&b(!1);let u=t.replace(/^\/*/,"/"),a=N.useMemo(()=>({basename:u,navigator:i,static:o,future:Rr({v7_relativeSplatPath:!1},s)}),[u,s,i,o]);typeof r=="string"&&(r=In(r));let{pathname:f="/",search:d="",hash:y="",state:E=null,key:m="default"}=r,x=N.useMemo(()=>{let S=Tn(f,u);return S==null?null:{location:{pathname:S,search:d,hash:y,state:E,key:m},navigationType:l}},[u,f,d,y,E,m,l]);return x==null?null:N.createElement(Dt.Provider,{value:a},N.createElement(ci.Provider,{children:n,value:x}))}function qm(e){let{children:t,location:n}=e;return Am(Ho(t),n)}new Promise(()=>{});function Ho(e,t){t===void 0&&(t=[]);let n=[];return N.Children.forEach(e,(r,l)=>{if(!N.isValidElement(r))return;let i=[...t,l];if(r.type===N.Fragment){n.push.apply(n,Ho(r.props.children,i));return}r.type!==Wo&&b(!1),!r.props.index||!r.props.children||b(!1);let o={id:r.props.id||i.join("-"),caseSensitive:r.props.caseSensitive,element:r.props.element,Component:r.props.Component,index:r.props.index,path:r.props.path,loader:r.props.loader,action:r.props.action,errorElement:r.props.errorElement,ErrorBoundary:r.props.ErrorBoundary,hasErrorBoundary:r.props.ErrorBoundary!=null||r.props.errorElement!=null,shouldRevalidate:r.props.shouldRevalidate,handle:r.props.handle,lazy:r.props.lazy};r.props.children&&(o.children=Ho(r.props.children,i)),n.push(o)}),n}/**
 * React Router DOM v6.30.3
 *
 * Copyright (c) Remix Software Inc.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE.md file in the root directory of this source tree.
 *
 * @license MIT
 */function Ql(){return Ql=Object.assign?Object.assign.bind():function(e){for(var t=1;t<arguments.length;t++){var n=arguments[t];for(var r in n)Object.prototype.hasOwnProperty.call(n,r)&&(e[r]=n[r])}return e},Ql.apply(this,arguments)}function ed(e,t){if(e==null)return{};var n={},r=Object.keys(e),l,i;for(i=0;i<r.length;i++)l=r[i],!(t.indexOf(l)>=0)&&(n[l]=e[l]);return n}function Jm(e){return!!(e.metaKey||e.altKey||e.ctrlKey||e.shiftKey)}function Ym(e,t){return e.button===0&&(!t||t==="_self")&&!Jm(e)}const bm=["onClick","relative","reloadDocument","replace","state","target","to","preventScrollReset","viewTransition"],Zm=["aria-current","caseSensitive","className","end","style","to","viewTransition","children"],e0="6";try{window.__reactRouterVersion=e0}catch{}const t0=N.createContext({isTransitioning:!1}),n0="startTransition",fa=Kd[n0];function r0(e){let{basename:t,children:n,future:r,window:l}=e,i=N.useRef();i.current==null&&(i.current=lm({window:l,v5Compat:!0}));let o=i.current,[s,u]=N.useState({action:o.action,location:o.location}),{v7_startTransition:a}=r||{},f=N.useCallback(d=>{a&&fa?fa(()=>u(d)):u(d)},[u,a]);return N.useLayoutEffect(()=>o.listen(f),[o,f]),N.useEffect(()=>Gm(r),[r]),N.createElement(Xm,{basename:t,children:n,location:s.location,navigationType:s.action,navigator:o,future:r})}const l0=typeof window<"u"&&typeof window.document<"u"&&typeof window.document.createElement<"u",i0=/^(?:[a-z][a-z0-9+.-]*:|\/\/)/i,o0=N.forwardRef(function(t,n){let{onClick:r,relative:l,reloadDocument:i,replace:o,state:s,target:u,to:a,preventScrollReset:f,viewTransition:d}=t,y=ed(t,bm),{basename:E}=N.useContext(Dt),m,x=!1;if(typeof a=="string"&&i0.test(a)&&(m=a,l0))try{let p=new URL(window.location.href),g=a.startsWith("//")?new URL(p.protocol+a):new URL(a),k=Tn(g.pathname,E);g.origin===p.origin&&k!=null?a=k+g.search+g.hash:x=!0}catch{}let S=Tm(a,{relative:l}),h=u0(a,{replace:o,state:s,target:u,preventScrollReset:f,relative:l,viewTransition:d});function c(p){r&&r(p),p.defaultPrevented||h(p)}return N.createElement("a",Ql({},y,{href:m||S,onClick:x||i?r:c,ref:n,target:u}))}),tl=N.forwardRef(function(t,n){let{"aria-current":r="page",caseSensitive:l=!1,className:i="",end:o=!1,style:s,to:u,viewTransition:a,children:f}=t,d=ed(t,Zm),y=fi(u,{relative:d.relative}),E=Dn(),m=N.useContext(Xf),{navigator:x,basename:S}=N.useContext(Dt),h=m!=null&&a0(y)&&a===!0,c=x.encodeLocation?x.encodeLocation(y).pathname:y.pathname,p=E.pathname,g=m&&m.navigation&&m.navigation.location?m.navigation.location.pathname:null;l||(p=p.toLowerCase(),g=g?g.toLowerCase():null,c=c.toLowerCase()),g&&S&&(g=Tn(g,S)||g);const k=c!=="/"&&c.endsWith("/")?c.length-1:c.length;let _=p===c||!o&&p.startsWith(c)&&p.charAt(k)==="/",P=g!=null&&(g===c||!o&&g.startsWith(c)&&g.charAt(c.length)==="/"),T={isActive:_,isPending:P,isTransitioning:h},M=_?r:void 0,L;typeof i=="function"?L=i(T):L=[i,_?"active":null,P?"pending":null,h?"transitioning":null].filter(Boolean).join(" ");let te=typeof s=="function"?s(T):s;return N.createElement(o0,Ql({},d,{"aria-current":M,className:L,ref:n,style:te,to:u,viewTransition:a}),typeof f=="function"?f(T):f)});var Qo;(function(e){e.UseScrollRestoration="useScrollRestoration",e.UseSubmit="useSubmit",e.UseSubmitFetcher="useSubmitFetcher",e.UseFetcher="useFetcher",e.useViewTransitionState="useViewTransitionState"})(Qo||(Qo={}));var da;(function(e){e.UseFetcher="useFetcher",e.UseFetchers="useFetchers",e.UseScrollRestoration="useScrollRestoration"})(da||(da={}));function s0(e){let t=N.useContext(ai);return t||b(!1),t}function u0(e,t){let{target:n,replace:r,state:l,preventScrollReset:i,relative:o,viewTransition:s}=t===void 0?{}:t,u=Om(),a=Dn(),f=fi(e,{relative:o});return N.useCallback(d=>{if(Ym(d,n)){d.preventDefault();let y=r!==void 0?r:Hl(a)===Hl(f);u(e,{replace:y,state:l,preventScrollReset:i,relative:o,viewTransition:s})}},[a,u,f,r,l,n,e,i,o,s])}function a0(e,t){t===void 0&&(t={});let n=N.useContext(t0);n==null&&b(!1);let{basename:r}=s0(Qo.useViewTransitionState),l=fi(e,{relative:t.relative});if(!n.isTransitioning)return!1;let i=Tn(n.currentLocation.pathname,r)||n.currentLocation.pathname,o=Tn(n.nextLocation.pathname,r)||n.nextLocation.pathname;return Vo(l.pathname,o)!=null||Vo(l.pathname,i)!=null}var c0={xmlns:"http://www.w3.org/2000/svg",width:24,height:24,viewBox:"0 0 24 24",fill:"none",stroke:"currentColor",strokeWidth:2,strokeLinecap:"round",strokeLinejoin:"round"};const f0=e=>e.replace(/([a-z0-9])([A-Z])/g,"$1-$2").toLowerCase(),oe=(e,t)=>{const n=N.forwardRef(({color:r="currentColor",size:l=24,strokeWidth:i=2,absoluteStrokeWidth:o,children:s,...u},a)=>N.createElement("svg",{ref:a,...c0,width:l,height:l,stroke:r,strokeWidth:o?Number(i)*24/Number(l):i,className:`lucide lucide-${f0(e)}`,...u},[...t.map(([f,d])=>N.createElement(f,d)),...(Array.isArray(s)?s:[s])||[]]));return n.displayName=`${e}`,n},d0=oe("Activity",[["path",{d:"M22 12h-4l-3 9L9 3l-3 9H2",key:"d5dnw9"}]]),p0=oe("Box",[["path",{d:"M21 8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16Z",key:"hh9hay"}],["path",{d:"m3.3 7 8.7 5 8.7-5",key:"g66t2b"}],["path",{d:"M12 22V12",key:"d0xqtd"}]]),h0=oe("CheckCircle2",[["path",{d:"M12 22c5.523 0 10-4.477 10-10S17.523 2 12 2 2 6.477 2 12s4.477 10 10 10z",key:"14v8dr"}],["path",{d:"m9 12 2 2 4-4",key:"dzmm74"}]]),m0=oe("GitBranch",[["line",{x1:"6",x2:"6",y1:"3",y2:"15",key:"17qcm7"}],["circle",{cx:"18",cy:"6",r:"3",key:"1h7g24"}],["circle",{cx:"6",cy:"18",r:"3",key:"fqmcym"}],["path",{d:"M18 9a9 9 0 0 1-9 9",key:"n2h4wq"}]]),y0=oe("Globe",[["circle",{cx:"12",cy:"12",r:"10",key:"1mglay"}],["path",{d:"M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20",key:"13o1zl"}],["path",{d:"M2 12h20",key:"9i4pu4"}]]),td=oe("Layers",[["path",{d:"m12.83 2.18a2 2 0 0 0-1.66 0L2.6 6.08a1 1 0 0 0 0 1.83l8.58 3.91a2 2 0 0 0 1.66 0l8.58-3.9a1 1 0 0 0 0-1.83Z",key:"8b97xw"}],["path",{d:"m22 17.65-9.17 4.16a2 2 0 0 1-1.66 0L2 17.65",key:"dd6zsq"}],["path",{d:"m22 12.65-9.17 4.16a2 2 0 0 1-1.66 0L2 12.65",key:"ep9fru"}]]),Qs=oe("LayoutDashboard",[["rect",{width:"7",height:"9",x:"3",y:"3",rx:"1",key:"10lvy0"}],["rect",{width:"7",height:"5",x:"14",y:"3",rx:"1",key:"16une8"}],["rect",{width:"7",height:"9",x:"14",y:"12",rx:"1",key:"1hutg5"}],["rect",{width:"7",height:"5",x:"3",y:"16",rx:"1",key:"ldoo1y"}]]),v0=oe("Maximize",[["path",{d:"M8 3H5a2 2 0 0 0-2 2v3",key:"1dcmit"}],["path",{d:"M21 8V5a2 2 0 0 0-2-2h-3",key:"1e4gt3"}],["path",{d:"M3 16v3a2 2 0 0 0 2 2h3",key:"wsl5sc"}],["path",{d:"M16 21h3a2 2 0 0 0 2-2v-3",key:"18trek"}]]),g0=oe("Menu",[["line",{x1:"4",x2:"20",y1:"12",y2:"12",key:"1e0a9i"}],["line",{x1:"4",x2:"20",y1:"6",y2:"6",key:"1owob3"}],["line",{x1:"4",x2:"20",y1:"18",y2:"18",key:"yk5zj1"}]]),x0=oe("MonitorPlay",[["path",{d:"m10 7 5 3-5 3Z",key:"29ljg6"}],["rect",{width:"20",height:"14",x:"2",y:"3",rx:"2",key:"48i651"}],["path",{d:"M12 17v4",key:"1riwvh"}],["path",{d:"M8 21h8",key:"1ev6f3"}]]),w0=oe("PlayCircle",[["circle",{cx:"12",cy:"12",r:"10",key:"1mglay"}],["polygon",{points:"10 8 16 12 10 16 10 8",key:"1cimsy"}]]),S0=oe("Settings",[["path",{d:"M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.08a2 2 0 0 1-1-1.74v-.5a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z",key:"1qme2f"}],["circle",{cx:"12",cy:"12",r:"3",key:"1v7zrd"}]]),E0=oe("ShieldCheck",[["path",{d:"M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10",key:"1irkt0"}],["path",{d:"m9 12 2 2 4-4",key:"dzmm74"}]]),k0=oe("Terminal",[["polyline",{points:"4 17 10 11 4 5",key:"akl6gq"}],["line",{x1:"12",x2:"20",y1:"19",y2:"19",key:"q2wloq"}]]),C0=oe("XCircle",[["circle",{cx:"12",cy:"12",r:"10",key:"1mglay"}],["path",{d:"m15 9-6 6",key:"1uzhvr"}],["path",{d:"m9 9 6 6",key:"z0biqf"}]]),nd=oe("X",[["path",{d:"M18 6 6 18",key:"1bl5f8"}],["path",{d:"m6 6 12 12",key:"d8bk6v"}]]),rd=oe("Zap",[["polygon",{points:"13 2 3 14 12 14 11 22 21 10 12 10 13 2",key:"45s27k"}]]),N0=oe("ZoomIn",[["circle",{cx:"11",cy:"11",r:"8",key:"4ej97u"}],["line",{x1:"21",x2:"16.65",y1:"21",y2:"16.65",key:"13gj7c"}],["line",{x1:"11",x2:"11",y1:"8",y2:"14",key:"1vmskp"}],["line",{x1:"8",x2:"14",y1:"11",y2:"11",key:"durymu"}]]);function ld(e,t){return function(){return e.apply(t,arguments)}}const{toString:R0}=Object.prototype,{getPrototypeOf:Ks}=Object,{iterator:di,toStringTag:id}=Symbol,pi=(e=>t=>{const n=R0.call(t);return e[n]||(e[n]=n.slice(8,-1).toLowerCase())})(Object.create(null)),Je=e=>(e=e.toLowerCase(),t=>pi(t)===e),hi=e=>t=>typeof t===e,{isArray:Fn}=Array,On=hi("undefined");function zr(e){return e!==null&&!On(e)&&e.constructor!==null&&!On(e.constructor)&&Re(e.constructor.isBuffer)&&e.constructor.isBuffer(e)}const od=Je("ArrayBuffer");function P0(e){let t;return typeof ArrayBuffer<"u"&&ArrayBuffer.isView?t=ArrayBuffer.isView(e):t=e&&e.buffer&&od(e.buffer),t}const _0=hi("string"),Re=hi("function"),sd=hi("number"),Ar=e=>e!==null&&typeof e=="object",j0=e=>e===!0||e===!1,vl=e=>{if(pi(e)!=="object")return!1;const t=Ks(e);return(t===null||t===Object.prototype||Object.getPrototypeOf(t)===null)&&!(id in e)&&!(di in e)},T0=e=>{if(!Ar(e)||zr(e))return!1;try{return Object.keys(e).length===0&&Object.getPrototypeOf(e)===Object.prototype}catch{return!1}},O0=Je("Date"),L0=Je("File"),z0=Je("Blob"),A0=Je("FileList"),I0=e=>Ar(e)&&Re(e.pipe),D0=e=>{let t;return e&&(typeof FormData=="function"&&e instanceof FormData||Re(e.append)&&((t=pi(e))==="formdata"||t==="object"&&Re(e.toString)&&e.toString()==="[object FormData]"))},F0=Je("URLSearchParams"),[M0,U0,B0,$0]=["ReadableStream","Request","Response","Headers"].map(Je),V0=e=>e.trim?e.trim():e.replace(/^[\s\uFEFF\xA0]+|[\s\uFEFF\xA0]+$/g,"");function Ir(e,t,{allOwnKeys:n=!1}={}){if(e===null||typeof e>"u")return;let r,l;if(typeof e!="object"&&(e=[e]),Fn(e))for(r=0,l=e.length;r<l;r++)t.call(null,e[r],r,e);else{if(zr(e))return;const i=n?Object.getOwnPropertyNames(e):Object.keys(e),o=i.length;let s;for(r=0;r<o;r++)s=i[r],t.call(null,e[s],s,e)}}function ud(e,t){if(zr(e))return null;t=t.toLowerCase();const n=Object.keys(e);let r=n.length,l;for(;r-- >0;)if(l=n[r],t===l.toLowerCase())return l;return null}const Ht=typeof globalThis<"u"?globalThis:typeof self<"u"?self:typeof window<"u"?window:global,ad=e=>!On(e)&&e!==Ht;function Ko(){const{caseless:e,skipUndefined:t}=ad(this)&&this||{},n={},r=(l,i)=>{const o=e&&ud(n,i)||i;vl(n[o])&&vl(l)?n[o]=Ko(n[o],l):vl(l)?n[o]=Ko({},l):Fn(l)?n[o]=l.slice():(!t||!On(l))&&(n[o]=l)};for(let l=0,i=arguments.length;l<i;l++)arguments[l]&&Ir(arguments[l],r);return n}const W0=(e,t,n,{allOwnKeys:r}={})=>(Ir(t,(l,i)=>{n&&Re(l)?e[i]=ld(l,n):e[i]=l},{allOwnKeys:r}),e),H0=e=>(e.charCodeAt(0)===65279&&(e=e.slice(1)),e),Q0=(e,t,n,r)=>{e.prototype=Object.create(t.prototype,r),e.prototype.constructor=e,Object.defineProperty(e,"super",{value:t.prototype}),n&&Object.assign(e.prototype,n)},K0=(e,t,n,r)=>{let l,i,o;const s={};if(t=t||{},e==null)return t;do{for(l=Object.getOwnPropertyNames(e),i=l.length;i-- >0;)o=l[i],(!r||r(o,e,t))&&!s[o]&&(t[o]=e[o],s[o]=!0);e=n!==!1&&Ks(e)}while(e&&(!n||n(e,t))&&e!==Object.prototype);return t},G0=(e,t,n)=>{e=String(e),(n===void 0||n>e.length)&&(n=e.length),n-=t.length;const r=e.indexOf(t,n);return r!==-1&&r===n},X0=e=>{if(!e)return null;if(Fn(e))return e;let t=e.length;if(!sd(t))return null;const n=new Array(t);for(;t-- >0;)n[t]=e[t];return n},q0=(e=>t=>e&&t instanceof e)(typeof Uint8Array<"u"&&Ks(Uint8Array)),J0=(e,t)=>{const r=(e&&e[di]).call(e);let l;for(;(l=r.next())&&!l.done;){const i=l.value;t.call(e,i[0],i[1])}},Y0=(e,t)=>{let n;const r=[];for(;(n=e.exec(t))!==null;)r.push(n);return r},b0=Je("HTMLFormElement"),Z0=e=>e.toLowerCase().replace(/[-_\s]([a-z\d])(\w*)/g,function(n,r,l){return r.toUpperCase()+l}),pa=(({hasOwnProperty:e})=>(t,n)=>e.call(t,n))(Object.prototype),ey=Je("RegExp"),cd=(e,t)=>{const n=Object.getOwnPropertyDescriptors(e),r={};Ir(n,(l,i)=>{let o;(o=t(l,i,e))!==!1&&(r[i]=o||l)}),Object.defineProperties(e,r)},ty=e=>{cd(e,(t,n)=>{if(Re(e)&&["arguments","caller","callee"].indexOf(n)!==-1)return!1;const r=e[n];if(Re(r)){if(t.enumerable=!1,"writable"in t){t.writable=!1;return}t.set||(t.set=()=>{throw Error("Can not rewrite read-only method '"+n+"'")})}})},ny=(e,t)=>{const n={},r=l=>{l.forEach(i=>{n[i]=!0})};return Fn(e)?r(e):r(String(e).split(t)),n},ry=()=>{},ly=(e,t)=>e!=null&&Number.isFinite(e=+e)?e:t;function iy(e){return!!(e&&Re(e.append)&&e[id]==="FormData"&&e[di])}const oy=e=>{const t=new Array(10),n=(r,l)=>{if(Ar(r)){if(t.indexOf(r)>=0)return;if(zr(r))return r;if(!("toJSON"in r)){t[l]=r;const i=Fn(r)?[]:{};return Ir(r,(o,s)=>{const u=n(o,l+1);!On(u)&&(i[s]=u)}),t[l]=void 0,i}}return r};return n(e,0)},sy=Je("AsyncFunction"),uy=e=>e&&(Ar(e)||Re(e))&&Re(e.then)&&Re(e.catch),fd=((e,t)=>e?setImmediate:t?((n,r)=>(Ht.addEventListener("message",({source:l,data:i})=>{l===Ht&&i===n&&r.length&&r.shift()()},!1),l=>{r.push(l),Ht.postMessage(n,"*")}))(`axios@${Math.random()}`,[]):n=>setTimeout(n))(typeof setImmediate=="function",Re(Ht.postMessage)),ay=typeof queueMicrotask<"u"?queueMicrotask.bind(Ht):typeof process<"u"&&process.nextTick||fd,cy=e=>e!=null&&Re(e[di]),w={isArray:Fn,isArrayBuffer:od,isBuffer:zr,isFormData:D0,isArrayBufferView:P0,isString:_0,isNumber:sd,isBoolean:j0,isObject:Ar,isPlainObject:vl,isEmptyObject:T0,isReadableStream:M0,isRequest:U0,isResponse:B0,isHeaders:$0,isUndefined:On,isDate:O0,isFile:L0,isBlob:z0,isRegExp:ey,isFunction:Re,isStream:I0,isURLSearchParams:F0,isTypedArray:q0,isFileList:A0,forEach:Ir,merge:Ko,extend:W0,trim:V0,stripBOM:H0,inherits:Q0,toFlatObject:K0,kindOf:pi,kindOfTest:Je,endsWith:G0,toArray:X0,forEachEntry:J0,matchAll:Y0,isHTMLForm:b0,hasOwnProperty:pa,hasOwnProp:pa,reduceDescriptors:cd,freezeMethods:ty,toObjectSet:ny,toCamelCase:Z0,noop:ry,toFiniteNumber:ly,findKey:ud,global:Ht,isContextDefined:ad,isSpecCompliantForm:iy,toJSONObject:oy,isAsyncFn:sy,isThenable:uy,setImmediate:fd,asap:ay,isIterable:cy};function A(e,t,n,r,l){Error.call(this),Error.captureStackTrace?Error.captureStackTrace(this,this.constructor):this.stack=new Error().stack,this.message=e,this.name="AxiosError",t&&(this.code=t),n&&(this.config=n),r&&(this.request=r),l&&(this.response=l,this.status=l.status?l.status:null)}w.inherits(A,Error,{toJSON:function(){return{message:this.message,name:this.name,description:this.description,number:this.number,fileName:this.fileName,lineNumber:this.lineNumber,columnNumber:this.columnNumber,stack:this.stack,config:w.toJSONObject(this.config),code:this.code,status:this.status}}});const dd=A.prototype,pd={};["ERR_BAD_OPTION_VALUE","ERR_BAD_OPTION","ECONNABORTED","ETIMEDOUT","ERR_NETWORK","ERR_FR_TOO_MANY_REDIRECTS","ERR_DEPRECATED","ERR_BAD_RESPONSE","ERR_BAD_REQUEST","ERR_CANCELED","ERR_NOT_SUPPORT","ERR_INVALID_URL"].forEach(e=>{pd[e]={value:e}});Object.defineProperties(A,pd);Object.defineProperty(dd,"isAxiosError",{value:!0});A.from=(e,t,n,r,l,i)=>{const o=Object.create(dd);w.toFlatObject(e,o,function(f){return f!==Error.prototype},a=>a!=="isAxiosError");const s=e&&e.message?e.message:"Error",u=t==null&&e?e.code:t;return A.call(o,s,u,n,r,l),e&&o.cause==null&&Object.defineProperty(o,"cause",{value:e,configurable:!0}),o.name=e&&e.name||"Error",i&&Object.assign(o,i),o};const fy=null;function Go(e){return w.isPlainObject(e)||w.isArray(e)}function hd(e){return w.endsWith(e,"[]")?e.slice(0,-2):e}function ha(e,t,n){return e?e.concat(t).map(function(l,i){return l=hd(l),!n&&i?"["+l+"]":l}).join(n?".":""):t}function dy(e){return w.isArray(e)&&!e.some(Go)}const py=w.toFlatObject(w,{},null,function(t){return/^is[A-Z]/.test(t)});function mi(e,t,n){if(!w.isObject(e))throw new TypeError("target must be an object");t=t||new FormData,n=w.toFlatObject(n,{metaTokens:!0,dots:!1,indexes:!1},!1,function(x,S){return!w.isUndefined(S[x])});const r=n.metaTokens,l=n.visitor||f,i=n.dots,o=n.indexes,u=(n.Blob||typeof Blob<"u"&&Blob)&&w.isSpecCompliantForm(t);if(!w.isFunction(l))throw new TypeError("visitor must be a function");function a(m){if(m===null)return"";if(w.isDate(m))return m.toISOString();if(w.isBoolean(m))return m.toString();if(!u&&w.isBlob(m))throw new A("Blob is not supported. Use a Buffer instead.");return w.isArrayBuffer(m)||w.isTypedArray(m)?u&&typeof Blob=="function"?new Blob([m]):Buffer.from(m):m}function f(m,x,S){let h=m;if(m&&!S&&typeof m=="object"){if(w.endsWith(x,"{}"))x=r?x:x.slice(0,-2),m=JSON.stringify(m);else if(w.isArray(m)&&dy(m)||(w.isFileList(m)||w.endsWith(x,"[]"))&&(h=w.toArray(m)))return x=hd(x),h.forEach(function(p,g){!(w.isUndefined(p)||p===null)&&t.append(o===!0?ha([x],g,i):o===null?x:x+"[]",a(p))}),!1}return Go(m)?!0:(t.append(ha(S,x,i),a(m)),!1)}const d=[],y=Object.assign(py,{defaultVisitor:f,convertValue:a,isVisitable:Go});function E(m,x){if(!w.isUndefined(m)){if(d.indexOf(m)!==-1)throw Error("Circular reference detected in "+x.join("."));d.push(m),w.forEach(m,function(h,c){(!(w.isUndefined(h)||h===null)&&l.call(t,h,w.isString(c)?c.trim():c,x,y))===!0&&E(h,x?x.concat(c):[c])}),d.pop()}}if(!w.isObject(e))throw new TypeError("data must be an object");return E(e),t}function ma(e){const t={"!":"%21","'":"%27","(":"%28",")":"%29","~":"%7E","%20":"+","%00":"\0"};return encodeURIComponent(e).replace(/[!'()~]|%20|%00/g,function(r){return t[r]})}function Gs(e,t){this._pairs=[],e&&mi(e,this,t)}const md=Gs.prototype;md.append=function(t,n){this._pairs.push([t,n])};md.toString=function(t){const n=t?function(r){return t.call(this,r,ma)}:ma;return this._pairs.map(function(l){return n(l[0])+"="+n(l[1])},"").join("&")};function hy(e){return encodeURIComponent(e).replace(/%3A/gi,":").replace(/%24/g,"$").replace(/%2C/gi,",").replace(/%20/g,"+")}function yd(e,t,n){if(!t)return e;const r=n&&n.encode||hy;w.isFunction(n)&&(n={serialize:n});const l=n&&n.serialize;let i;if(l?i=l(t,n):i=w.isURLSearchParams(t)?t.toString():new Gs(t,n).toString(r),i){const o=e.indexOf("#");o!==-1&&(e=e.slice(0,o)),e+=(e.indexOf("?")===-1?"?":"&")+i}return e}class ya{constructor(){this.handlers=[]}use(t,n,r){return this.handlers.push({fulfilled:t,rejected:n,synchronous:r?r.synchronous:!1,runWhen:r?r.runWhen:null}),this.handlers.length-1}eject(t){this.handlers[t]&&(this.handlers[t]=null)}clear(){this.handlers&&(this.handlers=[])}forEach(t){w.forEach(this.handlers,function(r){r!==null&&t(r)})}}const vd={silentJSONParsing:!0,forcedJSONParsing:!0,clarifyTimeoutError:!1},my=typeof URLSearchParams<"u"?URLSearchParams:Gs,yy=typeof FormData<"u"?FormData:null,vy=typeof Blob<"u"?Blob:null,gy={isBrowser:!0,classes:{URLSearchParams:my,FormData:yy,Blob:vy},protocols:["http","https","file","blob","url","data"]},Xs=typeof window<"u"&&typeof document<"u",Xo=typeof navigator=="object"&&navigator||void 0,xy=Xs&&(!Xo||["ReactNative","NativeScript","NS"].indexOf(Xo.product)<0),wy=typeof WorkerGlobalScope<"u"&&self instanceof WorkerGlobalScope&&typeof self.importScripts=="function",Sy=Xs&&window.location.href||"http://localhost",Ey=Object.freeze(Object.defineProperty({__proto__:null,hasBrowserEnv:Xs,hasStandardBrowserEnv:xy,hasStandardBrowserWebWorkerEnv:wy,navigator:Xo,origin:Sy},Symbol.toStringTag,{value:"Module"})),pe={...Ey,...gy};function ky(e,t){return mi(e,new pe.classes.URLSearchParams,{visitor:function(n,r,l,i){return pe.isNode&&w.isBuffer(n)?(this.append(r,n.toString("base64")),!1):i.defaultVisitor.apply(this,arguments)},...t})}function Cy(e){return w.matchAll(/\w+|\[(\w*)]/g,e).map(t=>t[0]==="[]"?"":t[1]||t[0])}function Ny(e){const t={},n=Object.keys(e);let r;const l=n.length;let i;for(r=0;r<l;r++)i=n[r],t[i]=e[i];return t}function gd(e){function t(n,r,l,i){let o=n[i++];if(o==="__proto__")return!0;const s=Number.isFinite(+o),u=i>=n.length;return o=!o&&w.isArray(l)?l.length:o,u?(w.hasOwnProp(l,o)?l[o]=[l[o],r]:l[o]=r,!s):((!l[o]||!w.isObject(l[o]))&&(l[o]=[]),t(n,r,l[o],i)&&w.isArray(l[o])&&(l[o]=Ny(l[o])),!s)}if(w.isFormData(e)&&w.isFunction(e.entries)){const n={};return w.forEachEntry(e,(r,l)=>{t(Cy(r),l,n,0)}),n}return null}function Ry(e,t,n){if(w.isString(e))try{return(t||JSON.parse)(e),w.trim(e)}catch(r){if(r.name!=="SyntaxError")throw r}return(n||JSON.stringify)(e)}const Dr={transitional:vd,adapter:["xhr","http","fetch"],transformRequest:[function(t,n){const r=n.getContentType()||"",l=r.indexOf("application/json")>-1,i=w.isObject(t);if(i&&w.isHTMLForm(t)&&(t=new FormData(t)),w.isFormData(t))return l?JSON.stringify(gd(t)):t;if(w.isArrayBuffer(t)||w.isBuffer(t)||w.isStream(t)||w.isFile(t)||w.isBlob(t)||w.isReadableStream(t))return t;if(w.isArrayBufferView(t))return t.buffer;if(w.isURLSearchParams(t))return n.setContentType("application/x-www-form-urlencoded;charset=utf-8",!1),t.toString();let s;if(i){if(r.indexOf("application/x-www-form-urlencoded")>-1)return ky(t,this.formSerializer).toString();if((s=w.isFileList(t))||r.indexOf("multipart/form-data")>-1){const u=this.env&&this.env.FormData;return mi(s?{"files[]":t}:t,u&&new u,this.formSerializer)}}return i||l?(n.setContentType("application/json",!1),Ry(t)):t}],transformResponse:[function(t){const n=this.transitional||Dr.transitional,r=n&&n.forcedJSONParsing,l=this.responseType==="json";if(w.isResponse(t)||w.isReadableStream(t))return t;if(t&&w.isString(t)&&(r&&!this.responseType||l)){const o=!(n&&n.silentJSONParsing)&&l;try{return JSON.parse(t,this.parseReviver)}catch(s){if(o)throw s.name==="SyntaxError"?A.from(s,A.ERR_BAD_RESPONSE,this,null,this.response):s}}return t}],timeout:0,xsrfCookieName:"XSRF-TOKEN",xsrfHeaderName:"X-XSRF-TOKEN",maxContentLength:-1,maxBodyLength:-1,env:{FormData:pe.classes.FormData,Blob:pe.classes.Blob},validateStatus:function(t){return t>=200&&t<300},headers:{common:{Accept:"application/json, text/plain, */*","Content-Type":void 0}}};w.forEach(["delete","get","head","post","put","patch"],e=>{Dr.headers[e]={}});const Py=w.toObjectSet(["age","authorization","content-length","content-type","etag","expires","from","host","if-modified-since","if-unmodified-since","last-modified","location","max-forwards","proxy-authorization","referer","retry-after","user-agent"]),_y=e=>{const t={};let n,r,l;return e&&e.split(`
`).forEach(function(o){l=o.indexOf(":"),n=o.substring(0,l).trim().toLowerCase(),r=o.substring(l+1).trim(),!(!n||t[n]&&Py[n])&&(n==="set-cookie"?t[n]?t[n].push(r):t[n]=[r]:t[n]=t[n]?t[n]+", "+r:r)}),t},va=Symbol("internals");function Gn(e){return e&&String(e).trim().toLowerCase()}function gl(e){return e===!1||e==null?e:w.isArray(e)?e.map(gl):String(e)}function jy(e){const t=Object.create(null),n=/([^\s,;=]+)\s*(?:=\s*([^,;]+))?/g;let r;for(;r=n.exec(e);)t[r[1]]=r[2];return t}const Ty=e=>/^[-_a-zA-Z0-9^`|~,!#$%&'*+.]+$/.test(e.trim());function Hi(e,t,n,r,l){if(w.isFunction(r))return r.call(this,t,n);if(l&&(t=n),!!w.isString(t)){if(w.isString(r))return t.indexOf(r)!==-1;if(w.isRegExp(r))return r.test(t)}}function Oy(e){return e.trim().toLowerCase().replace(/([a-z\d])(\w*)/g,(t,n,r)=>n.toUpperCase()+r)}function Ly(e,t){const n=w.toCamelCase(" "+t);["get","set","has"].forEach(r=>{Object.defineProperty(e,r+n,{value:function(l,i,o){return this[r].call(this,t,l,i,o)},configurable:!0})})}let Pe=class{constructor(t){t&&this.set(t)}set(t,n,r){const l=this;function i(s,u,a){const f=Gn(u);if(!f)throw new Error("header name must be a non-empty string");const d=w.findKey(l,f);(!d||l[d]===void 0||a===!0||a===void 0&&l[d]!==!1)&&(l[d||u]=gl(s))}const o=(s,u)=>w.forEach(s,(a,f)=>i(a,f,u));if(w.isPlainObject(t)||t instanceof this.constructor)o(t,n);else if(w.isString(t)&&(t=t.trim())&&!Ty(t))o(_y(t),n);else if(w.isObject(t)&&w.isIterable(t)){let s={},u,a;for(const f of t){if(!w.isArray(f))throw TypeError("Object iterator must return a key-value pair");s[a=f[0]]=(u=s[a])?w.isArray(u)?[...u,f[1]]:[u,f[1]]:f[1]}o(s,n)}else t!=null&&i(n,t,r);return this}get(t,n){if(t=Gn(t),t){const r=w.findKey(this,t);if(r){const l=this[r];if(!n)return l;if(n===!0)return jy(l);if(w.isFunction(n))return n.call(this,l,r);if(w.isRegExp(n))return n.exec(l);throw new TypeError("parser must be boolean|regexp|function")}}}has(t,n){if(t=Gn(t),t){const r=w.findKey(this,t);return!!(r&&this[r]!==void 0&&(!n||Hi(this,this[r],r,n)))}return!1}delete(t,n){const r=this;let l=!1;function i(o){if(o=Gn(o),o){const s=w.findKey(r,o);s&&(!n||Hi(r,r[s],s,n))&&(delete r[s],l=!0)}}return w.isArray(t)?t.forEach(i):i(t),l}clear(t){const n=Object.keys(this);let r=n.length,l=!1;for(;r--;){const i=n[r];(!t||Hi(this,this[i],i,t,!0))&&(delete this[i],l=!0)}return l}normalize(t){const n=this,r={};return w.forEach(this,(l,i)=>{const o=w.findKey(r,i);if(o){n[o]=gl(l),delete n[i];return}const s=t?Oy(i):String(i).trim();s!==i&&delete n[i],n[s]=gl(l),r[s]=!0}),this}concat(...t){return this.constructor.concat(this,...t)}toJSON(t){const n=Object.create(null);return w.forEach(this,(r,l)=>{r!=null&&r!==!1&&(n[l]=t&&w.isArray(r)?r.join(", "):r)}),n}[Symbol.iterator](){return Object.entries(this.toJSON())[Symbol.iterator]()}toString(){return Object.entries(this.toJSON()).map(([t,n])=>t+": "+n).join(`
`)}getSetCookie(){return this.get("set-cookie")||[]}get[Symbol.toStringTag](){return"AxiosHeaders"}static from(t){return t instanceof this?t:new this(t)}static concat(t,...n){const r=new this(t);return n.forEach(l=>r.set(l)),r}static accessor(t){const r=(this[va]=this[va]={accessors:{}}).accessors,l=this.prototype;function i(o){const s=Gn(o);r[s]||(Ly(l,o),r[s]=!0)}return w.isArray(t)?t.forEach(i):i(t),this}};Pe.accessor(["Content-Type","Content-Length","Accept","Accept-Encoding","User-Agent","Authorization"]);w.reduceDescriptors(Pe.prototype,({value:e},t)=>{let n=t[0].toUpperCase()+t.slice(1);return{get:()=>e,set(r){this[n]=r}}});w.freezeMethods(Pe);function Qi(e,t){const n=this||Dr,r=t||n,l=Pe.from(r.headers);let i=r.data;return w.forEach(e,function(s){i=s.call(n,i,l.normalize(),t?t.status:void 0)}),l.normalize(),i}function xd(e){return!!(e&&e.__CANCEL__)}function Mn(e,t,n){A.call(this,e??"canceled",A.ERR_CANCELED,t,n),this.name="CanceledError"}w.inherits(Mn,A,{__CANCEL__:!0});function wd(e,t,n){const r=n.config.validateStatus;!n.status||!r||r(n.status)?e(n):t(new A("Request failed with status code "+n.status,[A.ERR_BAD_REQUEST,A.ERR_BAD_RESPONSE][Math.floor(n.status/100)-4],n.config,n.request,n))}function zy(e){const t=/^([-+\w]{1,25})(:?\/\/|:)/.exec(e);return t&&t[1]||""}function Ay(e,t){e=e||10;const n=new Array(e),r=new Array(e);let l=0,i=0,o;return t=t!==void 0?t:1e3,function(u){const a=Date.now(),f=r[i];o||(o=a),n[l]=u,r[l]=a;let d=i,y=0;for(;d!==l;)y+=n[d++],d=d%e;if(l=(l+1)%e,l===i&&(i=(i+1)%e),a-o<t)return;const E=f&&a-f;return E?Math.round(y*1e3/E):void 0}}function Iy(e,t){let n=0,r=1e3/t,l,i;const o=(a,f=Date.now())=>{n=f,l=null,i&&(clearTimeout(i),i=null),e(...a)};return[(...a)=>{const f=Date.now(),d=f-n;d>=r?o(a,f):(l=a,i||(i=setTimeout(()=>{i=null,o(l)},r-d)))},()=>l&&o(l)]}const Kl=(e,t,n=3)=>{let r=0;const l=Ay(50,250);return Iy(i=>{const o=i.loaded,s=i.lengthComputable?i.total:void 0,u=o-r,a=l(u),f=o<=s;r=o;const d={loaded:o,total:s,progress:s?o/s:void 0,bytes:u,rate:a||void 0,estimated:a&&s&&f?(s-o)/a:void 0,event:i,lengthComputable:s!=null,[t?"download":"upload"]:!0};e(d)},n)},ga=(e,t)=>{const n=e!=null;return[r=>t[0]({lengthComputable:n,total:e,loaded:r}),t[1]]},xa=e=>(...t)=>w.asap(()=>e(...t)),Dy=pe.hasStandardBrowserEnv?((e,t)=>n=>(n=new URL(n,pe.origin),e.protocol===n.protocol&&e.host===n.host&&(t||e.port===n.port)))(new URL(pe.origin),pe.navigator&&/(msie|trident)/i.test(pe.navigator.userAgent)):()=>!0,Fy=pe.hasStandardBrowserEnv?{write(e,t,n,r,l,i,o){if(typeof document>"u")return;const s=[`${e}=${encodeURIComponent(t)}`];w.isNumber(n)&&s.push(`expires=${new Date(n).toUTCString()}`),w.isString(r)&&s.push(`path=${r}`),w.isString(l)&&s.push(`domain=${l}`),i===!0&&s.push("secure"),w.isString(o)&&s.push(`SameSite=${o}`),document.cookie=s.join("; ")},read(e){if(typeof document>"u")return null;const t=document.cookie.match(new RegExp("(?:^|; )"+e+"=([^;]*)"));return t?decodeURIComponent(t[1]):null},remove(e){this.write(e,"",Date.now()-864e5,"/")}}:{write(){},read(){return null},remove(){}};function My(e){return/^([a-z][a-z\d+\-.]*:)?\/\//i.test(e)}function Uy(e,t){return t?e.replace(/\/?\/$/,"")+"/"+t.replace(/^\/+/,""):e}function Sd(e,t,n){let r=!My(t);return e&&(r||n==!1)?Uy(e,t):t}const wa=e=>e instanceof Pe?{...e}:e;function Zt(e,t){t=t||{};const n={};function r(a,f,d,y){return w.isPlainObject(a)&&w.isPlainObject(f)?w.merge.call({caseless:y},a,f):w.isPlainObject(f)?w.merge({},f):w.isArray(f)?f.slice():f}function l(a,f,d,y){if(w.isUndefined(f)){if(!w.isUndefined(a))return r(void 0,a,d,y)}else return r(a,f,d,y)}function i(a,f){if(!w.isUndefined(f))return r(void 0,f)}function o(a,f){if(w.isUndefined(f)){if(!w.isUndefined(a))return r(void 0,a)}else return r(void 0,f)}function s(a,f,d){if(d in t)return r(a,f);if(d in e)return r(void 0,a)}const u={url:i,method:i,data:i,baseURL:o,transformRequest:o,transformResponse:o,paramsSerializer:o,timeout:o,timeoutMessage:o,withCredentials:o,withXSRFToken:o,adapter:o,responseType:o,xsrfCookieName:o,xsrfHeaderName:o,onUploadProgress:o,onDownloadProgress:o,decompress:o,maxContentLength:o,maxBodyLength:o,beforeRedirect:o,transport:o,httpAgent:o,httpsAgent:o,cancelToken:o,socketPath:o,responseEncoding:o,validateStatus:s,headers:(a,f,d)=>l(wa(a),wa(f),d,!0)};return w.forEach(Object.keys({...e,...t}),function(f){const d=u[f]||l,y=d(e[f],t[f],f);w.isUndefined(y)&&d!==s||(n[f]=y)}),n}const Ed=e=>{const t=Zt({},e);let{data:n,withXSRFToken:r,xsrfHeaderName:l,xsrfCookieName:i,headers:o,auth:s}=t;if(t.headers=o=Pe.from(o),t.url=yd(Sd(t.baseURL,t.url,t.allowAbsoluteUrls),e.params,e.paramsSerializer),s&&o.set("Authorization","Basic "+btoa((s.username||"")+":"+(s.password?unescape(encodeURIComponent(s.password)):""))),w.isFormData(n)){if(pe.hasStandardBrowserEnv||pe.hasStandardBrowserWebWorkerEnv)o.setContentType(void 0);else if(w.isFunction(n.getHeaders)){const u=n.getHeaders(),a=["content-type","content-length"];Object.entries(u).forEach(([f,d])=>{a.includes(f.toLowerCase())&&o.set(f,d)})}}if(pe.hasStandardBrowserEnv&&(r&&w.isFunction(r)&&(r=r(t)),r||r!==!1&&Dy(t.url))){const u=l&&i&&Fy.read(i);u&&o.set(l,u)}return t},By=typeof XMLHttpRequest<"u",$y=By&&function(e){return new Promise(function(n,r){const l=Ed(e);let i=l.data;const o=Pe.from(l.headers).normalize();let{responseType:s,onUploadProgress:u,onDownloadProgress:a}=l,f,d,y,E,m;function x(){E&&E(),m&&m(),l.cancelToken&&l.cancelToken.unsubscribe(f),l.signal&&l.signal.removeEventListener("abort",f)}let S=new XMLHttpRequest;S.open(l.method.toUpperCase(),l.url,!0),S.timeout=l.timeout;function h(){if(!S)return;const p=Pe.from("getAllResponseHeaders"in S&&S.getAllResponseHeaders()),k={data:!s||s==="text"||s==="json"?S.responseText:S.response,status:S.status,statusText:S.statusText,headers:p,config:e,request:S};wd(function(P){n(P),x()},function(P){r(P),x()},k),S=null}"onloadend"in S?S.onloadend=h:S.onreadystatechange=function(){!S||S.readyState!==4||S.status===0&&!(S.responseURL&&S.responseURL.indexOf("file:")===0)||setTimeout(h)},S.onabort=function(){S&&(r(new A("Request aborted",A.ECONNABORTED,e,S)),S=null)},S.onerror=function(g){const k=g&&g.message?g.message:"Network Error",_=new A(k,A.ERR_NETWORK,e,S);_.event=g||null,r(_),S=null},S.ontimeout=function(){let g=l.timeout?"timeout of "+l.timeout+"ms exceeded":"timeout exceeded";const k=l.transitional||vd;l.timeoutErrorMessage&&(g=l.timeoutErrorMessage),r(new A(g,k.clarifyTimeoutError?A.ETIMEDOUT:A.ECONNABORTED,e,S)),S=null},i===void 0&&o.setContentType(null),"setRequestHeader"in S&&w.forEach(o.toJSON(),function(g,k){S.setRequestHeader(k,g)}),w.isUndefined(l.withCredentials)||(S.withCredentials=!!l.withCredentials),s&&s!=="json"&&(S.responseType=l.responseType),a&&([y,m]=Kl(a,!0),S.addEventListener("progress",y)),u&&S.upload&&([d,E]=Kl(u),S.upload.addEventListener("progress",d),S.upload.addEventListener("loadend",E)),(l.cancelToken||l.signal)&&(f=p=>{S&&(r(!p||p.type?new Mn(null,e,S):p),S.abort(),S=null)},l.cancelToken&&l.cancelToken.subscribe(f),l.signal&&(l.signal.aborted?f():l.signal.addEventListener("abort",f)));const c=zy(l.url);if(c&&pe.protocols.indexOf(c)===-1){r(new A("Unsupported protocol "+c+":",A.ERR_BAD_REQUEST,e));return}S.send(i||null)})},Vy=(e,t)=>{const{length:n}=e=e?e.filter(Boolean):[];if(t||n){let r=new AbortController,l;const i=function(a){if(!l){l=!0,s();const f=a instanceof Error?a:this.reason;r.abort(f instanceof A?f:new Mn(f instanceof Error?f.message:f))}};let o=t&&setTimeout(()=>{o=null,i(new A(`timeout ${t} of ms exceeded`,A.ETIMEDOUT))},t);const s=()=>{e&&(o&&clearTimeout(o),o=null,e.forEach(a=>{a.unsubscribe?a.unsubscribe(i):a.removeEventListener("abort",i)}),e=null)};e.forEach(a=>a.addEventListener("abort",i));const{signal:u}=r;return u.unsubscribe=()=>w.asap(s),u}},Wy=function*(e,t){let n=e.byteLength;if(n<t){yield e;return}let r=0,l;for(;r<n;)l=r+t,yield e.slice(r,l),r=l},Hy=async function*(e,t){for await(const n of Qy(e))yield*Wy(n,t)},Qy=async function*(e){if(e[Symbol.asyncIterator]){yield*e;return}const t=e.getReader();try{for(;;){const{done:n,value:r}=await t.read();if(n)break;yield r}}finally{await t.cancel()}},Sa=(e,t,n,r)=>{const l=Hy(e,t);let i=0,o,s=u=>{o||(o=!0,r&&r(u))};return new ReadableStream({async pull(u){try{const{done:a,value:f}=await l.next();if(a){s(),u.close();return}let d=f.byteLength;if(n){let y=i+=d;n(y)}u.enqueue(new Uint8Array(f))}catch(a){throw s(a),a}},cancel(u){return s(u),l.return()}},{highWaterMark:2})},Ea=64*1024,{isFunction:nl}=w,Ky=(({Request:e,Response:t})=>({Request:e,Response:t}))(w.global),{ReadableStream:ka,TextEncoder:Ca}=w.global,Na=(e,...t)=>{try{return!!e(...t)}catch{return!1}},Gy=e=>{e=w.merge.call({skipUndefined:!0},Ky,e);const{fetch:t,Request:n,Response:r}=e,l=t?nl(t):typeof fetch=="function",i=nl(n),o=nl(r);if(!l)return!1;const s=l&&nl(ka),u=l&&(typeof Ca=="function"?(m=>x=>m.encode(x))(new Ca):async m=>new Uint8Array(await new n(m).arrayBuffer())),a=i&&s&&Na(()=>{let m=!1;const x=new n(pe.origin,{body:new ka,method:"POST",get duplex(){return m=!0,"half"}}).headers.has("Content-Type");return m&&!x}),f=o&&s&&Na(()=>w.isReadableStream(new r("").body)),d={stream:f&&(m=>m.body)};l&&["text","arrayBuffer","blob","formData","stream"].forEach(m=>{!d[m]&&(d[m]=(x,S)=>{let h=x&&x[m];if(h)return h.call(x);throw new A(`Response type '${m}' is not supported`,A.ERR_NOT_SUPPORT,S)})});const y=async m=>{if(m==null)return 0;if(w.isBlob(m))return m.size;if(w.isSpecCompliantForm(m))return(await new n(pe.origin,{method:"POST",body:m}).arrayBuffer()).byteLength;if(w.isArrayBufferView(m)||w.isArrayBuffer(m))return m.byteLength;if(w.isURLSearchParams(m)&&(m=m+""),w.isString(m))return(await u(m)).byteLength},E=async(m,x)=>{const S=w.toFiniteNumber(m.getContentLength());return S??y(x)};return async m=>{let{url:x,method:S,data:h,signal:c,cancelToken:p,timeout:g,onDownloadProgress:k,onUploadProgress:_,responseType:P,headers:T,withCredentials:M="same-origin",fetchOptions:L}=Ed(m),te=t||fetch;P=P?(P+"").toLowerCase():"text";let _e=Vy([c,p&&p.toAbortSignal()],g),we=null;const je=_e&&_e.unsubscribe&&(()=>{_e.unsubscribe()});let O;try{if(_&&a&&S!=="get"&&S!=="head"&&(O=await E(T,h))!==0){let B=new n(x,{method:"POST",body:h,duplex:"half"}),W;if(w.isFormData(h)&&(W=B.headers.get("content-type"))&&T.setContentType(W),B.body){const[pt,De]=ga(O,Kl(xa(_)));h=Sa(B.body,Ea,pt,De)}}w.isString(M)||(M=M?"include":"omit");const U=i&&"credentials"in n.prototype,me={...L,signal:_e,method:S.toUpperCase(),headers:T.normalize().toJSON(),body:h,duplex:"half",credentials:U?M:void 0};we=i&&new n(x,me);let R=await(i?te(we,L):te(x,me));const z=f&&(P==="stream"||P==="response");if(f&&(k||z&&je)){const B={};["status","statusText","headers"].forEach(nn=>{B[nn]=R[nn]});const W=w.toFiniteNumber(R.headers.get("content-length")),[pt,De]=k&&ga(W,Kl(xa(k),!0))||[];R=new r(Sa(R.body,Ea,pt,()=>{De&&De(),je&&je()}),B)}P=P||"text";let I=await d[w.findKey(d,P)||"text"](R,m);return!z&&je&&je(),await new Promise((B,W)=>{wd(B,W,{data:I,headers:Pe.from(R.headers),status:R.status,statusText:R.statusText,config:m,request:we})})}catch(U){throw je&&je(),U&&U.name==="TypeError"&&/Load failed|fetch/i.test(U.message)?Object.assign(new A("Network Error",A.ERR_NETWORK,m,we),{cause:U.cause||U}):A.from(U,U&&U.code,m,we)}}},Xy=new Map,kd=e=>{let t=e&&e.env||{};const{fetch:n,Request:r,Response:l}=t,i=[r,l,n];let o=i.length,s=o,u,a,f=Xy;for(;s--;)u=i[s],a=f.get(u),a===void 0&&f.set(u,a=s?new Map:Gy(t)),f=a;return a};kd();const qs={http:fy,xhr:$y,fetch:{get:kd}};w.forEach(qs,(e,t)=>{if(e){try{Object.defineProperty(e,"name",{value:t})}catch{}Object.defineProperty(e,"adapterName",{value:t})}});const Ra=e=>`- ${e}`,qy=e=>w.isFunction(e)||e===null||e===!1;function Jy(e,t){e=w.isArray(e)?e:[e];const{length:n}=e;let r,l;const i={};for(let o=0;o<n;o++){r=e[o];let s;if(l=r,!qy(r)&&(l=qs[(s=String(r)).toLowerCase()],l===void 0))throw new A(`Unknown adapter '${s}'`);if(l&&(w.isFunction(l)||(l=l.get(t))))break;i[s||"#"+o]=l}if(!l){const o=Object.entries(i).map(([u,a])=>`adapter ${u} `+(a===!1?"is not supported by the environment":"is not available in the build"));let s=n?o.length>1?`since :
`+o.map(Ra).join(`
`):" "+Ra(o[0]):"as no adapter specified";throw new A("There is no suitable adapter to dispatch the request "+s,"ERR_NOT_SUPPORT")}return l}const Cd={getAdapter:Jy,adapters:qs};function Ki(e){if(e.cancelToken&&e.cancelToken.throwIfRequested(),e.signal&&e.signal.aborted)throw new Mn(null,e)}function Pa(e){return Ki(e),e.headers=Pe.from(e.headers),e.data=Qi.call(e,e.transformRequest),["post","put","patch"].indexOf(e.method)!==-1&&e.headers.setContentType("application/x-www-form-urlencoded",!1),Cd.getAdapter(e.adapter||Dr.adapter,e)(e).then(function(r){return Ki(e),r.data=Qi.call(e,e.transformResponse,r),r.headers=Pe.from(r.headers),r},function(r){return xd(r)||(Ki(e),r&&r.response&&(r.response.data=Qi.call(e,e.transformResponse,r.response),r.response.headers=Pe.from(r.response.headers))),Promise.reject(r)})}const Nd="1.13.2",yi={};["object","boolean","number","function","string","symbol"].forEach((e,t)=>{yi[e]=function(r){return typeof r===e||"a"+(t<1?"n ":" ")+e}});const _a={};yi.transitional=function(t,n,r){function l(i,o){return"[Axios v"+Nd+"] Transitional option '"+i+"'"+o+(r?". "+r:"")}return(i,o,s)=>{if(t===!1)throw new A(l(o," has been removed"+(n?" in "+n:"")),A.ERR_DEPRECATED);return n&&!_a[o]&&(_a[o]=!0,console.warn(l(o," has been deprecated since v"+n+" and will be removed in the near future"))),t?t(i,o,s):!0}};yi.spelling=function(t){return(n,r)=>(console.warn(`${r} is likely a misspelling of ${t}`),!0)};function Yy(e,t,n){if(typeof e!="object")throw new A("options must be an object",A.ERR_BAD_OPTION_VALUE);const r=Object.keys(e);let l=r.length;for(;l-- >0;){const i=r[l],o=t[i];if(o){const s=e[i],u=s===void 0||o(s,i,e);if(u!==!0)throw new A("option "+i+" must be "+u,A.ERR_BAD_OPTION_VALUE);continue}if(n!==!0)throw new A("Unknown option "+i,A.ERR_BAD_OPTION)}}const xl={assertOptions:Yy,validators:yi},be=xl.validators;let Gt=class{constructor(t){this.defaults=t||{},this.interceptors={request:new ya,response:new ya}}async request(t,n){try{return await this._request(t,n)}catch(r){if(r instanceof Error){let l={};Error.captureStackTrace?Error.captureStackTrace(l):l=new Error;const i=l.stack?l.stack.replace(/^.+\n/,""):"";try{r.stack?i&&!String(r.stack).endsWith(i.replace(/^.+\n.+\n/,""))&&(r.stack+=`
`+i):r.stack=i}catch{}}throw r}}_request(t,n){typeof t=="string"?(n=n||{},n.url=t):n=t||{},n=Zt(this.defaults,n);const{transitional:r,paramsSerializer:l,headers:i}=n;r!==void 0&&xl.assertOptions(r,{silentJSONParsing:be.transitional(be.boolean),forcedJSONParsing:be.transitional(be.boolean),clarifyTimeoutError:be.transitional(be.boolean)},!1),l!=null&&(w.isFunction(l)?n.paramsSerializer={serialize:l}:xl.assertOptions(l,{encode:be.function,serialize:be.function},!0)),n.allowAbsoluteUrls!==void 0||(this.defaults.allowAbsoluteUrls!==void 0?n.allowAbsoluteUrls=this.defaults.allowAbsoluteUrls:n.allowAbsoluteUrls=!0),xl.assertOptions(n,{baseUrl:be.spelling("baseURL"),withXsrfToken:be.spelling("withXSRFToken")},!0),n.method=(n.method||this.defaults.method||"get").toLowerCase();let o=i&&w.merge(i.common,i[n.method]);i&&w.forEach(["delete","get","head","post","put","patch","common"],m=>{delete i[m]}),n.headers=Pe.concat(o,i);const s=[];let u=!0;this.interceptors.request.forEach(function(x){typeof x.runWhen=="function"&&x.runWhen(n)===!1||(u=u&&x.synchronous,s.unshift(x.fulfilled,x.rejected))});const a=[];this.interceptors.response.forEach(function(x){a.push(x.fulfilled,x.rejected)});let f,d=0,y;if(!u){const m=[Pa.bind(this),void 0];for(m.unshift(...s),m.push(...a),y=m.length,f=Promise.resolve(n);d<y;)f=f.then(m[d++],m[d++]);return f}y=s.length;let E=n;for(;d<y;){const m=s[d++],x=s[d++];try{E=m(E)}catch(S){x.call(this,S);break}}try{f=Pa.call(this,E)}catch(m){return Promise.reject(m)}for(d=0,y=a.length;d<y;)f=f.then(a[d++],a[d++]);return f}getUri(t){t=Zt(this.defaults,t);const n=Sd(t.baseURL,t.url,t.allowAbsoluteUrls);return yd(n,t.params,t.paramsSerializer)}};w.forEach(["delete","get","head","options"],function(t){Gt.prototype[t]=function(n,r){return this.request(Zt(r||{},{method:t,url:n,data:(r||{}).data}))}});w.forEach(["post","put","patch"],function(t){function n(r){return function(i,o,s){return this.request(Zt(s||{},{method:t,headers:r?{"Content-Type":"multipart/form-data"}:{},url:i,data:o}))}}Gt.prototype[t]=n(),Gt.prototype[t+"Form"]=n(!0)});let by=class Rd{constructor(t){if(typeof t!="function")throw new TypeError("executor must be a function.");let n;this.promise=new Promise(function(i){n=i});const r=this;this.promise.then(l=>{if(!r._listeners)return;let i=r._listeners.length;for(;i-- >0;)r._listeners[i](l);r._listeners=null}),this.promise.then=l=>{let i;const o=new Promise(s=>{r.subscribe(s),i=s}).then(l);return o.cancel=function(){r.unsubscribe(i)},o},t(function(i,o,s){r.reason||(r.reason=new Mn(i,o,s),n(r.reason))})}throwIfRequested(){if(this.reason)throw this.reason}subscribe(t){if(this.reason){t(this.reason);return}this._listeners?this._listeners.push(t):this._listeners=[t]}unsubscribe(t){if(!this._listeners)return;const n=this._listeners.indexOf(t);n!==-1&&this._listeners.splice(n,1)}toAbortSignal(){const t=new AbortController,n=r=>{t.abort(r)};return this.subscribe(n),t.signal.unsubscribe=()=>this.unsubscribe(n),t.signal}static source(){let t;return{token:new Rd(function(l){t=l}),cancel:t}}};function Zy(e){return function(n){return e.apply(null,n)}}function ev(e){return w.isObject(e)&&e.isAxiosError===!0}const qo={Continue:100,SwitchingProtocols:101,Processing:102,EarlyHints:103,Ok:200,Created:201,Accepted:202,NonAuthoritativeInformation:203,NoContent:204,ResetContent:205,PartialContent:206,MultiStatus:207,AlreadyReported:208,ImUsed:226,MultipleChoices:300,MovedPermanently:301,Found:302,SeeOther:303,NotModified:304,UseProxy:305,Unused:306,TemporaryRedirect:307,PermanentRedirect:308,BadRequest:400,Unauthorized:401,PaymentRequired:402,Forbidden:403,NotFound:404,MethodNotAllowed:405,NotAcceptable:406,ProxyAuthenticationRequired:407,RequestTimeout:408,Conflict:409,Gone:410,LengthRequired:411,PreconditionFailed:412,PayloadTooLarge:413,UriTooLong:414,UnsupportedMediaType:415,RangeNotSatisfiable:416,ExpectationFailed:417,ImATeapot:418,MisdirectedRequest:421,UnprocessableEntity:422,Locked:423,FailedDependency:424,TooEarly:425,UpgradeRequired:426,PreconditionRequired:428,TooManyRequests:429,RequestHeaderFieldsTooLarge:431,UnavailableForLegalReasons:451,InternalServerError:500,NotImplemented:501,BadGateway:502,ServiceUnavailable:503,GatewayTimeout:504,HttpVersionNotSupported:505,VariantAlsoNegotiates:506,InsufficientStorage:507,LoopDetected:508,NotExtended:510,NetworkAuthenticationRequired:511,WebServerIsDown:521,ConnectionTimedOut:522,OriginIsUnreachable:523,TimeoutOccurred:524,SslHandshakeFailed:525,InvalidSslCertificate:526};Object.entries(qo).forEach(([e,t])=>{qo[t]=e});function Pd(e){const t=new Gt(e),n=ld(Gt.prototype.request,t);return w.extend(n,Gt.prototype,t,{allOwnKeys:!0}),w.extend(n,t,null,{allOwnKeys:!0}),n.create=function(l){return Pd(Zt(e,l))},n}const J=Pd(Dr);J.Axios=Gt;J.CanceledError=Mn;J.CancelToken=by;J.isCancel=xd;J.VERSION=Nd;J.toFormData=mi;J.AxiosError=A;J.Cancel=J.CanceledError;J.all=function(t){return Promise.all(t)};J.spread=Zy;J.isAxiosError=ev;J.mergeConfig=Zt;J.AxiosHeaders=Pe;J.formToJSON=e=>gd(w.isHTMLForm(e)?new FormData(e):e);J.getAdapter=Cd.getAdapter;J.HttpStatusCode=qo;J.default=J;const{Axios:fv,AxiosError:dv,CanceledError:pv,isCancel:hv,CancelToken:mv,VERSION:yv,all:vv,Cancel:gv,isAxiosError:xv,spread:wv,toFormData:Sv,AxiosHeaders:Ev,HttpStatusCode:kv,formToJSON:Cv,getAdapter:Nv,mergeConfig:Rv}=J;function tv({taskId:e,taskName:t,onClose:n,mode:r="modal"}){const[l,i]=N.useState([]),o=N.useRef(null);N.useEffect(()=>{const a=async()=>{try{const d=await J.get(`/api/tasks/${e}/logs`);i(d.data)}catch(d){console.error(d)}};a();const f=setInterval(a,2e3);return()=>clearInterval(f)},[e]),N.useEffect(()=>{o.current&&o.current.scrollIntoView({behavior:"smooth"})},[l]);const s=r==="modal"?"fixed inset-0 bg-black/80 backdrop-blur-sm flex items-center justify-center p-8 z-50 animate-fade-in":"h-full w-full flex flex-col bg-[#020617]",u=r==="modal"?"bg-[#0f172a] w-full max-w-5xl h-[80vh] rounded-xl flex flex-col shadow-2xl border border-white/10 overflow-hidden text-sm font-mono":"h-full flex flex-col overflow-hidden text-sm font-mono bg-[#020617]";return v.jsx("div",{className:s,onClick:r==="modal"?a=>{a.target===a.currentTarget&&n()}:void 0,children:v.jsxs("div",{className:u,children:[v.jsxs("div",{className:"flex items-center justify-between p-4 bg-[#1e293b] border-b border-[#334155] flex-shrink-0",children:[v.jsxs("div",{className:"flex items-center gap-2 text-blue-400",children:[v.jsx(k0,{size:18}),v.jsx("span",{className:"font-bold truncate max-w-[300px]",title:t,children:t})]}),v.jsx("button",{onClick:n,className:"p-1 hover:bg-[#334155] rounded text-slate-400 hover:text-white transition-colors",children:v.jsx(nd,{size:20})})]}),v.jsxs("div",{className:"flex-1 min-h-0 overflow-y-auto p-4 space-y-1 bg-[#020617] custom-scrollbar font-mono text-xs md:text-sm",children:[l.length===0&&v.jsx("div",{className:"text-slate-600 italic px-2",children:"Waiting for logs..."}),l.map(a=>v.jsxs("div",{className:"text-slate-300 whitespace-pre-wrap break-words leading-tight hover:bg-white/5 px-2 py-0.5 rounded transition-colors group",children:[v.jsx("span",{className:"text-slate-600 text-[10px] mr-3 select-none w-14 inline-block opacity-50 group-hover:opacity-100 transition-opacity",children:new Date(a.timestamp).toLocaleTimeString()}),v.jsx("span",{className:a.content.includes("ERROR")||a.content.includes("❌")?"text-red-400 font-semibold":Number(a.content.includes("WARN"))?"text-orange-400":a.content.includes("SUCCESS")||a.content.includes("✔")?"text-emerald-400":"",children:a.content})]},a.id)),v.jsx("div",{ref:o})]}),v.jsxs("div",{className:"p-2 bg-[#1e293b] border-t border-[#334155] text-[10px] text-slate-500 flex justify-between flex-shrink-0",children:[v.jsxs("span",{className:"truncate max-w-[200px] font-mono opacity-70",children:["ID: ",e]}),v.jsxs("span",{className:"flex items-center gap-1.5 text-emerald-400",children:[v.jsxs("span",{className:"relative flex h-2 w-2",children:[v.jsx("span",{className:"animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"}),v.jsx("span",{className:"relative inline-flex rounded-full h-2 w-2 bg-emerald-400"})]}),"Live Connection"]})]})]})})}function nv(e){return e==="RUNNING"?"text-secondary":["COMPLETED","SUCCESS","APPROVED"].includes(e)?"text-success":["FAILED","REJECTED","FAILED_FINAL"].includes(e)?"text-error":"text-slate-500"}function _d(e){return e==="RUNNING"?"border-secondary":["COMPLETED","SUCCESS","APPROVED"].includes(e)?"border-success":["FAILED","REJECTED","FAILED_FINAL"].includes(e)?"border-error":"border-border"}function rl(e){return e.includes("PLANNING")?"PLANNER":e.includes("EXECUTION")?"WORKERS":e.includes("MERGE")?"MERGER":e.includes("REVIEW")?"REVIEWER":"OTHER"}const Xn=({start:e,end:t,status:n})=>{const r=(e.x+t.x)/2,l=`M ${e.x} ${e.y} C ${r} ${e.y}, ${r} ${t.y}, ${t.x} ${t.y}`,i=n==="RUNNING"||n==="SUCCESS"||n==="COMPLETED",o=i?"text-secondary":"text-slate-700";return v.jsxs("g",{className:`${o} transition-colors duration-300`,children:[v.jsx("path",{d:l,fill:"none",stroke:"currentColor",strokeWidth:i?"2":"1",className:i?"opacity-100":"opacity-30"}),n==="RUNNING"&&v.jsx("circle",{r:"3",fill:"currentColor",children:v.jsx("animateMotion",{dur:"1.5s",repeatCount:"indefinite",path:l})})]})},ll=({title:e,name:t,icon:n,status:r,onClick:l,isActive:i,isWorker:o=!1})=>{const s=r==="RUNNING";return v.jsx("div",{onClick:l,className:`
                relative transition-all duration-200 group cursor-pointer overflow-hidden
                bg-surfaceHighlight shadow-lg
                border-l-4 ${_d(r)}
                ${i?"ring-2 ring-primary ring-offset-2 ring-offset-background":""}
                w-[320px] p-5 rounded-sm
                hover:bg-[#3a3a3c]
            `,children:v.jsxs("div",{className:"flex flex-col h-full justify-between relative z-10",children:[v.jsx("div",{className:"flex items-start justify-between mb-3",children:v.jsxs("div",{className:"flex items-center gap-3",children:[v.jsx("div",{className:`p-1.5 rounded-sm ${s?"text-secondary":"text-slate-400"}`,children:v.jsx(n,{size:20})}),v.jsx("div",{className:"text-xs font-bold uppercase tracking-wider text-slate-500",children:e})]})}),v.jsx("div",{className:"font-mono text-sm text-slate-200 break-all leading-relaxed custom-scrollbar max-h-[100px] overflow-y-auto",children:t}),v.jsxs("div",{className:"mt-3 flex items-center justify-between border-t border-white/5 pt-2",children:[v.jsx("span",{className:`text-xs font-bold ${nv(r)}`,children:r||"PENDING"}),o&&v.jsxs("span",{className:"text-[10px] text-slate-600 font-mono",children:["ID: ",t.slice(-6)]})]})]})})};function rv(){var _,P,T,M,L,te,_e,we,je;const{id:e}=zm(),[t,n]=N.useState(null),[r,l]=N.useState(null),[i,o]=N.useState({x:0,y:0,k:1}),[s,u]=N.useState(!1),[a,f]=N.useState({x:0,y:0}),d=N.useRef(null);N.useEffect(()=>{if(!e)return;const O=async()=>{try{const me=await J.get(`/api/pipelines/${e}`);n(me.data)}catch(me){console.error(me)}};O();const U=setInterval(O,2e3);return()=>clearInterval(U)},[e]);const y=N.useCallback(O=>{if(O.ctrlKey||O.metaKey){O.preventDefault();const U=-O.deltaY*.001;o(me=>({...me,k:Math.max(.1,Math.min(4,me.k*(1+U)))}))}else o(U=>({...U,x:U.x-O.deltaX,y:U.y-O.deltaY}))},[]),E=O=>{O.button===0&&(u(!0),f({x:O.clientX,y:O.clientY}))},m=O=>{if(!s)return;const U=O.clientX-a.x,me=O.clientY-a.y;o(R=>({...R,x:R.x+U,y:R.y+me})),f({x:O.clientX,y:O.clientY})},x=()=>u(!1),S=()=>u(!1);if(!t)return v.jsx("div",{className:"flex items-center justify-center h-full text-slate-500 bg-background font-mono text-sm",children:"INITIALIZING WORKSPACE..."});const h=t.stages||[],c=h.find(O=>rl(O.name)==="PLANNER"),p=((_=h.find(O=>rl(O.name)==="WORKERS"))==null?void 0:_.tasks)||[],g=h.find(O=>rl(O.name)==="MERGER"),k=h.find(O=>rl(O.name)==="REVIEWER");return v.jsxs("div",{className:"h-full flex flex-col bg-background text-slate-200 font-sans overflow-hidden select-none",children:[v.jsxs("header",{className:"flex-none h-12 border-b border-border bg-surface flex items-center justify-between px-4 z-30",children:[v.jsxs("div",{className:"flex items-center gap-4 text-sm",children:[v.jsxs("div",{className:"font-bold text-slate-300 flex items-center gap-2",children:[v.jsx(N0,{size:14,className:"text-secondary"}),"WORKSPACE"]}),v.jsx("span",{className:"text-slate-500 font-mono text-xs hidden md:inline",children:t.objective})]}),v.jsxs("div",{className:"flex items-center gap-3",children:[v.jsx("button",{onClick:()=>o({x:0,y:0,k:1}),className:"p-1 hover:bg-surfaceHighlight rounded text-slate-400",title:"Reset View",children:v.jsx(v0,{size:14})}),v.jsxs("div",{className:"text-xs font-mono text-slate-500",children:[Math.round(i.k*100),"%"]}),v.jsx("div",{className:`px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider ${_d(t.status)} border text-slate-300`,children:t.status})]})]}),v.jsx("main",{className:"flex-1 relative overflow-hidden bg-background cursor-grab active:cursor-grabbing",onWheel:y,onMouseDown:E,onMouseMove:m,onMouseUp:x,onMouseLeave:S,children:v.jsx("div",{className:"absolute origin-top-left transition-transform duration-75 ease-linear",style:{transform:`translate(${i.x}px, ${i.y}px) scale(${i.k})`},children:v.jsxs("div",{className:"w-[3000px] h-[2000px] relative pt-20 pl-20",ref:d,children:[v.jsxs("svg",{className:"absolute inset-0 w-full h-full pointer-events-none z-0",children:[p.length>0?v.jsxs(v.Fragment,{children:[p.map((O,U)=>v.jsx(Xn,{start:{x:420,y:400},end:{x:570,y:400+p.length*180/2-p.length*180+U*180+90},status:(c==null?void 0:c.status)||"PENDING"},`p-w-${U}`)),p.map((O,U)=>v.jsx(Xn,{start:{x:890,y:400+p.length*180/2-p.length*180+U*180+90},end:{x:1040,y:400},status:O.status==="RUNNING"||O.status==="COMPLETED"||O.status==="SUCCESS"?"RUNNING":"PENDING"},`w-m-${U}`))]}):v.jsx(Xn,{start:{x:420,y:400},end:{x:570,y:400},status:(c==null?void 0:c.status)||"PENDING"}),v.jsx(Xn,{start:{x:1360,y:400},end:{x:1510,y:400},status:(g==null?void 0:g.status)||"PENDING"}),v.jsx(Xn,{start:{x:1830,y:400},end:{x:1980,y:416},status:(k==null?void 0:k.status)||"PENDING"})]}),v.jsx("div",{className:"absolute top-[320px] left-[100px] z-10",children:v.jsx(ll,{title:"Planner",name:((T=(P=c==null?void 0:c.tasks)==null?void 0:P[0])==null?void 0:T.name)||(c==null?void 0:c.name)||"Initializing...",icon:Qs,status:c==null?void 0:c.status,isActive:(r==null?void 0:r.id)===((L=(M=c==null?void 0:c.tasks)==null?void 0:M[0])==null?void 0:L.id),onClick:()=>{var O;return((O=c==null?void 0:c.tasks)==null?void 0:O[0])&&l({id:c.tasks[0].id,name:"Plan"})}})}),v.jsx("div",{className:"absolute left-[570px] z-10 flex flex-col gap-[20px]",style:{top:p.length>0?`${400-p.length*180/2}px`:"320px"},children:p.length>0?p.map(O=>v.jsx(ll,{title:"Worker Agent",name:O.name,icon:x0,isWorker:!0,status:O.status,isActive:(r==null?void 0:r.id)===O.id,onClick:()=>l({id:O.id,name:O.name})},O.id)):v.jsx("div",{className:"w-[320px] p-6 border border-dashed border-border text-slate-600 font-mono text-xs text-center glass-card",children:"// Awaiting dispatch..."})}),v.jsx("div",{className:"absolute top-[320px] left-[1040px] z-10",children:v.jsx(ll,{title:"Integrator",name:(g==null?void 0:g.name)||"Merge Pending",icon:m0,status:g==null?void 0:g.status,isActive:(r==null?void 0:r.id)===((_e=(te=g==null?void 0:g.tasks)==null?void 0:te[0])==null?void 0:_e.id),onClick:()=>{var O;return((O=g==null?void 0:g.tasks)==null?void 0:O[0])&&l({id:g.tasks[0].id,name:"Merge"})}})}),v.jsx("div",{className:"absolute top-[320px] left-[1510px] z-10",children:v.jsx(ll,{title:"Reviewer",name:(k==null?void 0:k.name)||"Review Pending",icon:E0,status:k==null?void 0:k.status,isActive:(r==null?void 0:r.id)===((je=(we=k==null?void 0:k.tasks)==null?void 0:we[0])==null?void 0:je.id),onClick:()=>{var O;return((O=k==null?void 0:k.tasks)==null?void 0:O[0])&&l({id:k.tasks[0].id,name:"Review"})}})}),v.jsxs("div",{className:"absolute top-[350px] left-[1980px] z-10 flex items-center gap-4",children:[v.jsx("div",{className:`
                                w-32 h-32 rounded-full border-4 flex items-center justify-center transition-all
                                ${t.status==="SUCCESS"?"border-success bg-background shadow-lg":t.status==="FAILED"?"border-error bg-background shadow-lg":"border-border bg-surfaceHighlight"}
                            `,children:t.status==="SUCCESS"?v.jsx(h0,{size:48,className:"text-success"}):t.status==="FAILED"?v.jsx(C0,{size:48,className:"text-error"}):v.jsx(w0,{size:48,className:"text-secondary animate-pulse"})}),v.jsx("div",{className:"text-2xl font-bold tracking-tight text-slate-300",children:t.status})]})]})})}),v.jsx("div",{className:`fixed inset-y-0 right-0 w-[600px] bg-background border-l border-border shadow-2xl transition-transform duration-200 z-50 flex flex-col ${r?"translate-x-0":"translate-x-full"}`,children:r&&v.jsx(tv,{taskId:r.id,taskName:r.name,onClose:()=>l(null),mode:"sidebar"})}),r&&v.jsx("div",{className:"fixed inset-0 bg-black/50 z-40",onClick:()=>l(null)})]})}const lv=()=>v.jsxs("div",{className:"fixed inset-0 overflow-hidden pointer-events-none -z-10 bg-background",children:[v.jsx("div",{className:"absolute top-[-10%] left-[-10%] w-[50%] h-[50%] bg-primary/20 rounded-full blur-[120px] animate-pulse-slow mix-blend-screen"}),v.jsx("div",{className:"absolute bottom-[-10%] right-[-10%] w-[50%] h-[50%] bg-secondary/20 rounded-full blur-[120px] animate-pulse-slow mix-blend-screen",style:{animationDelay:"2s"}}),v.jsx("div",{className:"absolute top-[40%] right-[20%] w-[20%] h-[20%] bg-accent/10 rounded-full blur-[100px] animate-float"}),v.jsx("div",{className:"absolute inset-0 bg-[url('/grid.svg')] opacity-[0.03] bg-[length:32px_32px]"})]});function iv({isOpen:e,onClose:t}){const[n,r]=N.useState([]);return N.useEffect(()=>{const l=async()=>{try{const o=await J.get("/api/pipelines");r(o.data)}catch(o){console.error(o)}};l();const i=setInterval(l,5e3);return()=>clearInterval(i)},[]),v.jsxs(v.Fragment,{children:[v.jsx("div",{className:`fixed inset-0 bg-black/60 backdrop-blur-sm z-40 transition-opacity duration-300 md:hidden ${e?"opacity-100":"opacity-0 pointer-events-none"}`,onClick:t}),v.jsxs("div",{className:`fixed top-0 left-0 h-full w-72 backdrop-blur-xl bg-surface/80 border-r border-white/5 z-50 transform transition-transform duration-500 cubic-bezier(0.16, 1, 0.3, 1) ${e?"translate-x-0":"-translate-x-full"}`,children:[v.jsxs("div",{className:"p-6 flex justify-between items-center",children:[v.jsxs("div",{className:"flex items-center gap-3",children:[v.jsx("div",{className:"w-10 h-10 rounded-xl bg-gradient-to-br from-primary to-secondary flex items-center justify-center shadow-lg shadow-primary/20",children:v.jsx(p0,{className:"text-white",size:20})}),v.jsxs("div",{children:[v.jsx("h1",{className:"text-lg font-bold text-white tracking-tight leading-none",children:"Orchestra"}),v.jsx("span",{className:"text-[10px] uppercase tracking-wider text-slate-400 font-semibold",children:"Pro Dashboard"})]})]}),v.jsx("button",{onClick:t,className:"md:hidden p-2 hover:bg-white/5 rounded-lg text-slate-400 hover:text-white transition-colors",children:v.jsx(nd,{size:20})})]}),v.jsx("div",{className:"px-3 mb-2",children:v.jsx("div",{className:"h-px bg-gradient-to-r from-transparent via-white/10 to-transparent"})}),v.jsxs("nav",{className:"flex-1 overflow-y-auto p-4 custom-scrollbar space-y-6",children:[v.jsxs("div",{children:[v.jsx("div",{className:"text-xs font-semibold text-slate-500 uppercase tracking-widest mb-3 px-2",children:"Main Menu"}),v.jsxs(tl,{to:"/",onClick:t,className:({isActive:l})=>`flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all duration-200 ${l?"bg-primary/10 text-primary-foreground shadow-sm ring-1 ring-primary/20":"text-slate-400 hover:text-white hover:bg-white/5"}`,children:[v.jsx(Qs,{size:18}),"Overview"]}),v.jsxs(tl,{to:"#",className:"flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium text-slate-400 hover:text-white hover:bg-white/5 transition-all duration-200 opacity-60 cursor-not-allowed",children:[v.jsx(td,{size:18}),"Deployments"]}),v.jsxs(tl,{to:"#",className:"flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium text-slate-400 hover:text-white hover:bg-white/5 transition-all duration-200 opacity-60 cursor-not-allowed",children:[v.jsx(S0,{size:18}),"Configuration"]})]}),v.jsxs("div",{children:[v.jsxs("div",{className:"flex items-center justify-between px-2 mb-3",children:[v.jsx("div",{className:"text-xs font-semibold text-slate-500 uppercase tracking-widest",children:"Active Pipelines"}),v.jsx("span",{className:"text-[10px] bg-primary/20 text-primary px-1.5 py-0.5 rounded-md font-mono",children:n.length})]}),v.jsx("div",{className:"space-y-1",children:n.map(l=>v.jsx(tl,{to:`/pipelines/${l.id}`,onClick:t,className:({isActive:i})=>`group relative block px-3 py-2.5 rounded-lg text-sm transition-all duration-200 ${i?"bg-gradient-to-r from-primary/10 to-transparent border-l-2 border-primary text-white":"hover:bg-white/5 text-slate-400 hover:text-slate-200 border-l-2 border-transparent"}`,children:({isActive:i})=>v.jsxs(v.Fragment,{children:[v.jsxs("div",{className:"flex justify-between items-center mb-1",children:[v.jsx("div",{className:"truncate pr-2 w-full font-medium",children:l.objective||"Untitled Task"}),i&&v.jsx("div",{className:"w-1.5 h-1.5 rounded-full bg-primary shadow-[0_0_8px_rgba(99,102,241,0.6)]"})]}),v.jsxs("div",{className:"flex items-center gap-2 text-[10px] opacity-60 font-mono",children:[v.jsx(ov,{status:l.status,small:!0}),v.jsxs("span",{children:["ID: ",l.id.slice(0,4),"...",l.id.slice(-4)]})]})]})},l.id))})]})]}),v.jsx("div",{className:"p-4 border-t border-white/5 bg-gradient-to-t from-black/40 to-transparent",children:v.jsxs("div",{className:"glass-card rounded-xl p-3 flex items-center gap-3",children:[v.jsxs("div",{className:"relative",children:[v.jsx("div",{className:"w-9 h-9 rounded-full bg-surfaceHighlight flex items-center justify-center text-slate-300 font-bold text-xs border border-white/10",children:"AI"}),v.jsx("span",{className:"absolute -bottom-0.5 -right-0.5 w-2.5 h-2.5 bg-emerald-500 border-2 border-surface rounded-full"})]}),v.jsxs("div",{children:[v.jsx("div",{className:"text-white text-xs font-medium",children:"System Status"}),v.jsxs("div",{className:"text-[10px] text-emerald-400 flex items-center gap-1 mt-0.5 font-medium",children:[v.jsx(rd,{size:10,className:"fill-emerald-400"}),"All Systems Operational"]})]})]})})]})]})}function ov({status:e,small:t}){const n=t?"w-1.5 h-1.5":"w-2 h-2";return e==="RUNNING"?v.jsx("div",{className:`shrink-0 ${n} rounded-full bg-blue-500 animate-pulse shadow-[0_0_8px_rgba(59,130,246,0.6)]`}):e==="SUCCESS"?v.jsx("div",{className:`shrink-0 ${n} rounded-full bg-emerald-500 shadow-[0_0_8px_rgba(16,185,129,0.6)]`}):e==="FAILED"?v.jsx("div",{className:`shrink-0 ${n} rounded-full bg-red-500 shadow-[0_0_8px_rgba(239,68,68,0.6)]`}):v.jsx("div",{className:`shrink-0 ${n} rounded-full bg-slate-600`})}function sv(){const[e,t]=N.useState(!0),n=Dn();return N.useEffect(()=>{const r=()=>{window.innerWidth<768?t(!1):t(!0)};return window.addEventListener("resize",r),r(),()=>window.removeEventListener("resize",r)},[]),v.jsxs("div",{className:"flex min-h-screen font-sans relative overflow-hidden bg-background text-slate-200",children:[v.jsx(lv,{}),v.jsx(iv,{isOpen:e,onClose:()=>t(!1)}),v.jsxs("main",{className:`flex-1 flex flex-col h-screen overflow-hidden relative transition-all duration-500 ease-in-out ${e?"md:ml-72":""}`,children:[v.jsxs("header",{className:"h-16 px-6 flex items-center justify-between border-b border-white/5 backdrop-blur-md z-30 sticky top-0",children:[v.jsxs("div",{className:"flex items-center gap-4",children:[!e&&v.jsx("button",{onClick:()=>t(!0),className:"p-2 hover:bg-white/5 rounded-lg text-slate-400 hover:text-white transition-colors",children:v.jsx(g0,{size:20})}),v.jsxs("div",{className:"flex items-center gap-2 text-sm text-slate-400",children:[v.jsx(y0,{size:14}),v.jsx("span",{children:"/"}),v.jsx("span",{className:"text-slate-200 font-medium",children:"Dashboard"}),n.pathname!=="/"&&v.jsxs(v.Fragment,{children:[v.jsx("span",{children:"/"}),v.jsx("span",{className:"text-primary truncate max-w-[200px]",children:n.pathname.split("/").pop()})]})]})]}),v.jsx("div",{className:"flex items-center gap-4",children:v.jsxs("div",{className:"flex items-center gap-2 px-3 py-1.5 rounded-full bg-white/5 border border-white/5 text-xs font-medium text-slate-300",children:[v.jsx("div",{className:"w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"}),"v2.4.0-stable"]})})]}),v.jsx("div",{className:"flex-1 overflow-y-auto custom-scrollbar p-6",children:v.jsxs(qm,{children:[v.jsx(Wo,{path:"/",element:v.jsxs("div",{className:"max-w-5xl mx-auto animate-fade-in",children:[v.jsxs("div",{className:"text-center mb-12 py-10",children:[v.jsxs("div",{className:"inline-flex items-center justify-center p-4 rounded-3xl bg-gradient-to-br from-primary/20 to-secondary/20 border border-white/10 mb-6 shadow-2xl relative group",children:[v.jsx("div",{className:"absolute inset-0 bg-primary/20 blur-xl rounded-3xl group-hover:bg-primary/30 transition-all duration-500"}),v.jsx(Qs,{size:48,className:"text-white relative z-10"})]}),v.jsxs("h2",{className:"text-4xl md:text-5xl font-bold text-white mb-4 tracking-tight",children:["Welcome to ",v.jsx("span",{className:"text-gradient-primary",children:"Orchestra"})]}),v.jsx("p",{className:"text-slate-400 text-lg max-w-xl mx-auto leading-relaxed",children:"Your advanced command center for managing autonomous agent pipelines. Select a pipeline to begin monitoring."})]}),v.jsx("div",{className:"grid grid-cols-1 md:grid-cols-3 gap-6",children:[{icon:d0,label:"Active Nodes",value:"12",color:"text-emerald-400",bg:"bg-emerald-400/10"},{icon:rd,label:"Total Throughput",value:"98.2%",color:"text-amber-400",bg:"bg-amber-400/10"},{icon:td,label:"Pipelines Queued",value:"4",color:"text-blue-400",bg:"bg-blue-400/10"}].map((r,l)=>v.jsxs("div",{className:"glass-card p-6 rounded-2xl flex flex-col items-center text-center hover:scale-[1.02] transition-transform cursor-default",children:[v.jsx("div",{className:`p-3 rounded-xl ${r.bg} mb-4`,children:v.jsx(r.icon,{className:r.color,size:24})}),v.jsx("div",{className:"text-3xl font-bold text-white mb-1",children:r.value}),v.jsx("div",{className:"text-sm text-slate-400 font-medium",children:r.label})]},l))})]})}),v.jsx(Wo,{path:"/pipelines/:id",element:v.jsx(rv,{})})]})})]})]})}function uv(){return v.jsx(r0,{children:v.jsx(sv,{})})}Gi.createRoot(document.getElementById("root")).render(v.jsx(Ua.StrictMode,{children:v.jsx(uv,{})}));
```

### dashboard/frontend/dist/index.html

```html
<!doctype html>
<html lang="en">

<head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/vite.svg" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Orchestrator Dashboard</title>
  <script type="module" crossorigin src="/assets/index-E3jWGKad.js"></script>
  <link rel="stylesheet" crossorigin href="/assets/index-DJPa3AgC.css">
</head>

<body>
    <div id="root"></div>
</body>

</html>
```

### dashboard/frontend/index.html

```html
<!doctype html>
<html lang="en">

<head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/vite.svg" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Orchestrator Dashboard</title>
</head>

<body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
</body>

</html>
```

### dashboard/frontend/postcss.config.js

```javascript
export default {
    plugins: {
        tailwindcss: {},
        autoprefixer: {},
    },
}
```

### dashboard/frontend/tailwind.config.js

```javascript
/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/*.{js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            fontFamily: {
                sans: ['Inter', 'system-ui', 'sans-serif'],
                display: ['Outfit', 'Inter', 'system-ui', 'sans-serif'],
                mono: ['JetBrains Mono', 'monospace'],
            },
            colors: {
                background: '#030712', // Rich Dark Slate (almost black)
                surface: '#0f172a',    // Deep Blue Slate
                surfaceHighlight: '#1e293b', // Lighter Slate
                border: '#1e293b',     // Subtle border

                // Professional Modern Palette
                primary: {
                    DEFAULT: '#6366f1', // Indigo 500
                    foreground: '#ffffff',
                    glow: 'rgba(99, 102, 241, 0.5)'
                },
                secondary: {
                    DEFAULT: '#8b5cf6', // Violet 500
                    foreground: '#ffffff',
                },
                accent: {
                    DEFAULT: '#06b6d4', // Cyan 500
                    foreground: '#ffffff',
                },
                success: '#10b981',    // Emerald 500
                error: '#ef4444',      // Red 500
                warning: '#f59e0b',    // Amber 500
                slate: {
                    850: '#151e32',
                }
            },
            backgroundImage: {
                'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
                'hero-glow': 'conic-gradient(from 180deg at 50% 50%, #2a8af6 0deg, #a853ba 180deg, #e92a67 360deg)',
            },
            animation: {
                'fade-in': 'fadeIn 0.6s cubic-bezier(0.16, 1, 0.3, 1)',
                'slide-in': 'slideIn 0.4s cubic-bezier(0.16, 1, 0.3, 1)',
                'pulse-slow': 'pulse 4s cubic-bezier(0.4, 0, 0.6, 1) infinite',
                'float': 'float 6s ease-in-out infinite',
            },
            keyframes: {
                fadeIn: {
                    '0%': { opacity: '0', transform: 'translateY(10px)' },
                    '100%': { opacity: '1', transform: 'translateY(0)' },
                },
                slideIn: {
                    '0%': { transform: 'translateX(-20px)', opacity: '0' },
                    '100%': { transform: 'translateX(0)', opacity: '1' },
                },
                float: {
                    '0%, 100%': { transform: 'translateY(0)' },
                    '50%': { transform: 'translateY(-10px)' },
                }
            }
        },
    },
    plugins: [],
}
```

### dashboard/frontend/vite.config.ts

```typescript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
    plugins: [react()],
    server: {
        proxy: {
            '/api': {
                target: 'http://localhost:8000',
                changeOrigin: true,
            },
            '/ws': {
                target: 'ws://localhost:8000',
                ws: true
            }
        }
    }
})
```

---

## Статистика
- Всего файлов: 40
- Файлов в категории 'html templates': 3
- Файлов в категории 'frontend src': 30
- Файлов в категории 'frontend': 7
