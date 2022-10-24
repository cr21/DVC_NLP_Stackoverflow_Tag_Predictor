from io import TextIOWrapper
import logging
from tqdm import tqdm
import random
import xml.etree.ElementTree as ET
import re

def process_text(f_in : TextIOWrapper, f_train_out:TextIOWrapper, f_test_out:TextIOWrapper, target_tag:str, split:float):

    line_num= 1

    for line in tqdm(f_in):
        try:
            f_out = f_train_out if random.random() > 0.3 else f_test_out
            # id, title, Body, text, label
            attr = ET.fromstring(line).attrib
            pid = attr.get('Id',"")
            label = 1 if target_tag in attr.get("Tags","") else 0
            title = re.sub("\s+"," ",attr.get("Title","")).strip()
            body = re.sub("\s+"," ",attr.get("Body","")).strip()
            text = title + " "+body

            f_out.write(f"{pid}\t{label}\t{text}\n")
            line_num+=1

            pass
        except Exception as e:
            msg =""
            msg+=f"skipping broken xml line {line_num} :{e}\n"
            logging.exception(msg)


        
    