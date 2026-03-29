import json


human = {"age":40, "name" : "asdada", "married" : True, "kids" : None}

a = open("abc2.json", "w")

json.dump(human, a)

a = open("abc.json", "r")

b = json.load(a)

print(b)
print(b["age"])


a =  '{"age":40, "name" : "asdada", "married" : true, "kids" : null }'

b = json.loads(a)

print(b)
print(type(b))
a = json.dumps(b)
print(a)
print(type(a))

#a = open("abc.json", "r")
#b = json.load(a)
#print(type(b))
#c = open("abc2.json", "w")
#
#json.dump(b["age"], c)

