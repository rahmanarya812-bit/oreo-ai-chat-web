"""Oreo AI Chat — backend API. Deploy ke Render sebagai Web Service."""
import os, time, json
import requests
from flask import Flask, request, jsonify, send_from_directory, redirect
from flask_cors import CORS
from models import PROVIDERS, MODEL_TO_PROVIDER, TOTAL
from quota import get_user_quota, consume_quota, reset_user_quota, get_daily_limit
from oauth_canva import generate_auth_url, exchange_token, get_canva_status, disconnect_canva

FRONTEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend"))

# Muat environment variables dari .env jika ada
_env_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
if os.path.exists(_env_file):
    with open(_env_file, "r", encoding="utf-8") as _f:
        for _line in _f:
            _line = _line.strip()
            if _line and not _line.startswith("#") and "=" in _line:
                _k, _v = _line.split("=", 1)
                os.environ[_k.strip()] = _v.strip().strip('"').strip("'")

app = Flask(__name__)
CORS(app)

# Firebase Admin (opsional — aktif kalau FIREBASE_CREDENTIALS_JSON diset)
_firebase_ok = False
try:
    import firebase_admin
    from firebase_admin import auth, credentials
    _cred_json = os.environ.get("FIREBASE_CREDENTIALS_JSON", "")
    if _cred_json:
        _cred = credentials.Certificate(json.loads(_cred_json))
        firebase_admin.initialize_app(_cred)
        _firebase_ok = True
except Exception as e:
    print("[warn] firebase admin tidak aktif:", e)


def _verify_token(id_token):
    """Verifikasi Firebase ID token. Return uid atau None."""
    if not _firebase_ok or id_token == "dev-token":
        return "dev-mode"  # tanpa firebase, izinkan (untuk testing lokal)
    try:
        decoded = auth.verify_id_token(id_token)
        return decoded.get("uid")
    except Exception:
        return None


def _is_admin(uid):
    if uid == "dev-mode":
        return True
    admins = os.environ.get("ADMIN_UIDS", "").split(",")
    return uid and uid.strip() in [a.strip() for a in admins if a.strip()]


def _user_has_unlimited_quota(uid):
    """Mengecek apakah user berhak mendapatkan kuota tanpa batas (misal Admin)."""
    admins = [a.strip() for a in os.environ.get("ADMIN_UIDS", "").split(",") if a.strip()]
    if uid and uid in admins:
        return True
    if uid == "dev-mode" and os.environ.get("DEV_UNLIMITED_QUOTA", "false").lower() == "true":
        return True
    return False


def _get_identity(req):
    """
    Identifikasi user:
    - Jika login via Firebase ID Token -> user UID
    - Jika dev-mode / guest -> header X-Client-Id (ID browser unik) atau IP
    """
    authz = req.headers.get("Authorization", "")
    id_token = authz.replace("Bearer ", "").strip()
    uid = _verify_token(id_token)

    client_id = req.headers.get("X-Client-Id", "").strip()
    if uid and uid != "dev-mode":
        user_key = f"user:{uid}"
    elif client_id:
        user_key = f"client:{client_id}"
    else:
        ip = req.headers.get("X-Forwarded-For", req.remote_addr or "127.0.0.1").split(",")[0].strip()
        user_key = f"ip:{ip}"

    admin = _is_admin(uid)
    is_unlimited = _user_has_unlimited_quota(uid)
    return uid, user_key, admin, is_unlimited


