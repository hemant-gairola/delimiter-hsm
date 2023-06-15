#
# Copyright (c) 2023 by Delphix. All rights reserved.
#

import pytest
from src.main import app
from starlette.testclient import TestClient


@pytest.fixture(scope="module", autouse=True)
def test_app():
    """
    fixture for test app
    """
    client = TestClient(app)
    yield client  # testing happens here
