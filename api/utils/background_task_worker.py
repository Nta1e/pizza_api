import asyncio


class BackgroundTaskWorker:
    @classmethod
    def start_work(cls, asyn_function, args):
        """This function helps to run an unpredictable function in the background.
        it uses an event loop as central executor.
        :param asyn_function: An asyn function that acts as coroutine.
        :param args: The async function args or params.
                     it should be a tuple of args.
        :return: None
        """
        event_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(event_loop)
        event_loop.run_in_executor(None, cls.run_task, asyn_function, args)

    @classmethod
    def run_task(cls, asyn_function, args):
        """This function creates a future task which runs in background
        until completion
        :param asyn_function: An asyn function that acts as coroutine
        :param args: The async function args or params
        :return: None
        """
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        task = asyncio.ensure_future(asyn_function(*args))

        loop.run_until_complete(task)
        loop.close()
