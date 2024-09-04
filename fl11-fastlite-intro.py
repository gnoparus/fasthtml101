from fastlite import *
from fastcore.utils import *
from fastcore.net import urlsave

url = "https://github.com/lerocha/chinook-database/raw/master/ChinookDatabase/DataSources/Chinook_Sqlite.sqlite"
path = Path("data/chinook.sqlite")
if not path.exists():
    urlsave(url, path)

db = database("data/chinook.sqlite")
