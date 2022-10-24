import argparse
from cgi import test
import os
import shutil
from tqdm import tqdm
import logging
from src.utils.common import read_yaml, create_directories
from src.utils.data_mgmt import process_text
import random


STAGE = "stage 02 prepare data" ## <<< change stage name 

logging.basicConfig(
    filename=os.path.join("logs", 'running_logs.log'), 
    level=logging.INFO, 
    format="[%(asctime)s: %(levelname)s: %(module)s]: %(message)s",
    filemode="a"
    )


def main(config_path, params_path):
    ## read config files
    config = read_yaml(config_path)
    params = read_yaml(params_path)

    input_data_dir = config['source_download_dir']['data_dir']
    input_data_filename = config['source_download_dir']['data_file']
    # create local file data path
    input_data_file_path = os.path.join(input_data_dir,input_data_filename)

    artifacts = config['artifacts']
    prepared_data_dir_path  = os.path.join(artifacts['ARTIFACTS_DIR'],artifacts['PREPARE_DATA'])
    create_directories([prepared_data_dir_path])
    train_data_path = os.path.join(prepared_data_dir_path,artifacts['TRAIN_DATA'])
    test_data_path = os.path.join(prepared_data_dir_path,artifacts['TEST_DATA'])

    seed = params['prepare']['seed']
    split = params['prepare']['split']
    encode = 'utf8'

    with open(input_data_file_path, encoding=encode) as file_in:
        with open(train_data_path,'w', encoding=encode) as file_train_out:
            with open(test_data_path, 'w',encoding=encode) as file_test_out:
                process_text(file_in, file_train_out, file_test_out, target_tag='<python>', split=0.3)




if __name__ == '__main__':
    args = argparse.ArgumentParser()
    args.add_argument("--config", "-c", default="configs/config.yaml")
    args.add_argument("--params", "-p", default="params.yaml")
    parsed_args = args.parse_args()

    try:
        logging.info("\n********************")
        logging.info(f">>>>> stage {STAGE} started <<<<<")
        main(config_path=parsed_args.config, params_path=parsed_args.params)
        logging.info(f">>>>> stage {STAGE} completed!<<<<<\n")
    except Exception as e:
        logging.exception(e)
        raise e