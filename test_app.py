from streamlit.testing.v1 import AppTest
from pathlib import Path
app=AppTest.from_file(str(Path(__file__).with_name('app.py')),default_timeout=40).run()
assert not app.exception
for idx in range(10):
 app.selectbox(key="experiment").set_value(idx).run()
 assert not app.exception, (idx,app.exception)
 if idx in (4,5,6):
  for option in app.radio[0].options:
   app.radio[0].set_value(option).run()
   assert not app.exception,(idx,option,app.exception)
 if idx==1:
  app.checkbox[0].check().run();assert not app.exception
 print('PASS screen',idx+1)
print('PASS all screens and alternate modes')
