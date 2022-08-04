import yaml
from kaist.utils import input_with_default


DEFAULT_CONFIG = {  'username': 'YOUR_USERNAME',
                    'video_id': 0,
                    'mute_video': True,
                    'answer_quiz': True,
                    'browser': 'chrome',
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
        print(f"Could not save configuration file:\n{exc}")


def input_config():
    """Input configuration file"""
    config = load_config()
    config['username'] = input_with_default("KAIST username: ", config['username'])
    config['video_id'] = int(input_with_default('Video ID: ', config['video_id']))
    config['answer_quiz'] = input_with_default(QUIZ_WARNING, config['answer_quiz'], True)
    use_default_config = input_with_default('Use other default values? ', True, True)
    if not use_default_config:
        config['mute_video'] = input_with_default('Mute video? ', config['mute_video'], True)
        config['driver_path'] = input_with_default('Chrome driver path: ', config['driver_path'])
        config['target_webpage'] = input_with_default('Target webpage: ', config['target_webpage'])
    dump_config(config)
    return config




