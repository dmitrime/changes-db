# -*- coding: utf-8 -*-
import pandas as pd
import json


class ChangesObj:

    def __init__(self, row):
        self.objTime = row.index
        self.objType = row['type']
        self.objId = row['id']
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
            data = pd.read_csv(
                filename,
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
            raise Exception('Failed to load CSV file, check CSV file dimentions!')

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
        if objTime is None or objType is None:
            return None

        until = pd.to_datetime(objTime, unit='s')
        # set the conditions
        condition = self.data.type == objType
        if objId is not None:
            condition = condition & (self.data.id == objId)

        # make the query
        items = self.data[condition][:until]
        if len(items) == 0:
            return None
        # get the latest state
        if objId is not None:
            items = items.tail(1)
            res = [{"id": objId,
                    "props": items['changes'].iloc[0],
                    "type": items['type'].iloc[0],
                    "time": items.index[0].to_datetime()}]
        else:
            # get the latest state for all unique ids
            res, ids = list(), set()
            print type(items.index)
            for idx, row in items.iloc[::-1].iterrows():
                if row['id'] not in ids:
                    ids.add(row['id'])
                    res.append({"id": row['id'],
                                "props": row['changes'],
                                "type": row['type'],
                                "time": idx.to_datetime()})
        return res

    def keys(self):
        return sorted(self.data['type'].unique())

if __name__ == '__main__':
    c = ChangesDB('sample.csv')
    #print c.query('ObjectA', 1, 467765765)
    print c.keys()
