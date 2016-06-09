import pandas as pd
import json


class ChangesObj:
    def getIdentifierFunc():
        return (self.objType, self.objId)

    def __init__(self, row):
        self.objTime = row.index
        self.objType = row['type']
        self.objId   = row['id']
        self.objProps = self.loadProps(row['changes'])

    def loadProps(self, props):
        try:
            return json.loads(props)
        except:
            raise Exception("Failed to load object properties")

    def update(self, time, changes):
        self.objTime = time
        self.objProps.update(self.loadProps(changes))

class ChangesDB:
    Columns = ['id', 'type', 'time', 'changes']
    Sep = '|'
    
    def __init__(self, filename):
        self.data = self.load(filename)

    def load(self, filename):
        try:
            data = pd.read_csv(filename,
                    sep=ChangesDB.Sep,
                    names=ChangesDB.Columns,
                    converters={'time': lambda t: pd.to_datetime(int(t.strip()), unit='s'),
                                'id': lambda t: int(t.strip()),
                                'type': lambda t: t.strip(),
                                'changes': lambda t: t.strip()},
                    header=0)
        except pd.parser.CParserError:
            raise Exception('Failed to load CSV file, check if CSV file is valid!')
        except ValueError:
            raise Exception('Failed to load CSV file, check if CSV file dimentions!')

        if len(data.keys()) != len(ChangesDB.Columns):
            raise Exception('Unexpected number of dimentions!')


        # sort changes by timestamp
        data.sort(['time'], inplace=True)

        # make the time the new index
        data.index = data['time']
        del data['time']

        # map of unique object ids to objects
        objects = dict()
        for idx, row in data.iterrows():
            key = row['type'], row['id']
            if key in objects:
                objects[key].update(idx, row['changes'])
            else:
                objects[key] = ChangesObj(row)
            # update the cell of the dataframe with the changes
            data.set_value(idx, 'changes', objects[key].objProps.copy())

        return data

    def query(self, objType, objId, objTime):
        until = pd.to_datetime(objTime, unit='s')

        res = self.data[
                (self.data['id'] == objId) & 
                (self.data['type'] == objType)
            ][:until]
        print len(res)
        print res.tail(1)

if __name__ == '__main__':
    ChangesDB('sample.csv').query('ObjectA', 1, 467765765)

