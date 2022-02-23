
# x = torch.ones(2, 20)
# net = MySequential(
#             nn.Linear(20, 256),
#             nn.ReLU(),
#             nn.Linear(256, 10))
# print(net.state_dict())
# net(x)

# from selenium import webdriver
#
# chorme_options = webdriver.ChromeOptions()
# chorme_options.headless = True
# chorme = webdriver.Chrome(chorme_options = chorme_options)
#
# page = chorme.get(url)
#
# page = BeautifulSoup

#树的遍历方法

from collections import deque

# 按层遍历，用队列实现
def level_order(root):
    queue = deque()
    queue.append(root)
    while len(queue) > 0:
        node = queue.popleft()
        print(node.data, end="")
        if node.lchild:
            queue.append(node.lchild)
        if node.rchild:
            queue.append(node.rchild)



class BiTreeNode:
    def __init__(self, data):
        self.data = data
        self.lchild = None
        self.rchild = None
        self.parent = None
        self.bf = 0 #平衡因子 右边深度减左边

class BST:
    def __init__(self, li=None):
        self.root = None
        if li:
            for i in li:
                self.insert_no_rec(i)

    #插入 的递归实现和 指针实现
    def insert(self, node, val):
        if not node: #node表示树的及几号节点  这个条件表示树是空的
            node = BiTreeNode(val)
        elif val < node.data:
            node.lchild = self.insert(node.lchild, val)
            node.lchild.parent = node
        elif val > node.data:
            node.rchild = self.insert(node.rchild, val)
            node.rchild.parent = node
        return node

    def insert_no_rec(self, val):
        p = self.root
        if not p:
            self.root = BiTreeNode(val)
            return
        while True:
            if val < p.data:
                if p.lchild:
                    p = p.lchild
                else:
                    p.lchild = BiTreeNode(val)
                    p.lchild.parent = p
                    return
            elif val > p.data:
                if p.rchild:
                    p = p.rchild
                else:
                    p.rchild = BiTreeNode(val)
                    p.rchild.parent = p
                    return
            else:
                return

    # 树的遍历方法
    def pre_order(self, root):
        if root:
            print(root.data, end=",")
            self.pre_order(root.lchild)
            self.pre_order(root.rchild)

    def in_order(self, root):
        if root:
            self.in_order(root.lchild)
            print(root.data, end=",")
            self.in_order(root.rchild)

    def post_order(self, root):
        if root:
            self.post_order(root.lchild)
            self.post_order(root.rchild)
            print(root.data, end=",")

    #树的查询
    def query_no_rec(self, val):
        p = self.root
        while p:
            if p.data > val:
                p = p.lchild
            elif p.data < val:
                p = p.rchild
            else:
                return p
        return None

    #树的删除

    # 1 删除的是叶子节点
    def __remove_node1(self, node):
        if not node.parent: #如果要删的叶子节点是根节点
            self.root = None
        elif node == node.parent.lchild:
            node.parent.lchild = None
        else:
            node.parent.rchild = None

    # 2
    def __remove_node21(self, node): #删除的节点只有一个左孩子
        if not node.parent:  # 根节点
            self.root = node.lchild
            node.lchild.parent = None

        elif node == node.parent.lchild:
            node.parent.lchild = node.lchild
            node.lchild.parent = node.parent
        else:
            node.parent.rchild = node.lchild
            node.lchild.parent = node.parent

    def __remove_node22(self, node):  # 删除的节点只有一个右孩子
        if not node.parent:  # 根节点
            self.root = node.rchild
            node.rchild.parent = None

        elif node == node.parent.lchild:
            node.parent.lchild = node.rchild
            node.rchild.parent = node.parent
        else:
            node.parent.rchild = node.rchild
            node.rchild.parent = node.parent

    def delete(self, val):
        if self.root:
            node = self.query_no_rec(val)
            if not node:
                return False
            if not node.lchild and not node.rchild:#叶子节点
                self.__remove_node1(node)
            elif not node.rchild: #没有右孩子加上上一个if约束 表示只有一个左孩子
                self.__remove_node21(node)
            elif not node.lchild:#没有左孩子加上上一个if约束 表示只有一个右孩子
                self.__remove_node22(node)
            else:#有两个孩子
                min_node = node.lchild
                while min_node:
                    min_node = min_node.lchild
                node.data = min_node.data
                #删除min_node，最小节点必然是 只有右孩子或者无孩子
                if min_node.rchild:
                    self.__remove_node22(min_node)
                else:
                    self.__remove_node1(min_node)


