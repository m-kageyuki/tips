https://qiita.com/hoto17296/items/0ca1569d6fa54c7c4732
```
import numpy as np
import psycopg2 as psy
import pickle

db_connect_kwargs = {
    'dbname': 'db',
    'user': 'r',
    'password': 'r',
    'host': 'localhost',
    'port': '5432'
}

connection = psy.connect(**db_connect_kwargs)
connection.set_session(autocommit=True)
cursor = connection.cursor()

arr = np.array(((33.58319992295478, 130.305930782875),
                (34.58319992295478, 131.305930782875),))

cursor.execute(
    """
    insert into test_table (
      col_bytea,
      col_boxg,
      col_int,
      col_text
    ) values (%s,%s,%s,%s)

    """,
    #(pickle.dumps(arr), '(10,20),(30,70)', 10000, 'aaa')
    (psy.Binary(arr), '(10,20),(30,70)', 10000, 'aaa')
)
```
```
cursor.execute(
    """
    select * from test_table
    """)
#for c in cursor:
#    print(psy.Binary(c[1]))
```
```
res = cursor.fetchall()
print(pickle.loads(res[0][1]).shape)
# -> (2, 2)
type(cursor)
# -> psycopg2.extensions.cursor
```
```
import sqlite3
import numpy as np
import io

def adapt_array(arr):
    """
    http://stackoverflow.com/a/31312102/190597 (SoulNibbler)
    """
    out = io.BytesIO()
    np.save(out, arr)
    out.seek(0)
    return sqlite3.Binary(out.read())

def convert_array(text):
    out = io.BytesIO(text)
    out.seek(0)
    return np.load(out)
# Converts np.array to TEXT when inserting
sqlite3.register_adapter(np.ndarray, adapt_array)

# Converts TEXT to np.array when selecting
sqlite3.register_converter("array", convert_array)
conn = sqlite3.connect('example.db',detect_types=sqlite3.PARSE_DECLTYPES)
```
```
import pickle
c = conn.cursor()
c.execute(
    """
    drop table if exists stocks
    """)
c.execute(
    """
    create table if not exists stocks(
      ID INTEGER PRIMARY KEY AUTOINCREMENT,
      DATA TEXT,
      POINTS array)
    """)
arr = np.array(((33.58319992295478, 130.305930782875),
                (34.58319992295478, 131.305930782875),))
c.execute(
    """
    insert into stocks (
      DATA, POINTS) 
      values (?,?)
      
    """,
    #("aaa", pickle.dumps(arr))
    ("bbb", arr)
)
conn.commit()
c.close()
conn.close()
```
```
dest = sqlite3.connect(':memory:',detect_types=sqlite3.PARSE_DECLTYPES)
conn.backup(dest)
dcur = dest.cursor()
dcur.execute("select * from stocks");
for d in dcur:
    print(d[0])
    print(d[1])
    print(d[2])
```
https://stackoverflow.com/questions/3850022/how-to-load-existing-db-file-to-memory-in-python-sqlite3

https://www.it-swarm.jp.net/ja/python/python-numpy%E9%85%8D%E5%88%97%E3%82%92sqlite3%E3%83%87%E3%83%BC%E3%82%BF%E3%83%99%E3%83%BC%E3%82%B9%E3%81%AB%E6%8C%BF%E5%85%A5/1042343525/

### polygon
```
from centerline.geometry import Centerline
from shapely.geometry import Point, Polygon, LineString
from shapely.geometry import Polygon, MultiPolygon, MultiLineString
from shapely.geometry import Point, Polygon, LineString
from shapely.ops import unary_union
from collections import Counter
pl1 = Polygon(([0,0],[0,4],[4,4],[4,0]))
#pl2 = Polygon(([0,4],[0,8],[4,8],[4,4]))
pl2 = Polygon(([4,8],[0,8],[0,4],[4,4]))
pl3 = Polygon(([5,12],[0,11],[0,8],[4,8]))
ml = MultiPolygon([pl1, pl2, pl3])
m = unary_union(ml)
centerline = Centerline(m, **attributes)

l=[]
for c in centerline:
    if pl2.intersects(c):
        l.append(c)

ms = MultiLineString(l)
ms

# show point of intersection
l1 = LineString([[0,0],[0,10]])
l2 = LineString([[-1,5],[2,5]])
print(l1.intersection(l2))

# references
https://github.com/simplegeo/shapely/tree/c582217b9e70edbedfde98d8027b6b97d95ce991
https://gis.stackexchange.com/questions/350252/combine-multiple-polygons-into-a-single-one-with-holes
https://shapely.readthedocs.io/en/latest/manual.html#shapely.ops.unary_union
https://automating-gis-processes.github.io/CSC18/index.html

# sample2
from centerline.geometry import Centerline
from shapely.geometry import Point, Polygon, LineString
from shapely.geometry import Polygon, MultiPolygon, MultiLineString
from shapely.geometry import Point, Polygon, LineString
from shapely.ops import unary_union
from collections import Counter
pl1 = Polygon(([0,0],[0,4],[4,4],[4,0]))
#pl2 = Polygon(([0,4],[0,8],[4,8],[4,4]))
pl2 = Polygon(([4,8],[0,8],[0,4],[4,4]))
pl3 = Polygon(([5,9],[0,10],[0,8],[4,8]))
ml = MultiPolygon([pl1, pl2, pl3])
m = unary_union(ml)
attributes = {"id": 1, "name": "polygon", "valid": True}
centerline = Centerline(m,**attributes)

l=[]
ls = LineString([[4,8],[0,8]])
print(len(centerline))
for c in centerline:
    if pl2.intersects(c):
        if not pl2.contains(c) and ls.intersects(c):
            p = ls.intersection(c)
            l.append(LineString([p,p]))
            continue
        l.append(c)
ms = MultiLineString(l)
ms

# sample3
from shapely.ops import unary_union
from shapely.geometry import MultiPolygon
from centerline.geometry import Centerline
p1 = Polygon([[0, 0], [0, 4], [4, 4], [4, 0]])
p2 = Polygon([[0, 4], [0, 8], [2, 8],[2,6], [2, 4]])
p3 = Polygon([[2, 4], [2,6],[2, 8], [4, 8], [4, 4]])
p4 = Polygon([[0, 0], [4, 0], [4, -4], [0, -4]])
l=[]
for ln in p2.intersection(p3):
    l.append(list(ln.coords)[0])
    l.append(list(ln.coords)[1])
print(l)
ll = []
ll.append(l)
#hole = [[(-170, 80), (-170, -80), (170, -80), (170, 80)]]
p = Polygon(shell=unary_union([p1,p2,p3,p4]).exterior.coords, holes=ll)
p

reference
https://automating-gis-processes.github.io/CSC18/lessons/L1/Geometric-Objects.html
```

### C#
```
https://csharp.keicode.com/basic/events-basic.php
https://blog.okazuki.jp/entry/2017/09/19/224857
https://docs.microsoft.com/en-us/dotnet/api/coreml?view=xamarin-ios-sdk-12
https://docs.microsoft.com/ja-jp/xamarin/ios/platform/introduction-to-ios11/coreml
https://docs.microsoft.com/ja-jp/dotnet/machine-learning/how-to-guides/save-load-machine-learning-models-ml-net
```
