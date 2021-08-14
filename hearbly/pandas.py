def request_data_base(base):
    import pandas as pd
    import matplotlib.pyplot as plt
    db = pd.read_excel(base)
    return format(sum(db['amount']),".2f")