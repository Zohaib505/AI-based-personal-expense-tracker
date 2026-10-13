import requests
s=requests.Session()
r=s.get('http://127.0.0.1:8000/add-expense')
csrftoken = s.cookies.get('csrftoken','')
print('csrf=', csrftoken)
payload={'amount':'100','description':'test expense','expense_date':'2026-05-01','category':'Food','initial_predicted_category':'Food'}
headers={'X-CSRFToken':csrftoken}
resp=s.post('http://127.0.0.1:8000/add-expense', data=payload, headers=headers)
print('STATUS', resp.status_code)
open('scripts/post_test_resp.html','w',encoding='utf-8').write(resp.text)
print('WROTE scripts/post_test_resp.html')
