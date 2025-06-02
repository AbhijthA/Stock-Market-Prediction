import yfinance as yf
tcs = yf.Ticker("TCS.NS")
tcs = tcs.history('max')
del tcs['Dividends']
del tcs['Stock Splits']
#del tcs['Capital Gains']
tcs = tcs.loc['2014-01-01':].copy()
tcs['tommorow'] = tcs['Close'].shift(-1)
tcs['target'] = (tcs['Open']<tcs['Close']).astype(int)
print(len(tcs[tcs['target']==1]))
print(tcs)
