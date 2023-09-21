from unittest.mock import MagicMock, patch

import pytest
from hamcrest import assert_that, equal_to

from .. import mbta


class TestMBTARequest:
    @pytest.fixture
    def mock_httpx_stream(self):
        with patch("mbta.httpx.stream") as mock_stream:
            yield mock_stream

    def test_make_api_request(self, mock_httpx_stream):
        # Prepare a fake response
        expected = [b'{"data": "spam eggs"}']
        fake_response = MagicMock()
        fake_response.iter_bytes.return_value = expected

        # Configure the mock stream to return the fake response
        mock_httpx_stream.return_value.__enter__.return_value = fake_response

        # Call the _make_api_request function
        endpoint = "fake_endpoint"
        params = {"spam": "eggs"}
        response = list(mbta._make_api_request(endpoint, params))

        # Assert that the request was made with the correct arguments
        mock_httpx_stream.assert_called_once_with(
            method="GET",
            url="https://api-v3.mbta.com/fake_endpoint",
            headers={"Accept": "text/event-stream", "X-API-Key": "mock-api-key"},
            params={"spam": "eggs"},
            timeout=None,
        )

        # Assert that the response contains the fake data
        assert_that(response, equal_to(expected))
