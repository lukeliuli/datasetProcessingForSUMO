# datasetProcessingForSUMO
 各种与SUMO相关的数据库预处理的程序

1. 将FCD.XML 转为GPS  
(1). 下载法国csv或者其他数据库
(2).  基本命令  
+ cd D:\Program Files (x86)\Eclipse\Sumo\bin
+ csv2xml.py D:\codes\datasetProcessingForSUMO\1.csv
+ traceExporter.py --fcd-input D:\codes\datasetProcessingForSUMO\fcd.xml --gpsdat-output D:\codes\datasetProcessingForSUMO\fcdgpsdat.gpsdat

> https://sumo.dlr.de/docs/Tools/TraceExporter.html