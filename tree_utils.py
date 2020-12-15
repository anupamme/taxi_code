from pyTree.Tree import Tree as Tree

class Node(object):
    
    def __init__(self, name):
        self.contents = name
        self.children = []
        self.num_requests = 0
        
    def print_cli(self, level = 0):
        tab_spaces = ''
        count = 0
        while count < level:
            tab_spaces += '\t'
            count += 1
        print(tab_spaces + str(level) + ' | ' + str(self.contents) + ' | ' + str(len(self.children)) + ' |' + str(self.num_requests))
        for item in self.children:
            item.print_cli(level = level + 1)
        
    def get_num_leaf_nodes(self):
        if len(self.children) == 0:
            return 1
        else:
            total = 0
            for item in self.children:
                total += item.get_num_leaf_nodes()
            return total

class Tree_Cli(object):
    
    def __init__ (self):
        node_ins = Node('root')
        self.root = node_ins
    
    def create_node(self, char, num_requests):
        node_ins = Node(char)
        node_ins.num_requests = num_requests
        return node_ins
    
    def add_node(current_ptr, node_ins):
        current_ptr.children.append(node_ins)
        current_ptr.children.sort(key=lambda x: x.contents)
        
    def get_node(self, current_ptr, char, num_requests):
        for node in current_ptr.children:
            if node.contents == char:
                node.num_requests += num_requests
                return node
        return None
        
        
    
    '''
    1. Input node: SHG2Mh
    Steps:
        1. Iterate over the code:
            does the node exist as a child:
                If yes, goto that node
                else: insert a node.
        2. As you trickle down keep updating the stats of the node.
    '''
    def add_node_recursive(self, node_details):
        node_id, num_requests = node_details
        current_ptr = self.root
        for char in node_id:
            next_node = self.get_node(current_ptr, char, num_requests)
            if next_node == None:
                new_node = self.create_node(char, num_requests)
                Tree_Cli.add_node(current_ptr, new_node)
                next_node = new_node
            current_ptr = next_node
            
    def print_cli(self):
        self.root.print_cli(level=0)
        
    def get_num_leaf_nodes(self):
        total = 0
        for item in self.root.children:
            total += item.get_num_leaf_nodes()
        return total
            
def wrapper(item_list):
    tr = Tree_Cli()
    for item in item_list:
        tr.add_node_recursive(item)
    tr.print_cli()
    print('#leaf nodes: ' + str(tr.get_num_leaf_nodes()))
    
    