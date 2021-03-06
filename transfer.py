import matplotlib.pyplot as plt, binascii, re, numpy as np, json, os, time,datetime as dtt

# 导入字典
dict_1500_json = open("transfer_1500.json", "r")
tf_1500_reader = json.load(dict_1500_json)

dict_200_json = open("transfer_200.json", "r")
tf_200_reader = json.load(dict_200_json)


# 字符串格式化函数
def low_split(s):
    return (''.join(s.split())).lower()


# 温度转换函数
def transfer_1500(s):
    k = tf_1500_reader[s]
    return k


def transfer_200(s):
    k = tf_200_reader[s]
    return k


# 读取文件并转换成矩阵
def sif2mat(filename, save_csv_num):
    fh = open(filename, 'rb')
    a = fh.read()
    # print 'raw: ',`a`,type(a)
    hexstr = binascii.b2a_hex(a)
    hexstr = hexstr.decode()
    # print(a)
    # print(hexstr)
    # 查找数据文件起始编码、结束编码、量程编码
    start = "49 30 30 30 00 E0 01 00 "
    stop = "00 F8 00 00 00 00 00 00 00 00"
    check_temp_200 = "00 00 00 00 00 00 5F 00  60 0E 00 00 00 00 00 00"
    check_temp_1500 = "00 00 00 00 00 00 1B 03  A0 64 00 00 00 00 00 00"
    start = low_split(start)
    stop = low_split(stop)
    check_temp_200 = low_split(check_temp_200)
    check_temp_1500 = low_split(check_temp_1500)

    search_200 = r'' + check_temp_200
    search_1500 = r'' + check_temp_1500
    search = r'' + start + '.*' + stop
    content_200 = re.compile(search_200)
    content_1500 = re.compile(search_1500)
    content = re.compile(search)
    # 使用正则表达式查询
    result_200 = re.findall(content_200, hexstr)
    result_1500 = re.findall(content_1500, hexstr)
    result = re.findall(content, hexstr)
    # print(len(result[0]))
    data_200 = len(result_200)
    data_1500 = len(result_1500)

    # 截取温度数据部分并转换
    data = result[0].replace(start, '')
    # print(len(data))
    data = data.replace(stop, '')
    # print(len(data))
    c = []
    for i in range(0, int(len(data) / 4)):
        if (i + 1) % 256 != 0:
            str1 = data[4 * i:4 * i + 4]
            c.append(str1)
    if data_1500:
        for i in range(0, len(c)):
            c[i] = transfer_1500(c[i])
    else:
        if data_200:
            for i in range(0, len(c)):
                c[i] = transfer_200(c[i])
        else:
            print("量程错误")

    table = np.array(c)
    table = table.reshape(239, 255)
    if save_csv_num != 0:
        np.savetxt(filename + 'one.csv', table, delimiter=',')
    # print(result_200,result_1500)
    fh.close()
    return table


# my_matrix = np.loadtxt(open("transfer.csv","rb"),delimiter=",",skiprows=0)

def plot_contour(tablename, save_path):
    folder = os.path.exists(save_path)
    if not folder:
        [numrow, numcol] = tablename.shape

        x = np.arange(0, numcol)
        y = np.arange(0, numrow)

        # 网格
        X, Y = np.meshgrid(x, y)

        # use plt.contourf to filling contours
        # X,Y and value for(X,Y) point
        # plt.contourf(X,Y,f(X,Y),8,alpha=0.75,cmap=plt.cm.cool)
        #plt.contourf(X, Y, tablename, 400)  # , alpha=1, cmap=plt.cm.gist_rainbow)
        # [fig,ax]=plt.subplots()
        # ax.set_label('cbar_label')#, rotation=270)
        # use plt.contour to add contour lines
        """try:
            C = plt.contour(X, Y, tablename, 8)  # , colors='black')  # ,linewidth=0.5)
            plt.clabel(C, inline=True, fontsize=10)
        except:
            print("无可见轮廓")
        """
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        axim = plt.contourf(X, Y, tablename, 400, alpha=1, cmap=plt.cm.rainbow)
        cb = fig.colorbar(axim)
        plt.xticks(())
        plt.yticks(())

        plt.savefig(save_path)
        # plt.show()
        plt.close()


def mkdir(path):
    folder = os.path.exists(path)

    if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(path)


