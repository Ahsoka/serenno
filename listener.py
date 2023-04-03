from .utils import WorkspaceEnum, ProductType, WrongWorkspace
from adsk.core import Application, Document, Workspace
from .pypresence.pypresence import Presence
from .fusion360utils import add_handler
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

        self.docs = {}

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
        self.current_state['start'] = int(time.time())
        self.document_change(app.activeDocument, update=False)
        self.workspace_change(app.userInterface.activeWorkspace, update=False)

        add_handler(
            app.documentActivating,
            lambda doc_event: self.document_change(doc_event.document)
        )
        add_handler(
            app.userInterface.workspacePreActivate,
            lambda workspace_event: self.workspace_change(workspace_event.workspace)
        )

        self.connect()
        self.update()

    def is_assembly(self, document: Document) -> bool:
        design = document.products.itemByProductType(ProductType.DESIGN)
        if design:
            design: Design
            return len(design.allComponents) > 1
        raise WrongWorkspace(f'Current workspace is {design.productType!r}')

    def document_change(self, document: Document, update: bool = True):
        try:
            self.docs[document.creationId] = self.is_assembly(document)
        except WrongWorkspace:
            pass

        document_name = document.name
        if document_name is None:
            self.current_state['details'] = "Idling"
        else:
            self.current_state['details'] = f"Editing {document_name}"

        if document.creationId in self.docs:
            self.current_state['large_text'] = (
                'Editing an Assembly' if self.docs[document.creationId] else 'Editing a Component'
            )
        else:
            self.current_state['large_text'] = None

        if update and self.connected:
            self.update()

    def workspace_change(self, workspace: Workspace, update: bool = True):
        workspace_name = workspace.name
        self.current_state['state'] = f"Workspace: {workspace_name}"

        for workspace_enum in WorkspaceEnum:
            if workspace.id == workspace_enum:
                # NOTE: Transforms enum name from GENERATIVE_DESIGN -> generative-design-workspace
                large_image = f"{workspace_enum.name.lower().replace('_', '-')}-workspace"
                self.current_state['large_image'] = large_image
                self.current_state['small_image'] = 'fusion-360-icon'
                self.current_state['small_text'] = 'Autodesk Fusion 360'
                break
        else:
            self.current_state['large_image'] = 'fusion-360-icon-borderless'
            self.current_state['small_image'] = None
            self.current_state['small_text'] = None

        if update and self.connected:
            self.update()
