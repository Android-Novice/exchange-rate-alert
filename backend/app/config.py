import os
import yaml
from pathlib import Path


def load_config():
    config_path = Path(__file__).parent.parent / "config.yaml"
    if config_path.exists():
        with open(config_path, "r", encoding="utf-8") as f:
            cfg = yaml.safe_load(f)
    else:
        cfg = {}

    # Environment variable overrides for cloud deployment
    cfg.setdefault("sms", {})
    if os.environ.get("SMS_ACCESS_KEY_ID"):
        cfg["sms"]["access_key_id"] = os.environ["SMS_ACCESS_KEY_ID"]
    if os.environ.get("SMS_ACCESS_KEY_SECRET"):
        cfg["sms"]["access_key_secret"] = os.environ["SMS_ACCESS_KEY_SECRET"]

    return cfg


config = load_config()
