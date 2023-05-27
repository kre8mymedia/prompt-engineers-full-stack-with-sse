"""Loads environment variables"""
import os
from dotenv import load_dotenv
load_dotenv()

APP_ENV = os.getenv('APP_ENV')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
