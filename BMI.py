import math

weight = float(raw_input("Insert weight in kg: "))
height = float(raw_input("Insert height in cm: "))
age = int(raw_input("Insert age: "))

bmr = (10.0*weight) + (6.25*height) - (5*age) + 5
bmi = weight/pow(height/100,2)

print("BMR is " + str(bmr))
print("BMI is " + str(bmi))
