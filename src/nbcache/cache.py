from .detectors import *
# from ._local import write_local
from ._colab import write_colab, load_colab
# from ._databricks import write_databricks

class Cache():

    def __init__(self,args={}):
        for key, value in args.items():
            try:
                setattr(self, key, value)
            except:
                pass

        self.vars = []
        self.email = None
        self.email_password = None
        self.cache_dir = None
        self.env = None
        self.enable_pickle = False
        self.failures = []
        self.mode = "json"
        self.log_failures = False

    def log_failures(self):
        self.log_failures = True
        return self


    def option(self, key, value):
        try:
            setattr(self, key, value)
        except:
            pass
        return self
    
    def add_var(self, var:str):
        self.vars.append(var)
        return self
    
    def add_vars(self, vars:list[str]):
        self.vars.extend(vars)
        return self
    
    def detect_environment(self):
        if detect_colab():
            self.env = "colab"
        elif detect_databricks():
            self.env = "databricks"
        else:
            self.env = "local"
        return self
    
    def write(self):
        if self.env == "colab":
            write_colab(self)
        # elif self.env == "databricks":
        #     write_databricks(self)
        # else:
        #     write_local(self)
        return self
    
    def load(self):
        if self.env == "colab":
            load_colab(self)
        # elif self.env == "databricks":
        #     load_databricks(self)
        # else:
        #     load_local(self)
        return self