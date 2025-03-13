class DataFormatter:
    def __init__(self, full_data):
        self._full_data = full_data

    def exmo_to_plot_format(self):
        
        formatted = {"Date": {}, "Open": {}, "Close": {}, "High": {}, "Low": {}, "Volume": {}}
