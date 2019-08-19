from Test.Homework.configs import *
import aiohttp
import asyncio
import datetime
import re
import pymongo
from Test.Homework.configs_mysql import MYSQL
print(datetime.datetime.today(), '开始采集')


class AioCar(object):
    def __init__(self):
        #  从这里面获取总的车辆品牌id， 注意，这是总的， 每个品牌id 又对应多个车型
        self.url_1 = 'http://db.auto.sohu.com/cxdata/xml/basic/brandList.xml'

    async def have_brand_id(self, url):
        """
        获取品牌id brand_id
        :param url:
        :return:
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url_1) as resp:
                result = await resp.text()
                brand_ids = re.findall('id="(\d+)"', result, re.S)
                brand_ids = list(brand_ids)
                # brand_ids = ", ".join(brand_ids) # 注意！！字符串循环的赋值不可行， 必须是单独的数字对象
                # print(brand_ids)
                return brand_ids

    async def have_brand_name(self, url):
        """
        http://db.auto.sohu.com/cxdata/xml/basic/brand145ModelListWithCorp.xml
        通过这个网址 ，提取车辆名字， 最后的数据显示会有多个， 每个对应多个车型
        :param url:
        :return:brand_name
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                result = await resp.text(encoding="GBK")
                brand_name = re.findall('brand name="(.*?)"', result, re.S)[0]
                return brand_name

    async def have_ids(self, url):
        """
        依旧是这个网址， 获取id， 这是真正的独一无二的id
        ，对应的是每个不同的车型， 注意数据对应
        :param url:
        :return:
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                result = await resp.text(encoding="gbk")
                ids = re.findall('id="(\d+)"', result, re.S)
                return ids


    async def have_leardboard_message(self, url):
        """
        通过id 获取数据，
        :param id:
        :return:
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                try:
                    result = await resp.text(encoding="GBK")
                except UnicodeError:
                    result = await resp.text(encoding="utf-8")

                datas = re.findall('date="(.*?)" salesNum="(\d+)"', result, re.S)
                item = []
                name = re.findall('name="(.*?)"', result, re.S)[0]
                for data in datas:
                    datetime = data[0]
                    sale_nums = data[1]
                    data_list = [name, datetime, sale_nums]
                    item.append(data_list)
                return item

    @staticmethod
    def save_message_to_mongodb(data):
        try:
            if db[MONGO_COLLECTION].insert(data):
                pass
        except Exception as e:
            print(e.args)
        else:
            pass

    async def main(self):
        aio_car = AioCar()
        task1 = aio_car.have_brand_id(self.url_1)
        return await asyncio.ensure_future(asyncio.gather(task1))


if __name__ == '__main__':
    aio_car = AioCar()
    mysql = MYSQL()
    loop = asyncio.get_event_loop()
    results = loop.run_until_complete(aio_car.main())
    url_2 = 'http://db.auto.sohu.com/cxdata/xml/basic/brand{}ModelListWithCorp.xml' # 包含车辆总名字以及id
    url_3 = 'http://db.auto.sohu.com/cxdata/xml/sales/model/model{}sales.xml'
    client = pymongo.MongoClient(MONGO_URL)
    db = client[MONGO_DB]
    for brand_id in results[0]:
        url = url_2.format(brand_id)
        task = aio_car.have_brand_name(url)  # 获取品牌名字函数
        brand_name = loop.run_until_complete(task)   # 获取车辆匹配总名字， 也就是搜寻的第一个名字
        ids = loop.run_until_complete(aio_car.have_ids(url))  # 利用事件循环获取ids
        for id in ids:
            url = url_3.format(id)
            task = aio_car.have_leardboard_message(url)
            datas = loop.run_until_complete(task)
            for item in datas:
                item = [brand_name, item[0], item[1], item[2]]
                item = " ".join(item)
                item = {
                    'result' : item
                }
                aio_car.save_message_to_mongodb(item) # 保存到MongoDB
                mysql.insert(item)  # 保存到Mysql


print('采集结束', datetime.datetime.today())




