import pytest
import mock
import datetime
from async_mock_ext import patch_async_mock
from duckmock.discord import MockAsyncIterator
from cogs.insights import Insights
from duckmock.datetime import patch_utcnow


@pytest.mark.asyncio
@patch_async_mock
@mock.patch('discord.ext.commands.Bot')
@mock.patch('server.channels')
@mock.patch('discord.TextChannel')
async def test_check_should_respond_no_messages(bot, channels, channel):
    bot.get_cog.return_value = channels
    channels.get_general_channel.return_value = channel
    channel.history.return_value = MockAsyncIterator(None)
    clazz = Insights(bot, start_tasks=False)
    await clazz._Insights__check_should_respond()
    channels.get_general_channel.assert_called()
    channel.send.assert_not_called()


@pytest.mark.asyncio
@patch_async_mock
@mock.patch('discord.ext.commands.Bot')
@mock.patch('server.channels')
@mock.patch('discord.TextChannel')
@mock.patch('discord.Message')
async def test_check_should_respond_new_message(bot, channels, channel, message):
    with patch_utcnow(datetime.datetime(2000, 1, 1, hour=12, minute=00)):
        bot.get_cog.return_value = channels
        channels.get_general_channel.return_value = channel
        message.created_at = datetime.datetime(2000, 1, 1, hour=11, minute=38)
        message.author.id = 244629273191645184
        channel.history.return_value = MockAsyncIterator(message)
        clazz = Insights(bot, start_tasks=False)
        await clazz._Insights__check_should_respond()
        channels.get_general_channel.assert_called()
        channel.send.assert_not_called()


@pytest.mark.asyncio
@patch_async_mock
@mock.patch('discord.ext.commands.Bot')
@mock.patch('server.channels')
@mock.patch('discord.TextChannel')
@mock.patch('discord.Message')
async def test_check_should_respond_not_special_user(bot, channels, channel, message):
    with patch_utcnow(datetime.datetime(2000, 1, 1, hour=12, minute=00)):
        bot.get_cog.return_value = channels
        channels.get_general_channel.return_value = channel
        message.created_at = datetime.datetime(2000, 1, 1, hour=11, minute=00)
        message.author.id = 0
        channel.history.return_value = MockAsyncIterator(message)
        clazz = Insights(bot, start_tasks=False)
        await clazz._Insights__check_should_respond()
        channels.get_general_channel.assert_called()
        channel.send.assert_not_called()


@pytest.mark.asyncio
@patch_async_mock
@mock.patch('discord.ext.commands.Bot')
@mock.patch('server.channels')
@mock.patch('discord.TextChannel')
@mock.patch('discord.Message')
async def test_check_should_respond_old_message_sent_by_special_user(bot, channels, channel, message):
    with patch_utcnow(datetime.datetime(2000, 1, 1, hour=12, minute=00)):
        bot.get_cog.return_value = channels
        channels.get_general_channel.return_value = channel
        message.created_at = datetime.datetime(2000, 1, 1, hour=11, minute=00)
        message.author.id = 244629273191645184
        channel.history.return_value = MockAsyncIterator(message)
        clazz = Insights(bot, start_tasks=False)
        await clazz._Insights__check_should_respond()
        channels.get_general_channel.assert_called()
        channel.send.assert_called()
