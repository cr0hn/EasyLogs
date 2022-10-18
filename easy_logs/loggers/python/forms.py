import logging
import datetime

from typing import Literal, Optional

from pydantic import BaseModel


class PythonHTTPHandlerEntryLogForm(BaseModel):
    msg: str
    name: str
    args: Optional[str]
    module: Optional[str]
    lineno: int
    thread: int
    msecs: float
    process: int
    funcName: str
    pathname: str
    filename: str
    created: float
    exec_info: Optional[str]
    exec_text: Optional[str]
    stack_info: Optional[str]
    threadName: str
    processName: str
    relativeCreated: float
    levelno: Literal["0", "10", "20", "30", "40", "50"]
    levelname: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]




