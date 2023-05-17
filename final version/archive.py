def exp(brain, s):
    f = open("brains/!" + s + ".txt", 'w')
    ans = ""
    
    for i in range(len(brain)):
        for j in range(len(brain[i])):
            ans += str(round(brain[i][j], 3))
            #for k in range(len(brain[i][j])):
                #ans += str(brain[i][j][k]) + " "
            if j < len(brain[i]) - 1:
                ans += ","
        if i < len(brain) - 1:
            ans += ";"
    
    f.write(ans)
    f.close()

def imp(s):
    f = open("brains/!" + s + ".txt", 'r')
    brain = []
    s = (f.read()).split(";")
    brain = s
    for i in range(len(brain)):
        brain[i] = brain[i].split(",")
        #for j in range(len(brain[i])):
            #print(brain)
            #brain[i][j] = list(map(float, brain[i][j].split()))
    f.close()
    return brain