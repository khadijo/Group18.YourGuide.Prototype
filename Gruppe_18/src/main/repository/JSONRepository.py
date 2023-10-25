import json


class JSONRepository:

    def save_to_json(self, entity, filename):
        try:
            with open(filename, "r") as json_file:
                filedata = json.load(json_file)
        except FileNotFoundError:
            filedata = []

        duplicate_found = False
        for item in filedata:
            if item == entity.to_dict():
                duplicate_found = True
                break

        if not duplicate_found:
            data = entity.to_dict()
            filedata.append(data)
        with open(filename, "w") as json_file:
            json.dump(filedata, json_file, indent=4)

    def save_to_stream(self, entity, io_stream):
        try:
            filedata = json.load(io_stream)
        except json.JSONDecodeError:
            filedata = []

        duplicate_found = False
        for item in filedata:
            if item['id'] == entity.get_id():
                duplicate_found = True
                break

        if not duplicate_found:
            data = self.to_dict(entity)
            filedata.append(data)

        io_stream.truncate(0)
        io_stream.seek(0)
        json.dump(filedata, io_stream, indent=4)

    def to_dict(self, entity):
        entity_dict = {}
        for key, value in entity.__dict__.items():
            entity_dict[key] = value
        return entity_dict

    def read_from_stream(stream):
        items = json.load(stream)
        stream.seek(0)
        return items




    # def from_json(self, entity, ):
