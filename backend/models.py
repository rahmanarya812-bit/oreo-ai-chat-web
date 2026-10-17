"""All AI models grouped by provider. Generated from live-verified lists."""
import json, os

_BASE = os.path.dirname(os.path.abspath(__file__))

def _load(name):
    with open(os.path.join(_BASE, name)) as f:
        return json.load(f)

PROVIDERS = {
    "discovery": {
        "label": "Intern Discovery",
        "base_url": "https://discovery-api.intern-ai.org.cn/v1",
        "key_env": "DISCOVERY_KEY",
        "models": _load("discovery_all_models.json"),
    },
    "radox": {
        "label": "Radox",
        "base_url": "https://radoxai.com/v1",
        "key_env": "RADOXAI_KEY",
        "models": _load("radox_all_models.json"),
    },
    "codecraft": {
        "label": "CodeCraftAPI",
        "base_url": "https://codecraftapi.com/v1",
        "key_env": "CC_KEY",
        "models": _load("cc_all_models.json"),
    },
    "clouvia": {
        "label": "Clouvia",
        "base_url": "https://router.clouvia.id/v1",
        "key_env": "CLOUVIA_KEY",
        "models": _load("clouvia_all_models.json"),
    },
    "devora": {
        "label": "Devora",
        "base_url": "https://api.devora.my.id/v1",
        "key_env": "DEVORA_KEY",
        "models": [
            "devora-01/stealth/space-bunny",
            "devora-01/stealth/dvr-v0.1-fp8",
            "devora-01/grok-cli/grok-4.7",
            "devora-01/deepseek/deepseek-v4-pro-0813",
            "devora-01/deepseek/deepseek-v4.1-flash",
            "devora-01/deepseek/deepseek-v4-pro",
            "devora-01/zai/glm-5.2",
            "devora-01/zai/glm-5.3-flash",
            "devora-01/xiaomi-mimo/mimo-v2.6-flash",
        ],
    },
    "atria": {
        "label": "Atria",
        "base_url": "https://api.atria-asi.ai/v1",
        "key_env": "ATRIA_KEY",
        "models": ["Atria-Dawn", "Atria-Dawn-Preview"],
    },
}

# model_id -> provider key
MODEL_TO_PROVIDER = {}
for pkey, p in PROVIDERS.items():
    for m in p["models"]:
        MODEL_TO_PROVIDER[m] = pkey

TOTAL = sum(len(p["models"]) for p in PROVIDERS.values())
