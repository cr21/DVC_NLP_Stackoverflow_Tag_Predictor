import argparse
import os
from tqdm import tqdm
import logging
from src.utils.common import create_directories, create_directories, read_yaml
import urllib.request as req


STAGE = "stage 01 get data" ## <<< change stage name 

# set logging level Info, logging file format and in append mode
logging.basicConfig(
    filename=os.path.join("logs", 'running_logs.log'), 
    level=logging.INFO, 
    format="[%(asctime)s: %(levelname)s: %(module)s]: %(message)s",
    filemode="a"
    )


def main(config_path):
    ## read config files
    config = read_yaml(config_path)
    source_data_url = config['source_data_url']
    local_data_dir = config['source_download_dir']['data_dir']
    # create local directories where data will be put
    create_directories([local_data_dir])
    data_filename = config['source_download_dir']['data_file']
    # create local file data path
    local_data_file_path = os.path.join(local_data_dir,data_filename)
    logging.info("Download started")
    # get data from url
    filename, headers = req.urlretrieve(source_data_url, local_data_file_path)
    logging.info("Download finished")
    logging.info(f"Download file is present at {filename}")
    logging.info(f"Download header  {headers}")


if __name__ == '__main__':
    args = argparse.ArgumentParser()
    args.add_argument("--config", "-c", default="configs/config.yaml")
    parsed_args = args.parse_args()

    try:
        logging.info("\n********************")
        logging.info(f">>>>> stage {STAGE} started <<<<<")
        main(config_path=parsed_args.config)
    except Exception as e:
        logging.exception(e)
        raise e