import uuid

myuuid = uuid.uuid4()

print('Your UUID is: ' + str(myuuid))
print(type(myuuid))
print(type(f"{myuuid}"))