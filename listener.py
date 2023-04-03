from .pypresence.pypresence import Presence


class Listener(Presence):
    def __init__(
        self,
        client_id: int,
        pipe: int = 0,
    ):
        super().__init__(str(client_id), pipe=pipe)
        self.connected = False
        self.current_state = {
            'state': None,
            'details': None,

            'large_image': None,
            'large_text': None,

            'small_image': None,
            'small_text': None,

            'start': None,
            'end': None
        }

    def update(self):
        super().update(**self.current_state)

    def connect(self):
        super().connect()
        self.connected = True

    def close(self):
        super().close()
        self.connected = False

    def destroy(self):
        # NOTE: Must use clear here otherwise it won't be cleared
        # HOWEVER even if for whatever reason clear doesn't run
        # Discord will automatically end the presence after seeing
        # that the PID is dead.
        self.clear()
        self.close()
