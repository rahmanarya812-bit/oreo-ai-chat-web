# Oreo AI Chat — Web

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/rahmanarya812-bit/oreo-ai-chat-web)

Web chat AI modern multimodal dengan kuota harian, persona keahlian, konektor integrasi aplikasi (Canva, GitHub, Sheets, dll.), backend di Render, dan frontend di Cloudflare Pages.

### 🚀 1-Click Deploy Cepat
- **Render Backend**: Klik tombol **[Deploy to Render](https://render.com/deploy?repo=https://github.com/rahmanarya812-bit/oreo-ai-chat-web)** di atas. Render akan otomatis membaca file `render.yaml` dan mengonfigurasi Web Service.
- **Cloudflare Pages**: Buka [Cloudflare Pages Dashboard](https://dash.cloudflare.com/?to=/:account/pages/new) > Connect Git > pilih `rahmanarya812-bit/oreo-ai-chat-web` > Root folder `frontend`.

## Isi
- `backend/` — API Flask (Python): `/api/models`, `/api/chat`, `/api/health`
- `frontend/index.html` — UI chat dark-modern, login Google via Firebase
- `render.yaml` — config deploy backend ke Render

## Total model: 150+
| Provider | Jumlah |
|---|---|
| Clouvia | 109 |
| Intern Discovery | 11 |
| Radox | 11 |
| CodeCraftAPI | 11 |
| Devora | 9 |
| Atria | 2 |

## Cara setup (yang ngurus: Arya)

### 1. Firebase
1. Buka console.firebase.google.com → buat project baru
2. Authentication → aktifkan provider **Google**
3. **Firestore Database** → buat database → mode production
4. Atur Security Rules Firestore:
```
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /users/{uid}/conversations/{doc=**} {
      allow read, write: if request.auth != null && request.auth.uid == uid;
    }
  }
}
```
5. Project Settings → tambah Web App → salin config (apiKey, authDomain, projectId, appId)
6. Tempel ke `frontend/index.html` bagian `firebaseConfig`
7. Project Settings → Service Accounts → Generate New Private Key → isi file JSON-nya ke env var `FIREBASE_CREDENTIALS_JSON` di Render

### 2. Backend → Render
1. Push folder ini ke GitHub (repo private!)
2. Render Dashboard → New → Web Service → pilih repo
3. render.yaml otomatis kepake
4. Isi Environment Variables: `DISCOVERY_KEY`, `RADOXAI_KEY`, `CC_KEY`, `CLOUVIA_KEY`, `DEVORA_KEY`, `ATRIA_KEY`, `FIREBASE_CREDENTIALS_JSON`
5. Deploy → catat URL backend (misal `https://oreo-ai-chat-api.onrender.com`)

### 3. Frontend → Cloudflare Pages
1. Di `frontend/index.html`, ganti `API_BASE` dengan URL backend dari langkah 2
2. Cloudflare Dashboard → Pages → Upload `frontend/` (atau connect ke GitHub)
3. Jadi deh — buka URL Pages-nya, login Google, pilih model, chat!

## Admin vs User Biasa

- **Admin**: akses SEMUA 153 model. Tandanya ada badge "ADMIN" di header.
- **User biasa**: cuma bisa pake model yang ada di `USER_MODELS` (default: kimi-k2.6, deepseek-v4-flash-0731, minimax-m3, 2 model Devora gratis).

Cara setting di Render (Environment Variables):
- `ADMIN_UIDS` — UID Firebase admin, pisahin koma kalau banyak (UID bisa diliat di Firebase Console → Authentication)
- `USER_MODELS` — daftar model buat user biasa, pisahin koma (opsional, ada default)

Backend ngecek role di tiap request, jadi user biasa nggak bisa akalin lewat API langsung.

## Catatan
- Tanpa `FIREBASE_CREDENTIALS_JSON`, backend jalan mode dev (tanpa verifikasi login) — JANGAN buat publik dalam mode ini
- Semua API key dibaca dari env var, jangan pernah commit key ke git
