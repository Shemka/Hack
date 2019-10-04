import pandas as pd

a = r'C:\Users\MSI1\Desktop\Хакатон.xlsx'
app = pd.read_excel(a, sheet_name='График', )
employees = pd.DataFrame(app[:25])
drivers = pd.DataFrame(app[25:])
print(employees)
print('\n\n\n')
print(drivers)