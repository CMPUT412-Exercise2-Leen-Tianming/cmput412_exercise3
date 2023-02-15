import yaml

class load_calibration:

    def __init__(self):
        pass


    def readYamlFile(self,fname):
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
                self.log("YAML syntax error. File: %s fname. Exc: %s"
                        %(fname, exc), type='fatal')
                return


def main():
    print("hello")
    load = load_calibration()
    yaml_dict = load.readYamlFile("camera_extrinsic.yaml")
    print(yaml_dict)
    yaml_dict = load.readYamlFile("camera_intrinsic.yaml")
    print(yaml_dict)
    yaml_dict = load.readYamlFile("map_file.yaml")
    print(yaml_dict)
main()