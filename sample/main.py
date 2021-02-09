import const.const as c
from work.work2.work import Work
from singleton import Singleton

if __name__ == "__main__":
    print c.CONST
    work = Work()
    work.getW()
    Singleton.getInstance().connect("ttt")
    print(Singleton.getInstance().getConn())
