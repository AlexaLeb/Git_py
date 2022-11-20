# f = open("file.rtf", "r")
# for somw_number in range(10):
#     data = f"me shiny data\n"
# f.write(data)

# raaded = f.readlines()
# print(raaded)
#
# f.close()

# with open("file.rtf", "r", encoding="utf-8") as f:
#     for line in f:
#         print(line)
#     print(f.closed)
# print(f.closed)

try:
    100/0
except ZeroDivisionError:
    print("На ноль делить нельзя")

