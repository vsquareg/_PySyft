# stdlib
from typing import Optional
from typing import Any

# third party
from google.protobuf.reflection import GeneratedProtocolMessageType

# syft relative
from ... import deserialize
from ... import serialize
from ...core.common import UID
from ...core.common.serde.serializable import bind_protobuf
from ...proto.lib.python.not_implemented_pb2 import (
    SyNotImplemented as NotImplemented_PB,
)
from .primitive_factory import PrimitiveFactory
from .primitive_interface import PyPrimitive
from .types import SyPrimitiveRet


@bind_protobuf
class _SyNotImplemented(PyPrimitive):
    def __init__(self, id: Optional[UID] = None):
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

    def __eq__(self, other: Any) -> SyPrimitiveRet:
        if isinstance(other, _SyNotImplemented):
            return PrimitiveFactory.generate_primitive(value=True)

        if other is NotImplemented:
            return PrimitiveFactory.generate_primitive(value=True)

        res = NotImplemented.__eq__(other)
        return PrimitiveFactory.generate_primitive(value=res)

    def upcast(self) -> type(NotImplemented):  # type: ignore
        return NotImplemented

    def __hash__(self) -> SyPrimitiveRet:
        res = NotImplemented.__hash__()
        return PrimitiveFactory.generate_primitive(value=res)

    def _object2proto(self) -> NotImplemented_PB:
        notImplemented_PB = NotImplemented_PB()
        notImplemented_PB.id.CopyFrom(serialize(obj=self.id))
        return notImplemented_PB

    @staticmethod
    def _proto2object(proto: NotImplemented_PB) -> "_SyNotImplemented":
        not_impl_id: UID = deserialize(blob=proto.id)

        de_not_impl = _SyNotImplemented()
        de_not_impl._id = not_impl_id
        print("DeSer")
        # stdlib
        import traceback

        traceback.print_stack()
        # return de_not_impl
        return NotImplemented

    @staticmethod
    def get_protobuf_schema() -> GeneratedProtocolMessageType:
        return NotImplemented_PB


SyNotImplemented = _SyNotImplemented()
