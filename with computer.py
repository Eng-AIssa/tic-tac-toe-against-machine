from copy import deepcopy


class Node:
    def __init__(self,s,a=None, p=None, c=0,u_v=None):
        self.state=s
        self.action=a
        self.parent=p
        self.cost=c
        self.utility_value = u_v



class TicTacToe:

    def __init__(self,c):
        self.__value =[[" "," "," "],[" "," "," "],[" "," "," "]]
        self.cost=c


    def MINMAXDIS(self):
        x = self.__value[:]
        n=Node(x)
        returned_action = self.MaxValue(n)
        return returned_action[1]


    def MaxValue(self,n):
        if self.Terminal_test(n,"O"):
            return (n.utility_value,0)

        n1=n
        value = -1000
        for i in self.CreateChild(n,'X'):
            min_result =self.MinValue(i)
            v = max(value,min_result)
            if min_result==value:
                if self.CheckWin("X",i.state):
                    n1=i
            if v > value:
                value=v
                n1=i

        return (value,n1.action)

    
    def MinValue(self,n):
        if self.Terminal_test(n,"X"):
            return n.utility_value

        value = 1000
        for i in self.CreateChild(n,'O'):
            max_result = self.MaxValue(i)
            value = min(value,max_result[0])

        return value


    def Terminal_test(self,n,player):
        if(self.CheckWin(player,n.state)):
            return True
        if(self.CheckDraw(n.state)):
            return True
        if(n.cost==self.cost):
            return True


    def Utility(self,state,a):
        result=[]
        for w in ["X","O"]:
            
            value = 0

            if(self.CheckWin("X",state)):
                return 10
            if(self.CheckWin("O",state)):
                return -10
        
            for i in state:
                value1 = self.Count(i,w)    #الصفوف
                value = value + value1

            x=[]
            for i in range(3):
                for j in range(3):
                    x.append(state[j][i])
                value2 = self.Count(x,w)    #الاعمدة
                value = value + value2
                x.clear()


            value3 = self.Count([state[0][0],state[1][1],state[2][2]],w)  #الاقطار
            value = value + value3
            value3 = self.Count([state[0][2],state[1][1],state[2][0]],w)
            value = value + value3

            result.append(value)
        
        return result[0]-result[1]


    def Count(self,a,b):
        counter = 0
        for i in a:
            counter=counter+1
            if i!=b and i!=" ":
                return 0
            elif counter==3:
                return 1


    def CreateChild(self,n,a):
        if(a=="X"):
            b="O"
        else:
            b="X"
        edited_state = deepcopy(n.state)
        ChildList=[]
        for i in range(3):
            for j in range(3):
                if edited_state[i][j]==" ":
                    edited_state[i][j]=a
                    newnode=Node(edited_state, str(i)+str(j),n, n.cost+1,self.Utility(edited_state,b))
                    ChildList.append(newnode)
                    edited_state = deepcopy(n.state)
        return ChildList




#------------------------------------------------------------------------------------------------------

        

    def DrawBoard(self):
        o=0
        for i in self.__value:
            for j in range(3):
                o = o+1
                if j!=2:
                    print (" "+i[j]+" |",end="")
                else:
                    print (" "+i[j])
                    if o!=9:
                        print("------------")


    def clearBoard(self):
        for i in self.__value:
            for j in range(3):
                i[j]=" "

    def newGame(self):
        while True:
            i = input("Do want to play again (y: Yes, N: No):")
            if i=='y' or i=='Y':
                self.clearBoard()
                self.DrawBoard()
                print()
                return True
            if i=='N' or i=='n':
                print("Than you.")
                return False    
            print("Wrong insertion, try again")

    def Set(self,v):
        self.__value[int(v[0])][int(v[1])] = "X"
    
    def Play(self,a):
        flag=True
        while flag:
            i = input("Player '"+a+"', enter your move (row[1-3] column[1-3]):")
            v = self.CheckEntery(i)
            if v[0]:
                self.__value[v[1]][v[2]] = a
                flag=False

    def CheckDraw(self,state=0):
        if state == 0:
            state=self.__value
        for i in state:
            for j in range(3):
                if i[j]==" ":
                    return False
        if state == 0:
            print("it's a draw")
        return True

    def CheckWin(self,a,state=0):
        x=[]
        if state == 0:
            state=self.__value
        for i in state:
            if self.CheckRow(i,a):
                return True
        for i in range(3):
            for j in range(3):
                x.append(state[j][i])
            if self.CheckColumn(x,a):
                return True
            x=[]
        if self.CheckDiagonal(a,state):
            return True
        return False

    def CheckColumn(self,a,b):
        for i in a:
            if i!=b:
                return False
        return True
                
    
    def CheckRow(self,a,b):
        for i in a:
            if i!=b:
                return False
        return True
            
            
    def CheckDiagonal(self,a,state):
        if state[1][1]==" ":
            return False
        if (state[0][0]==state[1][1]==state[2][2]==a or state[0][2]==state[1][1]==state[2][0]==a):
            return True
        return False

    def CheckEntery(self,b):
        v=[]
        for i in b:
            if i!=" ":
                v.append(i)
        if len(v)>2 or len(v)<2:
            print("Wrong insertion values must be 2 numbers, try again")
            return [False,]
        for i in range(2):
            if not v[i].isdigit():
                print("Wrong insertion only numbers are allowed, try again")
                return [False,]
            v[i]=int(v[i])-1
        
        if v[0]>2 or v[0]<0 or v[1]>2 or v[1]<0:
            print("Wrong insertion out of range[1-3], Try again…")
            return [False,]
        if self.__value[v[0]][v[1]]!=" ":
            print("This move at ("+str(v[0]+1)+","+str(v[1]+1)+") is not valid. Try again…")
            return [False,]
        return [True,v[0],v[1]]

    
depth=input("choose depth of tree(number) bigger number means smarter computer:")
p = TicTacToe(int(depth))
flag= True
while flag:
    p.Play("O")
    p.DrawBoard()
    print()
    if p.CheckWin('O'):
        print("You Won!")
        flag = p.newGame()
    else:
        if p.CheckDraw():
            print("it's a Draw!")
            flag = p.newGame()
        else:
            print("Computer Move:")
            action = p.MINMAXDIS()
            p.Set(action)
            p.DrawBoard()
            print()
            if p.CheckWin('X'):
                print("Computer Won!")
                flag = p.newGame()

