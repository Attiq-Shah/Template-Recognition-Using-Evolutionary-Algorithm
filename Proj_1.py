
import cv2 as cv
import numpy as np
from numpy import random
# import random
from matplotlib import patches
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle


group = cv.imread("groupGray.jpg", 0)
boothi = cv.imread("boothiGray.jpg", 0)


groupRows, groupCol = group.shape


boothiRows, boothiCol = boothi.shape

# print(group)
# cv.imshow("Group-Image",group)
# cv.imshow("Boothi-Image",boothi)
# cv.rectangle(group,(200,438),(100,100),(255,0,0))
# cv.imshow("img", group)
# cv.waitKey(0)
# cv.destroyAllWindows()


# arr = np.array(group)
# rows = arr[100:140]
# col = arr[100:140,635:670]
# cv.imshow("half", col)
# cv.waitKey(0)
# cv.destroyAllWindows()


def Initialize_Population(Group_Row, Group_Col, Size):
    Current_Generation = []
    Count = 0
    while Count < Size:
        row = random.randint(Group_Row)
        col = random.randint(Group_Col)
        if row + boothi.shape[0] > Group_Row or col + boothi.shape[1] > Group_Col:
            Count = Count
        else:
            Current_Generation.append(tuple([row, col]))
            Count += 1
    return Current_Generation



# print(Current_Gen)

def correlation_coefficient(T1, T2):
    numerator = np.mean((T1 - T1.mean()) * (T2 - T2.mean()))
    denominator = T1.std() * T2.std()
    if denominator == 0:
        return 0
    else:
        result = numerator / denominator
        return result

def Fitness_Evaluation(Current_Gen, Source_Img, Test_Img):
    Small_Img = []
    Corelation_Val = {}
    for i in range(len(Current_Gen)):
        Small_Img.append(Source_Img[Current_Gen[i][0]:Current_Gen[i][0] + boothi.shape[0], Current_Gen[i][1]:Current_Gen[i][1] + boothi.shape[1]])
        
    for i in range(len(Small_Img)):
        # Corelation = cv.matchTemplate(Small_Img[i], Test_Img, cv.TM_CCOEFF_NORMED)
        Corelation = correlation_coefficient(Small_Img[i], Test_Img)
        Corelation = round(Corelation, 2)
        # Corelation_Val.append(Corelation[0][0])
        Corelation_Val.update({Current_Gen[i]:Corelation})
    
    return Corelation_Val
    
    

# print(Fitness_Val)

def Selection(Fitness_Values):
    Selected_Gen = {}
    for key, value in sorted(Fitness_Values.items(), key=lambda kv: kv[1], reverse=True):
        Selected_Gen.update({key : value})
    
    return Selected_Gen


# # print(Selected_Gen)

def Binary_9_Bits(Number):
    Bin_List = []
    i = 1 << 8
    while i > 0:
        if Number & i != 0:
            Bin_List.append(1)
        else:
            Bin_List.append(0)
        i = i // 2
    return Bin_List

def Binary_10_Bits(Number):
    Bin_List = []
    i = 1 << 9
    while i > 0:
        if Number & i != 0:
            Bin_List.append(1)
        else:
            Bin_List.append(0)
        i = i // 2
    return Bin_List

# # #Test Case
# # point1 = (10,20)
# # point2 = (20,30)

# Current_Gen = [(20,30),(12,25),(35,40),(40,50)]


def Mutation(Current_Gen_Dict):
    Current_Gen = []
    Mutated_Gen = []
    for key in Current_Gen_Dict.keys():
        Current_Gen.append(key)
    i = 0
    while i < len(Current_Gen)-1:
        j = i + 1
        Bin_Point1 = Binary_9_Bits(Current_Gen[i][0])
        Bin_Point2 = Binary_10_Bits(Current_Gen[i][1])
        
        Bin_Point3 = Binary_9_Bits(Current_Gen[j][0])
        Bin_Point4 = Binary_10_Bits(Current_Gen[j][1])
# print(Bin_Point1)
# print(Bin_Point2)
        L1 = Bin_Point1 + Bin_Point2
        L2 = Bin_Point3 + Bin_Point4

        random_point = random.randint(19)
# print(random_point)
        Slice1, Slice2 = L1[:random_point], L1[random_point:]
        Slice3, Slice4 = L2[:random_point], L2[random_point:]
# print(Slice1)
# print(Slice4)
        Cross_Over1, Cross_Over2 = Slice1 + Slice4, Slice2 + Slice3

