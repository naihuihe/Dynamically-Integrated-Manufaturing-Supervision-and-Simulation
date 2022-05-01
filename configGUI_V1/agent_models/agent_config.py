
class AgentConfig:

    """
    Each Agent has a config_panel.

    The STRUCTURE of a config_panel has three layers:

    - The bottom layer is a Notebook
    - The middle layer is a CollapsiblePaneFrame, added to the bottom layer
    - The upper layer is CollapsiblePane, added to the middle layer

    In the following,

    ..._PANE_STRUCTURE: <dict> describe the structure of the middle layer.
                        Two elements are contained, 'heading' and 'children', while the former one must be

                        'heading': tab text to be shown on the Notebook for the CollapsiblePaneFrame
                                   'heading' must be included.

                        'children': <dict> showing the CollapsiblePanes to be added to the Frame.
                                    key ==> pane idd, value ==> pane heading

    ..._PANEL_STRUCTURE: <dict> descrbie the structure of the bottom layer.
                         By default, three CollapsiblePaneFrames are added to top of it for all agents

    """

    AGENT_MODEL_PANE_STRUCTURE = {'heading': 'Agent Model',
                                  'children': {'agent_info': 'Agent Information'}
                                  }

    SIMULATION_PANE_STRUCTURE = {'heading':'Simulation Model'}

    DB_MODEL_PANE_STRUCTURE = {'heading': 'D2S DB Model'}

    # dict: list of panels to be added to the config_panel of all agent by default
    # key ==> panel_id, value ==> panel heading
    CONFIG_PANEL_STRUCTURE = {'agent_model': AGENT_MODEL_PANE_STRUCTURE,
                              'simulation': SIMULATION_PANE_STRUCTURE,
                              'db_model': DB_MODEL_PANE_STRUCTURE}





class SystemConfig:

    """
    The config_panel structure above for agent is shared and loaded by default for System agent.

    If additional panel is to be added to the config_panel,
        the ...PANE_STRUCTURE must be defined with 'heading' element included at least

    if additional information is to be shown in an existing panel,
        the ...PANE_STRUCTURE for the existing panel must be re-stated at first.
        However, 'heading' element should not be included

    In other words, when setting up the config_panel, agent will determine if the configuration is for
    an exiting panel or new panel by checking if it has 'heading' element

    """
    AGENT_MODEL_PANE_STRUCTURE = {'children': {'layout': 'Layout and Appearance'}
                                  }

    CONFIG_PANEL_STRUCTURE = {'agent_model': AGENT_MODEL_PANE_STRUCTURE}



    LAYOUT_WIDTH = 1000
    LAYOUT_HEIGHT = 800
    LAYOUT_STYLE = {'fill': "", 'outline': "orange", 'stipple': "gray25"}