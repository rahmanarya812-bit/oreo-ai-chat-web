"""
Modul OAuth 2.0 PKCE Resmi Canva untuk Oreo AI Chat.
Menghubungkan aplikasi langsung ke akun Canva resmi pengguna via Canva Connect API.
"""
import os, time, json, hashlib, base64, secrets
import requests

CANVA_AUTH_BASE = "https://www.canva.com/api/oauth/authorize"
CANVA_TOKEN_URL = "https://api.canva.com/rest/v1/oauth/token"
CANVA_API_BASE = "https://api.canva.com/rest/v1"

DEFAULT_CLIENT_ID = os.environ.get("CANVA_CLIENT_ID", "OC-AZb1vOWcedZR")
DEFAULT_CLIENT_SECRET = os.environ.get("CANVA_CLIENT_SECRET", "")

CANVA_SCOPES = [
    "profile:read",
    "design:meta:read",
    "design:content:write",
    "design:content:read",
    "folder:read",
    "folder:write",
    "brandtemplate:content:read",
    "brandtemplate:meta:read",
    "brandtemplate:content:write",
    "comment:write",
    "comment:read",
    "asset:read",
    "asset:write",
    "brandkit:read",
    "help:answers:read",
    "help:answers:write"
]

DATA_DIR = os.path.dirname(os.path.abspath(__file__))
TOKEN_FILE = os.path.join(DATA_DIR, "canva_token.json")
SESSIONS_FILE = os.path.join(DATA_DIR, "oauth_sessions.json")


def _load_sessions():
    if os.path.exists(SESSIONS_FILE):
        try:
            with open(SESSIONS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}


def _save_sessions(sessions):
    try:
        with open(SESSIONS_FILE, "w", encoding="utf-8") as f:
            json.dump(sessions, f, indent=2)
    except Exception as e:
        print("[warn] gagal menyimpan oauth sessions:", e)


def generate_auth_url(redirect_uri, client_id=None):
    """
    Membuat URL Otorisasi Canva resmi menggunakan standar PKCE (RFC 7636).
    """
    cid = client_id or os.environ.get("CANVA_CLIENT_ID", DEFAULT_CLIENT_ID)
    
    # Generate PKCE verifier dan challenge
    code_verifier = secrets.token_urlsafe(64)
    hashed = hashlib.sha256(code_verifier.encode("ascii")).digest()
    code_challenge = base64.urlsafe_b64encode(hashed).decode("ascii").rstrip("=")
    
    state = secrets.token_urlsafe(32)

    # Simpan sesi PKCE
    sessions = _load_sessions()
    sessions[state] = {
        "code_verifier": code_verifier,
        "redirect_uri": redirect_uri,
        "client_id": cid,
        "created_at": time.time()
    }
    _save_sessions(sessions)

    scope_str = "+".join(CANVA_SCOPES)
    auth_url = (
        f"{CANVA_AUTH_BASE}?"
        f"client_id={cid}&"
        f"redirect_uri={requests.utils.quote(redirect_uri)}&"
        f"response_type=code&"
        f"scope={scope_str}&"
        f"code_challenge={code_challenge}&"
        f"code_challenge_method=s256&"
        f"state={state}&"
        f"mcp_client_type=MuseConnector"
    )
    return auth_url, state


def exchange_token(code, state, client_secret=None):
    """
    Menukarkan authorization code dengan access token resmi Canva.
    """
    sessions = _load_sessions()
    sess = sessions.get(state)
    if not sess:
        return False, "Sesi OAuth kedaluwarsa atau tidak valid. Silakan coba klik hubungkan kembali."

    code_verifier = sess["code_verifier"]
    redirect_uri = sess["redirect_uri"]
    client_id = sess["client_id"]
    secret = client_secret or os.environ.get("CANVA_CLIENT_SECRET", DEFAULT_CLIENT_SECRET)

    payload = {
        "grant_type": "authorization_code",
        "code_verifier": code_verifier,
        "code": code,
        "redirect_uri": redirect_uri,
        "client_id": client_id
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    if secret:
        creds = f"{client_id}:{secret}".encode("utf-8")
        headers["Authorization"] = "Basic " + base64.b64encode(creds).decode("utf-8")

    try:
        r = requests.post(CANVA_TOKEN_URL, data=payload, headers=headers, timeout=20)
        data = r.json()
        if not r.ok or "access_token" not in data:
            err = data.get("error_description") or data.get("error") or str(data)
            return False, f"Gagal menukar token Canva (HTTP {r.status_code}): {err}"

        # Simpan token Canva
        token_info = {
            "access_token": data.get("access_token"),
            "refresh_token": data.get("refresh_token"),
            "token_type": data.get("token_type", "Bearer"),
            "expires_in": data.get("expires_in", 14400),
            "scope": data.get("scope"),
            "obtained_at": time.time(),
            "client_id": client_id
        }

        with open(TOKEN_FILE, "w", encoding="utf-8") as f:
            json.dump(token_info, f, indent=2)

        # Hapus sesi yang telah terpakai
        del sessions[state]
        _save_sessions(sessions)

        return True, token_info
    except Exception as e:
        return False, f"Koneksi ke server Canva gagal: {str(e)[:150]}"


def get_canva_status():
    """
    Mengecek apakah token Canva aktif dan mengambil profil resmi pengguna Canva.
    """
    if not os.path.exists(TOKEN_FILE):
        return {"connected": False}

    try:
        with open(TOKEN_FILE, "r", encoding="utf-8") as f:
            t = json.load(f)
    except Exception:
        return {"connected": False}

    access_token = t.get("access_token")
    if not access_token:
        return {"connected": False}

    # Cek profil pengguna ke API Canva
    try:
        r = requests.get(
            f"{CANVA_API_BASE}/users/me/profile",
            headers={"Authorization": f"Bearer {access_token}"},
            timeout=8
        )
        if r.ok:
            prof = r.json().get("profile", {})
            return {
                "connected": True,
                "display_name": prof.get("display_name", "Pengguna Canva"),
                "user_id": prof.get("id"),
                "token_preview": access_token[:8] + "..."
            }
        else:
            return {
                "connected": True,
                "display_name": "Akun Canva Terhubung",
                "token_preview": access_token[:8] + "..."
            }
    except Exception:
        return {
            "connected": True,
            "display_name": "Akun Canva Terhubung",
            "token_preview": access_token[:8] + "..."
        }


def disconnect_canva():
    if os.path.exists(TOKEN_FILE):
        try:
            os.remove(TOKEN_FILE)
            return True
        except Exception:
            return False
    return True
