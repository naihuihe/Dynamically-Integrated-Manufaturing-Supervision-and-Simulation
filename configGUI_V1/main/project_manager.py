import pickle
import tkinter as tk
from tkinter.filedialog import askdirectory
from tkinter.filedialog import asksaveasfile
from tkinter.filedialog import asksaveasfilename



class ProjectManager:

    def __init__(self, name, wm):

        self.name = name
        self.wm = wm
        self.agent_mapper = Agent_Mapper()
        self.__creat_system()


    def __creat_system(self):
        sys_class = self.agent_mapper.get_agent_class('System')
        self.system_agent = sys_class(wm = self.wm, pm = self, name = self.name)


class Agent_Mapper:

    from main.config import AGENT_MAPPER

    class_mapper = AGENT_MAPPER

    def __init__(self):
        for each in Agent_Mapper.class_mapper:
            setattr(self, each, {})
            setattr(self, each + "_name_list", [])


    def get_agent_class(self, agent_type: str):
        try:
            return Agent_Mapper.class_mapper[agent_type]
        except:
            print(agent_type + " not defined")
            return None

    def get_agents(self, agent_type:str):
        """
        :param agent_type:
        :return: dict (key: id, value: agent)
        """
        return getattr(self, agent_type, None)

    def get_agent_name_list(self, agent_type: str):
        return getattr(self, agent_type + "_name_list", None)

    def add_agent(self, agent_type:str, agent):
        try:
            self.get_agents(agent_type)[agent.id] = agent
            self.get_agent_name_list(agent_type).append(agent.t_name)
        except:
            print(agent_type + " not defined")
            return None


    def get_agent_by_name(self, agent_type:str, agent_name:str):
        agent_id = self.find_id_by_name(agent_type, agent_name)
        return self.get_agent_by_id(agent_type, agent_id)

    def get_agent_by_id(self, agent_type:str, agent_id:int):
        return self.get_agents(agent_type)[agent_id]

    def find_id_by_name(self, agent_type:str, agent_name:str):
        agents = self.get_agents(agent_type)
        agent_names = [x.get() for x in self.get_agent_name_list(agent_type)]
        index = agent_names.index(agent_name)
        id = list(agents.keys())[index]

        return id


    def create_db_agent(self, agent_type: str):
        agents = self.get_agents(agent_type)
        db_agents = {}  # dict {agent_name: db_agent}
        for agent in agents.values():
            db_agent = agent.create_db_agent()
            db_agents[db_agent.name] = db_agent

        return db_agents



if __name__ == '__main__':

    import os
    import pathlib
    print(pathlib.Path.iterdir(os.getcwd()))