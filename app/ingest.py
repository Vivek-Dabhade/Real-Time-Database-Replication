import pandas as pd
import numpy as np
import opendatasets as od
from dotenv_vault import load_dotenv
import os

load_dotenv()

od.download("https://www.kaggle.com/datasets/abdulmaliklodhra/gold-price-dataset-2016-2026")

df = pd.read_csv(r"/content/gold-price-dataset-2016-2026/gold_prices_10y.csv")




