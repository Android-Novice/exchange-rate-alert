import logging
from app.config import config

logger = logging.getLogger(__name__)

sms_conf = config.get("sms", {})


def send_alert_sms(phone: str, currency_pair: str, change_percent: str, current_rate: str) -> bool:
    """发送阿里云短信预警。配置了真实 AK 后自动生效，否则仅打印日志。"""
    access_key_id = sms_conf.get("access_key_id", "")
    access_key_secret = sms_conf.get("access_key_secret", "")

    if not access_key_id or access_key_id == "YOUR_ACCESS_KEY_ID":
        logger.warning(f"[模拟短信] 发送至 {phone}: {currency_pair} 波动 {change_percent}%, 当前汇率 {current_rate}")
        return True

    try:
        from alibabacloud_dysmsapi20170525.client import Client
        from alibabacloud_dysmsapi20170525 import models as sms_models
        from alibabacloud_tea_openapi import models as open_api_models

        open_api = open_api_models.Config(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret,
        )
        open_api.endpoint = "dysmsapi.aliyuncs.com"
        client = Client(open_api)

        import json
        template_param = json.dumps({
            "currency_pair": currency_pair,
            "change_percent": change_percent,
            "current_rate": current_rate,
        }, ensure_ascii=False)

        request = sms_models.SendSmsRequest(
            phone_numbers=phone,
            sign_name=sms_conf.get("sign_name", "汇率预警"),
            template_code=sms_conf.get("template_code", ""),
            template_param=template_param,
        )
        response = client.send_sms(request)
        if response.body.code == "OK":
            return True
        else:
            logger.error(f"短信发送失败: {response.body.message}")
            return False
    except Exception as e:
        logger.error(f"短信发送异常: {e}")
        return False
