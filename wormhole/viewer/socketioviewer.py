from wormhole.viewer import AbstractViewer

from urllib.parse import urlparse
from typing import Callable
import socketio

# Base Class for Everything SocketIO Viewer
class SocketIOViewerBase(AbstractViewer):
    def __init__(
        self, 
        data_processor: Callable,
        url: str, 
        height: int, 
        width: int, 
        max_fps: int = 30, 
        *args,
        **kwargs
    ):
        # Save basic variables about stream
        parsed_url = urlparse(url)
        self.hostname = f"{parsed_url.scheme}://{parsed_url.netloc}"
        self.namespace = parsed_url.path
        
        # Save Raw Data Processing Function
        self.data_processor = data_processor
        
        # Setup SocketIO Client
        self.sio_client = socketio.Client(*args, **kwargs)
        
        # Initiate Video Parent Object
        super().__init__(height, width, max_fps=max_fps)
        
        # Create SocketIO Handler for when raw images stream in
        # Proxying the function with a lambda so that the self context is also passed in
        self.sio_client.on("frame", self.data_processor, namespace=self.namespace)
        
        # Connect To Server
        self.sio_client.connect(self.hostname, namespaces=[self.namespace])
