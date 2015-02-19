import sys, numpy, random

def load_train_data(train_data_file_name):
    train_data_list = []
    f = open(train_data_file_name)
    for line in f.readlines():
        tmp = line.replace('\n', '').replace('\r', '').replace('\t', ' ').split(" ")
        x = [1.0]

        for i in range(len(tmp)):
            if i == len(tmp) - 1:
                y = int(tmp[i])
            else:
                x.append(float(tmp[i]))

        train_data_list.append((numpy.array(x), y))
    return train_data_list

def learn(weight_vector, train_data_list, order_type, eta):
    update_counter = 0
    order = gen_order(order_type, len(train_data_list))

    while 1:
        mistake_counter = 0
        for i in order:
            data = train_data_list[i]
            if numpy.dot(weight_vector, data[0]) > 0:
                result = 1
            else:
                result = -1

            if result != data[1]:
                weight_vector = weight_vector + eta * data[1] * data[0]
                mistake_counter = mistake_counter + 1

        if mistake_counter == 0:
            return update_counter
        else:
            update_counter = update_counter + mistake_counter

def gen_order(order_type, len):
    if order_type == "pre_random":
        random.seed()
        return random.sample(range(len), len)
    else:
        return range(len)

def main():
    train_data_file_name = sys.argv[1]
    order_type = sys.argv[2]
    times = int(sys.argv[3])
    eta = float(sys.argv[4])

    weight_vector = numpy.array([0.0, 0.0, 0.0, 0.0, 0.0])

    train_data_list = load_train_data(train_data_file_name)

    total_update = 0
    for i in range(times):
        total_update = total_update + learn(weight_vector, train_data_list, order_type, eta)

    print "%d times, average = %f updates" % (times, total_update/times)

if __name__ == '__main__':
    main()
