from kaist.config import DEFAULT_CONFIG


def get_config_from_values(values, verbose=False):
    """Config from PySimpleGUI values"""
    config = DEFAULT_CONFIG.copy()
    for key in config.keys():
        try:
            if key == 'driver_path':
                value = values['Browse']
            else:
                value = values[key]
            value = values[key]
            if key == 'video_id':
                value = int(value)
            config[key] = value
        except Exception as e:
            if verbose:
                print("Could not get config from values:", e)
            continue
    return config


def load_config_to_window(window, values, config):
    """Load config to the main GUI"""
    for key in values.keys():
        try:
            if key == 'Browse':
                window['driver_path'](config['driver_path'])
                continue
            window[key](config[key])
        except Exception as e: 
            continue
    return window