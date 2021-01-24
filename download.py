from json import loads
from sys import argv
from typing import Any, Dict, Iterator, cast

from requests import get

gitlab_token: str = ""
max_url = 0


def get_from_gitlab(path: str) -> Dict[Any, Any]:
    response = get(
        f"https://gitlab.com/api/v4{path}",
        headers={"Authorization": f"Bearer {gitlab_token}"},
    )
    return cast(Dict[str, Any], loads(response.text))


def get_merge_diffs(
    project_id: int,
    merge_request_id: int,
) -> Iterator[int]:
    global max_url

    url = f"/projects/{project_id}/merge_requests/{merge_request_id}/changes"
    changes = get_from_gitlab(url)
    add = 0
    sub = 0

    for change in changes["changes"]:
        for line in str(change["diff"]).split("\n"):
            if line.startswith("+"):
                add += 1
            elif line.startswith("-"):
                sub += 1

    url = changes["web_url"]
    max_url = max(len(url), max_url)
    print(f'{url:<{max_url}} => {"+" + str(add):>7} {"-" + str(sub):>7}')

    yield add
    yield sub


def get_differences() -> Iterator[int]:
    page = 0
    while True:
        path = f"/merge_requests?state=merged&per_page=10&page={page}"
        page += 1

        merge_requests = get_from_gitlab(path)

        if not merge_requests:
            print("Finished.")
            return

        for merge_request in merge_requests:
            yield from get_merge_diffs(
                project_id=int(merge_request["project_id"]),
                merge_request_id=int(merge_request["iid"]),
            )


if __name__ == "__main__":
    gitlab_token = argv[1]
    filename = argv[2]

    with open(filename, "w") as stream:
        for difference in get_differences():
            sign = "-" if difference < 0 else "+"
            stream.write(sign + str(difference) + "\n")
