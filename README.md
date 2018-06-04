# app_rank

论文实验

## 项目结构：

- app_rank/crawler.py：爬取排名的文件（没有开线程），所得到的数据并非使用本文件爬取；
- app_rank/tmp/crawler.py：对每月排名开通线程，爬取的数据为2016-05-01到2018-04-30两年的数据，分为id_name和rank_list两类，每类以月份为单位，共有24个月的数据；
- app_rank/merge.py:对爬取的数据进行整合，即将得到的24个月的id_name与rank_list csv文件分别整合，得到id_name_all.csv与rank_list_all.csv文件。
- app_rank/data:存放着爬取的数据以及整合后的数据。
- app_rank/paper：存放着论文原文以及翻译版。
- app_rank/analysis/tool.py:关于event、session类的定义、evidence的计算函数以及一些全局变量（evidence用到的指数）。
- app_rank/analysis/test.py:结果的展示，指数的计算，证据聚合结果的存储。
- app_rank/analysis/data_info.py:对数据以及session的分析。
- app_rank/analysis/.csv：data_info.py生成的文件——分析数据的文件。
- app_rank/analysis/.png:使用.csv文件生成的图。
- app_rank/analysis/data：生成的ids以及app每天排名的文件、所有session的三个evidence以及evidence聚合后的结果。

## note：
- .py文件中的#注释部分，并不代表此处代码无用，大部分存储中间文件的代码注释掉是因为文件已经生成，无需再次运行。
- app_rank/analysis/test.py中#注释部分，是为了展示方便，只取其中一段运行即可。

## 已完成内容：

- 爬取2016_05_01到2018_05_01两年的appstore中每天排名前300的排名信息;
- 根据排名信息，生成排名折线图，并挖掘出其leading event和leading session;
- 根据挖掘出的session和event，计算出evidence1、evidence2、evidence3（根据所有的session).
- 对所得的三个evidence，求其聚合;
- 根据求得的所有session的evidence聚合，排序，找出最可能是欺诈的阶段.

## finish
