class CollectionObjects:

    def __init__(self):
        self._object_dictionary = {}

    '''Add a provided object to the organizing dictionary
    based on a provided key. Keys are used to point to
    a list of related objects.
    @params
    new_obj the object reference to store
    key the key used to group the related objects
    '''

    def add_object(self, new_obj, key):
        if key not in self._object_dictionary:
            self._object_dictionary[key] = []

        self._object_dictionary[key].append(new_obj)

    '''Return the total of all object.value() grouped
    on provided key.
    @params
    key the key used to group the related objects
    @return
    float The result of sum all object.value() for key
    '''

    def total(self, key):
        temp_sum = 0
        for obj in self._object_dictionary[key]:
            temp_sum = obj.value()
        return temp_sum

    '''Return the average of all object.value() grouped
    on provided key.
    @params
    key the key used to group the related objects
    @return
    float The result of average all object.value() for key
    '''

    def average(self, key):
        temp_sum = self.total(key)
        temp_avg = temp_sum / len(self._object_dictionary)
        return temp_avg

    '''Sort in place all objects grouped based on provided
    key. Sort is ascending based on comparison between
    object.value()
    @params
    key the key used to group the related objects
    '''

    def sort(self, key):
        self._object_dictionary[key].sort()

    '''Return the max value of all object.value() grouped
    on provided key.
    @params
    key the key used to group the related objects
    @return
    float The max value of all object.value() for key
    '''

    def max_value(self, key):
        return max(self._object_dictionary[key])

    '''Return the min value of all object.value() grouped
    on provided key.
    @params
    key the key used to group the related objects
    @return
    float The min value of all object.value() for key
    '''

    def min_value(self, key):
        return min(self._object_dictionary[key])

