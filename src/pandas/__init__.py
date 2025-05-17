class DataFrame:
    def __init__(self, records):
        self._records = list(records)
        self.columns = list(records[0].keys()) if records else []
        self.iloc = _ILoc(self._records)

    def __len__(self):
        return len(self._records)

    def __getitem__(self, key):
        return [row.get(key) for row in self._records]

    def __repr__(self):
        return f"DataFrame({self._records})"

class _ILoc:
    def __init__(self, records):
        self._records = records

    def __getitem__(self, idx):
        return self._records[idx]

