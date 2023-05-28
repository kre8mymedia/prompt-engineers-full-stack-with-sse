"""Loads environment variables"""
import os
from dotenv import load_dotenv
load_dotenv()

## App Env
APP_ENV = os.getenv('APP_ENV')
APP_NAME = os.getenv('APP_NAME')
APP_VERSION = os.getenv('APP_VERSION')

## OpenAI
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
