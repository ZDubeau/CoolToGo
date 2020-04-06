from time import sleep
import json
import re
import pandas as pd
from pandas import DataFrame
from pandas import isnull
import numpy as np
from collections import defaultdict
import psycopg2 as psy
import traceback

# df = pd.json_normalize(my_insee, errors='ignore') : for json to df

def pd_df(df):
