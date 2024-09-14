from fastlite import *
from fastcore.utils import *
from fastcore.net import urlsave

# download database file
url = "https://github.com/lerocha/chinook-database/raw/master/ChinookDatabase/DataSources/Chinook_Sqlite.sqlite"
path = Path("data/chinook.sqlite")
if not path.exists():
    urlsave(url, path)

db = database("data/chinook.sqlite")

# tables
dt = db.t
print("dt: ", dt)

# table, columns
artist = dt.artists
print("artist: ", artist)
print("artist.c: ", artist.c)

artist = dt.Artist
print("Artist: ", artist)
print("Artist.c: ", artist.c)

# tables in database
print("dt['Album', 'Artist', 'Customer']", dt["Album", "Artist", "Customer"])
print('"Artist" in dt ', "Artist" in dt)

# query
ac = artist.c
qry = f"select * from {artist} where {ac.Name} like 'AC/%'"
print("qyr: ", qry)
res = db.q(qry)
print("res: ", res)

# view
album = dt.Album
acca_sql = f"""select {album}.*
from {album} join {artist} using (ArtistId)
where {ac.Name} like 'AC/%'"""

db.create_view("AccDaccaAlbums", acca_sql, replace=True)
acca_dacca = db.q(f"select * from {db.v.AccDaccaAlbums}")
print(f"acca_dacca: {acca_dacca}")
