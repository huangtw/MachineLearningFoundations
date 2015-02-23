import sys, numpy, random

def load_data(data_file_name):
    data_list = []
    f = open(data_file_name)
    for line in f.readlines():
        tmp = line.replace('\n', '').replace('\r', '').replace('\t', ' ').split(" ")
        x = [1.0]

        for i in range(len(tmp)):
            if i == len(tmp) - 1:
                y = int(tmp[i])
            else:
                x.append(float(tmp[i]))

        data_list.append((numpy.array(x), y))
    return data_list

def find_mistakes(weight_vector, data_list):
    mistake_index_list = []
    for i in range(len(data_list)):
        data = data_list[i]
        if numpy.dot(weight_vector, data[0]) > 0:
            result = 1
        else:
            result = -1

        if result != data[1]:
            mistake_index_list.append(i)

    return mistake_index_list

def learn(weight_vector, train_data_list, order_type, eta, max_update_times):
    update_counter = 0
    if order_type == "pure_random":
        weight_vector_in_pocket = weight_vector
        mistake_index_list = find_mistakes(weight_vector_in_pocket, train_data_list)
        min_mistake_num = len(mistake_index_list)
        random.seed()
        while 1:
            random_index = random.choice(mistake_index_list)
            data = train_data_list[random_index]
            weight_vector = weight_vector + eta * data[1] * data[0]
            update_counter = update_counter + 1

            mistake_index_list = find_mistakes(weight_vector, train_data_list)
            if len(mistake_index_list) < min_mistake_num:
                weight_vector_in_pocket = weight_vector
                min_mistake_num = len(mistake_index_list)
            if update_counter >= max_update_times or len(mistake_index_list) == 0:
                return (weight_vector_in_pocket, update_counter)
                #return (weight_vector, update_counter)
    else:
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
                return (weight_vector, update_counter)
            else:
                update_counter = update_counter + mistake_counter

def gen_order(order_type, len):
    order = range(len)
    if order_type == "pre_random":
        random.seed()
        random.shuffle(order)
    return order

def main():
    train_data_file_name = sys.argv[1]
    order_type = sys.argv[2]
    times = int(sys.argv[3])
    eta = float(sys.argv[4])

    if len(sys.argv) > 5:
        max_update_times = int(sys.argv[5])
    else:
        max_update_times = -1

    if len(sys.argv) > 6:
        test_data_file_name = sys.argv[6]
    else:
        test_data_file_name = None

    weight_vector = numpy.array([0.0, 0.0, 0.0, 0.0, 0.0])

    train_data_list = load_data(train_data_file_name)

    if test_data_file_name:
        test_data_list = load_data(test_data_file_name)
    else:
        test_data_list = None

    total_update = 0
    total_mistake = 0
    for i in range(times):
        new_weight_vector, update_counter = learn(weight_vector, train_data_list, order_type, eta, max_update_times)
        if test_data_list:
            total_mistake = total_mistake + len(find_mistakes(new_weight_vector, test_data_list))
        total_update = total_update + update_counter

    output_string = "%d times, average = %f updates" % (times, total_update/times)
    if test_data_list:
        output_string = output_string + ", average error rate = %f" % (float(total_mistake)/(times*len(test_data_list)))

    print output_string


if __name__ == '__main__':
    main()
