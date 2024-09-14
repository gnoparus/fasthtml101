from fastlite import *
from fastcore.utils import *
from fastcore.net import urlsave
import dataclasses

# download database file
url = "https://github.com/lerocha/chinook-database/raw/master/ChinookDatabase/DataSources/Chinook_Sqlite.sqlite"
path = Path("data/chinook.sqlite")
if not path.exists():
    urlsave(url, path)

db = database("data/chinook.sqlite")

# tables
dt = db.t
print(f"dt: {dt}")

# table, columns
artist = dt.artists
print(f"artist: {artist}")
print(f"artist.c: {artist.c}")

artist = dt.Artist
print(f"Artist: {artist}")
print(f"Artist.c: {artist.c}")

# tables in database
print(f"dt['Album', 'Artist', 'Customer']: {dt['Album', 'Artist', 'Customer']}")
print(f'"Artist" in dt: {"Artist" in dt}')

# query
ac = artist.c
qry = f"select * from {artist} where {ac.Name} like 'AC/%'"
print(f"qyr: {qry}")
res = db.q(qry)
print(f"res: {res}")

# view
album = dt.Album
acca_sql = f"""select {album}.*
from {album} join {artist} using (ArtistId)
where {ac.Name} like 'AC/%'"""

db.create_view("AccDaccaAlbums", acca_sql, replace=True)
acca_dacca = db.q(f"select * from {db.v.AccDaccaAlbums}")
print(f"acca_dacca: {acca_dacca}")

# dataclass
album_dc = album.dataclass()

album_obj = album_dc(**acca_dacca[0])
print(f"album_obj: {album_obj}")

# source of dataclass
src = dataclass_src(album_dc)
print(hl_md(src, "python"))

# generate python module db_dc.py
create_mod(db, "db_dc")

# import python module db_dc.py
import db_dc

print(f"db_dc.Track: {db_dc.Track}")
