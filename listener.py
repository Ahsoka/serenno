from .utils import ProductType, WrongWorkspace
from .pypresence.pypresence import Presence
from .fusion360utils import add_handler
from adsk.core import Application
from adsk.fusion import Design

import time


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

    def init(self, app: Application):
        self.connect()
        self.app = app
        self.current_state['start'] = int(time.time())
        self.document_change(self.app.activeDocument.name, update=False)
        self.workspace_change(self.app.userInterface.activeWorkspace.name, update=False)
        self.update()

        add_handler(
            app.documentActivating,
            lambda doc_event: self.document_change(doc_event.document.name)
        )
        add_handler(
            app.userInterface.workspacePreActivate,
            lambda workspace_event: self.workspace_change(workspace_event.workspace.name)
        )

    def is_assembly(self) -> bool:
        product = self.app.activeProduct
        if product.productType == ProductType.DESIGN:
            product: Design
            return len(product.allComponents) > 1
        raise WrongWorkspace(f'Current workspace is {product.productType!r}')

    def document_change(self, document_name: str, update: bool = True):
        if document_name is None:
            self.current_state['details'] = "Idling"
        else:
            self.current_state['details'] = f"Editing {document_name}"

        if update and self.connected:
            self.update()

    def workspace_change(self, workspace_name: str, update: bool = True):
        self.current_state['state'] = f"Workspace: {workspace_name}"
        # TODO: Add image update logic.
        if update and self.connected:
            self.update()
