"""assets and liabilities endpoints testing"""

import json
from multiprocessing import Process
from typing import List, Dict, Union
import pytest
import requests


@pytest.mark.parametrize("base_access_app", ["users_schema"], indirect=True)
def test_asset_post(base_access_app: Process, dummy_assets: List[Dict[str, Union[str, float]]]):
    """Assets endpoint should be able to add assets when passing a valid api key"""
    
