import asyncio


async def test() -> None:
    pass


if __name__ == '__main__':
    try:
        asyncio.run(test())
    except KeyboardInterrupt:
        print('stop')