PERSONAS = {
    "canva": {
        "id": "canva",
        "name": "Canva Creative Specialist",
        "icon": "🎨",
        "tagline": "Pakar Desain & Konsep Visual Canva",
        "description": "Merancang konsep visual, palet warna HEX, font Canva, layout, dan elemen grafis.",
        "system_prompt": (
            "Kamu adalah Pakar Desain Grafis & Konsultan Kreatif Canva (Canva Creative Specialist). "
            "Keahlian utamamu adalah merancang konsep visual yang memukau untuk media sosial (Instagram feed/carousel/story, TikTok, YouTube thumbnail), poster promo, banner iklan, presentasi, dan branding.\n\n"
            "Setiap memberikan rekomendasi desain, susun jawabanmu dengan format rapi dan menarik:\n"
            "1. 🎯 **Konsep Visual & Mood**: Tema gaya visual (misal: Minimalis Elegan, Cyberpunk, Bold & Energetic, Pastel Aesthetic, dsb).\n"
            "2. 🎨 **Palet Warna Harmonis (HEX)**: Cantumkan 3-5 kode warna HEX (contoh: `#1E293B`, `#6366F1`) beserta peruntukannya (Latar belakang, Teks utama, Aksen/Tombol).\n"
            "3. 🔤 **Tipografi / Font Canva**: Rekomendasi font judul dan font isi yang tersedia di Canva (misal: *Montserrat Extra Bold* untuk Judul + *Open Sans* untuk Isi).\n"
            "4. ✍️ **Headline & Copy Naskah**: Teks judul yang memancing perhatian (hook) dan kalimat ajakan tindakan (CTA) yang efektif.\n"
            "5. 📐 **Tata Letak (Layout) & Kata Kunci Elemen Canva**: Panduan komposisi dan kata kunci pencarian grafis/elemen di Canva (misal: 'abstract gradient blob', '3d geometric badge').\n\n"
            "Gunakan bahasa Indonesia yang kreatif, antusias, dan profesional."
        )
    },
    "developer": {
        "id": "developer",
        "name": "Fullstack Software Architect",
        "icon": "💻",
        "tagline": "Senior Software Engineer & Arsitek Sistem",
        "description": "Menulis kode bersih, debugging error, arsitektur backend/frontend, dan optimasi performa.",
        "system_prompt": (
            "Kamu adalah Senior Fullstack Software Architect kelas dunia. "
            "Keahlianmu adalah memecahkan masalah koding, menyusun arsitektur sistem yang skalabel, dan menulis kode yang bersih, aman, efisien, serta terdokumentasi dengan baik. "
            "Gunakan standar industri modern. Sertakan blok kode lengkap dengan sintaks yang tepat, dan jelaskan langkah-langkah pentingnya secara sistematis."
        )
    },
    "copywriter": {
        "id": "copywriter",
        "name": "Viral Copywriter & Marketer",
        "icon": "✍️",
        "tagline": "Pakar Copywriting Persuasif & Konten Viral",
        "description": "Membuat hook konten, copywriting formula AIDA/PAS, caption medsos, dan email penjualan.",
        "system_prompt": (
            "Kamu adalah Copywriter Profesional & Digital Marketing Strategist berpengalaman. "
            "Kamu mahir menyusun pesan pemasaran yang menggugah emosi, persuasif, dan menghasilkan konversi tinggi menggunakan formula copywriting (seperti AIDA, PAS, BAB). "
            "Fokus pada hook pembuka yang kuat, copywriting yang mengalir, dan Call to Action (CTA) yang tegas."
        )
    },
    "analyst": {
        "id": "analyst",
        "name": "Business & Data Strategist",
        "icon": "📊",
        "tagline": "Konsultan Strategi Bisnis & Analisis Data",
        "description": "Merumuskan strategi bisnis, analisis peluang pasar, KPI, dan evaluasi logis.",
        "system_prompt": (
            "Kamu adalah Senior Business & Data Strategist. "
            "Keahlianmu adalah menganalisis situasi bisnis, merumuskan model monetisasi, mengidentifikasi peluang pasar, menetapkan metrik KPI yang jelas, dan menyusun laporan eksekutif terstruktur dengan rekomendasi yang actionable."
        )
    },
    "general": {
        "id": "general",
        "name": "Asisten Cerdas Serbaguna",
        "icon": "✨",
        "tagline": "Mode Standar Cerdas & Cepat",
        "description": "Mode serbaguna pintar untuk percakapan umum, riset, penjelasan konsep, dan tugas sehari-hari.",
        "system_prompt": (
            "Kamu adalah Oreo AI, asisten kecerdasan buatan serbaguna yang ramah, berwawasan luas, akurat, dan sangat membantu. "
            "Berikan jawaban yang jelas, terstruktur rapi dengan markdown, dan mudah dipahami."
        )
    }
}


# Model yang boleh dipakai user biasa (admin dapat semua)
USER_MODELS = [m.strip() for m in os.environ.get(
    "USER_MODELS",
    "kimi-k2.6,deepseek-v4-flash-0731,minimax-m3,"
    "devora-01/stealth/space-bunny,devora-01/stealth/dvr-v0.1-fp8"
).split(",") if m.strip()]


