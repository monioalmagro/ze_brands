# Third-party Libraries
import graphene


class NonNullConnection(graphene.relay.Connection, abstract=True):
    """
    Custom Connection because of graphene Does Not support non null
    edges field by default
    """

    @classmethod
    def __init_subclass_with_meta__(cls, node, **kwargs):
        if not hasattr(cls, "Edge"):
            _node = node

            class EdgeBase(graphene.ObjectType, name=f"{node._meta.name}Edge"):
                cursor = graphene.String(required=True)
                node = graphene.Field(_node, required=True)

            setattr(cls, "Edge", EdgeBase)  # noqa

        if not hasattr(cls, "edges"):
            setattr(  # noqa
                cls,
                "edges",
                graphene.List(graphene.NonNull(cls.Edge), required=True),
            )

        super(NonNullConnection, cls).__init_subclass_with_meta__(
            node=_node, **kwargs
        )
