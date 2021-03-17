

class DataSources(object):
    def __init__(self, dictionary, filters=None):
        self.dictionary = dictionary
        self.filters = {} if filters is None else filters

    def get(self, data_source):
        if 'group_%s' % data_source in self.dictionary:
            return self.dictionary['group_%s' % data_source]
        if 'filtered_%s' % data_source in self.dictionary:
            return self.dictionary['filtered_%s' % data_source]
        return self.dictionary[data_source]

    def get_original(self, data_source):
        return self.dictionary[data_source]

    def dependencies(self, data_source):
        return [(dependence, filter) for dependence, filter in self.filters.keys() if dependence[0] == data_source]

    def set_filter(self, data_source, data_frame):
        self.dictionary['filtered_%s' % data_source] = data_frame
        for dependence, filter in self.dependencies(data_source):
            dependent = self.get(dependence[1])
            self.set_filter(dependence[1], filter(data_frame, dependent))

    def set_group_filter(self, data_source, data_frame):
        self.dictionary['group_%s' % data_source] = data_frame

    def clear_group_filter(self):
        to_clear = [key for key in self.dictionary.keys() if key.startswith('group_')]
        for key in to_clear:
            self.dictionary.pop(key)

    def clear_filter(self):
        to_clear = [key for key in self.dictionary.keys() if key.startswith('filtered_') ]
        for key in to_clear:
            self.dictionary.pop(key)

    def clear(self):
        self.clear_filter()
        self.clear_group_filter()
