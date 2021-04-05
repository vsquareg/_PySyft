# stdlib
from collections import UserList
from typing import Any
from typing import List as ListType
from typing import Optional
from typing import Union

# third party
from google.protobuf.reflection import GeneratedProtocolMessageType

# syft relative
from ... import deserialize
from ... import serialize
from ...core.common import UID
from ...core.common.serde.serializable import bind_protobuf
from ...proto.lib.python.slice_pb2 import Slice as Slice_PB
from .iterator import Iterator
from .primitive_factory import PrimitiveFactory
from .primitive_factory import isprimitive
from .primitive_interface import PyPrimitive
from .slice import Slice
from .types import SyPrimitiveRet
from .util import downcast
from .util import upcast


class RangeIterator(Iterator):
    pass


@bind_protobuf
class Range(PyPrimitive):
    __slots__ = ["_id", "_index"]

    def __init__(self, start: int = 0, stop: int = None, step: int = 1, id: Optional[UID] = None):
        if stop is None:
            stop = start
            start = 0

        self.value = range(start, stop, step)
        self._id: UID = id if id else UID()

    @property
    def id(self) -> UID:
        """We reveal PyPrimitive.id as a property to discourage users and
        developers of Syft from modifying .id attributes after an object
        has been initialized.

        :return: returns the unique id of the object
        :rtype: UID
        """
        return self._id

    def __gt__(self, other: Any) -> SyPrimitiveRet:
        res = self.value.__gt__(other)
        return PrimitiveFactory.generate_primitive(value=res)

    def __le__(self, other: Any) -> SyPrimitiveRet:
        res = self.value.__le__(other)
        return PrimitiveFactory.generate_primitive(value=res)

    def __lt__(self, other: Any) -> SyPrimitiveRet:
        res = self.value.__lt__(other)
        return PrimitiveFactory.generate_primitive(value=res)

    def __contains__(self, other: Any) -> SyPrimitiveRet:
        res = self.value.__contains__(other)
        return PrimitiveFactory.generate_primitive(value=res)

    def __eq__(self, other: Any) -> SyPrimitiveRet:
        res = self.value.__eq__(other)
        return PrimitiveFactory.generate_primitive(value=res)

    def __ge__(self, other: Any) -> SyPrimitiveRet:
        res = self.value.__ge__(other)
        return PrimitiveFactory.generate_primitive(value=res)

    def __ne__(self, other: Any) -> SyPrimitiveRet:
        res = self.value.__ne__(other)
        return PrimitiveFactory.generate_primitive(value=res)

    def __sizeof__(self) -> SyPrimitiveRet:
        res = self.value.__sizeof__()
        return PrimitiveFactory.generate_primitive(value=res)

    def __bool__(self) -> SyPrimitiveRet:
        res = self.value.__bool__()
        return PrimitiveFactory.generate_primitive(value=res)

    def __len__(self) -> Any:
        res = self.value.__len__()
        return res
        return PrimitiveFactory.generate_primitive(value=res)

    def __getitem__(self, key: Union[int, str, slice, Slice]) -> Any:
        res = self.value.__getitem__(key)
        return PrimitiveFactory.generate_primitive(value=res)

    def __iter__(self, max_len: Optional[int] = None) -> RangeIterator:
        return RangeIterator(self, max_len=max_len)

    @property
    def start(self) -> Optional[int]:
        return self.value.start

    @property
    def step(self) -> Optional[int]:
        return self.value.step

    @property
    def stop(self) -> Optional[int]:
        return self.value.stop

    @property
    def index(self) -> Optional[int]:
        return self.value.index

    @property
    def count(self) -> Optional[int]:
        return self.value.count

    def _object2proto(self) -> Slice_PB:
        slice_pb = Slice_PB()
        if self.start:
            slice_pb.start = self.start
            slice_pb.has_start = True

        if self.stop:
            slice_pb.stop = self.stop
            slice_pb.has_stop = True

        if self.step:
            slice_pb.step = self.step
            slice_pb.has_step = True

        slice_pb.id.CopyFrom(self._id._object2proto())

        return slice_pb

    @staticmethod
    def _proto2object(proto: Slice_PB) -> "Slice":
        id_: UID = deserialize(blob=proto.id)
        start = None
        stop = None
        step = None
        if proto.has_start:
            start = proto.start

        if proto.has_stop:
            stop = proto.stop

        if proto.has_step:
            step = proto.step

        return Slice(
            start=start,
            stop=stop,
            step=step,
            id=id_,
        )

    @staticmethod
    def get_protobuf_schema() -> GeneratedProtocolMessageType:
        return Slice_PB
