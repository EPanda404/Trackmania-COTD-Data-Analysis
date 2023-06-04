import requests

headers = {'user-agent': 'cotd-data-analysis/0.0.1'}

#r = requests.get('https://competition.trackmania.nadeo.club/api/competitions?length=10&offset=0', headers=headers)
#r = requests.get('https://competition.trackmania.nadeo.club/api/competitions/6540/leaderboard?length=64', headers=headers)
r = requests.get('https://prod.trackmania.core.nadeo.online/accounts/displayNames/?accountIdList=3bb0d130-637d-46a6-9c19-87fe4bda3c52,9ebb2ece-61a8-4dbf-9173-25b9d64ad117', headers=headers)
print(r.status_code)
print(r)
print(r.headers)
print(r.json())