import json


status_conn_mqtt = True
json_file_path = "jsons\\test.json"


try:
    with open(json_file_path) as file:
        data = json.load(file)
    if status_conn_mqtt:
        print(f'\ntopic={data["System Description"]["Topic"]}, msg={json.dumps(data["System Description"])}')
        try:
            # data["Modbus2MQTT"]
            modbus2mqtt = data["Modbus2MQTT"]
            for var in modbus2mqtt:
                print(f'\n\n{modbus2mqtt[var]["Topic"]}\n')
        except:
            print('No key named "Modbus2MQTT"')
    else:
        print('Problem with the MQTT connection...')
except Exception as e:
    print('ERROR reading Json: ', e.args, end='')