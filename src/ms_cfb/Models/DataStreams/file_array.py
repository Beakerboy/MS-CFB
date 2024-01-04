import os
from ms_cfb.Models.DataStreams.array_stream import ArrayStream
from typing import TypeVar


T = TypeVar('T', bound='FileArray')


class FileArray(ArrayStream):
    """
    A FileArray is an array of FileStream objects.
    """
