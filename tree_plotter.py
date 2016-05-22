__author__ = 'jayanthvenkataraman'

import matplotlib.pyplot as plt

decision_node = dict(boxstyle="sawtooth", fc="0.8")
leaf_node = dict(boxstyle="round4", fc="0.8")
arrow_args = dict(arrowstyle="<-")

def get_number_of_leafs(my_tree):
    num_of_leafs = 0
    first_str = my_tree.keys()[0]
    second_dict = my_tree[first_str]
    for key in second_dict.keys():
        if type(second_dict[key]).__name__=='dict':#test to see if the nodes are dictonaires, if not they are leaf nodes
            num_of_leafs += get_number_of_leafs(second_dict[key])
        else:   num_of_leafs +=1
    return num_of_leafs

def get_tree_depth(my_tree):
    max_depth = 0
    first_str = my_tree.keys()[0]
    second_dict = my_tree[first_str]
    for key in second_dict.keys():
        if type(second_dict[key]).__name__=='dict':#test to see if the nodes are dictonaires, if not they are leaf nodes
            this_depth = 1 + get_tree_depth(second_dict[key])
        else:   this_depth = 1
        if this_depth > max_depth: max_depth = this_depth
    return max_depth

def plot_node(node_text, center_point, parent_point, node_type):
    create_plot.ax1.annotate(node_text, xy=parent_point,  xycoords='axes fraction',
             xytext=center_point, textcoords='axes fraction',
             va="center", ha="center", bbox=node_type, arrowprops=arrow_args )

def plot_mid_text(center_point, parent_point, text_string):
    x_mid = (parent_point[0]-center_point[0])/2.0 + center_point[0]
    y_mid = (parent_point[1]-center_point[1])/2.0 + center_point[1]
    create_plot.ax1.text(x_mid, y_mid, text_string, va="center", ha="center", rotation=30)

def plot_tree(my_tree, parent_point, node_text):#if the first key tells you what feat was split on
    num_leafs = get_number_of_leafs(my_tree)  #this determines the x width of this tree
    depth = get_tree_depth(my_tree)
    first_str = my_tree.keys()[0]     #the text label for this node should be this
    center_point = (plot_tree.xOff + (1.0 + float(num_leafs))/2.0/plot_tree.totalW, plot_tree.yOff)
    plot_mid_text(center_point, parent_point, node_text)
    plot_node(first_str, center_point, parent_point, decision_node)
    second_dict = my_tree[first_str]
    plot_tree.yOff = plot_tree.yOff - 1.0/plot_tree.totalD
    for key in second_dict.keys():
        if type(second_dict[key]).__name__=='dict':#test to see if the nodes are dictonaires, if not they are leaf nodes
            plot_tree(second_dict[key],center_point,str(key))        #recursion
        else:   #it's a leaf node print the leaf node
            plot_tree.xOff = plot_tree.xOff + 1.0/plot_tree.totalW
            plot_node(second_dict[key], (plot_tree.xOff, plot_tree.yOff), center_point, leaf_node)
            plot_mid_text((plot_tree.xOff, plot_tree.yOff), center_point, str(key))
    plot_tree.yOff = plot_tree.yOff + 1.0/plot_tree.totalD
#if you do get a dictonary you know it's a tree, and the first element will be another dict

def create_plot(in_tree):
    fig = plt.figure(1, facecolor='white')
    fig.clf()
    ax_props = dict(xticks=[], yticks=[])
    create_plot.ax1 = plt.subplot(111, frameon=False, **ax_props)    #no ticks
    #createPlot.ax1 = plt.subplot(111, frameon=False) #ticks for demo puropses
    plot_tree.totalW = float(get_number_of_leafs(in_tree))
    plot_tree.totalD = float(get_tree_depth(in_tree))
    plot_tree.xOff = -0.5/plot_tree.totalW; plot_tree.yOff = 1.0;
    plot_tree(in_tree, (0.5,1.0), '')
    plt.show()

#def create_plot():
#    fig = plt.figure(1, facecolor='white')
#    fig.clf()
#    createPlot.ax1 = plt.subplot(111, frameon=False) #ticks for demo puropses
#    plotNode('a decision node', (0.5, 0.1), (0.1, 0.5), decisionNode)
#    plotNode('a leaf node', (0.8, 0.1), (0.3, 0.8), leafNode)
#    plt.show()

def retrieve_tree(i):
    list_of_trees =[{'no surfacing': {0: 'no', 1: {'flippers': {0: 'no', 1: 'yes'}}}},
                  {'no surfacing': {0: 'no', 1: {'flippers': {0: {'head': {0: 'no', 1: 'yes'}}, 1: 'no'}}}}
                  ]
    return list_of_trees[i]

#create_plot(thisTree)