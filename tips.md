
#### postgresql
https://www.postgresql.org/download/linux/ubuntu/
https://wiki.postgresql.org/wiki/Apt
https://qiita.com/SierSetup/items/041939690cea80c1b1d9
https://qiita.com/H-A-L/items/fe8cb0e0ee0041ff3ceb
https://qiita.com/Takashi_Nishimura/items/da5551e6a4cb4b64f055
https://qiita.com/ritya/items/b1ae186f3f6308c52289
https://www.ashisuto.co.jp/db_blog/article/20160308_postgresql_with_python.html

```
## install python module on ubuntu
pip install psycopg2-binary

sudo service postgresql start
create role ロール名 with createdb login password 'パスワード';
create database データベース名;
\l
\q
```
#### ubuntu disk size
https://forums.linuxmint.com/viewtopic.php?t=280317
https://forums.linuxmint.com/viewtopic.php?f=90&t=280289#p1543983

## Virtual Box
### Install
```
Download VirtualBox platform packages
# https://www.virtualbox.org/wiki/Downloads
## -> VirtualBox-6.1.18-142142-OSX.dmg
and then install by double click

If it fails, check mac system setting(環境設定) -> セキュリティとプライバシー -> 一般
-> unlock -> allow prohibited package
then, tyr again

After that, create new machine named "ubuntu" by click "新規"

# reference
## https://shoji014.com/virtualbox-error/
```

### Install Ubuntu
```
Download ubuntu iso
# https://www.ubuntulinux.jp/download
## -> ubuntu-20.04.1-desktop-amd64.iso

set as following
# Right click on "ubuntu"(your machine name) on virtual box manager.
# 「設定」をクリックして、「ストレージ 」＞「コントローラー: IDE」 の下の「空」を選択します。
# CD/DVDドライブの右にあるディスクのアイコンをクリックして、仮想CD/DVDディスクファイルの選択で、ubuntuのisoイメージを選択し、「OK」をクリック。

Start the machine and follow a guidace from ubuntu installer.
Select Japanese language to adjust keyboard setting align with your host machine.

# reference
## https://cvtech.cc/virtualbox/
```
### Copy and Paste bidirectionally
```
Install Guest Additions CD image
Click "Devices" on top bar and click "Insert Guest Additions CD image"
After that click "run" button as system guide you through.
And then reboot.

# or download from https://w0.dk/~chlor/vboxguestadditions/
## VBoxGuestAdditions_6.1.18.iso
## In this case, set this iso like ubuntu iso and run the machine.
## After that, click CD image on ubuntu desk top(left bar) and then follow a guidance of installer
## And then reboot

After reboot, you can change copy and paste setting easily on "Devices"(top bar)

# reference url
## https://qiita.com/LemonLeaf/items/ac12404e277ff9bb3a65
```

### Web cam
```
Download Virtual Box Oracle VM VirtualBox Extension Pack.
# https://www.virtualbox.org/wiki/Downloads
## Oracle_VM_VirtualBox_Extension_Pack-6.1.18.vbox-extpack
## reference
### https://pc-karuma.net/virtualbox-extension-pack-install/

Install the extension pack by double click the installer, running ubuntu machine.

Check installed by following command on host command prompt. (not ubuntu terminal)
VBoxManage list webcams
# -> Video Input Devices: 1
# -> .1 "FaceTime HDカメラ"
# -> CC24076DX0QF6VVDK

Attach the webcam (or webcams) you want to use by following command
VboxManage controlvm "ubuntu" webcam attach .1
# "ubuntu" stands for the name of virtual box machine.
# The number at the end of the line indicates the camera.

After that move on to "Devices" of top bar and "webcams"

# Reference
## https://automaticaddison.com/connect-your-built-in-webcam-to-ubuntu-20-04-on-a-virtualbox/#:~:text=Open%20the%20Oracle%20VM%20VirtualBox,Launch%20Ubuntu.&text=Click%20Devices%20%2D%3E%20Webcams.,Enable%20your%20webcam(s).
```

## Anaconda
### Installer
```
https://repo.anaconda.com/archive/Anaconda3-2020.11-Linux-x86_64.sh

search by anaconda on google
https://docs.anaconda.com/anaconda/install/linux/
/bin/bash ~/Downloads/Anaconda3-2020.11-Linux-x86_64.sh
```

### Manage
```
https://docs.conda.io/projects/conda/en/latest/user-guide/getting-started.html#managing-conda

# check version
conda --version

# Update conda to the current version. Type the following:
conda update conda
## Conda compares versions and then displays what is available to install.
## If a newer version of conda is available, type y to update:
## Proceed ([y]/n)? y

# Create a new environment
conda create --name hogehoge
## Create a new environment and install a package in it.
## We will name the environment snowflakes and install the package BioPython. At the Anaconda Prompt or in your terminal window, type the following:
conda create --name snowflakes biopython

# Deactivate current environment
conda deactivate

# Activate another environment
conda hogehoge

# To see a list of all your environments, type:
conda info --envs

# run jupyter
jupyter-lab --ip=0.0.0.0 --allow-root &
```

## postgresql
https://rowingfan.hatenablog.jp/entry/2018/08/14/143200  
https://symfoware.blog.fc2.com/blog-entry-2173.html  

リポジトリの追加 
```
 echo "deb http://apt.postgresql.org/pub/repos/apt/ bionic-pgdg main" | sudo tee -a /etc/apt/sources.list.d/pgdg.list
```

信頼キーの取得と追加  
```
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
```
ここでエラーになったので以下を実行
```
sudo apt install gnupg

sudo apt update
sudo apt upgrade
```
PostgreSQL10とpgadmin4をインストールする。
```
sudo apt -y install postgresql-10 pgadmin4

psql --version
```
起動
```
sudo service postgresql start
```
最初のログイン
```
sudo -u postgres psql
```

ロールをつくる。
```
postgres=# create role vagrant with login createdb;
```
postgresユーザーのパスワードを変更する。
```
postgres=# alter user postgres password 'postgres';
```
ログアウト
```
postgres=# \q
```
peer認証の関係でpsqlログインできないのでpg_hba.confを修正。
```
/etc/postgresql/10/main/pg_hba.conf
local all postgres md5
```
postgresqlを再起動
```
psql -h /var/run/postgresql/ -p 5432 -U postgres -W 
```
```
cat sql | psql -h /var/run/postgresql/ -p 5432 -U postgres -W -A -F, > test.csv
```
