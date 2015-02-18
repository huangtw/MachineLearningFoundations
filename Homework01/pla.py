import sys, numpy

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

def find_mistake(weight_vector, input_data_list):
    for data in input_data_list:
        if numpy.dot(weight_vector, data[0]) > 0:
            result = 1
        else:
            result = -1

        if result != data[1]:
            return data[1]*data[0]
    return None


def learn(weight_vector, input_data_list):
    update_counter = 0 
    while 1:
        mistake = find_mistake(weight_vector, input_data_list)
        if mistake != None:
            weight_vector = weight_vector + mistake
            update_counter = update_counter + 1
        else:
            print str(update_counter) + " " + str(weight_vector)
            return

def main():
    input_file_name = sys.argv[1]
    weight_vector = numpy.array([0.0, 0.0, 0.0, 0.0, 0.0])

    input_data_list = load_data(input_file_name)
    learn(weight_vector, input_data_list)

if __name__ == '__main__':
    main()
