class BillData:
    def __init__(self, date, usage, cost):
        self.date = date
        self.usage = usage
        self.cost = cost

    def __repr__(self):
        return f"BillData(date={self.date}, usage={self.usage}, cost={self.cost})"