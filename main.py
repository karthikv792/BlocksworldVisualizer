output_file = "outputs/task1_reasoning.txt"

with open(output_file) as f:
    lines = f.readlines()
    instances = []
    instance = ""
    for i in lines:
        if "SUCCESS" in i or "FAILURE" in i:
            print(instance)
            instances.append(instance)
            instance = ""
        instance+=i
    print(len(instances))