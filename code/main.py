import evaluate

while True:
    x = str(input('>>> '))

    try:
        print(evaluate.evaluate(x))
    except OverflowError:
        print('Result too large')

    if x == 'exit':
        break
