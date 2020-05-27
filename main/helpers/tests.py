# from django.test import TestCase

# # Create your tests here.
# import smtplib, ssl

# port = 465  # For SSL
# password = input("Type your password and press enter: ")

# # Create a secure SSL context
# context = ssl.create_default_context()

# sender_email = "inyangete@gmail.com"
# receiver_email = "kboysreel@gmail.com"
# user = "omotayo"
# message = f"""{user} logged in"""

# with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
#     server.login("inyangete@gmail.com", password)
#     # TODO: Send email here
#     server.sendmail(sender_email, receiver_email, message,)

# import requests

# response = requests.get("""http://resolute40.pythonanywhere.com/get_data?user=shola&start=2018-07-06&end=2018-07-07""")

# data = response.json()

# import os

# cwd = os.getcwd()

# x = [{"a":23}, {"b":32}]

# # y = map(lambda x: x["a"] = x["a"] *8 )

# code = '''
# def myfunc():
#     return "hello works"

# # print("yeah")
# dee = "bla"
# '''

# file = open(cwd+"\\main\helpers\code.py", "w")
# file.write(code)
# file.close()

# import code

# # # print(cwd)
# code.dee
# # print(code.myfunc())

consumption_table = {
                            "0-10"   :  [0.9, 1.2, 1.7, 2.1], 
                            "11-12"  :  [1.0, 1.4, 2.1, 2.6], 
                            "13-15"  :  [1.3, 1.8, 2.6, 3.2], 
                            "16-20"  :  [1.7, 2.4, 3.5, 4.3], 
                            "21-25"  :  [2.1, 3.0, 4.3, 5.4], 
                            "26-30"  :  [2.6, 3.6, 5.2, 6.4], 
                            "31-40"  :  [3.4, 4.8, 7.0, 8.6], 
                            "41-50"  :  [4.3, 6.0, 8.6, 10.7], 
                            "51-75"  :  [6.4, 9.0, 12.7, 16.1], 
                            "76-100" : [8.3, 11.9, 16.1, 21.4], 
                            "101-150": [10.9, 17.3, 24.1, 32.1], 
                            "151-200": [14.1, 22.9, 32.7, 42.8], 
                            "200-250": [17.4, 28.6, 40.8, 53.5], 
                            "251-350": [23.7, 39.3, 56.0, 74.9], 
                            "351-500": [33.3, 55.6, 79.6, 107.0]
                            }
gen_cap = 102
load_factor = 0.1
keys = list(consumption_table.keys())
# print(keys)

for key in keys:
    lower_bound, upper_bound = int(key.split("-")[0]), int(key.split("-")[1])
    key_range = range(lower_bound, upper_bound+1)

    if gen_cap in key_range:
        # print(key_range)
        consumption_list = consumption_table[key]
        possibles = [0.25, 0.5, 0.75, 1]

        if load_factor <= 1 and load_factor > 0.75 or load_factor > 1: consumption_key = 3 
        elif load_factor <= 0.75 and load_factor > 0.5:consumption_key = 2
        elif load_factor <= 0.5 and load_factor > 0.25:consumption_key = 1
        elif load_factor < 0.25:consumption_key = 0

        consumption = consumption_list[consumption_key]
        # print(consumption)
        