from logging import error, info
from os import environ

from aiohttp import ClientSession


class HubexApi:
    __slots__ = ("token", "authed_token")
    __URL__ = "https://api.hubex.ru/fsm/"

    @classmethod
    async def create(cls,
                     token=environ["TOKEN"].replace("\"", "")):
        """
        :param token: Get it in Admin Panel
        :param access_token:  Get it in self._get_access_token()
        """
        self = HubexApi()
        self.token = token
        await self._get_access_token()
        return self

    async def _get_access_token(self):
        async with ClientSession() as s, s.request(url=self.__URL__ + "AUTHZ/AccessTokens",
                                                   method="POST",
                                                   json={"serviceToken": environ["TOKEN"].replace("\"", "")}) as r:
            result = await r.json()
            self.authed_token = result["access_token"]
            environ["AUTHED_TOKEN"] = result["access_token"]
            return result

    async def _call_api(self,
                        url: str,
                        method,
                        **kwargs):
        header = {
            'content-type': 'application/json',
            'authorization': 'Bearer ' + self.authed_token,
            'X-Application-ID': '3'
        }

        async with ClientSession() as s, s.request(url=url, method=method, json=kwargs, headers=header) as r:
            text = f"{method} {r.status} {url} {kwargs}"
            if r.status != 200:
                error(text)
                return {}
            info(text)
            return await r.json(content_type=None)

    async def get_task(self, task_id: int):
        return await self._call_api(
            url=f"{self.__URL__}WORK/Tasks/{task_id}",
            method="GET",
        )

    async def get_asset(self, asset_id: int):
        return await self._call_api(
            url=f"{self.__URL__}ES/Assets/{asset_id}",
            method="GET",
        )

    async def authorize(self):
        return await self._call_api(
            url=f"{self.__URL__}AUTHZ/Accounts/authorize",
            method="POST",
        )

    async def get_attr(self, asset_id: int):
        return await self._call_api(
            url=f"{self.__URL__}ES/Assets/{asset_id}/attributes",
            method="GET",
        )

    async def get_checklists(self):
        return await self._call_api(
            url=f"{self.__URL__}WORK/CheckLists",
            method="GET",
        )

    async def get_checklists_task(self, task_id: str):
        return await self._call_api(
            url=f"{self.__URL__}WORK/Tasks/{task_id}/checkLists",
            method="GET",
        )

    async def get_checklists_activated(self, task_id: str, check_id: str):
        return await self._call_api(
            url=f"{self.__URL__}WORK/Tasks/{task_id}/checkLists/{check_id}/results",
            method="GET",
        )
