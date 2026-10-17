"""
Manajer Kuota Harian Oreo AI
- Melacak penggunaan chat per user (berdasarkan UID atau Device ID/IP).
- Auto-reset otomatis setiap pergantian hari (00:00 / tanggal baru).
- Kuota harian dapat dikonfigurasi melalui environment variable DAILY_LIMIT (default: 30).
- Admin dapat memiliki kuota unlimited.
"""

import os
import json
import threading
from datetime import datetime

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
QUOTA_FILE = os.path.join(DATA_DIR, "quota.json")

_lock = threading.Lock()
_quota_cache = {}


def _ensure_data_dir():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR, exist_ok=True)


def _load_data():
    global _quota_cache
    _ensure_data_dir()
    if os.path.exists(QUOTA_FILE):
        try:
            with open(QUOTA_FILE, "r", encoding="utf-8") as f:
                _quota_cache = json.load(f)
        except Exception as e:
            print("[warn] Gagal membaca quota.json, inisialisasi ulang:", e)
            _quota_cache = {}
    else:
        _quota_cache = {}


def _save_data():
    _ensure_data_dir()
    try:
        temp_file = QUOTA_FILE + ".tmp"
        with open(temp_file, "w", encoding="utf-8") as f:
            json.dump(_quota_cache, f, indent=2)
        if os.path.exists(QUOTA_FILE):
            os.remove(QUOTA_FILE)
        os.rename(temp_file, QUOTA_FILE)
    except Exception as e:
        print("[error] Gagal menyimpan quota.json:", e)


# Muat data saat startup
_load_data()


def get_daily_limit():
    """Mengambil batas kuota harian dari env atau default 30."""
    try:
        return int(os.environ.get("DAILY_LIMIT", "30"))
    except ValueError:
        return 30


def get_today_str():
    """Mengembalikan tanggal hari ini dalam format YYYY-MM-DD."""
    return datetime.now().strftime("%Y-%m-%d")


def get_user_quota(user_id, is_admin=False):
    """
    Mengambil status kuota user hari ini.
    Otomatis reset hitungan jika tanggal sudah berubah.
    """
    today = get_today_str()
    limit = get_daily_limit()

    with _lock:
        user_data = _quota_cache.get(user_id, {})
        last_date = user_data.get("date")
        used = user_data.get("count", 0)

        # Jika hari berganti, reset otomatis ke 0
        if last_date != today:
            used = 0
            _quota_cache[user_id] = {"date": today, "count": 0}
            _save_data()

    remaining = max(0, limit - used) if not is_admin else 999999

    return {
        "user_id": user_id,
        "date": today,
        "limit": limit,
        "used": used,
        "remaining": remaining,
        "is_unlimited": bool(is_admin),
        "is_exceeded": (used >= limit) if not is_admin else False
    }


def consume_quota(user_id, is_admin=False):
    """
    Mengecek dan mengurangi 1 kuota harian user.
    Mengembalikan tuple (allowed: bool, quota_info: dict, error_message: str|None).
    """
    today = get_today_str()
    limit = get_daily_limit()

    with _lock:
        user_data = _quota_cache.get(user_id, {})
        last_date = user_data.get("date")
        used = user_data.get("count", 0)

        # Auto-reset harian jika tanggal baru
        if last_date != today:
            used = 0

        # Jika bukan admin dan kuota sudah habis
        if not is_admin and used >= limit:
            return False, {
                "user_id": user_id,
                "date": today,
                "limit": limit,
                "used": used,
                "remaining": 0,
                "is_unlimited": False,
                "is_exceeded": True
            }, f"Batas kuota harian ({limit} pesan/hari) sudah tercapai! Kuota akan di-reset otomatis besok (00:00)."

        # Tambahkan pemakaian
        used += 1
        _quota_cache[user_id] = {"date": today, "count": used}
        _save_data()

    remaining = max(0, limit - used) if not is_admin else 999999
    return True, {
        "user_id": user_id,
        "date": today,
        "limit": limit,
        "used": used,
        "remaining": remaining,
        "is_unlimited": bool(is_admin),
        "is_exceeded": False
    }, None


def reset_user_quota(user_id):
    """Reset manual kuota user tertentu (untuk admin atau testing)."""
    today = get_today_str()
    with _lock:
        _quota_cache[user_id] = {"date": today, "count": 0}
        _save_data()
    return get_user_quota(user_id)
