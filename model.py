import pandas as pd
import json


class ChangesObj:
    def getIdentifierFunc():
        return (self.objType, self.objId)

    def __init__(self, row):
        self.objType = row['type']
        self.objId   = row['id']
        self.objTime = row['time']
        self.objProps = self.loadProps(row['changes'])

    def loadProps(self, props):
        try:
            return json.loads(props.strip())
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
                    header=0)
        except pd.parser.CParserError:
            raise Exception('Failed to load CSV file, check if CSV file is valid!')
        except ValueError:
            raise Exception('Failed to load CSV file, check if CSV file dimentions!')

        if len(data.keys()) != len(ChangesDB.Columns):
            raise Exception('Unexpected number of dimentions!')


        # convert timestamp to datetime
        data['time'] = pd.to_datetime(data['time'], unit='s')
        # sort changes by timestamp
        data.sort(['time'], inplace=True)

        # map of unique object ids to objects
        objects = dict()
        for idx, row in data.iterrows():
            key = row['type'], row['id']
            if key in objects:
                objects[key].update(row['time'], row['changes'])
            else:
                objects[key] = ChangesObj(row)
            # update the cell of the dataframe with the changes
            data.set_value(idx, 'changes', objects[key].objProps.copy())

        return data

if __name__ == '__main__':
    ChangesDB('sample.csv')

