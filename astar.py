class Point:
    """点类"""
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        """重写函数，如果2个点相同位置，返回True;否则返回False"""
        if self.x == other.x and self.y == other.y:
            return True
        else:
            return False

    def __str__(self):
        """返回对象的字符串表达式"""
        return "x:" + str(self.x) +",y:" + str(self.y)

class AStar:
    """A*算法的python实现
    AStar算法就是计算F值，F=G+H，点的选取就是通过寻找F值的最小值
    g值是从该点出发到目标地点的实际距离，参考了网上找的一个A*算法教程，g的取值是横向或纵向移
    动一个，g取10，如果是斜上方或斜下方的格子，取15
    h值是该点到到要去的终点的距离，但这个距离只是一个判断值，并不是真实的距离，同时h的取值不考
    虑斜方向上的取值，即只有横向或纵向的移动，同时也不考虑不可到达的点，及不可行点的情况。
    """

    class Node:
        """A*算法的节点数据类，包括该点的坐标、该店是由哪个点扩展出来判断的、以及该点的g值、h值

        """
        def __init__(self, point, endpoint, g=0):
            """

            :param point: 该点的坐标
            :param endpoint:要到达的点，即终点
            :param g:上述的g取值
            """
            self.point = point
            self.father = None #该点的父节点
            self.g = g  #只是一个初始化，后面会再计算的
            self.h = (abs(endpoint.x - point.x) + abs(endpoint.y - point.y))

    def __init__(self, map, startpoint, endpoint, passtag=0):
        """
        构造AStar算法
        :param map: 即地图的Array2D类型的变量
        :param startpoint: 寻路的起点
        :param endpoint: 寻路的终点
        :param passtag: 地图中不可行走的标记
        """
        self.openList = []  #开启表，即需要判断的点的一个集合
        self.closeList = [] #关闭表，及已经判断的点的集合，后续不再判断这些点
        self.map = map
        if isinstance(startpoint, Point) and isinstance(endpoint, Point):   #判断给的点是否是Point类型
            self.startpoint = startpoint
            self.endpoint = endpoint
        else:   #转换成Point类型
            self.startpoint = Point(*startpoint)
            self.endpoint = Point(*endpoint)
        self.passtag = passtag

    def getMinNode(self):
        """得到openList中F值最小的节点
        返回值值是Node类型
        """
        currentNode = self.openList[0]  #最初的父节点就是出发的点
        for node in self.openList:
            if node.g + node.h < currentNode.g + currentNode.h:
                currentNode = node
        return currentNode

    def pointInCloseList(self, point):
        """检测这个点是否在closepoint列表中"""
        for node in self.closeList:
            if node.point == point:
                return True
        return False

    def pointInOpenList(self, point):
        """检测这个点是否在openList列表中"""
        for node in self.openList:
            if node.point == point:
                return node
        return None

    def endPointInCloseList(self):
        """这个检测的是终点是否在openList列表中，即是否会开始检测考虑终点了"""
        for node in self.closeList:
            if node.point == self.endpoint:
                return node
        return None

    def search_near(self, min_F, offset_x, offset_y):
        """
        搜索周围的点，即开始扩展列表openList
        :param min_F: F值最小的点
        :param offset_x: 坐标偏移量
        :param offset_y:
        :return:
        """
        #越界检测
        if min_F.point.x + offset_x < 0 or min_F.point.x + offset_x > self.map.w - 1 or min_F.point.y + offset_y < 0 or min_F.point.y + offset_y > self.map.h - 1:
            return
        #如果是障碍，忽略
        if self.map[min_F.point.x + offset_x][min_F.point.y + offset_y] == self.passtag:
            return
        #如果在关闭表中，忽略
        currentPoint = Point(min_F.point.x + offset_x, min_F.point.y + offset_y)
        if self.pointInCloseList(currentPoint):
            return

        #设置单位花费，即横向、纵向、斜着行走的消耗
        if offset_x == 0 or offset_y == 0:  #只要x、y的偏移量有一个为0，说明只是横向或纵向行走
            step = 10
        else:
            step = 14

        #如果这个节点不在openList列表中，就加进去
        currentNode = self.pointInOpenList(currentPoint)
        if not currentNode:
            currentNode = AStar.Node(currentPoint, self.endpoint, g=min_F.g + step)
            currentNode.father = min_F
            self.openList.append(currentNode)
            return

        #如果在openList中，判断min_F到当前点的G是否更小，如果更小就重新计算，并改变当前点的father
        if min_F.g + step < currentNode.g:
            currentNode.g = min_F.g + step
            currentNode.father = min_F

    def start(self):
        """开始寻路,并返回路径列表"""
        #判断寻路终点是否为障碍
        if self.map[int(self.endpoint.x)][int(self.endpoint.y)] == self.passtag:
            return None

        #1.将起点放入openList列表
        startNode = AStar.Node(self.startpoint, self.endpoint)
        self.openList.append(startNode)
        #2.主循环逻辑
        while True:
            #先找F值最小的点
            min_F = self.getMinNode()
            #把这个点加入closeList中，该点之后不再考虑,并将其从openList中移除
            self.closeList.append(min_F)
            self.openList.remove(min_F)
            #判断这个节点的周围的点
            self.search_near(min_F, 0, -1)  #最小点下面的点
            self.search_near(min_F, 0, 1)
            self.search_near(min_F, 1, 0)
            self.search_near(min_F, -1, 0)
            #判断是否终止
            point = self.endPointInCloseList()
            if point:   #如果在的话，就会返回终点
                cpoint = point
                pathList = []
                while True:
                    if cpoint.father:   #如果该点有父节点,利用父节点的关系，往回找路径，有点像之前的数据结构中的节点
                        pathList.append(cpoint.point)
                        cpoint = cpoint.father
                    else:
                        return list(reversed(pathList)) #表明已经找完了，将路径正序记录
            if len(self.openList) == 0:
                return None