# tree = BST([4,6,7,9,2,1,3,5,8])
# tree.pre_order(tree.root)
# print('')
# tree.in_order(tree.root)#中序序列是拍好序的
# print('')
# tree.post_order(tree.root)
# print('')
# print(tree.query_no_rec(3).data)
# tree.delete(3)
# print("")
# tree.in_order(tree.root)

class AVLNode(BiTreeNode):
    def __init__(self, data):
        BiTreeNode.__init__(self, data)
        self.bf = 0 #平衡因子 右边深度减左边

class AVLTree(BST):
    def __init__(self, li=None):
        BST.__init__(self, li)

    def rotata_left(self, p, c):#左旋
        s2 = c.lchild
        p.rchild = s2
        if s2: #none是没有父节点的，因此反向链回去时需要判断是否为none
            s2.parent = p

        c.lchild = p
        p.parent = c

        p.bf = 0
        c.bf = 0
        return c

    def rotata_right(self, p, c):#右旋
        s2 = c.rchild
        p.lchild = s2
        if s2:
            s2.parent = p

        c.rchild = p
        p.parent = c

        p.bf = 0
        c.bf = 0
        return c

    def rotata_right_left(self, p, c):
        g = c.lchild

        s3 = g.lchild
        c.lchild = s3
        if s3:
            s3.parent = c
        g.rchild = c
        c.parent = g

        s2 = g.rchild
        p.lchild =s2
        if s2:
            s2.parent = p

        g.lchild = p
        p.parent = g

        #更新bf, 分插入s2还是插入s3
        if g.bf > 0:
            p.bf = -1
            c.bf = 0
        elif g.bf < 0:
            p.bf = 0
            c.bf = 1
        else: #插入的是g
            p.bf = 0
            c.bf = 0
        return g

    def rotata_left_right(self, p, c):
        g = c.rchild

        s2 = g.lchild
        c.rchild = s2
        if s2:
            s2.parent = c
        g.lchild = c
        c.parent = g

        s3= g.lchild
        p.rchild = s3
        if s3:
            s3.parent = p

        g.rchild = p
        p.parent = g

        # 更新bf, 分插入s2还是插入s3
        if g.bf < 0:
            p.bf = 1
            c.bf = 0
        elif g.bf > 0:
            p.bf = 0
            c.bf = -1
        else:  # 插入的是g
            p.bf = 0
            c.bf = 0
        return g

    def insert_no_rec(self, val):
        #1.先插入
        p = self.root
        if not p:
            self.root = AVLNode(val)
            return
        while True:
            if val < p.data:
                if p.lchild:
                    p = p.lchild
                else:
                    p.lchild = AVLNode(val)
                    p.lchild.parent = p
                    node = p.lchild #存储插入的节点
                    break
            elif val > p.data:
                if p.rchild:
                    p = p.rchild
                else:
                    p.rchild = AVLNode(val)
                    p.rchild.parent = p
                    node = p.rchild
                    break
            else:
                return
        #2.更新bf
        while node.parent:
            if node == node.parent.lchild:#左子树插入
                if node.parent.bf < 0:#parent bf 为-1 那么更新后为-2，需要进行旋转
                    g = node.parent.parent
                    x = node.parent
                    if node.bf > 0: #node 右边沉
                        n = self.rotata_left_right(node.parent, node) #此时为左偏 右沉
                    else:
                        n = self.rotata_right(node.parent, node)


                elif node.parent.bf > 0:
                    node.parent.bf = 0
                    break

                else:#parent bf 为0
                    node.parent.bf = -1
                    node = node.parent
                    continue

            else:#右子树插入
                if node.parent.bf > 0:  # parent bf 为1 那么更新后为2，需要进行旋转
                    g = node.parent.parent
                    x = node.parent
                    if node.bf < 0:  # node 左边沉
                        n = self.rotata_right_left(node.parent, node)  # 此时为右偏 左沉
                    else:
                        n = self.rotata_left(node.parent, node)


                elif node.parent.bf < 0:
                    node.parent.bf = 0
                    break

                else:  # parent bf 为0
                    node.parent.bf = 1
                    node = node.parent
                    continue

            n.parent = g
            if g:
                if x == g.lchild: #判断需要旋转的树的根 是g的哪个孩子
                    g.lchild = n
                if x == g.rchild:
                    g.rchild = n
                break
            else:
                self.root = n
                break

tree = AVLTree([4,6,7,2,1,3,5,8])
# tree.pre_order(tree.root)
# print('')
tree.in_order(tree.root)#中序序列是拍好序的
# print('')
# tree.insert_no_rec(11)
# print("")
# tree.in_order(tree.root)
