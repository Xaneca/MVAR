import os

import requests
from dotenv import load_dotenv
from tqdm import tqdm

from models.paper import Paper
from .base import BaseSearcher

from pprint import pprint