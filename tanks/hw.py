class item():
    def __init__(self, name, weight, cost):
        self.name = name
        self.weight = weight
        self.cost = cost
        
class backpack():
    def __init__(self, maxweight):
        self.maxweight = maxweight
        self.itemlist = []
        self.totWeight = 0
        self.totCost = 0
        
    def additem(self, item):
        if self.totWeight + item.weight > self.maxweight:
            print(f"предмет {item.name} слишком тяжелый")
        else:
            self.itemlist.append(item)
            self.totWeight += item.weight
            self.totCost += item.cost
        
    def get_total_weight(self):
        return self.totWeight
    
    def get_total_cost(self):
        return self.totCost
    
    
    
a = item("арбуз", 5, 100)
b = item("гиря", 100, 50)
c = backpack(105)
c.additem(a)
c.additem(b)
print(c.get_total_cost())
print(c.get_total_weight())