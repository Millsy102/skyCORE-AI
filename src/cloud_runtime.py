
import os

class CloudRuntime:
    def __init__(self, runtime):
        self.runtime = runtime

    def push_state(self):
        os.system("rsync -avz --exclude='.venv' ./ remote:~/skycore_backup/")
