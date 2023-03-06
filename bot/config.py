from environs import Env
import os, sys, django


env = Env()
env.read_env()

TOKEN = env.str("TOKEN")


print('[+] Django is setting up ...')
APP_PACKAGE = 'server'
PARENT_DIR = os.path.dirname(os.path.dirname(__file__))
APP_DIR = os.path.join(PARENT_DIR, APP_PACKAGE)

sys.path.append(APP_DIR)
sys.path.append(PARENT_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()