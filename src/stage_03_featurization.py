import argparse
import os
import logging
from src.utils.common import read_yaml, create_directories,get_df
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from src.utils.featuerize import save_matrix
STAGE = "Stage 03 featurization" 

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
    artifacts = config['artifacts']
    prepared_data_dir_path  = os.path.join(artifacts['ARTIFACTS_DIR'],artifacts['PREPARE_DATA'])
    train_data_path = os.path.join(prepared_data_dir_path,artifacts['TRAIN_DATA'])
    test_data_path = os.path.join(prepared_data_dir_path,artifacts['TEST_DATA'])

    featured_data_dir_path = os.path.join(artifacts['ARTIFACTS_DIR'],artifacts['FEATURIZED_DATA'])
    create_directories([featured_data_dir_path])
    featurized_train_data_path = os.path.join(featured_data_dir_path,artifacts['FEATURIZED_TRAIN_DATA'])
    featurized_test_data_path = os.path.join(featured_data_dir_path,artifacts['FEATURIZED_TEST_DATA'])

    train_df = get_df(train_data_path)
    train_words = np.array(train_df.text.str.lower().values.astype("U"))
    max_features = params['featurize']['max_features']
    ngrams = params['featurize']['ngrams']

    bag_of_words = CountVectorizer(
                                    stop_words='english',
                                    max_features=max_features,
                                    ngram_range=(1, ngrams)
                                )
    bag_of_words.fit(train_words)
    train_words_binary_matrix = bag_of_words.transform(train_words)
    logging.info(f"[Training Data ] Bag of words transformation matrix size {train_words_binary_matrix.shape}")


    tfIdf = TfidfTransformer(smooth_idf=False)
    tfIdf.fit(train_words_binary_matrix)
    train_words_tfidf_matrix = tfIdf.transform(train_words_binary_matrix)
    logging.info(f"[Training Data ] TfIdf word transformation matrix size {train_words_tfidf_matrix.shape}")

    save_matrix(train_df,featurized_train_data_path,train_words_tfidf_matrix)

    test_df = get_df(test_data_path)
    test_words = np.array(test_df.text.str.lower().values.astype("U"))

    test_words_binary_matrix = bag_of_words.transform(test_words)
    logging.info(f"[Test Data] Bag of words transformation matrix size {test_words_binary_matrix.shape}")

    test_words_tfidf_matrix = tfIdf.transform(test_words_binary_matrix)
    logging.info(f"[Test Data] TfIdf word transformation matrix size {test_words_tfidf_matrix.shape}")

    save_matrix(test_df,featurized_test_data_path,test_words_tfidf_matrix)

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