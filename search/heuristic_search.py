#a_star.py
import queue.py # the one in example code
def search(initial_node, goal_node, graph, heuristic):
    """
    finds the shortest path from initial_node to goal_node on graph
    returns the shortest path, or returns None if there is no path
    """
    
    ## setup queue
    open_nodes = MinHeap() # from queue.py
    closed_nodes = []
    previous_node = {}
    
    ## setup first node
    open_nodes.insert(initial_node, heuristic(initial_node))
    
    while open_nodes:
        next_node = open_nodes.extract()
        if next_node == goal_node:
            break
        for new_node, edge_weight in next_node.get_edges():
            if new_node in closed_nodes:
                continue
            if new_node not in all_nodes:
                all_nodes.append(new_node)
                new_node_key += 1
            new_node_key = all_nodes.index(new_node)
    else:
        return None
        
    
    #the action matrix holds what action it took to get to that point on the map
    action=[[-1 for row in map[0]] for col in map] 
    dim=[len(map),len(map[0])]   #remember dimensions
    # heuristic function is the distance from the goal without obstacles
    heuristic=[[abs(goal[0]-i)+abs(goal[1]-j) for j in range(dim[1])]\
    for i in range(dim[0])]
    moves=[[-1,0],[0,-1],[1,0],[0,1]]  # possible moves from each point
    closed[init[0]][init[1]]=True      # close the initial spot
    g=0                                # g value of initial spot
    f=g+heuristic[init[0]][init[1]]    # f value of initial spot
    open=[[f,g,init[0],init[1]]]
    done=False
    while not done:
        if len(open)==0:
            done=True
            return  #if open is empty return None
        else:
            # choose the box with the lowest f value then the lowest g val
            open.sort()
            bestF=open[0][0]
            bestG=open[0][1]
            for i in range(len(open)):
                if open[i][0]==bestF:
                    if open[i][1]<=bestG:
                        index=i
                        bestG=open[0][1]
            expand=open[index]
            f=expand[0]
            g=expand[1]
            x=expand[2]
            y=expand[3]
            open.remove(expand) # remove from open
            
            if goal[0]==x and goal[1]==y: #did we make it to the goal
                done=True                     
                minLen=g                   # the shortest path has that g value
                break
            ##
            for m in range(len(moves)):  #expand all the possible moves
                newX=x+moves[m][0]
                newY=y+moves[m][1]
                #check if within map
                if newX>=0 and newX<dim[0] and newY>=0 and newY<dim[1]:
                    if not closed[newX][newY]:  
                        open.append([g+heuristic[newX][newY]+1,g+1,newX,newY])
                        action[newX][newY]=m
                        closed[newX][newY]=True
    # create path backwards from action
    pos=[goal[0],goal[1]] # start from the end
    # path should be one longer than the number of moves
    revPath=[[0,0] for i in range(minLen+1)] 
    # initialize the first part of the path
    revPath[0][0]=pos[0]
    revPath[0][1]=pos[1]
    for i in range(1,minLen+1):
        if action[pos[0]][pos[1]]!=-1:
            move=moves[action[pos[0]][pos[1]]]
            #move backwards from last position
            pos[0]-=move[0]
            pos[1]-=move[1]
        revPath[i][0]=pos[0]
        revPath[i][1]=pos[1]
    path=revPath[::-1]# reverse the path
    return path # return path
