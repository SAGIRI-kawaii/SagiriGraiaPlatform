import json


def load_config(config_file: str = "config.json") -> dict:
    necessary_parameters = ["miraiHost", "authKey", "BotQQ"]
    with open(config_file, 'r', encoding='utf-8') as f:  # 从json读配置
        config = json.loads(f.read())
    for key in config.keys():
        config[key] = config[key].strip() if isinstance(config[key], str) else config[key]
    if any(parameter not in config for parameter in necessary_parameters):
        raise ValueError(f"{config_file} Missing necessary parameters! (miraiHost, authKey, BotQQ)")
    else:
        return config
