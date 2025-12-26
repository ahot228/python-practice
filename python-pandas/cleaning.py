import pandas as pd

employees_raw = pd.read_csv("../data_raw/employees.csv")
sales_raw = pd.read_csv("../data_raw/sales_data.csv")
students_raw = pd.read_csv("../data_raw/students.csv")

## NA and Duplicate Checks
na_employees = employees_raw.loc[employees_raw[["name", "age", "salary"]].isna().any(axis=1)]
print(na_employees)
duplicates_employees = employees_raw.duplicated(subset=["name","age","salary"])
print(duplicates_employees)
na_sales = sales_raw.loc[sales_raw[["customer", "region", "units_sold", "revenue"]].isna().any(axis=1)]
print(na_sales)
duplicates_sales = sales_raw.duplicated(subset=["customer", "region", "units_sold", "revenue"])
print(duplicates_sales)
na_students = students_raw.loc[students_raw[["name", "math_score", "science_score", "grade"]].isna().any(axis=1)]
print(na_students)
duplicates_students = students_raw.duplicated(subset=["name", "math_score", "science_score", "grade"])
print(duplicates_students)

## Employees
employees = employees_raw
employees.drop_duplicates(subset=["name","age","salary"], inplace = True)

# name
employees.dropna(subset=["name"], inplace= True)

# age
for x in employees.index:
  if employees.loc[x, "age"] > 100 or employees.loc[x, "age"] < 0:
    employees.loc[x, "age"] = pd.NA
med_age = employees["age"].median()
employees.fillna({"age": med_age}, inplace = True)

# salary
employees["salary"] = pd.to_numeric(employees["salary"], errors='coerce')
Q1_salary = employees["salary"].quantile(0.25)
Q3_salary = employees["salary"].quantile(0.75)
IQR_salary = Q3_salary - Q1_salary
lower_salary = Q1_salary - 1.5 * IQR_salary
upper_salary = Q3_salary + 1.5 * IQR_salary
mean_salary = employees.loc[(employees["salary"] >= lower_salary) & (employees["salary"] <= upper_salary),"salary"].mean()
employees.loc[(employees["salary"] < lower_salary) | (employees["salary"] > upper_salary),"salary"] = mean_salary
employees.fillna({"salary": mean_salary}, inplace = True)

# final checks on table
employees = employees.astype({"id": int, "name": str,"age": int,"salary": float})
print(employees.to_string())
print(employees.info())

## Sales
sales = sales_raw
sales.drop_duplicates(subset=["customer", "region", "units_sold", "revenue"], inplace = True)

# units_sold
Q1_units_sold = sales["units_sold"].quantile(0.25)
Q3_units_sold = sales["units_sold"].quantile(0.75)
IQR_units_sold = Q3_units_sold - Q1_units_sold
lower_units_sold = Q1_units_sold - 1.5 * IQR_units_sold
upper_units_sold = Q3_units_sold + 1.5 * IQR_units_sold
mean_units_sold = sales.loc[(sales["units_sold"] >= lower_units_sold) & (sales["units_sold"] <= upper_units_sold),"units_sold"].mean()
sales.loc[(sales["units_sold"] < lower_units_sold) | (sales["units_sold"] > upper_units_sold),"units_sold"] = mean_units_sold
sales.fillna({"units_sold": mean_units_sold}, inplace = True)

# revenue
Q1_revenue = sales["revenue"].quantile(0.25)
Q3_revenue = sales["revenue"].quantile(0.75)
IQR_revenue = Q3_revenue - Q1_revenue
lower_revenue = Q1_revenue - 1.5 * IQR_revenue
upper_revenue = Q3_revenue + 1.5 * IQR_revenue
mean_revenue = sales.loc[(sales["revenue"] >= lower_revenue) & (sales["revenue"] <= upper_revenue),"revenue"].mean()
sales.loc[(sales["revenue"] < lower_revenue) | (sales["revenue"] > upper_revenue),"revenue"] = mean_revenue.round(2)
sales.fillna({"revenue": mean_revenue.round(2)}, inplace = True)

# final checks on table
sales = sales.astype({"order_id": int, "customer": str, "region": str, "units_sold": int,"revenue": float})
print(sales.to_string())
print(sales.info())

## Students
students = students_raw

# math_score
students["math_score"] = pd.to_numeric(students["math_score"], errors='coerce')
for x in students.index:
  if students.loc[x, "math_score"] > 100 or students.loc[x, "math_score"] < 0:
    students.loc[x, "math_score"] = pd.NA

students["math_score"] = students["math_score"].fillna(students["science_score"])

# science_score
students["science_score"] = pd.to_numeric(students["science_score"], errors='coerce')
for x in students.index:
  if students.loc[x, "science_score"] > 100 or students.loc[x, "science_score"] < 0:
    students.loc[x, "science_score"] = pd.NA

students["science_score"] = students["science_score"].fillna(students["math_score"])

# grade
students["grade"] = pd.Categorical(
    students["grade"],
    categories=['A','B','C','D','F'],
    ordered=True
)
for x in students.index:
  if students.loc[x, "science_score"] >= students.loc[x, "math_score"] and pd.isna(students.loc[x, "grade"]):
    if students.loc[x, "science_score"] >= 90:
      students.loc[x, "grade"] = 'A'
    elif students.loc[x, "science_score"] >= 80:
      students.loc[x, "grade"] = 'B'
    elif students.loc[x, "science_score"] >= 70:
      students.loc[x, "grade"] = 'C'
    elif students.loc[x, "science_score"] >= 60:
      students.loc[x, "grade"] = 'D'  
    else:
      students.loc[x, "grade"] = 'F' 
  elif students.loc[x, "math_score"] >students.loc[x, "science_score"] and pd.isna(students.loc[x, "grade"]):
    if students.loc[x, "math_score"] >= 90:
      students.loc[x, "grade"] = 'A'
    elif students.loc[x, "math_score"] >= 80:
      students.loc[x, "grade"] = 'B'
    elif students.loc[x, "math_score"] >= 70:
      students.loc[x, "grade"] = 'C'
    elif students.loc[x, "math_score"] >= 60:
      students.loc[x, "grade"] = 'D'  
    else:
      students.loc[x, "grade"] = 'F' 

# final checks on table
students = students.astype({"student_id": str, "name": str, "math_score": int, "science_score": int, "grade": "category"})
print(students.to_string())
print(students.info())