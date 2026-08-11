from pydantic import BaseModel


class Address(BaseModel):
    city: str
    pin: str
    street: str


class Student(BaseModel):
    name: str
    age: int
    address: Address


address_payload = {
    "city": "Peshawar",
    "pin": "1232",
    "street": "Hassan Khel"
}

address = Address(**address_payload)

student_payload = {
    "name": "zulkaif",
    "age": 12,
    "address": address
}

student = Student(**student_payload)


print(student)
print(student.address.pin)

temp = student.model_dump() 
# this convert the pydantic class into python dictonary

print(temp)
print(type(temp))

temp_json = student.model_dump_json() # this convert into json 
print(temp_json)
print(type(temp_json))

# can also include and exclude 
temp_exclude = student.model_dump_json(exclude=['name'])
print(temp_exclude)