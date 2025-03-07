#!/usr/bin/env python3
# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

"""
This contains the TorchX AppDef and related component definitions. These are
used by components to define the apps which can then be launched via a TorchX
scheduler or pipeline adapter.
"""

from typing import Dict, Optional

from torchx.specs.named_resources_aws import NAMED_RESOURCES as AWS_NAMED_RESOURCES
from torchx.util.entrypoints import load_group

from .api import (  # noqa: F401 F403
    ALL,
    AppDef,
    AppDryRunInfo,
    AppHandle,
    AppState,
    AppStatus,
    BindMount,
    CfgVal,
    DeviceMount,
    from_function,
    get_type_name,
    InvalidRunConfigException,
    is_terminal,
    macros,
    make_app_handle,
    MalformedAppHandleException,
    MISSING,
    NONE,
    NULL_RESOURCE,
    parse_app_handle,
    parse_mounts,
    ReplicaState,
    ReplicaStatus,
    Resource,
    RetryPolicy,
    Role,
    RoleStatus,
    runopt,
    runopts,
    UnknownAppException,
    UnknownSchedulerException,
    VolumeMount,
)


GiB: int = 1024


def _load_named_resources() -> Dict[str, Resource]:
    resource_methods = load_group("torchx.named_resources", default={})
    materialized_resources = {}
    default = AWS_NAMED_RESOURCES
    for name, resource in default.items():
        materialized_resources[name] = resource()
    for resource_name, resource_method in resource_methods.items():
        materialized_resources[resource_name] = resource_method()
    materialized_resources["NULL"] = NULL_RESOURCE
    return materialized_resources


named_resources: Dict[str, Resource] = _load_named_resources()


def resource(
    cpu: Optional[int] = None,
    gpu: Optional[int] = None,
    memMB: Optional[int] = None,
    h: Optional[str] = None,
) -> Resource:
    """
    Convenience method to create a ``Resource`` object from either the
    raw resource specs (cpu, gpu, memMB) or the registered named resource (``h``).
    Note that the (cpu, gpu, memMB) is mutually exclusive with ``h``
    with ``h`` taking predecence if specified.

    If ``h`` is specified then it is used to look up the
    resource specs from the list of registered named resources.
    See `registering named resource <https://pytorch.org/torchx/latest/advanced.html#registering-named-resources>`_.

    Otherwise a ``Resource`` object is created from the raw resource specs.

    Example:

    .. code-block:: python

         resource(cpu=1) # returns Resource(cpu=1)
         resource(named_resource="foobar") # returns registered named resource "foo"
         resource(cpu=1, named_resource="foobar") # returns registered named resource "foo" (cpu=1 ignored)
         resource() # returns default resource values
         resource(cpu=None, gpu=None, memMB=None) # throws
    """

    if h:
        return get_named_resources(h)
    else:
        # could make these defaults customizable via entrypoint
        # not doing that now since its not a requested feature and may just over complicate things
        # keeping these defaults method local so that no one else takes a dep on it
        DEFAULT_CPU = 2
        DEFAULT_GPU = 0
        DEFAULT_MEM_MB = 1024

        return Resource(
            cpu=cpu or DEFAULT_CPU,
            gpu=gpu or DEFAULT_GPU,
            memMB=memMB or DEFAULT_MEM_MB,
        )


def get_named_resources(res: str) -> Resource:
    """
    Get resource object based on the string definition registered via entrypoints.txt.

    TorchX implements ``named_resource`` registration mechanism, which consists of
    the following steps:

    1. Create a module and define your resource retrieval function:

    .. code-block:: python

     # my_module.resources
     from typing import Dict
     from torchx.specs import Resource

     def gpu_x_1() -> Dict[str, Resource]:
         return Resource(cpu=2, memMB=64 * 1024, gpu = 2)

    2. Register resource retrieval in the entrypoints section:

    ::

     [torchx.named_resources]
     gpu_x_1 = my_module.resources:gpu_x_1

    The ``gpu_x_1`` can be used as string argument to this function:

    ::

     from torchx.specs import named_resources
     resource = named_resources["gpu_x_1"]

    """
    return named_resources[res]
