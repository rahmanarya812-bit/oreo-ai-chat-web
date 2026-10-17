// Cloudflare Worker backend for Oreo AI Chat
// Handles /api/* routes directly on Cloudflare edge CDN

const PROVIDERS = {
  "clouvia": {
    "label": "Clouvia",
    "base_url": "https://router.clouvia.id/v1",
    "key": "clv_live_w0cGiOa6hU2i8RThgDfe8Msp9yH4RZByV9maSBjYH1P",
    "models": [
      "gpt-6.1-sol",
      "gpt-6-sol",
      "gpt-6-luna",
      "gpt-6-astra",
      "gpt-5.6-luna",
      "gpt-5.6-terra",
      "gpt-5.6-sol",
      "gpt-5.5",
      "gpt-5.4",
      "gpt-oss-120b-medium(xhigh)",
      "gpt-oss-120b-medium",
      "auto",
      "coding-high",
      "gemini-3.8-flash-high",
      "sonnet-4.5-thinking-agentic",
      "qwen-3.8-max-thinking-agentic",
      "qwen-3.8-Flash",
      "qwen3.7-max",
      "qwen3.7-plus",
      "glm5.3-thinking-agentic",
      "glm5.3-flash",
      "glm5.2",
      "deepseek-v4-pro",
      "deepseek-v4-flash",
      "kimi-k3",
      "kimi-k2.7-coder",
      "minimax-m3",
      "claude-opus-4.8",
      "free-model",
      "deepseek-4.1",
      "deepseek-v4.1-flash",
      "sonus",
      "coding-high-flash",
      "claude-sonnet-5-thinking-agentic",
      "claude-haiku-4.5-thinking-agentic",
      "gemini-3.8-flash-medium",
      "gemini-3.8-flash-low",
      "gemini-3.8-flash",
      "gemini-3.7-flash-high",
      "gemini-3.7-flash-medium",
      "gemini-3.7-flash-low",
      "gemini-3.6-flash-high",
      "gemini-3.6-flash-medium",
      "gemini-3.6-flash-low",
      "gemini-3.5-flash-high",
      "gemini-3-flash-agent",
      "gemini-3.5-flash-low",
      "gemini-3.5-flash-extra-low",
      "gemini-pro-agent",
      "gemini-3.1-pro-low",
      "gemini-3-flash",
      "gemini-3.5-flash-lite",
      "gemini-3.1-flash-lite",
      "gemini-2.5-flash-thinking",
      "gemini-2.5-flash",
      "gemini-2.5-flash-lite",
      "gemini-2.5-pro",
      "gemini-3.8-flash-tiered",
      "gemini-3.7-flash-tiered",
      "gemini-3.6-flash-tiered",
      "gemini-3.7-flash",
      "gemini-3.6-flash",
      "gemini-3.5-flash",
      "gemini-3.1-pro",
      "gemini-3.1-pro-high",
      "claude-opus-4.6",
      "claude-sonnet-4.6",
      "deepseek-v4-pro-v2",
      "deepseek-v4-flash-v2",
      "deepseek-v4.1-flash-v2",
      "kimi-k3-v2",
      "kimi-k2.7-v2",
      "minimax-m3-v2",
      "glm-5.3-v2",
      "glm-5.3-flash-v2",
      "glm-5.2-v2",
      "deepseek-v3.2",
      "deepseek-v3.2-volc",
      "deepseek-v3",
      "deepseek-r1",
      "deepseek-v3-0324",
      "glm-5.3-flashx",
      "glm-5.0-turbo",
      "glm-5.1",
      "glm-5v-turbo",
      "minimax-m2.7",
      "minimax-m3-pay",
      "kimi-k3-1",
      "kimi-k3-2",
      "kimi-k2.8-preview",
      "kimi-k2.6",
      "kimi-k2.5",
      "hy3",
      "hy3-preview",
      "hy3-x",
      "hy4-preview",
      "hunyuan-chat",
      "hunyuan-2.0-instruct",
      "claude-opus-5",
      "glm-5.0-turbo-v2",
      "glm-4.7",
      "minimax-m2.7-v2",
      "hy3-preview-v2",
      "deepseek-v4-pro-v3",
      "deepseek-v3.2-volc-v2",
      "agnes-3.0-flash",
      "agnes-2.5-flash",
      "agnes-2.0-flash",
      "step-5-preview"
    ]
  },
  "discovery": {
    "label": "Intern Discovery",
    "base_url": "https://discovery-api.intern-ai.org.cn/v1",
    "key": "sk-8586e07e038f21958a48dfc2f41226c6bb0ea3810a1e2c8609049e9c5f376430",
    "models": [
      "minimax-m3",
      "kimi-k2.6",
      "deepseek-v4-pro-0813",
      "deepseek-v4-flash-vision",
      "deepseek-v4-flash-0731",
      "Atria-Dawn-Preview",
      "Atria-Dawn",
      "Agents-A1",
      "intern-s2",
      "intern-decision-4b",
      "glm-5.3"
    ]
  },
  "radox": {
    "label": "Radox",
    "base_url": "https://radoxai.com/v1",
    "key": "cc_jYnRpmkOQgBBb91jJR6qULtB0gH8paGcISZmvZkmKYRsX9O0",
    "models": [
      "gpt-5.6-luna",
      "gpt-5.6-terra",
      "gpt-5.6-sol",
      "gpt-5.5-pro",
      "gpt-5.5",
      "gemini-3.6-flash",
      "claude-sonnet-5",
      "claude-mythos-preview",
      "deepseek-v4-flash-0731",
      "kimi-k3",
      "qwen3.8-max"
    ]
  },
  "codecraft": {
    "label": "CodeCraftAPI",
    "base_url": "https://codecraftapi.com/v1",
    "key": "cc_mAckDqkUAiAS0Kd8NEAVBTGMQx5xSjlnDWjEDLx2LseaqsA9",
    "models": [
      "gpt-5.6-luna",
      "gpt-5.6-terra",
      "gpt-5.6-sol",
      "gpt-5.5-pro",
      "gpt-5.5",
      "gemini-3.6-flash",
      "claude-sonnet-5",
      "claude-mythos-preview",
      "deepseek-v4-flash-0731",
      "kimi-k3",
      "qwen3.8-max"
    ]
  },
  "devora": {
    "label": "Devora",
    "base_url": "https://api.devora.my.id/v1",
    "key": "SK-DEVORA-qckap1jfb01xw305j195ahsu3a3lzvjc",
    "models": [
      "devora-01/stealth/space-bunny",
      "devora-01/stealth/dvr-v0.1-fp8",
      "devora-01/grok-cli/grok-4.7",
      "devora-01/deepseek/deepseek-v4-pro-0813",
      "devora-01/deepseek/deepseek-v4.1-flash",
      "devora-01/deepseek/deepseek-v4-pro",
      "devora-01/zai/glm-5.2",
      "devora-01/zai/glm-5.3-flash",
      "devora-01/xiaomi-mimo/mimo-v2.6-flash"
    ]
  },
  "atria": {
    "label": "Atria",
    "base_url": "https://api.atria-asi.ai/v1",
    "key": "atr_yni3zdvrjiJEwXPDRrr4k2h-S875DSd5",
    "models": [
      "Atria-Dawn",
      "Atria-Dawn-Preview"
    ]
  }
};
const MODEL_TO_PROVIDER = {
  "gpt-6.1-sol": "clouvia",
  "gpt-6-sol": "clouvia",
  "gpt-6-luna": "clouvia",
  "gpt-6-astra": "clouvia",
  "gpt-5.6-luna": "codecraft",
  "gpt-5.6-terra": "codecraft",
  "gpt-5.6-sol": "codecraft",
  "gpt-5.5": "codecraft",
  "gpt-5.4": "clouvia",
  "gpt-oss-120b-medium(xhigh)": "clouvia",
  "gpt-oss-120b-medium": "clouvia",
  "auto": "clouvia",
  "coding-high": "clouvia",
  "gemini-3.8-flash-high": "clouvia",
  "sonnet-4.5-thinking-agentic": "clouvia",
  "qwen-3.8-max-thinking-agentic": "clouvia",
  "qwen-3.8-Flash": "clouvia",
  "qwen3.7-max": "clouvia",
  "qwen3.7-plus": "clouvia",
  "glm5.3-thinking-agentic": "clouvia",
  "glm5.3-flash": "clouvia",
  "glm5.2": "clouvia",
  "deepseek-v4-pro": "clouvia",
  "deepseek-v4-flash": "clouvia",
  "kimi-k3": "codecraft",
  "kimi-k2.7-coder": "clouvia",
  "minimax-m3": "discovery",
  "claude-opus-4.8": "clouvia",
  "free-model": "clouvia",
  "deepseek-4.1": "clouvia",
  "deepseek-v4.1-flash": "clouvia",
  "sonus": "clouvia",
  "coding-high-flash": "clouvia",
  "claude-sonnet-5-thinking-agentic": "clouvia",
  "claude-haiku-4.5-thinking-agentic": "clouvia",
  "gemini-3.8-flash-medium": "clouvia",
  "gemini-3.8-flash-low": "clouvia",
  "gemini-3.8-flash": "clouvia",
  "gemini-3.7-flash-high": "clouvia",
  "gemini-3.7-flash-medium": "clouvia",
  "gemini-3.7-flash-low": "clouvia",
  "gemini-3.6-flash-high": "clouvia",
  "gemini-3.6-flash-medium": "clouvia",
  "gemini-3.6-flash-low": "clouvia",
  "gemini-3.5-flash-high": "clouvia",
  "gemini-3-flash-agent": "clouvia",
  "gemini-3.5-flash-low": "clouvia",
  "gemini-3.5-flash-extra-low": "clouvia",
  "gemini-pro-agent": "clouvia",
  "gemini-3.1-pro-low": "clouvia",
  "gemini-3-flash": "clouvia",
  "gemini-3.5-flash-lite": "clouvia",
  "gemini-3.1-flash-lite": "clouvia",
  "gemini-2.5-flash-thinking": "clouvia",
  "gemini-2.5-flash": "clouvia",
  "gemini-2.5-flash-lite": "clouvia",
  "gemini-2.5-pro": "clouvia",
  "gemini-3.8-flash-tiered": "clouvia",
  "gemini-3.7-flash-tiered": "clouvia",
  "gemini-3.6-flash-tiered": "clouvia",
  "gemini-3.7-flash": "clouvia",
  "gemini-3.6-flash": "codecraft",
  "gemini-3.5-flash": "clouvia",
  "gemini-3.1-pro": "clouvia",
  "gemini-3.1-pro-high": "clouvia",
  "claude-opus-4.6": "clouvia",
  "claude-sonnet-4.6": "clouvia",
  "deepseek-v4-pro-v2": "clouvia",
  "deepseek-v4-flash-v2": "clouvia",
  "deepseek-v4.1-flash-v2": "clouvia",
  "kimi-k3-v2": "clouvia",
  "kimi-k2.7-v2": "clouvia",
  "minimax-m3-v2": "clouvia",
  "glm-5.3-v2": "clouvia",
  "glm-5.3-flash-v2": "clouvia",
  "glm-5.2-v2": "clouvia",
  "deepseek-v3.2": "clouvia",
  "deepseek-v3.2-volc": "clouvia",
  "deepseek-v3": "clouvia",
  "deepseek-r1": "clouvia",
  "deepseek-v3-0324": "clouvia",
  "glm-5.3-flashx": "clouvia",
  "glm-5.0-turbo": "clouvia",
  "glm-5.1": "clouvia",
  "glm-5v-turbo": "clouvia",
  "minimax-m2.7": "clouvia",
  "minimax-m3-pay": "clouvia",
  "kimi-k3-1": "clouvia",
  "kimi-k3-2": "clouvia",
  "kimi-k2.8-preview": "clouvia",
  "kimi-k2.6": "discovery",
  "kimi-k2.5": "clouvia",
  "hy3": "clouvia",
  "hy3-preview": "clouvia",
  "hy3-x": "clouvia",
  "hy4-preview": "clouvia",
  "hunyuan-chat": "clouvia",
  "hunyuan-2.0-instruct": "clouvia",
  "claude-opus-5": "clouvia",
  "glm-5.0-turbo-v2": "clouvia",
  "glm-4.7": "clouvia",
  "minimax-m2.7-v2": "clouvia",
  "hy3-preview-v2": "clouvia",
  "deepseek-v4-pro-v3": "clouvia",
  "deepseek-v3.2-volc-v2": "clouvia",
  "agnes-3.0-flash": "clouvia",
  "agnes-2.5-flash": "clouvia",
  "agnes-2.0-flash": "clouvia",
  "step-5-preview": "clouvia",
  "deepseek-v4-pro-0813": "discovery",
  "deepseek-v4-flash-vision": "discovery",
  "deepseek-v4-flash-0731": "codecraft",
  "Atria-Dawn-Preview": "atria",
  "Atria-Dawn": "atria",
  "Agents-A1": "discovery",
  "intern-s2": "discovery",
  "intern-decision-4b": "discovery",
  "glm-5.3": "discovery",
  "gpt-5.5-pro": "codecraft",
  "claude-sonnet-5": "codecraft",
  "claude-mythos-preview": "codecraft",
  "qwen3.8-max": "codecraft",
  "devora-01/stealth/space-bunny": "devora",
  "devora-01/stealth/dvr-v0.1-fp8": "devora",
  "devora-01/grok-cli/grok-4.7": "devora",
  "devora-01/deepseek/deepseek-v4-pro-0813": "devora",
  "devora-01/deepseek/deepseek-v4.1-flash": "devora",
  "devora-01/deepseek/deepseek-v4-pro": "devora",
  "devora-01/zai/glm-5.2": "devora",
  "devora-01/zai/glm-5.3-flash": "devora",
  "devora-01/xiaomi-mimo/mimo-v2.6-flash": "devora"
};
const PERSONAS = {
  "canva": {
    "id": "canva",
    "name": "Canva Creative Specialist",
    "icon": "\ud83c\udfa8",
    "tagline": "Pakar Desain & Konsep Visual Canva",
    "description": "Merancang konsep visual, palet warna HEX, font Canva, layout, dan elemen grafis.",
    "system_prompt": "Kamu adalah Pakar Desain Grafis & Konsultan Kreatif Canva (Canva Creative Specialist). Keahlian utamamu adalah merancang konsep visual yang memukau untuk media sosial (Instagram feed/carousel/story, TikTok, YouTube thumbnail), poster promo, banner iklan, presentasi, dan branding.\n\nSetiap memberikan rekomendasi desain, susun jawabanmu dengan format rapi dan menarik:\n1. \ud83c\udfaf **Konsep Visual & Mood**: Tema gaya visual (misal: Minimalis Elegan, Cyberpunk, Bold & Energetic, Pastel Aesthetic, dsb).\n2. \ud83c\udfa8 **Palet Warna Harmonis (HEX)**: Cantumkan 3-5 kode warna HEX (contoh: `#1E293B`, `#6366F1`) beserta peruntukannya (Latar belakang, Teks utama, Aksen/Tombol).\n3. \ud83d\udd24 **Tipografi / Font Canva**: Rekomendasi font judul dan font isi yang tersedia di Canva (misal: *Montserrat Extra Bold* untuk Judul + *Open Sans* untuk Isi).\n4. \u270d\ufe0f **Headline & Copy Naskah**: Teks judul yang memancing perhatian (hook) dan kalimat ajakan tindakan (CTA) yang efektif.\n5. \ud83d\udcd0 **Tata Letak (Layout) & Kata Kunci Elemen Canva**: Panduan komposisi dan kata kunci pencarian grafis/elemen di Canva (misal: 'abstract gradient blob', '3d geometric badge').\n\nGunakan bahasa Indonesia yang kreatif, antusias, dan profesional."
  },
  "developer": {
    "id": "developer",
    "name": "Fullstack Software Architect",
    "icon": "\ud83d\udcbb",
    "tagline": "Senior Software Engineer & Arsitek Sistem",
    "description": "Menulis kode bersih, debugging error, arsitektur backend/frontend, dan optimasi performa.",
    "system_prompt": "Kamu adalah Senior Fullstack Software Architect kelas dunia. Keahlianmu adalah memecahkan masalah koding, menyusun arsitektur sistem yang skalabel, dan menulis kode yang bersih, aman, efisien, serta terdokumentasi dengan baik. Gunakan standar industri modern. Sertakan blok kode lengkap dengan sintaks yang tepat, dan jelaskan langkah-langkah pentingnya secara sistematis."
  },
  "copywriter": {
    "id": "copywriter",
    "name": "Viral Copywriter & Marketer",
    "icon": "\u270d\ufe0f",
    "tagline": "Pakar Copywriting Persuasif & Konten Viral",
    "description": "Membuat hook konten, copywriting formula AIDA/PAS, caption medsos, dan email penjualan.",
    "system_prompt": "Kamu adalah Copywriter Profesional & Digital Marketing Strategist berpengalaman. Kamu mahir menyusun pesan pemasaran yang menggugah emosi, persuasif, dan menghasilkan konversi tinggi menggunakan formula copywriting (seperti AIDA, PAS, BAB). Fokus pada hook pembuka yang kuat, copywriting yang mengalir, dan Call to Action (CTA) yang tegas."
  },
  "analyst": {
    "id": "analyst",
    "name": "Business & Data Strategist",
    "icon": "\ud83d\udcca",
    "tagline": "Konsultan Strategi Bisnis & Analisis Data",
    "description": "Merumuskan strategi bisnis, analisis peluang pasar, KPI, dan evaluasi logis.",
    "system_prompt": "Kamu adalah Senior Business & Data Strategist. Keahlianmu adalah menganalisis situasi bisnis, merumuskan model monetisasi, mengidentifikasi peluang pasar, menetapkan metrik KPI yang jelas, dan menyusun laporan eksekutif terstruktur dengan rekomendasi yang actionable."
  },
  "general": {
    "id": "general",
    "name": "Asisten Cerdas Serbaguna",
    "icon": "\u2728",
    "tagline": "Mode Standar Cerdas & Cepat",
    "description": "Mode serbaguna pintar untuk percakapan umum, riset, penjelasan konsep, dan tugas sehari-hari.",
    "system_prompt": "Kamu adalah Oreo AI, asisten kecerdasan buatan serbaguna yang ramah, berwawasan luas, akurat, dan sangat membantu. Berikan jawaban yang jelas, terstruktur rapi dengan markdown, dan mudah dipahami."
  }
};

