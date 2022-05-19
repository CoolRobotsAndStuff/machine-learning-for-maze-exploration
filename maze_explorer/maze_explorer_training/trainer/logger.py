import mlflow

class MultiLogger:
    def __init__(self, files:tuple, file_paths:tuple):
        self.files = files
        self.file_paths = file_paths
        self.do_ml_flow_logging = False

    def write(self, data):
        for f in self.files:
            f.write(data)
        for fp in self.file_paths:
            with open(fp, 'a') as f:
                f.write(data)
                
            if self.do_ml_flow_logging:
                try:
                    mlflow.log_artifact(fp)
                except Exception as e:
                    pass

    def flush(self):
        for f in self.files:
            f.flush()
        for fp in self.file_paths:
            with open(fp, 'a') as f:
                f.flush()