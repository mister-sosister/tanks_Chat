import queue
#abc = "привет"
#babc = abc.encode()
#pack = int.to_bytes(len(babc), 4, "big") + babc + b"asdfgjkdsgf"
#head = int.from_bytes(pack[:4], "big")
#body = pack[4:4+head]
#print(head)
#print(body)
#print(pack)
##чтобы не было ошибок с коол-вом байтов не отправлоять больше 1 сообщения\
    
#i = [1,2,3,4,5]
#i.remove()
#print(i)

#a = int(input())
##print(str(int(input())).replace("0", "").replace("1", ""))
#output = ""
#for i in a:
#    if i == "0" or i == "1":
#        pass
#    else:
#        output += i
#print(output)

#summ = 0
#a = 5
#b = 8
#while a <= 31:
#    summ += (a / b)
#    a += 2
#    b += 2
#print(round(summ, 3))

#a = input().split()
#
#shortest = 1000000
#word = ""
#newstr = ""
#for i in a:
#    if len(i) < shortest and i[-1] == "e":
#        shortest = len(i)
#        word = i
#    #else:
#        #if newstr == "":
#        #    newstr += i
#        #else:
#        #    newstr += f" {i}"
#        
#while word in a:
#    a.remove(word)
#print(" ".join(a))

#a = input().split()
#c = []
#d = []
#
#summ = 0
#outlist = []
#
#for i in b:
#   c.append(int(i))
#   if int(i) > 0:
#       d.append(int(i))
#       
#
#for i in c:
#    outlist.append(i)
#    if i > 0 and not i == sorted(d)[-1]:
#        summ += i
#    if i == sorted(d)[-1]:
#        outlist.append(summ)
#        
#print(summ)
#print(outlist)
        
#b = [int(i) for i in input().split()]
#maxin = b.index(max(b))
#positivesumm = sum([i for i in b[:maxin] if i > 0])
#b.insert(maxin + 1, positivesumm)
#print(b)

#maxtrix = [  [1, 2, 3, 4,5, 6],
#           [7, 8, 9, 10,90,12],
#           [13,14,15,16,17,18],
#           [19,20,21,22,23,24],
#           [25,40,27,28,29,30,],
#           [31,32,33,34,35,36]]
#
#
#maxup, maxdown = 0, 0
#iup, jup = 0, 0
#idown, jdown = 0, 0
#
#for i in range(len(maxtrix)):
#    for j in range(len(maxtrix)):
#        if i >= j and maxtrix[i][j] >= maxdown :
#           
#           idown, jdown = i, j
#           maxdown = maxtrix[i][j]
#        elif i < j and maxtrix[i][j] >= maxup:
#            
#            iup, jup = i, j
#            maxup = maxtrix[i][j]
#maxtrix[iup][jup], maxtrix[idown] [jdown] = maxtrix[idown][jdown], maxtrix[iup][jup]
#
#for i in maxtrix:
#    print(i)



#print([[j * 6 + i + 1 for i  in range(6)] for j in range(6)])

#print("123")

#a = []
#b = int(input())
#while b != 0:
#    a.append(b)
#    b = int(input())
#a.sort()
#print(a[-1] + a[-2])
#print(a[0] + a[1])

a = queue.Queue()
a.put(1)
a.put(1)
a.put(1)
print(list(a.queue))