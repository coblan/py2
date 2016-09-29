import requests

# url = 'https://www.googleapis.com/plus/v1/people?query=heyulin&key=AIzaSyAiuhnR6N-iQZbH1XRroByMLuQCNezWsnk'
url='https://www.googleapis.com/gmail/v1/users/heyulin%40smalltreemedia.com/profile?fields=emailAddress&key=AIzaSyAiuhnR6N-iQZbH1XRroByMLuQCNezWsnk&access_token=ya29.CjHsAohRm22hj8UrOjDWDQzWx6av24thFSvQHbNd-4pCyrFIItsZzVDtqopPFru2lEHT'
url='https://www.googleapis.com/gmail/v1/users/me/labels?key=AIzaSyAiuhnR6N-iQZbH1XRroByMLuQCNezWsnk&access_token=ya29.CjHsAoJiQ3SZ3yBEeh3GmbGdEZrvbH3I83_Rpoy7Mpns1da2fcP5I8Cp0TvcllVno717'
rt = requests.get(url)
print(rt.text)