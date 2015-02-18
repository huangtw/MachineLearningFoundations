import sys, numpy, random

def load_data(input_file_name):
    input_data_list = []
    f = open(input_file_name)
    for line in f.readlines():
        tmp = line.replace('\n', '').replace('\r', '').replace('\t', ' ').split(" ")
        vector = [1.0]

        for i in range(len(tmp)):
            if i == len(tmp) - 1:
                result = int(tmp[i])
            else:
                vector.append(float(tmp[i]))

        input_data_list.append((numpy.array(vector), result))
    return input_data_list

def learn(weight_vector, input_data_list, order_type):
    update_counter = 0
    order = gen_order(order_type, len(input_data_list))

    while 1:
        mistake_counter = 0
        for i in order:
            data = input_data_list[i]
            if numpy.dot(weight_vector, data[0]) > 0:
                result = 1
            else:
                result = -1

            if result != data[1]:
                weight_vector = weight_vector + data[1]*data[0]
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
    input_file_name = sys.argv[1]
    order_type = sys.argv[2]
    times = int(sys.argv[3])
    weight_vector = numpy.array([0.0, 0.0, 0.0, 0.0, 0.0])

    input_data_list = load_data(input_file_name)

    total_update = 0
    for i in range(times):
        total_update = total_update + learn(weight_vector, input_data_list, order_type)

    print "%d times, average = %f updates" % (times, total_update/times)

if __name__ == '__main__':
    main()
