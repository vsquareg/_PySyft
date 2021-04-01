# stdlib
import json
from os import path
import os.path
from typing import Dict
from typing import Union

# third party
from packaging import version
import pytest
import torch
import torchvision as tv
import PIL

# syft absolute
import syft as sy
from syft.lib.torchvision.allowlist import allowlist


TORCHVISION_VERSION = version.parse(tv.__version__)


@pytest.fixture(scope="function")
def pil_img() -> PIL.Image.Image:
    img_file = '../../../../docs/img/logo.png'
    if path.isfile(img_file):
        return PIL.Image.open(img_file)
    else:
        raise Exception('Image file not found for loading tests.')


@pytest.fixture(scope="function")
def tens(pil_img) -> torch.Tensor:
    return tv.transforms.functional.to_tensor(pil_img)


@pytest.fixture(scope="function")
def alice() -> sy.VirtualMachine:
    return sy.VirtualMachine(name="alice")


def version_supported(support_dict: Union[str, Dict[str, str]]) -> bool:
    if isinstance(support_dict, str):
        return True
    else:
        if "min_version" not in support_dict.keys():
            return True
        return TORCHVISION_VERSION >= version.parse(support_dict["min_version"])


def test_allowlist(alice: sy.VirtualMachine, tens: torch.Tensor, pil_img: PIL.Image.Image) -> None:
    # Required for testing on torchvision==1.6.0
    sy.load('PIL')
    alice_client = alice.get_root_client()
    torchvision = alice_client.torchvision
    torch = alice_client.torch
    PIL = alice_client.PIL
    try:
        tx = torch.rand(4)
        tx = tx * 2
    except Exception as e:
        print(e)

    try:
        with open(__file__.replace(".py", "_params.json"), "r") as f:
            TEST_PARAMS = json.loads(f.read())
    except Exception as e:
        print(f"Exception {e} triggered")
        raise e

    transforms = torchvision.transforms
    transforms.RandomAffine(2)
    for item in allowlist:
        arr = item.split(".")
        # print(item)
        if (
            arr[1] == "datasets"
            and len(arr) <= 3
            and item in TEST_PARAMS.keys()
            and version_supported(support_dict=allowlist[item])
        ):
            try:
                exec(item + TEST_PARAMS[item])
            except RuntimeError as e:
                assert (
                    "not found" in str(e)
                    or "not present in the root directory" in str(e)
                    or "does not exist" in str(e)
                )
            except FileNotFoundError as e:
                assert "No such file or directory" in str(
                    e
                ) or "cannot find the path" in str(e)
            except ModuleNotFoundError as e:
                assert "No module named" in str(e)
            except KeyError:
                pass
        elif item in TEST_PARAMS.keys() and version_supported(
            support_dict=allowlist[item]
        ):
            exec(item + TEST_PARAMS[item])
