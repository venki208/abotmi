var webSocketBridge;

function create_websocket_connection(){
  var ws_path = "/trex/stream/";
  webSocketBridge = new channels.WebSocketBridge();
  webSocketBridge.connect(ws_path);
  webSocketBridge.socket.onopen = function(){
    webSocketBridge.send({
      "command": "join",
      "room": 1
    });
  }
  set_websocket(webSocketBridge);
  return webSocketBridge;
}

function get_websocket(){
  return webSocketBridge;
}

function set_websocket(data){
  webSocketBridge = data;																																								return webSocketBridge;
}
