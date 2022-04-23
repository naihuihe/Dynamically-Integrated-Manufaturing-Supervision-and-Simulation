

# this class is defined to facilitate the storage and
# retrieving of particular attributes of agents in a manner of using array list

class AgentArray(list):

    def __init__(self, retrieve_attr):
        """
        :param retrieve_attr: the name of the attribute of the saved agents, which the users need to retrieve
        """
        self.retrieve_attr = retrieve_attr

    def __getitem__(self, item):
        """
        to get the value of the retrive_attribute of the indexed agent saved in the list
        ==> x[y].retrieve_attr
        :param item: index
        :return:
        """
        return super().__getitem__(item).__getattribute__(self.retrieve_attr)




class A:

    def __init__(self, name):
        self.name = name

if __name__ == "__main__":

    array = AgentArray("name")
    for i in range(10):
        a = A("a"+str(i))
        array.append(a)
    print(array[0])

