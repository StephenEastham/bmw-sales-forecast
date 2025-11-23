mods = [
    'sys', 'os', 'requests', 'pandas', 'numpy', 'matplotlib', 'matplotlib.pyplot',
    'seaborn', 'datetime', 'warnings', 'logging', 'glob', 'pathlib', 'webbrowser',
    'statsmodels', 'statsmodels.tsa.arima.model', 'statsmodels.tsa.holtwinters',
    'sklearn', 'sklearn.metrics', 'plotly', 'plotly.graph_objects', 'plotly.subplots'
]

import importlib
import sys
for m in mods:
    try:
        mod = importlib.import_module(m)
        path = getattr(mod, '__file__', None)
        ver = getattr(mod, '__version__', None)
        print(f'OK\t{m}\tpath={path}\tver={ver}')
    except Exception as e:
        print(f'FAIL\t{m}\t{e}')
print('EXE\t' + sys.executable)