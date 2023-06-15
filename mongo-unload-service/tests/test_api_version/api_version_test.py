#
# Copyright (c) 2023 by Delphix. All rights reserved.
#

from src.config import get_config

config = get_config()


def test_api_version(test_app):
    """
    tests positive flow of GET api-version
    Args:
        test_app: fixture
    """
    response = test_app.get("/api/api-version")
    assert response.status_code == 200
    assert response.json() == {"versionId": config["default"]["version"]}
