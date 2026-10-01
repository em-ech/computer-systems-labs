int_values = []
max_values = 5

if __name__ == '__main__':
    n_values = 6
    even_sum = 0

    while n_values > max_values:
        n_values = int(input('How many values do you want to enter? '))

        if n_values > max_values:
            print(f'{max_values} is the maximum amount allowed')

    for i in range(n_values):
        int_values.append(int(input(f'Enter value {i + 1}: ')))

    for value in int_values:
        if value % 2 == 0:
            even_sum += value

    print(f'The values are {str(int_values)}')
    print(f'The sum of even values is {even_sum}')
