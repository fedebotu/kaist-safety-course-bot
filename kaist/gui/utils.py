
def get_config_from_values(values):
    """Config from PySimpleGUI values"""
    from kaist.config import DEFAULT_CONFIG
    config = DEFAULT_CONFIG
    for key in config.keys():
        if key == 'driver_path':
            value = values['Browse']
        else:
            value = values[key]
        value = values[key]
        if key == 'video_id':
            value = int(value)
        config[key] = value
    return config


def load_config_to_window(window, values, config):
    """Load config to the main GUI"""
    for key in values.keys():
        try:
            if key == 'Browse':
                window['driver_path'](config['driver_path'])
                continue
            window[key](config[key])
        except: continue
    return window