"""
这是一份网络设备互联关系数据，四列依次代表：一端设备名，一端设备端口，另一端设备名，另一端设备端口
数据是.csv格式
1、读取数据DEVNAME和PEERDEVNAME两列
2、对两列分别以“-”拆分，拆分一次（maxsplit=1），两列可以拆分成四列，四列新增到dataframe，
    依次命名为SouDev，SouArea，DesDev，DesArea
    例如：JCK72WA01-A1拆出两列JCK72WA01和A1，分别放入SouDev，SouArea
3、对SouDev、DesDev列以正则\d+进行拆分，并同时捕捉拆分的数字。
    例如：[JCK72WA01]拆分成[JCK,72,WA,01,'']，还有一种设备名字是以0A或0B结尾，所以拆分开可能是[JCK,72,WA,0,B]
4、上步拆分出的内容，保存列表数字索引0的值，赋值给新增字段SouPark，同理DesPark，同时进行部分合并，
    并新增到dataframe中，列名可随便取，假设是一、二
    例如：[JCK,72,WA,01,'']或[JCK,72,WA,0,B]，将0列保存为SouPark，并将0:2合并，同时将3:4合并，合并为[JCK72WA,01]


5、接下来需要做一些判断，如果列二的值是单数，就将SouDev的值变为"列一值+该单数|列一直+(该单数+1)”，
    如果列二的值是双数，就将SouDev的值变为"列一值+（该双数-1)|列一直+(该双数-1)"。
    结尾是A、B、C、D的比较特殊，有的设备是两台A、B就结束了，有的设备四台A、B、C、D，所以需要摘出来，
    先判断这组设备有几台，按列一的值分组，看每组有几条数据，然后合并名字。
    例如：JCK72WA,01  01是单数，SouDev名变成JCK72WA01|JCK72WA02

6、SouDev和DesDev均按上述处理逻辑变成两个设备名的合并，之后对整体数据进行一些删除，
    若SouDev==DesDev删除，删除DEVNAME和PEERDEVNAME两列，删除一、二两列

7、遍历SouPark和DesPark，如果正则匹配到前两个字母是NF，则改值为NF，否则改为BF
8、复制一份dataframe，但列名需要调换一下，SouDev、SouArea、SouPark与Des的对调
9、原来dataframe和复制并修改列名的dataframe合并concat一下，然后drop_duplicates
10、新增一列timerange，它是采集当天00:00:00-23:59:59

"""
import re
import numpy as np
import pandas as pd

def produce_data():
    df=pd.DataFrame(
        data={
            'DEVNAME':['JCK72WA01-A1','JCK72WA01-A1','JCK72WA02-A1','JCK72WA02-A1','JCK31BL11-C1','JCK31BL11-C1',],
            'T.INTTYPE||T.ININUM':['GigabitEthernet0/1','GigabitEthernet0/2','GigabitEthernet0/1','GigabitEthernet0/2','FastEthernet0','GigabitEthernet1/0/23'],
            'PEERDEVNAME':['JCK65RTOA-C1','JCK65RTOB-C1','JCK65RTOA-C1','JCK65RTOB-C1','JCK31BL12-C1','JCK65RTOA-C1',],
            'T.PEERINTTYPE||T.PEERINTNUM':['GigabitEthernet3/1','GigabitEthernet3/1','GigabitEthernet3/2','GigabitEthernet3/2','FastEthernet0','GigabitEthernet2/41'],
        }
    )
    df.to_csv('../06_Huojiangyou/01_Ornginal_Data/Device_Name_Original.csv',index=False,mode='a')

def load_data():
    data=pd.read_csv('../06_Huojiangyou/01_Ornginal_Data/decice_name.csv',encoding='ansi')
    return data  #  返回原始数据信息

def split_devname_peerdevname(data):
    # print("拆分前的数据的形状是:【{}】".format(data.shape))
    data1 = data.join(data["DEVNAME"].str.split('-', 1, expand=True))
    data = data1.rename(columns={0: "SouDev", 1: "SouArea"})
    data2 = data.join(data["PEERDEVNAME"].str.split('-', 1, expand=True))
    new_data = data2.rename(columns={0: "DesDev", 1: "DesArea"})
    # print("拆分后的数据的形状是:【{}】".format(new_data.shape))
    new_data.to_csv('../06_Huojiangyou/01_Ornginal_Data/Decice_Name_Split_1.csv', index=False, mode='a')
    return new_data  #  返回拆分后的数据

