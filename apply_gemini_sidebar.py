import re

with open("frontend/index.html", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update CSS with Google Gemini Sidebar Styles
gemini_sidebar_css = """
/* === Google Gemini Signature Sidebar Styling (Image 2) === */
#sidebar {
  width: 270px;
  background: #131316;
  border-right: 1px solid rgba(255, 255, 255, 0.06);
  display: flex;
  flex-direction: column;
  transition: margin-left 0.25s cubic-bezier(0.2, 0, 0, 1);
  z-index: 30;
  user-select: none;
}
#sidebar.collapsed {
  margin-left: -270px;
}

.gemini-sidebar-header {
  padding: 16px 16px 12px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
}
.gemini-brand {
  display: flex;
  align-items: center;
  gap: 10px;
}
.gemini-cookie-icon {
  font-size: 22px;
  line-height: 1;
}
.gemini-brand-title {
  font-size: 17px;
  font-weight: 600;
  letter-spacing: -0.3px;
  color: #e3e3e3;
}
.gemini-header-btn {
  background: transparent;
  border: none;
  color: #c4c7c5;
  width: 34px;
  height: 34px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: background 0.15s, color 0.15s;
}
.gemini-header-btn:hover {
  background: rgba(255, 255, 255, 0.08);
  color: #ffffff;
}

.gemini-nav-group {
  padding: 6px 12px 14px;
  display: flex;
  flex-direction: column;
  gap: 4px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}
.gemini-nav-row {
  width: 100%;
  background: transparent;
  border: none;
  color: #c4c7c5;
  padding: 10px 16px;
  border-radius: 24px;
  font-size: 13.5px;
  font-weight: 500;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 14px;
  text-align: left;
  transition: all 0.15s ease;
  font-family: inherit;
}
.gemini-nav-row:hover {
  background: #23252a;
  color: #ffffff;
}
.gemini-nav-row.active {
  background: #282a2f;
  color: #ffffff;
}
.gemini-nav-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  color: inherit;
  flex-shrink: 0;
}
.gemini-nav-text {
  flex: 1;
  letter-spacing: -0.1px;
}

.gemini-section-header {
  padding: 16px 18px 8px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.gemini-section-heading {
  font-size: 12px;
  font-weight: 600;
  color: #8e918f;
  letter-spacing: 0.3px;
}
.gemini-funnel-icon {
  color: #8e918f;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  padding: 4px;
  border-radius: 4px;
  transition: color 0.15s;
}
.gemini-funnel-icon:hover {
  color: #e3e3e3;
}

.gemini-conv-list {
  flex: 1;
  overflow-y: auto;
  padding: 4px 10px 14px;
  display: flex;
  flex-direction: column;
  gap: 2px;
}
.gemini-conv-list::-webkit-scrollbar {
  width: 5px;
}
.gemini-conv-list::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 4px;
}

.conv-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 9px 14px;
  border-radius: 20px;
  font-size: 13.5px;
  color: #c4c7c5;
  cursor: pointer;
  transition: all 0.15s ease;
  position: relative;
  text-align: left;
}
.conv-item:hover {
  background: #23252a;
  color: #ffffff;
}
.conv-item.active {
  background: #282a2f;
  color: #ffffff;
  font-weight: 500;
}
.conv-item-icon {
  color: #8e918f;
  display: flex;
  align-items: center;
  flex-shrink: 0;
}
.conv-item.active .conv-item-icon {
  color: #ffffff;
}
.conv-title {
  flex: 1;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  letter-spacing: -0.1px;
}
.conv-del {
  display: none;
  color: #8e918f;
  font-size: 13px;
  width: 22px;
  height: 22px;
  border-radius: 50%;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  transition: all 0.15s;
}
.conv-item:hover .conv-del {
  display: flex;
}
.conv-del:hover {
  color: #fca5a5;
  background: rgba(239, 68, 68, 0.2);
}
"""

content = content.replace("</style>", gemini_sidebar_css + "\n</style>", 1)

# 2. Replace #sidebar HTML structure with Gemini-style HTML
old_sidebar_re = re.compile(r'<aside id="sidebar">[\s\S]*?</aside>')

new_sidebar_html = """<aside id="sidebar">
    <!-- Header Sidebar Gaya Gemini (Persis Gambar 2) -->
    <div class="gemini-sidebar-header">
      <div class="gemini-brand">
        <span class="gemini-cookie-icon">🍪</span>
        <span class="gemini-brand-title">Oreo AI</span>
        <span id="adminBadgeWrap"></span>
      </div>
      <button id="btnSidebarCollapse" class="gemini-header-btn" title="Ciutkan Menu">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
          <line x1="9" y1="3" x2="9" y2="21"></line>
        </svg>
      </button>
    </div>

    <!-- Navigasi Utama Gaya Gemini (Persis Gambar 2) -->
    <div class="gemini-nav-group">
      <!-- 1. Percakapan baru -->
      <button id="btnNew" class="gemini-nav-row active" type="button">
        <span class="gemini-nav-icon">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 20h9"></path><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"></path></svg>
        </span>
        <span class="gemini-nav-text">Percakapan baru</span>
      </button>

      <!-- 2. Gambar (Analisis Gambar / Upload) -->
      <button id="btnNavImage" class="gemini-nav-row" type="button">
        <span class="gemini-nav-icon">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect><circle cx="8.5" cy="8.5" r="1.5"></circle><polyline points="21 15 16 10 5 21"></polyline></svg>
        </span>
        <span class="gemini-nav-text">Gambar</span>
      </button>

      <!-- 3. Ekspor Riwayat -->
      <button id="btnExportChat" class="gemini-nav-row" type="button">
        <span class="gemini-nav-icon">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="7 10 12 15 17 10"></polyline><line x1="12" y1="15" x2="12" y2="3"></line></svg>
        </span>
        <span class="gemini-nav-text">Ekspor Obrolan</span>
      </button>
    </div>

    <!-- Judul Seksi Riwayat Obrolan dengan Ikon Filter -->
    <div class="gemini-section-header">
      <span class="gemini-section-heading">Riwayat Obrolan</span>
      <span class="gemini-funnel-icon" title="Riwayat Obrolan">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"></polygon>
        </svg>
      </span>
    </div>

    <!-- Daftar Obrolan -->
    <div id="convList" class="gemini-conv-list"></div>
  </aside>"""

content = old_sidebar_re.sub(new_sidebar_html, content)

# 3. Update JavaScript:
# Hook up btnSidebarCollapse and btnNavImage
js_hook = """
if($("btnSidebarCollapse")){
  $("btnSidebarCollapse").onclick = () => {
    $("sidebar").classList.toggle("collapsed");
  };
}
if($("btnNavImage")){
  $("btnNavImage").onclick = () => {
    $("fileInput").click();
  };
}
"""

content = content.replace('$("btnToggleSidebar").onclick = () => {', js_hook + '\n$("btnToggleSidebar").onclick = () => {')

# 4. Update renderConvItem to use clean SVG chat icon
old_render_conv_item = re.compile(r'function renderConvItem\(id, data\)\{[\s\S]*?el\.innerHTML = `[\s\S]*?`;[\s\S]*?\$\("convList"\)\.appendChild\(el\);\s*\}')

new_render_conv_item = """function renderConvItem(id, data){
  const el = document.createElement("div");
  el.className = "conv-item" + (id === convId ? " active" : "");
  el.innerHTML = `
    <span class="conv-item-icon">
      <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path></svg>
    </span>
    <span class="conv-title">${escapeHtml(data.title || "Obrolan baru")}</span>
    <span class="conv-del" title="Hapus chat">✕</span>
  `;
  el.onclick = (e) => {
    if(e.target.classList.contains("conv-del")){
      e.stopPropagation();
      deleteConv(id);
      return;
    }
    openConv(id, data);
  };
  $("convList").appendChild(el);
}"""

content = old_render_conv_item.sub(new_render_conv_item, content)

with open("frontend/index.html", "w", encoding="utf-8") as f:
    f.write(content)

print("Applied Gemini sidebar redesign successfully!")
