import yaml
from src.utils import input_with_default


DEFAULT_CONFIG = {  'username': 'duckduckgoose',
                    'video_id': 0,
                    'playback_rate': 10,
                    'max_retries': 10,
                    'mute_video': True,
                    'answer_quiz': True,
                    'browser': 'Chrome',
                    'driver_path': '/usr/bin/chromedriver',
                    'target_webpage': 'https://safety.kaist.ac.kr/main/main.do',
                    'debug_path': 'debug.html'}

QUIZ_WARNING = "Answer quiz?\nNOTE: this will try to answer the quiz many times iteratively until solved, \
                we assume to have unlimited retries. Do at your own risk ;D"


def load_config(config_file='config.yaml'):
    """Load configuration file"""
    try:
        with open(config_file, 'r') as file:
            config = yaml.load(file, Loader=yaml.FullLoader)
            if config == None:
                config = DEFAULT_CONFIG
    except Exception:
        config = DEFAULT_CONFIG
    return config


def dump_config(config, config_file='config.yaml'):
    """Dump configuration file"""
    try:
        with open(config_file, 'w') as file:
            yaml.dump(config, file, Dumper=yaml.Dumper)
    except Exception as exc:
        pass
        # print(f"Could not save configuration file:\n{exc}")




