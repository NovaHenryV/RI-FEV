import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import binascii,re,numpy as np,json


#导入字典
dict_1500_json=open("transfer_1500.json","r")
tf_1500_reader=json.load(dict_1500_json)

dict_200_json=open("transfer_200.json","r")
tf_200_reader=json.load(dict_200_json)

#字符串格式化函数
def low_split(s):
    return (''.join(s.split())).lower()
#温度转换函数
def transfer_1500(s):
    k=tf_1500_reader[s]
    return k

def transfer_200(s):
    k=tf_200_reader[s]
    return k
#读取文件并转换成矩阵
def sif2mat(filename,save_csv_num):
    fh = open(filename, 'rb')
    a = fh.read()
    #print 'raw: ',`a`,type(a)
    hexstr = binascii.b2a_hex(a)
    hexstr=hexstr.decode()
    #print(a)
    #print(hexstr)
    #查找数据文件起始编码、结束编码、量程编码
    start = "49 30 30 30 00 E0 01 00 "
    stop = "00 F8 00 00 00 00 00 00 00 00"
    check_temp_200 = "00 00 00 00 00 00 5F 00  60 0E 00 00 00 00 00 00"
    check_temp_1500 = "00 00 00 00 00 00 1B 03  A0 64 00 00 00 00 00 00"
    start=low_split(start)
    stop = low_split(stop)
    check_temp_200 = low_split(check_temp_200)
    check_temp_1500 = low_split(check_temp_1500)

    search_200 = r'' + check_temp_200
    search_1500 = r'' + check_temp_1500
    search = r'' + start+ '.*'+stop
    content_200 = re.compile(search_200)
    content_1500 = re.compile(search_1500)
    content = re.compile(search)
    #使用正则表达式查询
    result_200 = re.findall(content_200, hexstr)
    result_1500 = re.findall(content_1500, hexstr)
    result = re.findall(content, hexstr)
    #print(len(result[0]))
    data_200 = len(result_200)
    data_1500 = len(result_1500)

    #截取温度数据部分并转换
    data = result[0].replace(start, '')
    #print(len(data))
    data=data.replace(stop, '')
    #print(len(data))
    c=[]
    for i in range(0,int(len(data)/4)):
        if (i+1)%256!=0:
            str1=data[4*i:4*i+4]
            c.append(str1)
    if data_1500:
        for i in range(0, len(c)):
            c[i] = transfer_1500(c[i])
    else :
        if data_200:
            for i in range(0, len(c)):
                c[i] = transfer_200(c[i])
        else:
            print("量程错误")

    table = np.array(c)
    table = table.reshape(239, 255)
    if save_csv_num!=0:
        np.savetxt(filename+'one.csv', table, delimiter=',')
    #print(result_200,result_1500)
    return table


#my_matrix = np.loadtxt(open("transfer.csv","rb"),delimiter=",",skiprows=0)

def plot_contour(tablename):
    [numrow,numcol]=tablename.shape

    x = np.arange(0, numcol)
    y = np.arange(0, numrow)

    # 网格
    X,Y = np.meshgrid(x,y)

    # use plt.contourf to filling contours
    # X,Y and value for(X,Y) point
    # plt.contourf(X,Y,f(X,Y),8,alpha=0.75,cmap=plt.cm.cool)
    plt.contourf(X,Y,tablename,400,alpha=1,cmap=plt.cm.copper)
    # use plt.contour to add contour lines
    try:
        C = plt.contour(X,Y,tablename,5,colors='black')#,linewidth=0.5)
        plt.clabel(C,inline=True,fontsize=10)
    except:
        print("无可见轮廓")

    plt.xticks(())
    plt.yticks(())
    plt.show()


table=sif2mat('G:\\下载\\湖大\\毕设\\实验\\实验数据\\shuju1\\0428\\no\\1.sif',0)
e=table[120:220,75:205]#len(table[0])]
plot_contour(table)