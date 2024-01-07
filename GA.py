import random
import math
import matplotlib.pyplot as plt

count=0
def getInt(list): #計算二進位改成十進位
    num=0
    for i in range(len(list)):
        num += list[i] * (2 ** (len(list)-1-i))   
    return num

def getFitness(list): #計算適應性--課本公式
    x = getInt(list[0:8])
    y = getInt(list[8:])
    x = x*0.0235294 - 3
    y = y*0.0235294 - 3
    return ((1-x)**2)* math.exp(-(x**2)-(y+1)**2) - (x-x**3-y**3) * math.exp (-(x**2)-(y**2))

def selection(probability): #輪盤法隨機挑出親代
    total_probability=sum(probability)
    random_num = random.uniform(0, total_probability)
    current_sum = 0
    for index, fitness in enumerate(probability):
        current_sum += fitness
        if current_sum > random_num:
            return index
            
def GA(list,numbers,mating,mutation): #基因演算
    fitness = []
    for i in range(numbers):
        fitness.append(getFitness(list[i]))
    global count
    count+=1
    average_fitness = sum(fitness) / numbers #平均適應性
    print('第',count,'代''  最佳適應性=',round(max(fitness),8),'   平均適應性=',round(average_fitness,8)) #顯示當前適應性
    y1.append(max(fitness))  #最佳適應性放入y1
    y2.append(average_fitness)  #平均適應性放入y2
    
    probability = [] #適應性比例陣列
    for i in range(numbers):
        probability.append(fitness[i]/sum(fitness))
    
    parents = []  #轉輪盤得出雙親進行交配運算
    for i in range(int(numbers/2)):
        parents.append([list[selection(probability)],list[selection(probability)]]) #選擇雙親 
        randomPlace=random.randint(1,14)  #隨機選擇交配位置
        if(random.uniform(0, 1) <=mating):   #交配
            offspring1 = parents[i][0][0:randomPlace]+parents[i][1][randomPlace:]
            offspring2 = parents[i][1][0:randomPlace]+parents[i][0][randomPlace:]
        else:
            offspring1 = parents[i][0]
            offspring2 = parents[i][1]
        list.append(offspring1)
        list.append(offspring2)
 
    for i in range(numbers*2):  #突變 
        if(random.uniform(0, 1) <=  mutation):
            ran=random.randint(0,15)
            list[i][ran] = list[i][ran] ^ 1
   
    
    for i in range(numbers): #依照適應性比對親代子代，挑選下一代
        if(getFitness(list[i])<getFitness(list[int(numbers/2)+i])): 
            list[i] , list[int(numbers/2)+i] = list[int(numbers/2)+i] , list[i]
    del list[numbers:]


numbers=int(input("種群大小: "))
mating=float(input("交配機率: "))
mutation=float(input("突變機率: "))
generations=int(input("進行幾代: "))
cols=16 #基因長度
x1 = []
y1 = []
y2 = []
list=[[random.randint(0,1) for _ in range(cols)]for _ in range(numbers)] #隨機產生初始基因
for i in list:
    print(i)
for n in range(generations):
    x1.append(n+1) 
    GA(list,numbers,mating,mutation)

#製圖
plt.plot(x1, y1, color='black',linewidth="1", markersize="3", marker=".",label="Best")
plt.plot(x1, y2, color='red', linewidth="1", markersize="3", marker=".", label="Average")
plt.xlabel('Generations')  
plt.ylabel('Fitness')
plt.legend()  
plt.title('Performance graph', fontsize="15") 
plt.show()