#! /usr/bin/python3
import requests, json, typing, logging, os, datetime, time
# logging.basicConfig(filename=f"{os.path.dirname(__file__)}/logs/qiitaAPI_log.txt",level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")
# logging.info("start program")


# NOTE: https://qiita.com/api/v2/items?page=1&per_page={1}    {1} represents how many items API gets
# NOTE: URL for new items for test (https://qiita.com/items)



def get_new_items(num_items: int = 100) -> typing.List[typing.Dict[str, typing.Union[str, int]]]:
    """get new items from Qiita"""
    # get JSON of new items
    res = requests.get(f"https://qiita.com/api/v2/items?page=1&per_page={num_items}")
    res.raise_for_status()

    logging.info("done loading")
    contents = json.loads(res.text)


    # process data
    articles = []
    for article in contents:
        articleData = {
            "title": article["title"],                          # Get title of item
            "url": article["url"],                              # Get URL of item
            "tags": [tag["name"] for tag in article["tags"]],   # Get tags of item
            "date": article["updated_at"],                      # Get date of item
            "user": {
                "id": article["user"]["id"],
                "name": article["user"]["name"]
            },
            "read": 1
            # NOTE: wanna make simple discription
        }
        articles.append(articleData)
    return articles



"""
# get previous datas
nowTime = datetime.datetime.now()
prevItems: typing.List[typing.Dict] = json.load(open(f"{os.path.dirname(__file__)}/data/qiitaNewItems.json"))
print(len(prevItems))



# get new items
# logging.info("getting new items")
articles = get_new_items()


# delete multify 
i = 0; deleteItems = []
for item in prevItems:
    s = 0
    for article in articles:
        if item["title"] == article["title"]:
            deleteItems.append(item)
            s += 1
            break
    if s == 0:
        i += 1
    if i > 5:
        break
for i in deleteItems:
    prevItems.remove(i)

# delete old data
indOlderData = []
for item in prevItems[::50]:
    delta = nowTime - datetime.datetime.strptime(item["date"], '%Y-%m-%dT%H:%M:%S+09:00')
    if delta.days > 10:
        indOlderData = prevItems.index(item)
# logging.info(indOlderData)
if indOlderData:
    for item in prevItems[:indOlderData:-1]:
        prevItems.remove(item)

articles = articles + prevItems      # merge two data

# JSONに保存する
json.dump(articles, open(f"{os.path.dirname(__file__)}/data/qiitaNewItems.json", "w"), indent=2, ensure_ascii=False)



# logging.info("end program")
"""