def _chat(provider_key, model, messages, max_tokens=2000, temperature=0.7):
    p = PROVIDERS[provider_key]
    key = os.environ.get(p["key_env"], "").strip()
    if not key:
        user_msg = messages[-1].get("content", "") if messages else ""
        if isinstance(user_msg, list):
            user_msg = " ".join([b.get("text", "") for b in user_msg if isinstance(b, dict) and b.get("type") == "text"])
        return (
            f"[Respon Mode Tes]\n\n"
            f"✅ Backend & UI Oreo AI Chat berhasil terhubung!\n"
            f"• Model: `{model}`\n"
            f"• Pesan kamu: \"{user_msg}\"\n\n"
            f"ℹ️ (Untuk menggunakan AI sungguhan, masukkan API key ke file .env / Environment Variables).",
            None
        )
    try:
        r = requests.post(
            p["base_url"] + "/chat/completions",
            headers={"Authorization": f"Bearer {key}",
                     "Content-Type": "application/json"},
            json={"model": model, "messages": messages,
                  "max_tokens": max_tokens, "temperature": temperature},
            timeout=120,
        )
        try:
            d = r.json()
        except Exception:
            return None, f"Penyedia AI merespons format tidak valid (HTTP {r.status_code})"

        if not r.ok or "choices" not in d:
            err_msg = d.get("error", {})
            if isinstance(err_msg, dict):
                err_msg = err_msg.get("message", str(err_msg))
            err_str = str(err_msg)
            if key:
                err_str = err_str.replace(key, "***")
            return None, f"Penyedia AI ({r.status_code}): {err_str[:200]}"
        content = d["choices"][0]["message"].get("content")
        if not content:
            # beberapa model reasoning taruh output di reasoning_content
            content = d["choices"][0]["message"].get("reasoning_content", "")
        return content, None
    except Exception as e:
        return None, str(e)[:200]


@app.route("/api/models")
def api_models():
    uid, _, admin, _ = _get_identity(request)
    out = []
    for pkey, p in PROVIDERS.items():
        models = p["models"] if admin else [m for m in p["models"] if m in USER_MODELS]
        if models:
            out.append({"provider": pkey, "label": p["label"], "models": models})
    total = sum(len(p["models"]) for p in out)
    return jsonify({"total": total, "providers": out, "admin": admin})


@app.route("/api/me")
def api_me():
    uid, user_key, admin, is_unlimited = _get_identity(request)
    if not uid:
        return jsonify({"ok": False}), 401
    quota_info = get_user_quota(user_key, is_admin=is_unlimited)
    return jsonify({"ok": True, "uid": uid, "admin": admin, "quota": quota_info})


@app.route("/api/quota", methods=["GET"])
def api_quota():
    uid, user_key, admin, is_unlimited = _get_identity(request)
    quota_info = get_user_quota(user_key, is_admin=is_unlimited)
    return jsonify({"ok": True, "quota": quota_info})


@app.route("/api/personas")
def api_personas():
    return jsonify({
        "ok": True,
        "personas": [
            {
                "id": p["id"],
                "name": p["name"],
                "icon": p["icon"],
                "tagline": p["tagline"],
                "description": p["description"]
            }
            for p in PERSONAS.values()
        ]
    })


@app.route("/api/quota/reset", methods=["POST"])
def api_quota_reset():
    uid, user_key, admin, is_unlimited = _get_identity(request)
    quota_info = reset_user_quota(user_key)
    return jsonify({"ok": True, "quota": quota_info, "message": "Kuota harian berhasil di-reset!"})


@app.route("/api/chat", methods=["POST"])
def api_chat():
    uid, user_key, admin, is_unlimited = _get_identity(request)
    if not uid:
        return jsonify({"ok": False, "error": "Silakan login terlebih dahulu"}), 401

    data = request.get_json(force=True)
    model = data.get("model", "")
    messages = data.get("messages", [])
    if not model or not messages:
        return jsonify({"ok": False, "error": "model/messages kosong"}), 400

    pkey = MODEL_TO_PROVIDER.get(model)
    if not pkey:
        return jsonify({"ok": False, "error": "model tidak dikenal"}), 400
    if not admin and model not in USER_MODELS:
        return jsonify({"ok": False, "error": "model khusus admin"}), 403

    # Cek batas kuota harian & auto-reset
    allowed, quota_info, err_quota = consume_quota(user_key, is_admin=is_unlimited)
    if not allowed:
        return jsonify({
            "ok": False,
            "error": err_quota,
            "quota_exceeded": True,
            "quota": quota_info
        }), 429

    # Terapkan mode persona / keahlian (Canva Designer, Developer, Copywriter, dll.)
    persona_key = data.get("persona", "general")
    persona_obj = PERSONAS.get(persona_key, PERSONAS["general"])
    sys_prompt = persona_obj["system_prompt"]

    # Integrasi Konektor Aplikasi yang aktif
    connected_apps = data.get("connected_apps", [])
    if connected_apps:
        app_names = {
            "canva": "Canva", "gmail": "Gmail", "kurir": "Kurir / Messenger",
            "withings": "Withings", "gcal": "Google Kalender", "gdrive": "Google Drive",
            "gsheets": "Google Spreadsheet", "meta": "Meta Business Suite",
            "github": "GitHub", "dropbox": "Dropbox", "zoom": "Zoom"
        }
        active_list = [app_names.get(a, a) for a in connected_apps]
        sys_prompt += f"\n\n[Konektor Aplikasi Aktif]: Pengguna telah mengaktifkan integrasi dengan: {', '.join(active_list)}. Kamu dapat memberikan format naskah/desain/kode/data yang siap diintegrasikan atau diekspor langsung ke aplikasi tersebut."

    augmented_messages = []
    has_system = any(isinstance(m, dict) and m.get("role") == "system" for m in messages)
    if not has_system:
        augmented_messages.append({"role": "system", "content": sys_prompt})
    augmented_messages.extend(messages)

    t0 = time.time()
    content, err = _chat(pkey, model, augmented_messages,
                         max_tokens=data.get("max_tokens", 2000))
    if err:
        return jsonify({"ok": False, "error": err, "quota": quota_info}), 502
    return jsonify({"ok": True, "content": content,
                    "model": model, "provider": pkey,
                    "persona": persona_key,
                    "elapsed": round(time.time() - t0, 1),
                    "quota": quota_info})


