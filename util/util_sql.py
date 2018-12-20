#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Date: 18-12-12


from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, DateTime, VARCHAR, String, Numeric

from config import DB_CONFIG, DEFAULT_SCORE


Base = declarative_base()

class Proxy(Base):
    __tablename__ = "proxy"

    id = Column(Integer, primary_key=True, autoincrement=True)
    ip = Column(VARCHAR(16), nullable=False)
    port = Column(VARCHAR(5), nullable=False)
    protocol = Column(Integer, nullable=False, default=-1)
    types = Column(Integer, nullable=False, default=-1)
    country = Column(VARCHAR(100), nullable=False)
    area = Column(VARCHAR(100), nullable=False)
    updatetime = Column(DateTime, default=datetime.now)
    speed = Column(Numeric(5, 2), nullable=False)
    score = Column(Integer, nullable=False, default=DEFAULT_SCORE)

class SQLManager():
    params = {
        "ip": Proxy.ip,
        "port": Proxy.port,
        "types": Proxy.types,
        "protocol": Proxy.protocol,
        "country": Proxy.country,
        "area": Proxy.area,
        "speed": Proxy.speed,
        "score": Proxy.score
    }

    def __init__(self):
        self.engine = create_engine(DB_CONFIG["DB_CONNECT_STRING"], echo=False)
        self.session = Session(self.engine)

    def create(self):
        Base.metadata.create_all(self.engine)

    def drop(self):
        Base.metadata.drop_all(self.engine)

    def insert(self, value):
        proxy = Proxy(ip=value["ip"], port=value["port"], protocol=value["protocol"], types=value["types"],
                      country=value["country"], area=value["area"], speed=value["speed"], score=value["score"])
        self.session.add(proxy)
        self.session.commit()

    def delete(self, conditions=None):
        """
        conditions的格式是单个IP或者是IP列表
        :param conditions:
        :return: True, False
        """
        del_num = 0
        if conditions:
            try:
                if isinstance(conditions, list):
                    for condition in conditions:
                        query = self.session.query(Proxy)
                        query = query.filter(Proxy.ip == condition)
                        del_num += query.delete()
                        self.session.commit()
                else:
                    query = self.session.query(Proxy)
                    query = query.filter(Proxy.ip == conditions)
                    del_num += query.delete()
                    self.session.commit()
                if del_num > 0:
                    return True
                else:
                    return False
            except:
                return False
        else:
            return False

    def update(self, condition=None):
        """
        conditions的格式是个字典。类似self.params
        :param condition:
        :param value:也是个字典：{"ip":192.168.0.1}
        :return: True, False
        proxy = {"ip": ip, "port": port, "types": -1, "protocol": -1,
         "country": "", "area": "", "speed": 0, "score": 0}
        """
        if condition:
            try:
                if condition.get("ip"):
                    condition["updatetime"] = datetime.now()
                    query = self.session.query(Proxy).filter(Proxy.ip == condition["ip"])
                    if query.count():
                        query.update(condition)
                        self.session.commit()
                        return True
                    else:
                        return False
                else:
                    return False
            except:
                return False
        else:
            return False

    def select(self, count=None, conditions=None):
        """
        conditions的格式是个字典。类似self.params
        :param count: 返回结果的个数
        :param conditions: 筛选的条件
        :return: list
        """
        if conditions:
            conditon_list = []
            for key in list(conditions.keys()):
                if self.params.get(key, None):
                    conditon_list.append(self.params.get(key) == conditions.get(key))
            conditions = conditon_list
        else:
            conditions = []

        query = self.session.query(Proxy.ip, Proxy.port, Proxy.score)
        if len(conditions) > 0 and count:
            for condition in conditions:
                query = query.filter(condition)
            return query.order_by(Proxy.score.desc(), Proxy.speed).limit(count).all()
        elif count:
            return query.order_by(Proxy.score.desc(), Proxy.speed).limit(count).all()
        elif len(conditions) > 0:
            for condition in conditions:
                query = query.filter(condition)
            return query.order_by(Proxy.score.desc(), Proxy.speed).all()
        else:
            return query.order_by(Proxy.score.desc(), Proxy.speed).all()

def test():
    # SQLManager().drop()
    pro = {
        "ip": "1.1.1.1",
        "port": "8080",
        "types": 1,
        "protocol": 1,
        "country": "CN",
        "area": "DG",
        "score": 10,
        "speed": 1
    }
    # SQLManager().create()
    # SQLManager().insert(pro)
    # print(SQLManager().delete(["2.1.1.1", "1.1.1.1"]))
    # print(SQLManager().select(count=10, conditions={"types": 1, "country": "CN"}))
    # print(SQLManager().select(count=10))
    # print(SQLManager().update(pro))


if __name__ == "__main__":
    test()