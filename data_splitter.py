# import csv

f = open("./dataset/taxi_data.csv")
data = open("data_1996.csv", 'a')
data2 = open("data_3998.csv", 'a')
half_1a = (next(f) for i in range(5000))
# # half_1b = (next(f) for i in range(47))
# half_2a = (next(f) for i in range(47))
# # half_2b = (next(f) for i in range(51))
count = 1
for line_1a in half_1a:
    print(count, line_1a[:50])
    data.write(line_1a)
    count +=1
#     if count > 1997:
#         break
#
# for line_2a in half_2a:
#     print(count, line_2a[:50])
#     data.write(line_2a)
#     count += 1