# print(Cross_Over1)
        New_X1, New_Y1 = Cross_Over1[:9], Cross_Over1[9:]
        New_X2, New_Y2 = Cross_Over2[:9], Cross_Over2[9:]
        num1 = ""
        num2 = ""
        num3 = ""
        num4 = ""
        for elem in New_X1:
            num1 = num1+str(elem)

        for elem in New_Y1:
            num2 = num2+str(elem)
            
        for elem in New_X2:
            num3 = num3+str(elem)
            
        for elem in New_Y1:
            num4 = num4+str(elem)

        # print(New_X1)
        # print(New_Y1)
        New_X1 = int(num1,2)
        New_Y1 = int(num2,2)
        New_X2 = int(num3,2)
        New_Y2 = int(num4,2)
        
        # print([New_X1,New_Y1], [New_X2, New_Y2])
        if New_X1 + boothiRows > groupRows or New_Y1 + boothiCol > groupCol :
            i = i
        elif New_X2 + boothiRows > groupRows or New_Y2 + boothiCol > groupCol:
            i = i
        else:
            Mutated_Gen.append(tuple([New_X1, New_Y1]))
            Mutated_Gen.append(tuple([New_X2, New_Y2]))
            i += 2
            
    return Mutated_Gen

# print(New_Generation)

BestFitter = []
Current_Gen = Initialize_Population(groupRows, groupCol, 500)
for i in range(100):
    Fitness_Val = Fitness_Evaluation(Current_Gen, group, boothi)
    x = []
    y = []
    for key in Fitness_Val.keys():
        x.append(key)
        y.append(Fitness_Val[key])
        
    if y[0] >= 0.85:
        print("Corelation: ",y[0])
        BestFitter.append(y[0])
        break
    Selected_Gen = Selection(Fitness_Val)

    New_Generation = Mutation(Selected_Gen)
    Current_Gen = New_Generation
    
# print(Selected_Gen)


x = []
y = []
for key in Selected_Gen.keys():
    x.append(key)
    y.append(Selected_Gen[key])
    
Point = x[0]
print(Point)

# fig, (xy, ax2) = plt.subplots(1,2, figsize=(20,8))
# xy.imshow(group, cmap='gray')
# Imgrect = patches.Rectangle(
#     (Point[0], Point[1]), 30, 30, linewidth=2, edgecolor='b', facecolor='none')
# xy.add_patch(Imgrect)
# plt.show()


# fig = plt.figure()
  
# ax = fig.add_subplot(111)
# ax.imshow(group, cmap = plt.cm.gray)
# ax.add_patch( Rectangle((Point[0], Point[1]),
#                         30, 30,
#                         fc ='none', 
#                         ec ='g',
#                         lw = 1.5) )
  
# plt.show()
    
    
# print(x)
# print(y)
# plt.plot(x,y)
# plt.xlabel("Generation_Points")
# plt.ylabel("Corelation")
# plt.title("Graph")
# plt.show()
# New_Generation = Mutation(Selected_Gen)

# print(len(New_Generation))
# NewFit = Fitness_Evaluation(New_Generation, group, boothi)

# print(NewFit)



# Max = Selected_Gen[1][0]
# Max_Points = Selected_Gen[0][0]






# Img = cv.rectangle(group,(Max_Points[0],Max_Points[1]),(Max_Points[0]+35,Max_Points[1]+29),(255,0,0))
# cv.imshow("Img",Img)
# cv.waitKey(0)
# cv.destroyAllWindows()
# print(New_Generation)
# print(New_Fit)
# while True:
#     Fitness_Val = Fitness_Evaluation(Current_Gen, group, boothi)
#     Selected_Gen = Selection(Fitness_Val)
#     if Fitness_Val[Selected_Gen[0]] > 0.85000000000000000000000000:
#         print("Fitness Match")
#         print(Selected_Gen[0])
#     else:
#         New_Generation = New_Gen(Selected_Gen)
#         Current_Gen = New_Generation
# # print(Fitness_Val)
# print(Selected_Gen)

# print(Corelation)
# find_max = max(Corelation_Val, key=Corelation_Val.get)
# print(find_max)
# img = Small_Img[find_max]
# cv.imshow("img",img)
# cv.waitKey(0)
 
# for i in range(len(Current_Gen)):
#         if len(Small_Img[i][0]) == len(boothi[0]) and len(Small_Img[i]) == len(boothi):
#             numerator = np.mean(
#                 (Small_Img[i] - Small_Img[i].mean()) * (boothi - boothi.mean()))
#             denominator = Small_Img[i].std() * boothi.std()
#             if denominator == 0:
#                 Corelation_Val.append(0)
#             else:
#                 result = numerator / denominator
#                 Corelation_Val.append(result)
#         else:
#             Corelation_Val.append(-1)
# Corelation_Val = [round(num, 2) for num in Corelation_Val]
    # return Corelation_Val
# print(Corelation_Val)


# find_max = max(Corelation_Val)
# ind = Corelation_Val.index(find_max)


# for i in range(len(Current_Gen)):
#     Corelation = np.corrcoef(Small_Img[i],boothi)[1, 0]
#     Corelation_Val.update({i:Corelation})
    
    # print(Corelation)
    
# print(Corelation_Val)
# #     # Corelation_Val.append(Corelation)
# #     # print(Corelation)
# # print(Corelation_Val)
# # # sort = sort(Corelation_Val)


