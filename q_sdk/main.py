import base64
import enum
import json
import logging
import os.path
from hashlib import sha256
from pprint import pprint
from typing import Union

import httpx

from objects.check import Check, CheckParam
from objects.global_variable import GlobalVariable
from objects.metric import Metric
from objects.metric_template import MetricTemplate, MetricTemplateParam
from objects.time_period import TimePeriod, TimePeriodParam

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
        path = os.path.expanduser("~/.q-sdk/")
        self.token_path = os.path.join(path, sha256(f"{self.uri}-{self.username}.txt".encode("utf-8")).hexdigest())
        if not os.path.exists(path) or not os.path.isdir(path):
            os.makedirs(path)
        if os.path.exists(self.token_path):
            try:
                self.token = open(self.token_path).read()
            except FileNotFoundError:
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
                    with open(os.path.expanduser(self.token_path), "w") as fh:
                        fh.write(self.token)
                    break
            except PermissionError:
                logger.error(f"Authentication failed {i}/3")
        else:
            exit(1)

    def _make_request(self, method: Method, endpoint: str, data: dict = None):
        if not self.token:
            self.authenticate()
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
            if ret.status_code == 401:
                logger.debug(f"Authentication failed, trying to authenticate..")
                self.authenticate()
                self._make_request(method, endpoint, data)
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

    def check_update(self, check_id: Union[str, int], changes: dict) -> None:
        """This method is used to update a check.

        :param check_id: ID of the check
        :param changes: Dict of parameters to change. Key has to be Union[CheckParam, str], the value str
        """
        changes = {x.value if isinstance(x, CheckParam) else x: changes[x] for x in changes}
        self._make_request(Method.PUT, f"check/{check_id}", data=changes)

    def check_delete(self, check_id: Union[str, int]) -> None:
        """This method is used to delete a check

        :param check_id: ID of the check to delete
        :return:
        """
        self._make_request(Method.DELETE, f"check/{check_id}")

    def metric_get(self, metric_id: Union[str, int, list] = None) -> Union[list, Metric]:
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

    def metric_create(
            self, name: str, linked_host_id: Union[str, int], linked_check_id: Union[str, int] = "",
            disabled: bool = False, metric_templates: list = None, scheduling_interval: Union[str, int] = "",
            scheduling_period_id: Union[str, int] = "", notification_period_id: Union[str, int] = "", variables=None
    ) -> int:
        """This method is used to create a metric

        :param name: Name of the metric
        :param linked_host_id: ID of the linked_host
        :param linked_check_id: Optional. ID of the linked_check
        :param disabled: Optional. Specify True if you want to disable the metric
        :param metric_templates: Optional. List of IDs of MetricTemplates
        :param scheduling_interval: Optional. Interval time the check should be executed
        :param scheduling_period_id: Optional. ID of a TimePeriod
        :param notification_period_id: Optional. ID of a TimePeriod
        :param variables: Optional. Dictionary of key value pairs.

        :return: ID of the created Metric
        """
        params = {
            "name": name,
            "linked_host": linked_host_id,
        }
        if linked_check_id:
            params["linked_check"] = linked_check_id
        if disabled:
            params["disabled"] = disabled
        if metric_templates:
            params["metric_templates"] = metric_templates
        if scheduling_interval:
            params["scheduling_interval"] = scheduling_interval
        if scheduling_period_id:
            params["scheduling_period"] = scheduling_period_id
        if notification_period_id:
            params["notification_period"] = notification_period_id
        if variables:
            params["variables"] = variables
        ret = self._make_request(Method.POST, "metric", data=params)
        return ret["data"]

    def metric_update(self, metric_id: Union[str, int], changes: dict) -> None:
        """This method is used to update a metric

        :param metric_id: ID of the metric
        :param changes: Dictionary with MetricParam as key and its value as str
        """
        changes = {x.value if isinstance(x, CheckParam) else x: changes[x] for x in changes}
        self._make_request(Method.PUT, f"metric/{metric_id}", data=changes)

    def metric_delete(self, metric_id: Union[str, int]):
        """This method is used to delete a metric

        :param metric_id: ID of the Metric to delete
        :return:
        """
        self._make_request(Method.DELETE, f"metric/{metric_id}")

    def time_period_get(self, time_period_id: Union[int, str, list] = None) -> Union[list, TimePeriod]:
        """This method is used to retrieve a time period

        :param time_period_id: ID of a TimePeriod

        :return: Returns a TimePeriod or a list of TimePeriods
        """
        if time_period_id:
            if isinstance(time_period_id, list):
                ret = self._make_request(Method.GET, "timeperiod", {"filter": [str(x) for x in time_period_id]})
                return [TimePeriod(**x) for x in ret["data"]]
            elif isinstance(time_period_id, str) or isinstance(time_period_id, int):
                ret = self._make_request(Method.GET, f"timeperiod/{time_period_id}")
                return TimePeriod(**ret["data"])
            else:
                raise ValueError
        else:
            ret = self._make_request(Method.GET, "timeperiod")
        return [TimePeriod(**x) for x in ret["data"]]

    def time_period_create(self, name: str, time_periods: dict) -> int:
        """This method is used to create a TimePeriod

        :param name: Name of the TimePeriod
        :param time_periods: Periods of a week. For the exact syntax see TimePeriodParam.TIME_PERIODS' docstring.

        :return: ID of the created TimePeriod
        """
        params = {
            "name": name,
            "time_periods": time_periods
        }
        ret = self._make_request(Method.POST, "timeperiod", data=params)
        return ret["data"]

    def time_period_update(self, time_period_id: Union[str, int], changes: dict) -> None:
        """This method is used to update a TimePeriod

        :param time_period_id: ID of the TimePeriod
        :param changes: Changes to submit. The keys define the parameter to update and the value sets its value.
        """
        changes = {x.value if isinstance(x, TimePeriodParam) else x: changes[x] for x in changes}
        self._make_request(Method.PUT, f"timeperiod/{time_period_id}", data=changes)

    def time_period_delete(self, time_period_id: Union[str, int]) -> None:
        """This method is used to delete a TimePeriod

        :param time_period_id: ID of the TimePeriod
        """
        self._make_request(Method.DELETE, f"timeperiod/{time_period_id}")

    def global_variable_get(self, global_variable_id: Union[str, int, list] = None) -> Union[list, GlobalVariable]:
        """This method is used to create a GlobalVariable.

        :param global_variable_id: ID or list of IDs of GlobalVariables

        :return: Returns a GlobalVariable or a list of them
        """
        if global_variable_id:
            if isinstance(global_variable_id, list):
                ret = self._make_request(Method.GET, "globalvariable", {"filter": [str(x) for x in global_variable_id]})
                return [GlobalVariable(**x) for x in ret["data"]]
            elif isinstance(global_variable_id, str) or isinstance(global_variable_id, int):
                ret = self._make_request(Method.GET, f"globalvariable/{global_variable_id}")
                return GlobalVariable(**ret["data"])
            else:
                raise ValueError
        else:
            ret = self._make_request(Method.GET, "globalvariable")
        return [GlobalVariable(**x) for x in ret["data"]]

    def global_variable_update(self, global_variable_id: Union[str, int], changes: dict) -> None:
        """This method is used to update a GlobalVariable

        :param global_variable_id: ID of a GlobalVariable
        :param changes: Changes to submit. The keys define the parameter to update and the value sets its value.
        """
        changes = {x.value if isinstance(x, TimePeriodParam) else x: changes[x] for x in changes}
        self._make_request(Method.PUT, f"globalvariable/{global_variable_id}", data=changes)

    def global_variable_delete(self, global_variable_id: Union[str, int]) -> None:
        """This method is used to delete a GlobalVariable

        :param global_variable_id: ID of the GlobalVariable
        """
        self._make_request(Method.DELETE, f"globalvariable/{global_variable_id}")

    def metric_template_get(self, metric_template_id: Union[str, int, list] = None) -> Union[list, MetricTemplate]:
        """This method is used to create a MetricTemplate.

        :param metric_template_id: ID or list of IDs of MetricTemplate

        :return: Returns a MetricTemplate or a list of them
        """
        if metric_template_id:
            if isinstance(metric_template_id, list):
                ret = self._make_request(Method.GET, "metrictemplate", {"filter": [str(x) for x in metric_template_id]})
                return [MetricTemplate(**x) for x in ret["data"]]
            elif isinstance(metric_template_id, str) or isinstance(metric_template_id, int):
                ret = self._make_request(Method.GET, f"metrictemplate/{metric_template_id}")
                return MetricTemplate(**ret["data"])
            else:
                raise ValueError
        else:
            ret = self._make_request(Method.GET, "metrictemplate")
        return [MetricTemplate(**x) for x in ret["data"]]

    def metric_template_create(
            self, name: str, linked_check_id: Union[str, int] = "", metric_templates: Union[list, str, int] = None,
            scheduling_interval: Union[str, int] = "", scheduling_period_id: Union[str, int] = "",
            notification_period_id: Union[str, int] = "", variables: dict = None
    ) -> int:
        """This method is used to create a MetricTemplate

        :param name: Name of the MetricTemplate
        :param linked_check_id: Optional. ID of a Check.
        :param metric_templates: Optional. ID or list of IDs of MetricTemplate this MetricTemplate should inherit from.
        :param scheduling_interval: Optional. Interval the checks should be executed
        :param scheduling_period_id: Optional. ID of the TimePeriod in which check should be executed
        :param notification_period_id: Optional. ID of the TimePeriod in which checks should cause notifications
        :param variables: Optional. Dictionary of key value pairs.
        :return:
        """
        params = {"name": name}
        if linked_check_id:
            params["linked_check"] = linked_check_id
        if metric_templates:
            params["metric_templates"] = metric_templates
        if scheduling_interval:
            params["scheduling_interval"] = scheduling_interval
        if scheduling_period_id:
            params["scheduling_period"] = scheduling_period_id
        if notification_period_id:
            params["notification_period"] = notification_period_id
        if variables:
            params["variables"] = variables

        ret = self._make_request(Method.POST, "metrictemplate", data=params)
        return ret["data"]

    def metric_template_update(self, metric_template_id: Union[str, int], changes: dict) -> None:
        """This method is used to update a MetricTemplate

        :param metric_template_id: ID of a MetricTemplate
        :param changes: Changes to submit. The keys define the parameter to update and the value sets its value.
        """
        changes = {x.value if isinstance(x, MetricTemplateParam) else x: changes[x] for x in changes}
        self._make_request(Method.PUT, f"metrictemplate/{metric_template_id}", data=changes)

    def metric_template_delete(self, metric_template_id: Union[str, int]) -> None:
        """This method is used to delete a MetricTemplate

        :param metric_template_id: ID of a MetricTemplate
        """
        self._make_request(Method.DELETE, f"metrictemplates/{metric_template_id}")
