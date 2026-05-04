from unittest.mock import AsyncMock


def test_ssrf_vulnerability(client, mock_httpx):
    mock_response = AsyncMock()
    mock_response.status_code = 200
    mock_response.text = '{"SUPER_SECRET_KEY": "123"}'

    mock_httpx.get = AsyncMock(return_value=mock_response)

    response = client.get(
        "/vulnerable/ssrf/fetch",
        params={"url": "http://internal/metadata"},
    )

    assert "SUPER_SECRET_KEY" in response.json()["content"]