def split_soudev_desdev(new_data_1):
    tmp_list=[]
    soudev_list1,desdev_list1=[],[]
    for i,j in zip(new_data_1["SouDev"],new_data_1["DesDev"]):
        res1=re.split(r'(\d+)',i)
        res2=re.split(r'(\d+)',j)
        soudev_list1.append(res1)
        desdev_list1.append(res2)
        # tmp_list.append([res1,res2])
    return new_data_1,soudev_list1,desdev_list1

def add_columns_soupark_despark(new_data_1,soudev_list1,desdev_list1):
    count=0
    soupark_list_1,despark_list_1=[],[]

    # (1)合并字段soupark
    for i in soudev_list1:
        count+=1
        # print("这是第【{}】个行数据，其数据内容是【{}】".format(count, i))
        Soupark, number_1 = ''.join(i[:3]), ''.join(i[3:])  # 拆分合并第一个
        soupark_list_1.append([Soupark, number_1])
    soupark_data = pd.DataFrame(soupark_list_1, columns=['SouPark', 'number_1'])
    # (2) 合并字段despark
    for i in desdev_list1:
        count += 1
        # print("这是第【{}】个行数据，其数据内容是【{}】".format(count, i))
        Despark, number_2 = ''.join(i[:3]), ''.join(i[3:])  # 拆分合并第一个
        despark_list_1.append([Despark, number_2])
    despark_data = pd.DataFrame(despark_list_1, columns=['DesPark', 'number_2'])

    # (3)合并到DataFrame中
    new_data_2=pd.concat([new_data_1,soupark_data,despark_data],axis=1,join='outer',ignore_index=False)
    # print("数据合并之后的形状是【{}】".format(new_data_2.shape))

    # (4)保存至新的csv文件
    # soupark_data.to_csv('../06_Huojiangyou/01_Ornginal_Data/SouPark_1.csv',index=False,mode='a',columns=['SouPark','number_1'])
    # despark_data.to_csv('../06_Huojiangyou/01_Ornginal_Data/DesPark_1.csv',index=False,mode='a',columns=['DesPark','number_2'])
    # new_data_2.to_csv('../06_Huojiangyou/01_Ornginal_Data/Device_Name_Add_Columns.csv', index=False, mode='a')

    return new_data_2,soupark_data,despark_data  # 返回拆分并合并之后的新数据

