class MockSubProcess:
    def __init__(self, stdout: str):
        self.stdout = stdout.encode("utf-8") if stdout else None
