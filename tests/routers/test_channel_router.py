from routers.channel_router import get_channels

import pytest
import asyncio

from unittest.mock import AsyncMock, patch

fake_data = range(10)
mocked_method = AsyncMock(return_value=fake_data)

@pytest.mark.asyncio
@patch('routers.channel_router.get_channel_records', new=mocked_method)
async def test_get_channels():
    # arrange - do setup here
    
   
    # act - call/invoke SUT
    results = await get_channels() 
    
    # assert 
    mocked_method.assert_called_once()
    mocked_method.assert_called_with(0, 10)
    assert len(results) == 10