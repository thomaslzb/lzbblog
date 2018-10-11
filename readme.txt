程序需要启动：

MYSQL：数据库服务
https://blog.csdn.net/androidjiaocheng/article/details/7957714
控制面板-管理工具-服务
C:\Program Files\MySQL\MySQL Server 5.7\bin\net start mysql
（注意：必须使用管理员的权限才能启动MYSQL服务）


Elasticsearch： 文本搜索服务
D:\0-Python\Python-download\elasticsearch-6.4.0\bin
elasticsearch.bat

启动成功后， 在浏览器的中 http://127.0.0.1:9200/ 

返回
{
  "name" : "EWsv5e1",
  "cluster_name" : "elasticsearch",
  "cluster_uuid" : "cpajBp3SSvaIAd2cVbJGyw",
  "version" : {
    "number" : "6.4.0",
    "build_flavor" : "default",
    "build_type" : "zip",
    "build_hash" : "595516e",
    "build_date" : "2018-08-17T23:18:47.308994Z",
    "build_snapshot" : false,
    "lucene_version" : "7.4.0",
    "minimum_wire_compatibility_version" : "5.6.0",
    "minimum_index_compatibility_version" : "5.0.0"
  },
  "tagline" : "You Know, for Search"
}
