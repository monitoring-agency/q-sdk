import base64
import enum
import json
import logging
import os.path
from pprint import pprint
from typing import Union

import httpx

from objects.check import Check, CheckParam
from objects.metric import Metric
from objects.time_period import TimePeriod

logger = logging.getLogger("QApi")


class Method(enum.Enum):
    GET = "get"
    POST = "post"
    PUT = "put"
    DELETE = "delete"


class QApi:
    """The main class to initialize.

    :param username: Username of Q account
    :param password: Password of Q account
    :param uri: Uri of the API Endpoint. Something like https://example.com/api/v1/
    :param verify: Verify SSL/TLS. Defaults to True

    :returns: Instance of Q API
    """
    def __init__(self, username="", password="", uri="", verify=True):
        self.username = username
        self.password = password
        self.uri = uri
        self.token = ""
        self.client = httpx.Client(verify=verify)

    def authenticate(self):
        for i in range(1, 4):
            try:
                data = {
                    "username": self.username,
                    "password": self.password
                }
                ret = self.client.post(os.path.join(self.uri, "authenticate"), json=data)
                if not ret.status_code == 200:
                    raise PermissionError("Authentication failed")
                try:
                    decoded = json.loads(ret.text)
                except json.JSONDecodeError:
                    logger.error("Could not decode answer from server")
                    raise PermissionError("Could not decode answer from server")
                if "success" not in decoded:
                    logger.error("Got malformed json")
                    raise PermissionError("Got malformed json")
                if decoded["success"]:
                    logger.debug("Authentication was successful, saving token")
                    self.token = decoded["data"]
                    break
            except PermissionError:
                logger.error(f"Authentication failed {i}/3")
        else:
            exit(1)

    def _make_request(self, method: Method, endpoint: str, data: dict = None):
        encoded = base64.urlsafe_b64encode(f"{self.username}:{self.token}".encode("utf-8"))
        header = {"Authentication": encoded.decode("utf-8")}
        if method == Method.GET:
            ret = self.client.get(os.path.join(self.uri, endpoint), params=data, headers=header)
        elif method == Method.POST:
            ret = self.client.post(os.path.join(self.uri, endpoint), json=data, headers=header)
        elif method == Method.PUT:
            ret = self.client.put(os.path.join(self.uri, endpoint), json=data, headers=header)
        elif method == Method.DELETE:
            ret = self.client.delete(os.path.join(self.uri, endpoint), headers=header)

        if ret.status_code != 200:
            pprint(ret.text)
            exit(1)
        decoded = json.loads(ret.text)
        if not decoded["success"]:
            pprint(decoded["message"])
        return decoded

    def check_get(self, check_id: Union[list, str, int] = None) -> Union[list, Check]:
        """This method is used to retrieve checks

        :param check_id: If None, all checks are retrieved. Str or int to retrieve a single check.
        List of str or int to retrieve a list of checks.
        :return: Check or List of Checks
        """
        if check_id:
            if isinstance(check_id, list):
                ret = self._make_request(Method.GET, "check", {"filter": [str(x) for x in check_id]})
                return [Check(**x) for x in ret["data"]]
            elif isinstance(check_id, str) or isinstance(check_id, int):
                ret = self._make_request(Method.GET, f"check/{str(check_id)}")
                return Check(**ret["data"])
            else:
                raise ValueError
        else:
            ret = self._make_request(Method.GET, "check")
        return [Check(**x) for x in ret["data"]]

    def check_create(self, name: str, cmd: str = "", check_type: str = "") -> int:
        """This method is used to create a Check

        :param name: Name of the Check
        :param cmd: Optional. Command line of the check
        :param check_type: Optional. CheckType of the check
        :return: Returns the id of the check.
        """
        params = {
            "name": name
        }
        if cmd:
            params["cmd"] = cmd
        if check_type:
            params["check_type"] = check_type
        return self._make_request(Method.POST, "check", params)["data"]

    def check_change(self, check_id: Union[str, int], changes: dict):
        """This method is used to change a check.

        :param check_id: ID of the check
        :param changes: Dict of parameters to change. Key has to be Union[CheckParam, str], the value str
        """
        check_id = str(check_id)
        changes = {x.value if isinstance(x, CheckParam) else x: changes[x] for x in changes}
        self._make_request(Method.PUT, f"check/{check_id}", data=changes)

    def check_delete(self, check_id):
        """This method is used to delete a check

        :param check_id: ID of the check to delete
        :return:
        """
        check_id = str(check_id)
        self._make_request(Method.DELETE, f"check/{check_id}")

    def metric_get(self, metric_id=None):
        """This method is used to retrieve metrics

        :param metric_id: Optional. If None, all Metrics are retrieved. Str or int to retrieve a single metric.
        List of str or int to retrieve a list of Metrics.
        :return: Metric or list of Metrics
        """
        if metric_id:
            if isinstance(metric_id, list):
                ret = self._make_request(Method.GET, "metric", {"filter": [str(x) for x in metric_id]})
                return [Metric(**x) for x in ret["data"]]
            elif isinstance(metric_id, str) or isinstance(metric_id, int):
                ret = self._make_request(Method.GET, f"metric/{str(metric_id)}")
                return Metric(**ret["data"])
            else:
                raise ValueError
        else:
            ret = self._make_request(Method.GET, "metric")
        return [Metric(**x) for x in ret["data"]]

    def time_period_get(self, time_period_id=None):
        """This method is used to retrieve a time period

        :param time_period_id:
        :return:
        """
        if time_period_id:
            if isinstance(time_period_id, list):
                ret = self._make_request(Method.GET, "timeperiod", {"filter": [str(x) for x in time_period_id]})
                return [TimePeriod(**x) for x in ret["data"]]
            elif isinstance(time_period_id, str) or isinstance(time_period_id, int):
                ret = self._make_request(Method.GET, f"timeperiod/{str(time_period_id)}")
                return TimePeriod(**ret["data"])
            else:
                raise ValueError
        else:
            ret = self._make_request(Method.GET, "timeperiod")
        return [TimePeriod(**x) for x in ret["data"]]
