from extract import extract
from transform import transform
from load_warehouse import load_warehouse
from dotenv import load_dotenv
import os

load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env"))

dirty_datas = extract()
clean_datas = transform(dirty_datas)
load_warehouse(clean_datas)