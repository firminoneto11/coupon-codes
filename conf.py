def _get_settings_module():
    from api.conf import settings

    return settings


settings = _get_settings_module()
