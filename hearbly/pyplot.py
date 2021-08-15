def make_pie(base):
    import pandas as ps
    import matplotlib.pyplot as plot
    dp = ps.read_excel(base)
    dp['currency_iso_code'].value_counts().plot.pie(figsize=(5, 5))
    plot.savefig('/home/hamza/Desktop/First_year/Firstyear_project/hearbly/static/PIEPLOT/pie.png', transparent=True)
    plot.figure()