@app.route("/api/health")
def health():
    return jsonify({"ok": True, "models": TOTAL,
                    "firebase": _firebase_ok})


@app.route("/api/oauth/canva/authorize")
def api_oauth_canva_authorize():
    # Gunakan redirect_uri dari query param atau otomatis ke callback server
    redirect_uri = request.args.get("redirect_uri")
    if not redirect_uri:
        redirect_uri = request.host_url.rstrip("/") + "/api/oauth/canva/callback"
    client_id = request.args.get("client_id")
    auth_url, state = generate_auth_url(redirect_uri, client_id=client_id)
    if request.args.get("redirect") == "true":
        return redirect(auth_url)
    return jsonify({"ok": True, "auth_url": auth_url, "state": state})


@app.route("/api/oauth/canva/callback")
def api_oauth_canva_callback():
    code = request.args.get("code")
    state = request.args.get("state")
    error = request.args.get("error")
    if error:
        return f"""<!DOCTYPE html><html><body style="background:#131316;color:#ef4444;font-family:sans-serif;text-align:center;padding:40px;"><h3>Otorisasi Canva Ditolak / Dibatalkan</h3><p>{error}</p><button onclick="window.close()" style="background:#334155;color:#fff;border:none;padding:8px 16px;border-radius:8px;cursor:pointer;">Tutup</button></body></html>""", 400
    if not code or not state:
        return "Parameter code atau state tidak valid", 400
    
    ok, info = exchange_token(code, state)
    if not ok:
        return f"""<!DOCTYPE html><html><body style="background:#131316;color:#ef4444;font-family:sans-serif;text-align:center;padding:40px;"><h3>Gagal Menyimpan Token Canva</h3><p>{info}</p><button onclick="window.close()" style="background:#334155;color:#fff;border:none;padding:8px 16px;border-radius:8px;cursor:pointer;">Tutup</button></body></html>""", 400
    
    return """<!DOCTYPE html><html><head><title>Canva Terhubung</title></head><body style="background:#131316;color:#fff;font-family:sans-serif;text-align:center;padding:50px 20px;"><div style="font-size:48px;margin-bottom:12px;">🎉</div><h2 style="color:#10b981;margin-bottom:8px;">Akun Canva Berhasil Terhubung!</h2><p style="color:#94a3b8;font-size:14px;margin-bottom:20px;">Oreo AI sekarang telah memiliki izin resmi untuk mengakses akun Canva Anda.</p><p style="color:#64748b;font-size:12px;">Jendela ini akan otomatis menutup...</p><script>if(window.opener){ try { window.opener.postMessage({type:'CANVA_OAUTH_SUCCESS'}, '*'); } catch(e){} } setTimeout(()=>window.close(), 1600);</script></body></html>"""


@app.route("/api/oauth/canva/status")
def api_oauth_canva_status():
    status = get_canva_status()
    return jsonify({"ok": True, "canva": status})


@app.route("/api/oauth/canva/disconnect", methods=["POST"])
def api_oauth_canva_disconnect():
    disconnect_canva()
    return jsonify({"ok": True, "message": "Akun Canva berhasil diputus"})


@app.route("/api/connectors/n8n-template")
def api_connector_template():
    tpl_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "n8n_template.json")
    if os.path.exists(tpl_path):
        with open(tpl_path, "r", encoding="utf-8") as f:
            return jsonify(json.load(f))
    return jsonify({"error": "Template not found"}), 404