const CORS_HEADERS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type, Authorization, X-Client-Id',
};

function jsonResp(data, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: {
      'Content-Type': 'application/json',
      ...CORS_HEADERS
    }
  });
}

// In-memory quota storage (persists while worker instance is warm)
const quotaStore = new Map();
const DAILY_LIMIT = 30;

function getTodayStr() {
  const now = new Date();
  return now.toISOString().slice(0, 10);
}

function getUserQuota(userKey) {
  const today = getTodayStr();
  let entry = quotaStore.get(userKey);
  if (!entry || entry.date !== today) {
    entry = { date: today, count: 0 };
    quotaStore.set(userKey, entry);
  }
  const used = entry.count;
  const remaining = Math.max(0, DAILY_LIMIT - used);
  return {
    user_id: userKey,
    date: today,
    limit: DAILY_LIMIT,
    used,
    remaining,
    is_unlimited: false,
    is_exceeded: used >= DAILY_LIMIT
  };
}

function consumeQuota(userKey) {
  const quota = getUserQuota(userKey);
  if (quota.is_exceeded) {
    return {
      allowed: false,
      quota,
      error: `Batas kuota harian (${DAILY_LIMIT} pesan/hari) sudah tercapai! Kuota di-reset otomatis setiap hari (00:00).`
    };
  }
  const entry = quotaStore.get(userKey);
  entry.count += 1;
  const updatedQuota = getUserQuota(userKey);
  return { allowed: true, quota: updatedQuota, error: null };
}

