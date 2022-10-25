import os
import pandas as pd
import joblib
import logging
import scipy.sparse as sparse
import numpy as np

def save_matrix(df: pd.DataFrame,out_file_path:str, tf_idf_matrix: sparse.csr_matrix):
    logging.info("Creating sparse combined matrix")
    id_matrix = sparse.csr_matrix(df.id.astype(np.int64)).T
    label_matrix = sparse.csr_matrix(df.id.astype(np.int64)).T
    result = sparse.hstack([id_matrix, label_matrix, tf_idf_matrix], format="csr")
    joblib.dump(result, out_file_path)
    msg =f"The output matrix saved at  {out_file_path} of size {result.shape} and data type {result.dtype}"

    logging.info(msg)