howoften1 = int(input())
howoften2 = int(input())
runtime = int(input())
howoften1list = [howoften1 * i for i in range(runtime)]
howoften2list = [howoften2 * i for i in range(runtime)]
sunseen = 0
for i in range(runtime):
    if i % 2 == 0:
        for j in range(runtime):
            if howoften1list[j] > i:
                break
            elif howoften1list[j] == i:
                sunseen += 1
    else:
        for j in range(runtime):
            if howoften2list[j] > i:
                break
            elif howoften2list[j] == i:
                sunseen += 1
print(sunseen)