# 5、接下来需要做一些判断，如果列二的值是单数，就将SouDev的值变为"列一值+该单数|列一直+(该单数+1)”，
#     如果列二的值是双数，就将SouDev的值变为"列一值+（该双数-1)|列一直+(该双数-1)"。
#     结尾是A、B、C、D的比较特殊，有的设备是两台A、B就结束了，有的设备四台A、B、C、D，所以需要摘出来，
#     先判断这组设备有几台，按列一的值分组，看每组有几条数据，然后合并名字。
#     例如：JCK72WA,01  01是单数，SouDev名变成JCK72WA01|JCK72WA02
def odd_even_data(new_data_2,soudev_list1,desdev_list1):
    # soupark=pd.read_csv('../06_Huojiangyou/01_Ornginal_Data/SouPark_1.csv')
    # despark=pd.read_csv('../06_Huojiangyou/01_Ornginal_Data/DesPark_1.csv')
    print("需要处理的数据字段是【{}】，其形状是【{}】".format(new_data_2.columns,new_data_2.shape))
    pattern = re.compile('^[0-9][A-Z]$') # 匹配结尾数字和字母数据

    # (1)处理SouDec数据
    NewSouDev= [] # 存放SouDev数据
    list1,list2=[],[]
    for i,j in zip(new_data_2["SouPark"],new_data_2["number_1"]):
        if j.isdigit():  # 判断是字符串是纯数字类型
            if int(j)%2!=0:
                new_soupark=i+'%02d'%(int(j))+'|'+i+'%02d'%(int(j)+1)
            elif int(j)%2==0:
                new_soupark =i+'%02d'%(int(j)-1)+'|'+i+'%02d'%(int(j)-1)
            NewSouDev.append(new_soupark)
    print(NewSouDev)
    print(len(NewSouDev))
    #     elif not j.isdigit():  # 判断包含字母
    #         if j not in list1:
    #             res=pattern.match(j)
    #             if res:
    #                 list1.append(res.group())  # 统计设备数量
    #         str1='|'.join(list1)
    #         new_str=i+str1
    #         if new_str not in list2:
    #             list2.append(new_str)
    #             new_soupark=list2[-1]
    #     else:
    #         print("数据异常")
    #
    # soupark_equipment.append(new_soupark_list[-1])  # 存放设备编号
    # # print("SouPark的设备号【{}】".format(soupark_equipment))
    # soupark_df=pd.DataFrame(new_soupark_list,columns=["odd_even"])
    # soupark_data=pd.concat([soupark,soupark_df],axis=1,join='outer',ignore_index=False)
    # # print("合并后的现状是【{}】".format(soupark_data.shape))
    # # soupark_data.to_csv('../06_Huojiangyou/01_Ornginal_Data/SouPark_1.csv', index=False, mode='w')
    print("*"*100)
    # (2)处理DesDev
    NewDesDev= [] # 存放SouDev数据
    list3,list4=[],[]
    for i,j in zip(new_data_2["DesPark"],new_data_2["number_2"]):
        if j.isdigit():
            if int(j)%2!=0:
                new_despark=i+'%02d'%(int(j))+'|'+i+'%02d'%(int(j)+1)
            elif int(j)%2==0:
                new_despark =i+'%02d'%(int(j)-1)+'|'+i+'%02d'%(int(j)-1)
            NewDesDev.append(new_despark)

        # elif not j.isdigit():
        #     if j not in list3:
        #     res=pattern.match(j)
    #             if res:
    #                 list3.append(res.group())  # 统计设备数量
    #         str1='|'.join(list3)
    #         new_str=i+str1
    #         if new_str not in list4:
    #             list4.append(new_str)
    #             new_despark=list4[-1]
    #         despark_equipment.append(j)
    #     new_despark_list.append(new_despark)
    # print(len(new_despark_list))
    # print(new_despark_list)
    # despark_df=pd.DataFrame(new_despark_list,columns=["odd_even"])
    # despark_data=pd.concat([despark,despark_df],axis=1,join='outer',ignore_index=False)
    # print("合并后的现状是【{}】".format(despark_data.shape))
    # # despark_data.to_csv('../06_Huojiangyou/01_Ornginal_Data/DesPark_1.csv', index=False, mode='w')
    # print("DesPark的设备号【{}】".format(despark_equipment))

# 6、SouDev和DesDev均按上述处理逻辑变成两个设备名的合并，之后对整体数据进行一些删除，
# 若SouDev==DesDev删除，删除DEVNAME和PEERDEVNAME两列，删除一、二两列
def join_del_soudev_desdev():
    data=pd.read_csv('../06_Huojiangyou/01_Ornginal_Data/SouPark_1.csv',encoding='ansi')

def traversal_soudev_desdev(soupark_data,despark_data):
    # soupark_data = pd.read_csv('../06_Huojiangyou/01_Ornginal_Data/SouPark_1.csv', encoding='ansi')
    # despark_data = pd.read_csv('../06_Huojiangyou/01_Ornginal_Data/DesPark_1.csv', encoding='ansi')
    print("字段是【{}】，【{}】".format(soupark_data.columns,despark_data.columns))
    print("形状是是【{}】，【{}】".format(soupark_data.shape,despark_data.shape))
    soupark_data_list_1,despark_data_list_1=[],[]
    pattern=re.compile('^[A-Z]{2}')
    for i,j in zip(soupark_data["SouPark"],despark_data["DesPark"]):
        soupark_res,despark_res  = pattern.match(i),pattern.match(j)
        if (soupark_res.group() or despark_res.group()) == 'NF':
            soupark_data_list_1.append(i)
            despark_data_list_1.append(j)
        else:
            soupark_ret,despark_ret = pattern.sub('BF',i),pattern.sub('BF',j)
            soupark_data_list_1.append(soupark_ret)
            despark_data_list_1.append(despark_ret)

    soupark_res=pd.DataFrame(soupark_data_list_1,columns=['new_soupark_1'])
    despark_res=pd.DataFrame(despark_data_list_1,columns=['new_soupark_1'])
    soupark_data=pd.concat([soupark_data,soupark_res],axis=1,join='outer',ignore_index=False)
    despark_data=pd.concat([despark_data,despark_res],axis=1,join='outer',ignore_index=False)
    print("改变之后的字段是【{}】，其形状是【{}】".format(soupark_data.columns,soupark_data.shape))
    print("改变之后的字段是【{}】，其形状是【{}】".format(despark_data.columns,despark_data.shape))

    # soupark_data.to_csv('../06_Huojiangyou/01_Ornginal_Data/SouPark_1.csv', index=False, mode='w')
    # despark_data.to_csv('../06_Huojiangyou/01_Ornginal_Data/SouPark_1.csv', index=False, mode='w')
    return soupark_data,despark_data