@app.route("/api/connectors/test-webhook", methods=["POST"])
def api_connector_test():
    data = request.get_json(force=True) or {}
    webhook_url = data.get("webhook_url", "").strip()
    if not webhook_url:
        return jsonify({"ok": False, "error": "URL Webhook belum diisi"}), 400
    try:
        t0 = time.time()
        r = requests.post(
            webhook_url,
            json={"event": "ping", "source": "oreo_ai_chat", "time": time.time()},
            headers={"Content-Type": "application/json", "User-Agent": "OreoAI-Hub/1.0"},
            timeout=8
        )
        elapsed = round(time.time() - t0, 2)
        return jsonify({
            "ok": r.ok,
            "status_code": r.status_code,
            "elapsed": elapsed,
            "message": f"Webhook merespons HTTP {r.status_code} dalam {elapsed}s"
        })
    except Exception as e:
        return jsonify({"ok": False, "error": f"Gagal menghubungi webhook: {str(e)[:150]}"}), 502


@app.route("/api/connectors/dispatch", methods=["POST"])
def api_connector_dispatch():
    data = request.get_json(force=True) or {}
    app_id = data.get("app", "canva")
    action = data.get("action", "execute")
    payload = data.get("payload", {})
    webhook_url = data.get("webhook_url", "").strip()

    # 1. Jika pengguna telah menyambungkan Webhook n8n / Composio asli:
    if webhook_url:
        try:
            r = requests.post(
                webhook_url,
                json={
                    "app": app_id,
                    "action": action,
                    "payload": payload,
                    "timestamp": time.time()
                },
                headers={"Content-Type": "application/json", "User-Agent": "OreoAI-Hub/1.0"},
                timeout=20
            )
            try:
                res_data = r.json()
            except Exception:
                res_data = {"raw_text": r.text[:300]}
            return jsonify({
                "ok": r.ok,
                "real_n8n": True,
                "status_code": r.status_code,
                "app": app_id,
                "action": action,
                "data": res_data
            })
        except Exception as e:
            return jsonify({
                "ok": False,
                "error": f"Error saat mengeksekusi via webhook n8n: {str(e)[:150]}"
            }), 502

    # 2. Mode Simulasi Cerdas (Ketika belum ada webhook n8n eksternal):
    # Menyajikan data hasil aksi langsung sesuai aplikasi
    results_map = {
        "canva": {
            "title": payload.get("title", "Desain Visual Oreo AI"),
            "status": "Dibuat",
            "message": "Template konsep desain berhasil disiapkan untuk Canva!",
            "action_url": "https://www.canva.com/id_id/buat/",
            "action_label": "Buka & Sunting di Canva",
            "details": payload
        },
        "gmail": {
            "subject": payload.get("subject", "Draf dari Oreo AI"),
            "status": "Draf Siap",
            "message": "Draf email berhasil diformat dan siap dikirim via Gmail.",
            "action_url": f"https://mail.google.com/mail/?view=cm&fs=1&su={requests.utils.quote(payload.get('subject', 'Draf Oreo AI'))}&body={requests.utils.quote(payload.get('body', ''))}",
            "action_label": "Buka di Gmail Compose",
            "details": payload
        },
        "github": {
            "repo": payload.get("repo", "oreo-ai-snippet"),
            "status": "Kode Siap",
            "message": "Kode naskah/komponen siap dipublish ke repositori GitHub.",
            "action_url": "https://github.com/new",
            "action_label": "Buat Repositori di GitHub",
            "details": payload
        },
        "gsheets": {
            "title": payload.get("title", "Tabel Data Oreo AI"),
            "status": "Tabel Siap",
            "message": "Format baris dan kolom data siap diekspor ke Google Spreadsheet.",
            "action_url": "https://sheets.new",
            "action_label": "Buka Spreadsheet Baru",
            "details": payload
        }
    }
    res = results_map.get(app_id, {
        "status": "Sukses",
        "message": f"Aksi '{action}' untuk aplikasi {app_id} berhasil diproses.",
        "action_url": "#",
        "action_label": "Selesai",
        "details": payload
    })
    return jsonify({
        "ok": True,
        "real_n8n": False,
        "app": app_id,
        "action": action,
        "result": res
    })


@app.route("/")
def serve_index():
    return send_from_directory(FRONTEND_DIR, "index.html")


@app.route("/<path:path>")
def serve_static(path):
    if path.startswith("api/"):
        return jsonify({"ok": False, "error": "Endpoint tidak ditemukan"}), 404
    file_path = os.path.join(FRONTEND_DIR, path)
    if os.path.isfile(file_path):
        return send_from_directory(FRONTEND_DIR, path)
    return send_from_directory(FRONTEND_DIR, "index.html")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

