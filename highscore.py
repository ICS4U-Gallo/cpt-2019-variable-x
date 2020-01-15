import json


sorted_list = []
user = int(input("Enter a value: "))

def bubblesort(numbers):
    n = len(numbers)

    for i in range(n):
        for j in range(n - i - 1):
            if numbers[j] < numbers[j + 1]:
                numbers[j], numbers[j+1] = numbers[j+1], numbers[j]

    return numbers




with open("data.json", "r") as f:
    data = json.load(f)
    


data[f"user {len(data) + 1}"] = user

with open("data.json", 'w') as f:
    json.dump(data, f)


def score_board():
    with open("data.json", "r") as f:
        data = json.load(f)

    for values in data.values():
        sorted_list.append(values)
        bubblesort(sorted_list)
   

    for i in range(len(sorted_list)):
        print(f" {i + 1}. {sorted_list[i]}")
        

result = score_board()
print(result)

