import re

with open("frontend/index.html", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update CSS
css_old = re.search(r"<style>([\s\S]*?)</style>", content).group(1)

# Add custom modal CSS & enhanced sleek components
custom_additions = """
/* === Custom Modern Modal (Hapus Obrolan & Logout) === */
.custom-modal-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.72);
  backdrop-filter: blur(10px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  opacity: 1;
  transition: opacity 0.2s ease;
}
.custom-modal-backdrop.hidden {
  opacity: 0;
  pointer-events: none;
}
.custom-modal-card {
  width: 90%;
  max-width: 380px;
  background: #14161d;
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: 22px;
  padding: 26px 22px 22px;
  text-align: center;
  box-shadow: 0 24px 60px rgba(0, 0, 0, 0.7), 0 0 0 1px rgba(255, 255, 255, 0.05);
  animation: modalScaleUp 0.22s cubic-bezier(0.16, 1, 0.3, 1);
}
@keyframes modalScaleUp {
  from { opacity: 0; transform: scale(0.92); }
  to { opacity: 1; transform: scale(1); }
}
.custom-modal-icon-wrap {
  width: 54px;
  height: 54px;
  margin: 0 auto 16px;
  border-radius: 18px;
  background: rgba(239, 68, 68, 0.12);
  border: 1px solid rgba(239, 68, 68, 0.25);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 26px;
}
.custom-modal-icon-wrap.logout {
  background: rgba(99, 102, 241, 0.12);
  border-color: rgba(99, 102, 241, 0.25);
}
.custom-modal-title {
  margin: 0 0 8px;
  font-size: 17px;
  font-weight: 700;
  color: #fff;
  letter-spacing: -0.3px;
}
.custom-modal-desc {
  margin: 0 0 24px;
  font-size: 13px;
  color: #9499ab;
  line-height: 1.5;
}
.custom-modal-actions {
  display: flex;
  gap: 10px;
}
.btn-modal-cancel {
  flex: 1;
  background: rgba(255, 255, 255, 0.06);
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: #d1d5db;
  padding: 11px 16px;
  border-radius: 12px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}
.btn-modal-cancel:hover {
  background: rgba(255, 255, 255, 0.1);
  color: #fff;
}
.btn-modal-confirm {
  flex: 1;
  background: linear-gradient(135deg, #ef4444, #dc2626);
  border: none;
  color: #fff;
  padding: 11px 16px;
  border-radius: 12px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  box-shadow: 0 4px 12px rgba(239, 68, 68, 0.3);
  transition: all 0.2s;
}
.btn-modal-confirm:hover {
  opacity: 0.92;
  transform: translateY(-1px);
}
.btn-modal-confirm.logout {
  background: linear-gradient(135deg, #6366f1, #4f46e5);
  box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
}

/* === Modern Sleek Buttons & Badges === */
.brand {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 16px;
  font-weight: 700;
  letter-spacing: -0.3px;
  background: none !important;
  -webkit-text-fill-color: initial !important;
}
.brand-text {
  background: linear-gradient(135deg, #a5b4fc 0%, #c084fc 50%, #f472b6 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
.badge-admin {
  background: rgba(245, 158, 11, 0.15) !important;
  border: 1px solid rgba(245, 158, 11, 0.35) !important;
  color: #fbbf24 !important;
  font-size: 10px !important;
  font-weight: 700 !important;
  padding: 2px 7px !important;
  border-radius: 6px !important;
  letter-spacing: 0.8px !important;
  text-transform: uppercase !important;
  -webkit-text-fill-color: #fbbf24 !important;
  -webkit-background-clip: initial !important;
  box-shadow: none !important;
  display: inline-block !important;
  vertical-align: middle !important;
}

.btn-new-chat {
  width: 100%;
  background: rgba(255, 255, 255, 0.05) !important;
  color: #f1f3f9 !important;
  border: 1px solid rgba(255, 255, 255, 0.1) !important;
  border-radius: 12px !important;
  padding: 9px 14px !important;
  font-size: 13px !important;
  font-weight: 500 !important;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1) !important;
  box-shadow: none !important;
}
.btn-new-chat:hover {
  background: rgba(255, 255, 255, 0.09) !important;
  border-color: rgba(255, 255, 255, 0.2) !important;
  transform: translateY(-1px);
}
.btn-export-chat {
  width: 38px;
  height: 38px;
  background: rgba(255, 255, 255, 0.05);
  color: #9499ab;
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s;
  flex-shrink: 0;
}
.btn-export-chat:hover {
  background: rgba(255, 255, 255, 0.1);
  color: #fff;
  border-color: rgba(255, 255, 255, 0.2);
}

.user-chip {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  font-weight: 500;
  color: #e2e8f0;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.08);
  padding: 4px 10px 4px 4px;
  border-radius: 20px;
}
.user-avatar {
  width: 26px;
  height: 26px;
  border-radius: 50%;
  background: linear-gradient(135deg, #4f46e5, #7c3aed);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 11px;
  font-weight: 700;
  color: #fff;
}
.btn-logout-sleek {
  background: rgba(255, 255, 255, 0.04);
  color: #9499ab;
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 10px;
  padding: 6px 12px;
  font-size: 12px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}
.btn-logout-sleek:hover {
  background: rgba(239, 68, 68, 0.12);
  color: #fca5a5;
  border-color: rgba(239, 68, 68, 0.3);
}

.hero-cookie-badge {
  width: 64px;
  height: 64px;
  border-radius: 22px;
  background: radial-gradient(circle at 30% 30%, rgba(99, 102, 241, 0.25), rgba(139, 92, 246, 0.1));
  border: 1px solid rgba(255, 255, 255, 0.12);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 20px;
  box-shadow: 0 12px 30px rgba(0, 0, 0, 0.4), 0 0 24px rgba(99, 102, 241, 0.2);
}
.hero-cookie-icon {
  font-size: 32px;
  filter: drop-shadow(0 2px 8px rgba(0,0,0,0.3));
}
.hero-title {
  font-size: 28px !important;
  font-weight: 700 !important;
  letter-spacing: -0.6px !important;
  margin-bottom: 8px !important;
  color: #f1f3f9 !important;
  background: none !important;
  -webkit-text-fill-color: initial !important;
}
.hero-desc {
  font-size: 14px !important;
  color: #8b92a5 !important;
  max-width: 520px !important;
  line-height: 1.5 !important;
  margin-bottom: 30px !important;
}
.suggestions-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
  width: 100%;
  max-width: 700px;
}
.sug-card {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.07);
  border-radius: 16px;
  padding: 16px 18px;
  text-align: left;
  cursor: pointer;
  transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.sug-card:hover {
  background: rgba(255, 255, 255, 0.06);
  border-color: rgba(99, 102, 241, 0.4);
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
}
.sug-card .sug-head {
  font-size: 13.5px;
  font-weight: 600;
  color: #f1f3f9;
  display: flex;
  align-items: center;
  gap: 8px;
}
.sug-card .sug-sub {
  font-size: 12px;
  color: #8b92a5;
  line-height: 1.4;
}
"""

content = content.replace("</style>", custom_additions + "\n</style>", 1)

# 2. Update Topbar HTML
topbar_pattern = re.compile(r'<header id="topbar">[\s\S]*?</header>')
new_topbar = """<header id="topbar">
  <button id="btnToggleSidebar" class="icon-btn" title="Toggle Sidebar">
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="3" y1="12" x2="21" y2="12"></line><line x1="3" y1="6" x2="21" y2="6"></line><line x1="3" y1="18" x2="21" y2="18"></line></svg>
  </button>
  <div class="brand">
    <span class="emoji">🍪</span>
    <span class="brand-text">Oreo AI</span>
    <span id="adminBadgeWrap"></span>
  </div>

  <div class="header-spacer"></div>

  <div id="quotaBadge" class="quota-badge" style="display:none;" title="Batas kuota harian. Di-reset otomatis setiap hari pukul 00:00. Klik untuk detail.">
    <span id="quotaText">⚡ Kuota: --/--</span>
  </div>

  <div id="headerUserInfo" class="user-chip">
    <div id="userAvatar" class="user-avatar">?</div>
    <span id="userName">Tamu</span>
  </div>

  <button id="btnAuth" class="btn-secondary" style="display:none">Login</button>
  <button id="btnLogout" class="btn-logout-sleek" style="display:none">Keluar</button>
</header>"""

content = topbar_pattern.sub(new_topbar, content)

# 3. Remove connector modal and add customConfirmModal
conn_modal_pattern = re.compile(r'<!-- Modal Konektor Aplikasi[\s\S]*?</div>\s*</div>\s*(?=<!-- Halaman Login -->)')
new_modal_html = """<!-- Modal Konfirmasi Estetik (Hapus Obrolan & Logout) -->
<div id="customConfirmModal" class="custom-modal-backdrop hidden">
  <div class="custom-modal-card">
    <div class="custom-modal-icon-wrap" id="modalIconWrap">
      <span id="modalIcon">⚠️</span>
    </div>
    <h3 class="custom-modal-title" id="modalTitle">Konfirmasi</h3>
    <p class="custom-modal-desc" id="modalDesc">Apakah Anda yakin?</p>
    <div class="custom-modal-actions">
      <button type="button" class="btn-modal-cancel" id="btnModalCancel">Batal</button>
      <button type="button" class="btn-modal-confirm" id="btnModalConfirm">Lanjutkan</button>
    </div>
  </div>
</div>\n\n"""

content = conn_modal_pattern.sub(new_modal_html, content)

# 4. Update sidebar header in #sidebar
sidebar_head_pattern = re.compile(r'<div class="sidebar-header"[\s\S]*?</div>\s*(?=<div class="sidebar-section-title">)')
new_sidebar_head = """<div class="sidebar-header">
      <button id="btnNew" class="btn-new-chat">
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line></svg>
        <span>Obrolan Baru</span>
      </button>
      <button id="btnExportChat" class="btn-export-chat" title="Unduh Percakapan (Markdown)">
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="7 10 12 15 17 10"></polyline><line x1="12" y1="15" x2="12" y2="3"></line></svg>
      </button>
    </div>\n    """

content = sidebar_head_pattern.sub(new_sidebar_head, content)

# 5. Update initial Hero state
hero_pattern = re.compile(r'<div id="heroState">[\s\S]*?</div>\s*</div>\s*(?=<!-- Input Bar Dock)')
new_hero = """<div id="heroState">
        <div class="hero-cookie-badge">
          <span class="hero-cookie-icon">🍪</span>
        </div>
        <h2 class="hero-title" id="heroTitle">Ada yang bisa saya bantu hari ini?</h2>
        <p class="hero-desc" id="heroDesc">Mulai percakapan baru, tanyakan konsep, analisis ide, tulis kode, atau minta bantuan apa saja.</p>
        <div class="suggestions-grid" id="suggestionsGrid"></div>
      </div>
    </div>\n\n    """

content = hero_pattern.sub(new_hero, content)

# 6. Update JavaScript:
# Add modal confirm controller & wire to deleteConv and btnLogout
# Replace confirm() calls

js_modal_functions = """
// === MODAL KONFIRMASI ESTETIK ===
let modalConfirmCallback = null;

function showModalConfirm({ icon = "⚠️", title, desc, confirmText = "Lanjutkan", isDanger = true, onConfirm }){
  const modal = $("customConfirmModal");
  const iconEl = $("modalIcon");
  const iconWrap = $("modalIconWrap");
  const titleEl = $("modalTitle");
  const descEl = $("modalDesc");
  const confirmBtn = $("btnModalConfirm");

  iconEl.textContent = icon;
  titleEl.textContent = title;
  descEl.textContent = desc;
  confirmBtn.textContent = confirmText;

  if(isDanger){
    iconWrap.className = "custom-modal-icon-wrap";
    confirmBtn.className = "btn-modal-confirm";
  } else {
    iconWrap.className = "custom-modal-icon-wrap logout";
    confirmBtn.className = "btn-modal-confirm logout";
  }

  modalConfirmCallback = onConfirm;
  modal.classList.remove("hidden");
}

function hideModalConfirm(){
  const modal = $("customConfirmModal");
  if(modal) modal.classList.add("hidden");
  modalConfirmCallback = null;
}

$("btnModalCancel").onclick = hideModalConfirm;
$("btnModalConfirm").onclick = () => {
  if(modalConfirmCallback) modalConfirmCallback();
  hideModalConfirm();
};
"""

content = content.replace("const $ = id => document.getElementById(id);", "const $ = id => document.getElementById(id);" + js_modal_functions)

# Update deleteConv to use showModalConfirm
old_delete_conv = re.compile(r'async function deleteConv\(id\)\{[\s\S]*?if\(confirm\("Hapus obrolan ini\?"\)\)\{[\s\S]*?\}\s*\}')
new_delete_conv = """async function deleteConv(id){
  showModalConfirm({
    icon: "🗑️",
    title: "Hapus Obrolan?",
    desc: "Percakapan ini akan dihapus secara permanen dan tidak dapat dipulihkan.",
    confirmText: "Hapus",
    isDanger: true,
    onConfirm: async () => {
      if(!db || uid === "dev-mode"){
        delete devConvs[id];
        localStorage.setItem("oreo_dev_convs", JSON.stringify(devConvs));
      } else {
        await convsRef().doc(id).delete();
      }
      if(convId === id) newChat();
      else loadConvs();
    }
  });
}"""

content = old_delete_conv.sub(new_delete_conv, content)

# Update btnLogout to use showModalConfirm
old_logout = re.compile(r'\$\("btnLogout"\)\.onclick\s*=\s*\(\)\s*=>\s*\{[\s\S]*?uid\s*=\s*null;\s*idToken\s*=\s*null;[\s\S]*?\};')
new_logout = """$("btnLogout").onclick = () => {
  showModalConfirm({
    icon: "🚪",
    title: "Keluar dari Akun?",
    desc: "Anda akan keluar dari sesi Oreo AI. Anda dapat masuk kembali dengan akun Google Anda kapan saja.",
    confirmText: "Ya, Keluar",
    isDanger: false,
    onConfirm: () => {
      if(auth) auth.signOut();
      uid = null; idToken = null;
      $("loginBox").style.display="flex"; $("main").style.display="none";
      $("btnAuth").style.display="inline"; $("btnLogout").style.display="none";
      $("userName").textContent="Tamu";
      $("userAvatar").textContent="?";
    }
  });
};"""

content = old_logout.sub(new_logout, content)

# Update loadModels to place admin badge into adminBadgeWrap cleanly
old_admin_append = 'document.querySelector(".brand").appendChild(badge);'
new_admin_append = 'const wrap = document.getElementById("adminBadgeWrap"); if(wrap){ wrap.innerHTML = ""; wrap.appendChild(badge); } else { document.querySelector(".brand").appendChild(badge); }'
content = content.replace(old_admin_append, new_admin_append)

# Clean up metaBar in addMsg (remove connector buttons)
old_metabar_block = re.compile(r'let connBtnsHtml = "";[\s\S]*?metaBar\.innerHTML = `[\s\S]*?\${connBtnsHtml}[\s\S]*?`;')
new_metabar_block = """metaBar.innerHTML = `
      <span>⚡ ${meta}</span>
      <button class="btn-copy-msg" onclick="copyText(this, ${JSON.stringify(text)})">📋 Salin</button>
    `;"""
content = old_metabar_block.sub(new_metabar_block, content)

# Update createHeroElement & renderHeroSuggestions to use neutral ChatGPT/Gemini style
old_hero_funcs = re.compile(r'const HERO_SUGGESTIONS = [\s\S]*?setTimeout\(\(\) => renderHeroSuggestions\(\), 10\);\s*return hero;\s*\}')
new_hero_funcs = """const HERO_SUGGESTIONS = [
  { head: "💡 Jelaskan Konsep", sub: "Komputasi kuantum dalam bahasa sederhana", prompt: "Jelaskan konsep komputasi kuantum secara sederhana dengan analogi yang mudah dipahami pemula." },
  { head: "💻 Koding & Debugging", sub: "Bantu arsitektur API atau script", prompt: "Buatkan contoh arsitektur REST API modern dengan otentikasi aman dan best practices." },
  { head: "✍️ Tulis & Rangkum", sub: "Draf tulisan profesional atau ringkasan", prompt: "Bantu buatkan draf pesan profesional yang padat, persuasif, dan terstruktur rapi." },
  { head: "🎨 Ide & Desain Kreatif", sub: "Konsep visual, palet warna, atau layout", prompt: "Berikan konsep visual kreatif lengkap dengan rekomendasi palet warna HEX dan ide tata letak yang estetik." }
];

function renderHeroSuggestions(){
  const grid = $("suggestionsGrid");
  if(!grid) return;
  grid.innerHTML = "";

  if($("heroTitle")){
    $("heroTitle").textContent = "Ada yang bisa saya bantu hari ini?";
  }
  if($("heroDesc")){
    $("heroDesc").textContent = "Mulai percakapan baru, tanyakan konsep, analisis ide, tulis kode, atau minta bantuan apa saja.";
  }

  HERO_SUGGESTIONS.forEach(s => {
    const card = document.createElement("div");
    card.className = "sug-card";
    card.innerHTML = `
      <span class="sug-head">${escapeHtml(s.head)}</span>
      <span class="sug-sub">${escapeHtml(s.sub)}</span>
    `;
    card.onclick = () => useSuggestion(s.prompt);
    grid.appendChild(card);
  });
}

function createHeroElement(){
  const hero = document.createElement("div");
  hero.id = "heroState";
  hero.innerHTML = `
    <div class="hero-cookie-badge">
      <span class="hero-cookie-icon">🍪</span>
    </div>
    <h2 class="hero-title" id="heroTitle">Ada yang bisa saya bantu hari ini?</h2>
    <p class="hero-desc" id="heroDesc">Mulai percakapan baru, tanyakan konsep, analisis ide, tulis kode, atau minta bantuan apa saja.</p>
    <div class="suggestions-grid" id="suggestionsGrid"></div>
  `;
  setTimeout(() => renderHeroSuggestions(), 10);
  return hero;
}"""

content = old_hero_funcs.sub(new_hero_funcs, content)

with open("frontend/index.html", "w", encoding="utf-8") as f:
    f.write(content)

print("Applied UI upgrade successfully!")
