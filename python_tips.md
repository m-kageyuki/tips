### csvを読み込む
```
import pandas as pd
df = pd.read_csv("/home/jovyan/ml/exercise/01_input/ec_trans.csv", sep=",")
```

### CustomerIDが非NULLのデータを対象に、データ件数を取得
```
len(df[df["CustomerID"].isnull() == False])
または
df2 = df[df["CustomerID"].notnull()]
# CustomerIDのユニーク件数
df2 = df[df["CustomerID"].isnull() == False]
len(df2['CustomerID'].unique())
# CustomerIDが非NULLのデータを対象に、購買数量（Quantity）の最小値・平均値・最大値
df2.Quantity.max()
df2.Quantity.min()
df2.Quantity.mean()
# CustomerIDが非Nullのデータを対象に、以下2つのケースについて数値確認せよ。
# InvoiceNoが"C"始まりのときの、Qunatityの最小値・平均値・最大値
df_cancel = df[(df.CustomerID.notnull()) & (df.InvoiceNo.str.startswith('C'))]
df_cancel.Quantity.max()
df_cancel.Quantity.min()
df_cancel.Quantity.mean()
# InvoiceNoが"C"始まりでないときの、Qunatityの最小値・平均値・最大値
df_cancel = df[(df.CustomerID.notnull()) & (df.InvoiceNo.str.startswith('C') == False)]
df_cancel.Quantity.max()
df_cancel.Quantity.min()
df_cancel.Quantity.mean()
# 参考までにto_numpy()を用いたこういうやり方も
df_cancel = df[(df.CustomerID.notnull()) & ([s.startswith('C') for s in df.InvoiceNo.to_numpy()])]
```

### PandasのSelect文
```
import pandas as pd
data = {'Name' : ['a','b','c'],
       'Location' : ['Tokyo','Osaka','Fukuoka'],
       'Age' : [10,20,30]}
pd_data = pd.DataFrame(data)

display(pd_data[(pd_data.Location == 'Fukuoka') & (pd_data.Age > 10)])
```

### Pandas Python講座の学習メモ
```
import numpy as np
def get_df():
  return pd.read_csv("./data/bank-additional.csv", sep=";")

df = get_df()
df[df == "yes"] = np.nan # housingがyesのデータがnullに置き換わる
df = df[df["housing"].isnull() != True] # housingがnullでない行が削除される
```
```
# ピボットせよ。値はage、インデックスはjobとmarital、集計関数は平均を用いよ。
df.pivot_table(values="age", index=["job", "marital"], aggfunc=np.mean)
```
### Pandas その他
##### ペアプロット(scatter_matrix)の例
すべての組合せ可能な特徴量の組合せをプロットするもの
```
# Pythonではじめる機械学習 p.19,20 
from pandas.plotting import scatter_matrix
import mglearn
import matplotlib.pyplot as plt
iris_dataframe = pd.DataFrame(X_train, columns=iris_dataset.feature_names)
grr = pd.plotting.scatter_matrix(iris_dataframe, c=y_train,figsize=(15,15) ,marker='o',
                       hist_kwds={'bins':20}, s=60, alpha=.8, cmap=mglearn.cm3)
```

### PIL Image
```
from PIL import Image

image = None
if(path.startswith('http')):
    response = urlopen(path)
    image_data = response.read()
    image_data = BytesIO(image_data)
    image = Image.open(image_data)
else:
    image_data = tf.io.gfile.GFile(path, 'rb').read()
    image = Image.open(BytesIO(image_data))

(im_width, im_height) = image.size
return np.array(image.getdata()).reshape(
      (1, im_height, im_width, 3)).astype(np.uint8)
```

### expand_dims
```
img = np.expand_dims(img,0)
# tensorflow has also similar method (tf.expand_dims)
```

### argmax
```
import numpy as np
rands = np.random.rand(2,3) # array of 2 * 3
softmax = []
for r in rands:
    softmax.append(np.exp(r) / sum(np.exp(r)))
print(np.argmax(softmax, 1))
print(softmax)
# ->
# [1 2]
# [array([0.34446803, 0.35190022, 0.30363175]), array([0.29781803, 0.33700931, 0.36517266])]
```
