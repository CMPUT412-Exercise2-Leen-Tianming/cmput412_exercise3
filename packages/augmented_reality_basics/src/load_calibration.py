import yaml

def readYamlFile(fname):
    """
    Reads the YAML file in the path specified by 'fname'.
    E.G. :
        the calibration file is located in : `/data/config/calibrations/filename/DUCKIEBOT_NAME.yaml`
    """
    with open(fname, 'r') as in_file:
        try:
            yaml_dict = yaml.load(in_file)
            return yaml_dict
        except yaml.YAMLError as exc:
            print("ERROR TAML")
            return
