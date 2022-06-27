from os import environ

from aiohttp import ClientSession

from modules.core.logger import logging_info_async


class HubexApi:
    __slots__ = ("token", "authed_token")
    __URL__ = "https://api.hubex.ru/fsm/"

    def __init__(self,
                 token=environ["TOKEN"].replace("\"", ""),
                 access_token=environ.get("AUTHED_TOKEN", "").replace("\"", "")):
        self.token = token
        self.authed_token = access_token

    async def _get_access_token(self):
        async with ClientSession() as s, \
                s.request(url=self.__URL__ + "AUTHZ/AccessTokens",
                          method="POST",
                          json={"serviceToken": environ["TOKEN"].replace("\"", "")}
                          ) as r:
            result = await r.json()

            environ["AUTHED_TOKEN"] = result["access_token"]
            return result

    @logging_info_async
    async def _call_api(self,
                        url: str,
                        method,
                        **kwargs):
        header = {
            'content-type': 'application/json',
            'authorization': 'Bearer ' + self.authed_token,
            'X-Application-ID': '1'
        }

        async with ClientSession() as s, s.request(url=url, method=method, json=kwargs, headers=header) as r:
            return await r.json()

    async def get_task(self, task_id: int):
        return await self._call_api(
            url= f"{self.__URL__}WORK/tasks/{task_id}",
            method="GET",
        )