# 8、复制一份dataframe，但列名需要调换一下，SouDev、SouArea、SouPark与Des的对调
def copy_switch_columns(new_data_2):
    copy_data=new_data_2
    print("调换前的字段名是：\n",format(copy_data.columns))
    # (1)调换列名，列值随列名位置变换
    data1=copy_data[['DEVNAME', 'T.INTTYPE||T.ININUM', 'PEERDEVNAME','T.PEERINTTYPE||T.PEERINTNUM',
                           'DesDev', 'DesArea', 'SouDev', 'SouArea','DesPark', 'number_1', 'SouPark', 'number_2']]
    print("调换后的字段名是：\n",format(data1.columns))
    print("*"*100)
    # (2)调换列名名称，其值不变
    copy_data.columns=['DEVNAME', 'T.INTTYPE||T.ININUM', 'PEERDEVNAME','T.PEERINTTYPE||T.PEERINTNUM',
                           'DesDev', 'DesArea', 'SouDev', 'SouArea','DesPark', 'number_1', 'SouPark', 'number_2']
    print("调换后的字段名是：\n",format(copy_data.columns))
    return data1,copy_data  # data1:调换了列的顺序，值变化；copy_data:只是变更了列名，值不变化

# 9、原来dataframe和复制并修改列名的dataframe合并concat一下，然后drop_duplicates
def concat_new_lod_data(new_data_2,copy_data):
    finally_data=pd.concat([new_data_2,copy_data],axis=1,join="outer",ignore_index=False)
    pass

def main():
    # 一、没有数据，需要构造数据
    # 1、产生设备的数据信息
    # produce_data()

    # 二、加载数据集
    # 1、需求一：加载数据——读取数据DEVNAME和PEERDEVNAME两列
    data=load_data()
    # 2、需求二：数据拆分——两列拆分四列
    new_data_1=split_devname_peerdevname(data)  # new_data:第一次拆分之后的数据
    # 3、需求三：数据拆分——对SouDev、DesDev列以正则\d+进行拆分，并同时捕捉拆分的数字。
    new_data_1,soudev_list1,desdev_list1=split_soudev_desdev(new_data_1)
    # 4、需求4：数组合并——赋值并新增字段SouPark，同理DesPark
    new_data_2,soupark_data,despark_data =add_columns_soupark_despark(new_data_1,soudev_list1,desdev_list1)


    # 5、需求五：单双互变
    # odd_even_data(new_data_2,soudev_list1,desdev_list1)


    # 6、需求六：同理5合并(SouDev和DesDev),再删除重复数据。
    # join_del_soudev_desdev()
    # 7、遍历SouPark和DesPark，如果正则匹配到前两个字母是NF，则改值为NF，否则改为BF
    # traversal_soudev_desdev(soupark_data,despark_data)
    # 8、需求八：复制一份dataframe，但列名需要调换一下，SouDev、SouArea、SouPark与Des的对调
    data1,copy_data=copy_switch_columns(new_data_2)
    # 9、需求九：原来dataframe和复制并修改列名的dataframe合并concat一下，然后drop_duplicates
    concat_new_lod_data(new_data_2,copy_data)

if __name__ == '__main__':
    main()