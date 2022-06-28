import yaml

__all__ = (
    "color",
    "config",
    "emoji",
    "token"
)


with open("yaml/color.yaml") as f:
    color = yaml.load(f, Loader=yaml.FullLoader)

with open("yaml/config.yaml") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

with open("yaml/emoji.yaml") as f:
    emoji = yaml.load(f, Loader=yaml.FullLoader)

with open("yaml/token.yaml") as f:
    token = yaml.load(f, Loader=yaml.FullLoader)