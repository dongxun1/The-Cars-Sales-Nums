# The-Cars-Sales-Nums
抓取汽车销量
思路：

先进入网址， 通过多次点击查询，同时打开开发者工具可以找到一些汽车信息 在http://db.auto.sohu.com/cxdata/xml/basic/brandList.xml中包含了大多数汽车的品牌id ，注意 ， 此id是一个车辆车型的总称 也就是说他还对应着多个其旗下的汽车品牌， 比如奥迪A6 .等车型， 获取id后在通过抓包进入 http://db.auto.sohu.com/cxdata/xml/basic/brand145ModelListWithCorp.xml网址 提取车辆名字 ， 因为要注意数据的对应，所以定义一个函数只提取brand_name， 然后在定义一个函数来提取id , 获取这个id后最后进入抓包得到的销量网址 ： http://db.auto.sohu.com/cxdata/xml/sales/model/model191sales.xml, model后面的id就是第一步提取的brand_id， 进入后提取数据 最后做好数据对应就行了

需要注意的是， 获取的车辆id 要处理为单个的对象组成的列表， 或者是字符串 比如['1', '2', '3'], 而不是 ['1, 2, 3'] ， 这样将id代入网址是得不到目标网址的。还有数据请求的编码 ， 数据有的是gbk 有的是utf-8， 要做好对应， 否则会报错。
