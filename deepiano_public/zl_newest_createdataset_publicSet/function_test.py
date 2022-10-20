import os
import random
import csv


def parse_maestro_v3_split(input_dir):
    train_dataset = []
    test_dataset = []
    csv_file_name = os.path.join(input_dir, 'maestro-v3.0.0.csv')
    with open(csv_file_name) as f:
        items = csv.reader(f)
        for item in items:
            year = item[3]
            midi_filename = item[4]
            audio_filename = item[5]
            split = item[2]

            # if split == 'train' and random.randint(0,9)==0:
            #         dataset.append((year, midi_filename, audio_filename))
            # elif split == 'test' and random.randint(0,9)==0:
            #         dataset.append((year, midi_filename, audio_filename))
            if split == 'train':
                train_dataset.append((year, midi_filename, audio_filename))
            elif split == 'test':
                test_dataset.append((year, midi_filename, audio_filename))
    return train_dataset, test_dataset


def randomsample(list_temp):
    random.seed(6)
    result = random.sample(list_temp, int(len(list_temp) * 0.1))
    return result


if __name__ =='__main__':
    input_dir = '/deepiano_data/dataset/maestro-v3.0.0'
    train_dataset, test_dataset = parse_maestro_v3_split(input_dir)
    print(len(train_dataset))
    print(len(test_dataset))
    resample_train_dataset = randomsample(train_dataset)
    resample_test_dataset = randomsample(test_dataset)
    print(len(resample_train_dataset))
    print(resample_test_dataset)