import json


def save_to_json(entity, filename):
    try:
        with open(filename, "r") as json_file:
            filedata = json.load(json_file)
    except FileNotFoundError:
        filedata = []

    data = entity.to_dict()
    filedata.append(data)

    with open(filename, "w") as json_file:
        json.dump(filedata, json_file, indent=4)


def save_to_stream(entity, io_stream):
    data = entity.to_dict()
    try:
        filedata = json.load(io_stream)
    except json.JSONDecodeError:
        filedata = []

    filedata.append(data)

    io_stream.truncate(0)
    io_stream.seek(0)
    json.dump(filedata, io_stream, indent=4)


def to_dict(entity):
    pass


def from_dict(entity, data):
    pass