def file_name(file_dir):
    k = file_dir.split('\\')
    length = len(k)
    print("正在生成图片……")
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            filename = (file.split('.'))[-2]
            # print((file.split('.'))[-1])
            if (file.split('.'))[-1] == 'sif':
                k = root.split('\\')
                k[length - 1] = k[length - 1] + '_plot'
                new_path = '\\'.join(k)
                # print(new_path)
                old_path = os.path.join(root, file)
                mkdir(new_path)
                table = sif2mat(old_path, 0)
                plot_contour(table, new_path + '\\' + filename + '.jpg')
    print("已将" + file_dir + "下所有sif文件转换为图片")


"""
table = sif2mat('G:\\下载\\湖大\\毕设\\实验\\实验数据\\shuju1\\0428\\no\\50.sif', 0)
e = table[120:220, 75:205]  # len(table[0])]
plot_contour(table)
"""


def check_path_standard(path):
    path = path.replace('/', '\\')
    return path


def check_path():
    work_path = input("请输入文件夹绝对目录\n")
    folder = os.path.exists(work_path)
    if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
        print("请输入正确路径\n")
        check_path()
    else:
        # print(work_path)
        work_path = check_path_standard(work_path)
        # print(work_path)
        return work_path


# file_name(check_path(0))

def plot_contour1(tablename):
    [numrow, numcol] = tablename.shape

    x = np.arange(0, numcol)
    y = np.arange(0, numrow)

    # 网格
    X, Y = np.meshgrid(x, y)

    # use plt.contourf to filling contours
    # X,Y and value for(X,Y) point
    # plt.contourf(X,Y,f(X,Y),8,alpha=0.75,cmap=plt.cm.cool)

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    # axim = ax.imshow(Z, norm = LogNorm())
    # axim = ax.contourf(X, Y, Z, levels=[1e0, 1e-1, 1e-2, 1e-3], cmap=plt.cm.jet, norm=LogNorm())
    axim = plt.contourf(X, Y, tablename, 400,alpha=1, cmap=plt.cm.rainbow)
    cb = fig.colorbar(axim)

    # [fig,ax]=plt.subplots()
    # ax.set_label('cbar_label')#, rotation=270)
    # use plt.contour to add contour lines
    #C = plt.contour(X, Y, tablename, 18,cmap=plt.cm.copper)#, colors='black')  # ,linewidth=0.5)
    #plt.clabel(C, inline=True, fontsize=10,fontcolors='black')

    plt.xticks(())
    plt.yticks(())

    plt.show()
    plt.close()


def scatter_plot_file_name(file_dir):  # 散点图
    L = []
    L1=[]
    TIME = []
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            if (file.split('.'))[-1] == 'sif':
                old_path = os.path.join(root, file)
                start_time = os.path.getmtime(old_path)
                #dt = dtt.datetime.strptime(start_time, "%Y-%m-%d  %H:%M:%S")
                TIME.append(start_time)
                table = sif2mat(old_path, 0)
                e = table[128:200, 75:200]
                L.append(e[30,60])
                L1.append(e[16,60])
    for i in range(1, len(TIME)):
        TIME[i] = TIME[i] - TIME[0]

    TIME[0] = (TIME[0] - TIME[0])
    print(TIME, '\n', L)
    title_name='-'.join((file_dir.split("\\"))[4:6])
    plt.title(title_name)
    plt.xlabel("Time(s)")
    plt.ylabel("Temperature(℃)")
    l1, = plt.plot(TIME, L, 'o',label='Non-ribbed')
    l2, = plt.plot(TIME, L1, 'o',label='ribbed')
    plt.legend()
    plt.show()

"""
table = sif2mat('D:\\test\\shuju1\\0427\\300\\gel\\20.sif', 0)
e = table[120:190, 78:200]  # len(table[0])]
print(table[139, 156],e.max(),e[16,50])
plot_contour1(e)


table = sif2mat('G:\\下载\\湖大\\毕设\\实验\\实验数据\\shuju1\\0428\\gel\\50.sif', 0)
e = table[128:200, 75:200]  # len(table[0])]
print(table[139, 156])
plot_contour1(table)

table = sif2mat('G:\\下载\\湖大\\毕设\\实验\\实验数据\\shuju1\\0428\\water\\50.sif', 0)
e = table[128:200, 75:200]  # len(table[0])]
print(table[139, 156])
plot_contour1(e)
scatter_plot_file_name('D:\\test\\shuju1\\0428\\500\\no')"""
file_name(check_path())