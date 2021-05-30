import os
import sys
from main import app as app  # noqa
from data.db_session import global_init

path = os.path.abspath('')
if path not in sys.path:
    sys.path.append(path)

global_init("db/blogs.db")
