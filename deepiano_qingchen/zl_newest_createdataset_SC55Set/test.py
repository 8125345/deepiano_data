import json

json_dir = '/deepiano_data/zhaoliang/SplitModel_data/json_with_beep/beep_train.json'
train_json = '/deepiano_data/zhaoliang/SplitModel_data/json_with_beep/beep_train_.json'
with open(json_dir, 'r', encoding='utf-8') as f:
    result = json.load(f)
    print(result)
    sample_0 = result['0']
    sample_1 = result['1']
    res = {}
    print(res)
    for i in range(0, 5000):
        res[i] = sample_0
    for j in range(5001, 10000):
        res[j] = sample_1
    print(res)
    # print(sample_0)
    # print(sample_1)
    # train_json_data = dict(zip(range(10), sample_0))
    # test_json_data = dict(zip(range(500), sample_1))
    # print(train_json_data)
    with open(train_json, "w+") as json_file:
        json.dump(res, json_file, ensure_ascii=False)





