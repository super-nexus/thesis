import yaml


def load_config(config_path):
    with open(config_path) as file:
        data = yaml.load(file, Loader=yaml.FullLoader)
        return data


def get_class_name(string):
    temp = string.split('_')
    return ''.join(ele.title() for ele in temp)
