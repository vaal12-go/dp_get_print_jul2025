import types


def hash_array_tuple_tree(hash_to_update, arr) -> None:
    # TODO: make reservation for circular references
    for el in arr:
        if isinstance(el, list) or isinstance(el, tuple) \
                or isinstance(el, types.GeneratorType):
            hash_array_tuple_tree(hash_to_update, el)
        else:
            hash_to_update.update(el.__str__().encode('utf-8'))
