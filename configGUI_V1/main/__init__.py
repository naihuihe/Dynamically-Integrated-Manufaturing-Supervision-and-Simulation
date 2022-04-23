
def InitTTKStyles():

    import tkinter.ttk as ttk
    import tkinter as tk

    style = ttk.Style()

    style.theme_use('alt')

    style.configure("Container.TPanedwindow", background = 'white')

    style.configure('TFrame', relief = 'sunken', background = 'white', borderwidth = 0)

    style.configure('SurfaceNotebook', background = 'white')

    style.configure('SurfaceNotebook.Tab', padding=(10, 2, 10, 2), relief = 'sunken')

    style.map('SurfaceNotebook.Tab',
              foreground=[('active', 'blue')],
              background=[('selected', 'lightblue')],
              )

    style.configure('Config.TNotebook', background = 'white', sticky = 'nswe')

    style.layout('Config.TNotebook.Tab', [("Config.Notebook.tab", {"sticky": "nswe",
                                                                  "children": [
                                                                      ('Config.Notebook.padding', {'side': 'top',
                                                                                                   'sticky': 'nswe',
                                                                                                   'children': [('Config.Notebook.label',{"side": "left", "sticky": ''}),]
                                                                                                   }
                                                                       )]
                                                                  }
                                          )]
                 )

    style.configure('Config.TNotebook.Tab', backround = 'lightblue', borderwidth = 2, padding = (10,2,10,2))

    style.map('Config.TNotebook.Tab',
              background = [('!selected', '!active', '#def2fc'), ('active', '#66b6d2'), ('selected', '#66b6d2')],
              relief = [('!selected', 'sunken'), ('selected', 'groove')],
              padding = [('selected', (10,3,10,3))],
              sashrelief = [('!selected', 'sunken'), ('selected', 'groove')])

    style.configure('Nav.Treeview', background = 'white', fieldbackground = 'white')

    style.configure('Nav.Treeview.Heading', background = '#def2fc', padding = (10, 2, 10, 2))

    # set the background color of Treeview heading no matter if it is active or not
    style.map('Nav.Treeview.Heading', background=[('', '#def2fc')])

    # remove the layout element of Treeitem.focus
    # in order to disable the dotted focus line when item is active or selected
    style.layout('Nav.Treeview.Item',[('Nav.Treeitem.padding',
                                       {'sticky': 'nswe',
                                        'children': [('Nav.Treeitem.indicator', {'side': 'left', 'sticky': ''}),
                                                     ('Nav.Treeitem.image', {'side': 'left', 'sticky': ''}),
                                                     ('Nav.Treeitem.text', {'side': 'left', 'sticky': ''})
                                                     ]})])
    style.map('Nav.Treeview',
              background = [('selected', '#66b6d2')])

    style.configure('TLabel', anchor  = 'w', border = 0, background = 'white')

    style.configure('Heading.TLabel', background = '#def2fc')

    style.configure('TEntry', sticky = 'ew')

    style.configure('TButton', background = '#e6eef1')

    style.configure('Dnd.TButton', background = '#def2fc',
                    sticky = 'nwse', padding = 5, width = 20, borderwidth = 2, relief = tk.GROOVE)

    style.layout('Dnd.TButton', [('Button.border',{'sticky': 'nswe',
                                                   'border': '1',
                                                   'children': [('Button.padding', {'sticky': 'nswe',
                                                                                    'children': [('Button.label', {'sticky': 'nswe'})]})]})])

    style.map('Dnd.TButton',
              relief = [('focus', 'pressed', 'raised')],
              borderwidth = [('focus', 5)],
              padding = [('focus', 2)],
              background = [('focus', '#66b6d2')])


    return style
