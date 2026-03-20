from notion_client import Client
import os
from typing import Dict, Any, Generator
from datetime import timezone, timedelta, datetime

NOTION_API_KEY = os.environ["NOTION_API_KEY"]
NOTION_DATA_SOURCE_ID = os.environ["NOTION_DATA_SOURCE_ID"]

JST = timezone(timedelta(hours=9))
now_jst = datetime.now(JST)

deadline_condition: Dict[str, Any] = {
    "property" : "期限",
    "date" : {
        "before": now_jst.isoformat()
    }
}

completed_condition: Dict[str, Any] = {
    "property" : "完了",
    "checkbox" : {
        "equals": True,
    }
}

updated_condition: Dict[str, Any] = {
    "property" : "終了",
    "checkbox" : {
        "equals": False,
    }
}
is_reward: Dict[str, Any] = {
    "property" : "種類",
    "select" : {
        "equals": "報酬",
    }
}

is_homework: Dict[str, Any] = {
    "property" : "種類",
    "select" : {
        "equals": "課題",
    }
}

is_needed_things: Dict[str, Any] = {
    "property" : "種類",
    "select" : {
        "equals": "持ち物",
    }
}

homework_condition = {
    "and" : [
        deadline_condition,
        completed_condition,
        updated_condition,
        is_homework
    ]
}

needed_condition = {
    "and" : [
        deadline_condition,
        completed_condition,
        updated_condition,
        is_needed_things
    ]
}

reward_condition = {
    "and" : [
        completed_condition,
        updated_condition,
        is_reward
    ]
}

filter_condition = {
    "or" : [
        homework_condition,
        needed_condition,
        reward_condition
    ]
}

def fetch_datasource_page(client: Client, query_filter: Dict[str, Any]={}) -> Generator[Dict[str, Any], None, None]:
    start_cursor = None
    has_more = True
    while has_more:
        res = client.data_sources.query(data_source_id=NOTION_DATA_SOURCE_ID, start_cursor=start_cursor, filter=query_filter)
        has_more = res["has_more"]
        start_cursor = res["next_cursor"]
        for result in res["results"]:
            yield result
            
            
def archive_page(client: Client, page_id: str) -> bool:
    try:
        client.pages.update(
            page_id=page_id,
            properties={
                "終了": {
                    "checkbox": True
                }
            }
        )
        print(f"id{page_id}の処理に成功しました。")
        return True
    except Exception as e:
        print(str(e))
        return False
    

if __name__ == "__main__":
    client = Client(auth=NOTION_API_KEY)
    total_count = 0
    success_count = 0
    for result in fetch_datasource_page(client=client, query_filter=filter_condition):
        is_succeeded = archive_page(client, result["id"])
        total_count += 1
        if is_succeeded:
            success_count += 1
    print(f"完了：{success_count}/{total_count} 件を更新しました")