function resetQuota(userKey) {
  const today = getTodayStr();
  quotaStore.set(userKey, { date: today, count: 0 });
  return getUserQuota(userKey);
}

function getUserKey(request) {
  const authHeader = request.headers.get('Authorization') || '';
  const token = authHeader.replace(/^Bearer\s+/i, '').trim();
  const clientId = request.headers.get('X-Client-Id') || '';
  if (token && token !== 'dev-token') {
    return 'user:' + token.slice(-16);
  }
  if (clientId) {
    return 'client:' + clientId;
  }
  return 'ip:' + (request.headers.get('cf-connecting-ip') || 'unknown');
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    // Handle CORS preflight
    if (request.method === 'OPTIONS') {
      return new Response(null, { status: 204, headers: CORS_HEADERS });
    }

    // API Routes
    if (url.pathname === '/api/models') {
      const out = [];
      let total = 0;
      for (const [pkey, p] of Object.entries(PROVIDERS)) {
        out.push({ provider: pkey, label: p.label, models: p.models });
        total += p.models.length;
      }
      return jsonResp({ total, providers: out, admin: true });
    }

    if (url.pathname === '/api/health') {
      let total = 0;
      for (const p of Object.values(PROVIDERS)) total += p.models.length;
      return jsonResp({ ok: true, models: total, server: 'Cloudflare Worker' });
    }

    if (url.pathname === '/api/personas') {
      const pList = Object.values(PERSONAS).map(p => ({
        id: p.id,
        name: p.name,
        icon: p.icon,
        tagline: p.tagline,
        description: p.description
      }));
      return jsonResp({ ok: true, personas: pList });
    }

    if (url.pathname === '/api/quota') {
      const userKey = getUserKey(request);
      return jsonResp({ ok: true, quota: getUserQuota(userKey) });
    }

    if (url.pathname === '/api/quota/reset' && request.method === 'POST') {
      const userKey = getUserKey(request);
      return jsonResp({ ok: true, quota: resetQuota(userKey), message: 'Kuota harian berhasil di-reset!' });
    }

    if (url.pathname === '/api/me') {
      const userKey = getUserKey(request);
      return jsonResp({ ok: true, uid: userKey, admin: true, quota: getUserQuota(userKey) });
    }

    if (url.pathname === '/api/oauth/canva/status') {
      return jsonResp({
        ok: true,
        canva: {
          connected: true,
          connected_at: 'Aktif',
          client_id: 'oreo-ai-hub',
          user_id: 'arya-canva'
        }
      });
    }

    if (url.pathname === '/api/oauth/canva/disconnect' && request.method === 'POST') {
      return jsonResp({ ok: true, message: 'Akun Canva berhasil diputus' });
    }

    if (url.pathname === '/api/connectors/test-webhook' && request.method === 'POST') {
      try {
        const body = await request.json();
        const webhookUrl = (body.webhook_url || '').trim();
        if (!webhookUrl) {
          return jsonResp({ ok: false, error: 'URL Webhook belum diisi' }, 400);
        }
        const t0 = Date.now();
        const r = await fetch(webhookUrl, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', 'User-Agent': 'OreoAI-Hub/1.0' },
          body: JSON.stringify({ event: 'ping', source: 'oreo_ai_chat', time: Date.now() })
        });
        const elapsed = ((Date.now() - t0) / 1000).toFixed(2);
        return jsonResp({
          ok: r.ok,
          status_code: r.status,
          elapsed,
          message: `Webhook merespons HTTP ${r.status} dalam ${elapsed}s`
        });
      } catch (e) {
        return jsonResp({ ok: false, error: 'Gagal menghubungi webhook: ' + e.message }, 502);
      }
    }

    if (url.pathname === '/api/connectors/dispatch' && request.method === 'POST') {
      try {
        const body = await request.json();
        const appId = body.app || 'canva';
        const action = body.action || 'execute';
        const payload = body.payload || {};
        const webhookUrl = (body.webhook_url || '').trim();

        if (webhookUrl) {
          const r = await fetch(webhookUrl, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', 'User-Agent': 'OreoAI-Hub/1.0' },
            body: JSON.stringify({ app: appId, action, payload, timestamp: Date.now() })
          });
          let resData;
          try { resData = await r.json(); } catch (_) { resData = { raw_text: await r.text() }; }
          return jsonResp({
            ok: r.ok,
            real_n8n: true,
            status_code: r.status,
            app: appId,
            action,
            data: resData
          });
        }

        // Smart Simulation response
        let resultObj = { message: `Aksi ${action} pada ${appId} berhasil diproses.` };
        if (appId === 'canva') {
          const query = encodeURIComponent(payload.template || payload.query || 'Instagram Post');
          resultObj = {
            message: `Desain konsep Canva siap dibuka dan diedit langsung.`,
            action_url: `https://www.canva.com/search?q=${query}`,
            action_label: 'Buka Desain di Canva'
          };
        } else if (appId === 'gmail') {
          resultObj = {
            message: `Draf email untuk '${payload.subject || 'Pesan Baru'}' telah disiapkan.`,
            action_url: 'https://mail.google.com',
            action_label: 'Buka Gmail'
          };
        } else if (appId === 'github') {
          resultObj = {
            message: `Kode repositori siap disinkronkan.`,
            action_url: 'https://github.com',
            action_label: 'Buka GitHub'
          };
        }
        return jsonResp({ ok: true, app: appId, action, result: resultObj });
      } catch (e) {
        return jsonResp({ ok: false, error: e.message }, 500);
      }
    }

    if (url.pathname === '/api/image' && request.method === 'POST') {
      try {
        const body = await request.json();
        const prompt = (body.prompt || '').trim();
        const aspectRatio = body.aspect_ratio || '1:1';
        if (!prompt) {
          return jsonResp({ ok: false, error: 'Deskripsi gambar tidak boleh kosong' }, 400);
        }

        const userKey = getUserKey(request);
        const quotaCheck = consumeQuota(userKey);
        if (!quotaCheck.allowed) {
          return jsonResp({
            ok: false,
            error: quotaCheck.error,
            quota_exceeded: true,
            quota: quotaCheck.quota
          }, 429);
        }

        // Resolusi berdasarkan Rasio Aspek
        let width = 1024, height = 1024;
        if (aspectRatio === '9:16') {
          width = 720; height = 1280;
        } else if (aspectRatio === '3:4') {
          width = 768; height = 1024;
        } else if (aspectRatio === '4:3') {
          width = 1024; height = 768;
        } else if (aspectRatio === '16:9') {
          width = 1280; height = 720;
        }

        const seed = Math.floor(Math.random() * 1000000000);
        const encodedPrompt = encodeURIComponent(prompt);
        // Engine AI image Flux beresolusi tinggi via Pollinations
        const imageUrl = `https://image.pollinations.ai/prompt/${encodedPrompt}?width=${width}&height=${height}&seed=${seed}&nologo=true&model=flux`;

        const t0 = Date.now();
        const elapsed = "1.5";

        return jsonResp({
          ok: true,
          is_image: true,
          image_url: imageUrl,
          prompt,
          aspect_ratio: aspectRatio,
          width,
          height,
          seed,
          model: 'Imagen 3 / Flux AI',
          content: `Berikut adalah karya gambar yang dihasilkan dari deskripsi Anda:\n\n**"${prompt}"**\n\n![${prompt}](${imageUrl})\n\n*Rasio: ${aspectRatio} (${width}×${height}px) • Model: Imagen / Flux AI*`,
          elapsed,
          quota: quotaCheck.quota
        });
      } catch (e) {
        return jsonResp({ ok: false, error: 'Gagal membuat gambar: ' + e.message }, 500);
      }
    }

    if (url.pathname === '/api/chat' && request.method === 'POST') {
      try {
        const body = await request.json();
        const model = body.model || '';
        const messages = body.messages || [];
        const personaKey = body.persona || 'general';
        const connectedApps = body.connected_apps || [];

        if (!model || !messages.length) {
          return jsonResp({ ok: false, error: 'Model atau pesan tidak boleh kosong' }, 400);
        }

        const userKey = getUserKey(request);
        const quotaCheck = consumeQuota(userKey);
        if (!quotaCheck.allowed) {
          return jsonResp({
            ok: false,
            error: quotaCheck.error,
            quota_exceeded: true,
            quota: quotaCheck.quota
          }, 429);
        }

        const providerKey = MODEL_TO_PROVIDER[model] || 'clouvia';
        const provider = PROVIDERS[providerKey] || PROVIDERS.clouvia;
        let userPromptText = "";
        for (let i = messages.length - 1; i >= 0; i--) {
          if (messages[i].role === 'user') {
            const c = messages[i].content;
            if (typeof c === 'string') userPromptText = c;
            else if (Array.isArray(c)) {
              const t = c.find(item => item.type === 'text');
              if (t) userPromptText = t.text;
            }
            break;
          }
        }
        const lowerPrompt = userPromptText.toLowerCase();

        let sysPrompt = "";
        let detectedPersona = personaKey;
        if (personaKey && personaKey !== 'auto' && PERSONAS[personaKey]) {
          sysPrompt = PERSONAS[personaKey].system_prompt;
        } else {
          // Dynamic adaptive persona detection based on user query
          if (/(canva|desain|design|feed|banner|poster|logo|palet|warna|hex|layout|carousel|thumbnail|tipografi|font canva|grafis|flyer|brosur|kemasan)/i.test(lowerPrompt)) {
            sysPrompt = PERSONAS.canva.system_prompt;
            detectedPersona = "canva";
          } else if (/(koding|coding|code|script|python|javascript|typescript|html|css|php|sql|api|function|bug|debug|error|class|git|react|fastapi|backend|frontend|query|endpoint|server)/i.test(lowerPrompt)) {
            sysPrompt = PERSONAS.developer.system_prompt;
            detectedPersona = "developer";
          } else if (/(copywriting|copywriter|caption|iklan|hook|aida|headline|naskah|promo|sales|penjualan|slogan|tagline|cta|reels|tiktok)/i.test(lowerPrompt)) {
            sysPrompt = PERSONAS.copywriter.system_prompt;
            detectedPersona = "copywriter";
          } else if (/(bisnis|strategi|analis|kpi|pasar|roi|revenue|monetisasi|investor|pitch deck|finansial|omset|swot)/i.test(lowerPrompt)) {
            sysPrompt = PERSONAS.analyst.system_prompt;
            detectedPersona = "analyst";
          } else {
            sysPrompt = `Kamu adalah Oreo AI, asisten kecerdasan buatan serbaguna yang ramah, berwawasan luas, akurat, dan sangat membantu. Secara cerdas sesuaikan keahlian dan gaya jawabanmu dengan apa yang diminta oleh pengguna (Desain Canva, Koding, Copywriting, Bisnis, atau Percakapan Umum) dengan format markdown yang rapi, terstruktur, dan mudah dipahami.`;
            detectedPersona = "general";
          }
        }

        if (connectedApps.length > 0) {
          sysPrompt += `\n\n[Konektor Aplikasi Aktif]: Pengguna telah mengaktifkan integrasi dengan: ${connectedApps.join(', ')}. Berikan rekomendasi konten dan instruksi yang siap diintegrasikan atau dibuka di aplikasi tersebut.`;
        }

        const augmentedMessages = [];
        const hasSystem = messages.some(m => m.role === 'system');
        if (!hasSystem) {
          augmentedMessages.push({ role: 'system', content: sysPrompt });
        }
        for (const m of messages) {
          augmentedMessages.push({ role: m.role, content: m.content });
        }

        const t0 = Date.now();
        const apiResp = await fetch(provider.base_url + '/chat/completions', {
          method: 'POST',
          headers: {
            'Authorization': 'Bearer ' + provider.key,
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
          },
          body: JSON.stringify({
            model,
            messages: augmentedMessages,
            max_tokens: body.max_tokens || 2000,
            temperature: 0.7
          })
        });

        if (!apiResp.ok) {
          let errBody = '';
          try { errBody = await apiResp.text(); } catch (_) {}
          return jsonResp({
            ok: false,
            error: `Penyedia AI (${provider.label} HTTP ${apiResp.status}): ${errBody.slice(0, 200)}`,
            quota: quotaCheck.quota
          }, 502);
        }

        const apiData = await apiResp.json();
        let content = '';
        if (apiData.choices && apiData.choices[0] && apiData.choices[0].message) {
          content = apiData.choices[0].message.content || apiData.choices[0].message.reasoning_content || '';
        }

        const elapsed = ((Date.now() - t0) / 1000).toFixed(1);
        return jsonResp({
          ok: true,
          content: content || 'Tidak ada konten respons dari model.',
          model,
          provider: providerKey,
          persona: detectedPersona,
          elapsed,
          quota: quotaCheck.quota
        });
      } catch (e) {
        return jsonResp({ ok: false, error: 'Worker error: ' + e.message }, 500);
      }
    }

    // Fallback: serve frontend assets (static files)
    if (env && env.ASSETS) {
      return env.ASSETS.fetch(request);
    }

    return new Response('Not found', { status: 404 });
  }
};
