def request_data_base(base):
    data_base = {}
    import pandas as pd
    import matplotlib.pyplot as plt
    db = pd.read_excel(base)
    data_base['amount'] = format(sum(db['amount']),".2f")
    data_base['client'] = db.shape[0]
    data_base['herblyUSD'] = int(db.loc[db['merchant_account_id'] == 'herbalyUSD' , 'merchant_account_id'].value_counts())
    data_base['herblyCAD'] = int(db.loc[db['merchant_account_id'] == 'herbalyCAD' , 'merchant_account_id'].value_counts())
    return data_base

def make_plot(base):
    import pandas as pd
    import matplotlib.pyplot as plt 
    db = pd.read_excel(base)
    db['amount'].plot.area(color ='#44AA99', figsize=(9, 6))
    plt.savefig("hearbly/static/PYPLOT/plot.png" , transparent=True)
    plt.figure()
