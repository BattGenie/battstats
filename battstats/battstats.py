import helper_functions as hf
import logging
import sys

logging.basicConfig(level=logging.DEBUG, 
                    filename='log.log', 
                    filemode='w', 
                    format='%(asctime)s %(name)s - %(levelname)s - %(message)s')

log = logging.getLogger(__name__)

def initialize_battstats():
    return

if __name__ == "__main__":
    cmd_line_args = sys.argv
    if len(cmd_line_args) < 2:
        log.info("Too few CLI arguments! Pass the test_config.json file!")
        exit()
    elif len(cmd_line_args) > 2:
        log.info("Too many CLI arguments!")
        exit()
    
    config_file = cmd_line_args[1]
    config_dict = hf._create_config_dict(config_file)

    if config_dict is None:
        log.error("No config dict created. Make sure correct path for config file is passed as argument.")
        exit()
    
    test_name = config_dict['test_name']

    test_id = hf.lookup_id()
    meta_variables = hf.get_meta_variables(['charge_steps', 'cv_voltage_threshold_mv', 'discharge_steps'], test_name)

    # Check to see if test_name exists in testdata_meta
    if not meta_variables:
        log.error('No meta variables passed.')
        exit()
    
    data = hf.load_data()


    