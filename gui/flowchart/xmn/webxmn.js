function create_flowchart(data) {
    // start the init function of flowchart
    flowchart(data);
}

function flowchart(jsondata) {
    jsPlumb.ready(function() {

        var conn_out = ["BottomLeft", "BottomRight", "TopLeft", "TopRight"];
        var conn_in = ["LeftMiddle", "TopCenter", "RightMiddle", "BottomCenter"];

        var data = jsondata;
        var connection_label = {};

        //connection label
        for (i in data['connection']) {
            connection_label[
                'flowchart' + data['connection'][i]['chain'][0] + '-'
                + 'flowchart' + data['connection'][i]['chain'][1]
            ] = data['connection'][i]['title'];
        }

        var instance = jsPlumb.getInstance({
            // default drag options
            DragOptions : { cursor: 'pointer', zIndex:2000 },
            // the overlays to decorate each connection with.
            // note that the label overlay uses a function to generate
            // the label text; in this
            // case it returns the 'labelText' member that we set on each
            // connection in the 'init' method below.
            ConnectionOverlays : [
                [ "Arrow", { location:1 } ],
                [ "Label", {
                    location:0.1,
                    id:"label",
                    cssClass:"aLabel"
                }]
            ],
            Container:"flowchart-webxmn"
        });

        // this is the paint style for the connecting lines..
        var connectorPaintStyle = {
            lineWidth:4,
            strokeStyle:"#61B7CF",
            joinstyle:"round",
            outlineColor:"white",
            outlineWidth:2
        };

        // .. and this is the hover style.
        var connectorHoverStyle = {
            lineWidth:4,
            strokeStyle:"#216477",
            outlineWidth:2,
            outlineColor:"white"
        };

        var endpointHoverStyle = {
            fillStyle:"#216477",
            strokeStyle:"#216477"
        };

        // the definition of source endpoints (the small blue ones)
        var sourceEndpoint = {
            endpoint:"Dot",
            anchor: conn_out,
            paintStyle:{
                strokeStyle:"#7AB02C",
                fillStyle:"transparent",
                radius:4,
                lineWidth:3
            },
            maxConnections:-1,
            isSource:true,
            connector:[
                "Flowchart", {
                    stub:[40, 60], gap:10,
                    cornerRadius:5,
                    alwaysRespectStubs:true } ],
            connectorStyle:connectorPaintStyle,
            hoverPaintStyle:endpointHoverStyle,
            connectorHoverStyle:connectorHoverStyle,
            dragOptions:{},
            overlays:[
                [ "Label", {
                    location:[0.5, 1.5],
                    label:"Drag",
                    cssClass:"endpointSourceLabel"
                } ]
            ]
        };

        // the definition of target endpoints
        // (will appear when the user drags a connection)
        var targetEndpoint = {
            endpoint:"Dot",
            anchor: conn_in,
            paintStyle:{ fillStyle:"#7AB02C",radius:8 },
            hoverPaintStyle:endpointHoverStyle,
            maxConnections:-1,
            dropOptions:{ hoverClass:"hover", activeClass:"active" },
            isTarget:true,
            overlays:[
                [ "Label", {
                    location:[0.5, -0.5],
                    label:"Drop",
                    cssClass:"endpointTargetLabel" } ]
            ]
        };

        var init = function(connection, connection_label) {
            label = connection.sourceId + '-' + connection.targetId;
            _id = connection.sourceId + '-' + connection.targetId;

            if(_id in connection_label) {
                label = connection_label[_id];
            }

            connection.getOverlay("label").setLabel(label);
            connection.bind("editCompleted", function(o) {
                if (typeof console != "undefined")
                    console.log("connection edited. path is now ", o.path);
            });
        };

        var _addEndpoints = function(
            toId, sourceAnchors, targetAnchors, labelConnection
        ) {
            for (var i = 0; i < sourceAnchors.length; i++) {
                var sourceUUID = toId + sourceAnchors[i];

                instance.addEndpoint(
                    "flowchart" + toId,
                    sourceEndpoint, {
                        anchor:sourceAnchors[i],
                        uuid:sourceUUID,
                        label: labelConnection});
            }
            for (var j = 0; j < targetAnchors.length; j++) {
                var targetUUID = toId + targetAnchors[j];
                instance.addEndpoint(
                    "flowchart" + toId,
                    targetEndpoint, {
                        anchor:targetAnchors[j],
                        uuid:targetUUID,
                        label: labelConnection});
            }
        };

        var create_node = function (_data) {
            data = data.concat(_data);
            for (i in _data['box']) {
                $('#flowchart-webxmn').append(
                    '<div class="window" id="flowchart' + _data['box'][i]['id'] + '" '
                    + ' style="top:' + _data['box'][i]['top']
                    + '; left:' + _data['box'][i]['left'] + ';">'
                    + '<strong>' + _data['box'][i]['label'] + '</strong><br/><br/></div>'
                );
            }
             /*
            _addEndpoints("Window4", ["TopCenter", "BottomCenter"], ["LeftMiddle", "RightMiddle"]);
            _addEndpoints("Window2", ["LeftMiddle", "BottomCenter"], ["TopCenter", "RightMiddle"]);
            _addEndpoints("Window3", ["RightMiddle", "BottomCenter"], ["LeftMiddle", "TopCenter"]);
            _addEndpoints("Window1", ["LeftMiddle", "RightMiddle"], ["TopCenter", "BottomCenter"]);
            */
            for(i in _data['box']) {
                _addEndpoints(
                    _data['box'][i]['id'],
                    _data['box'][i]['conn_out'],
                    _data['box'][i]['conn_in']);
            }

            // listen for new connections; initialise them the same way we
            // initialise the connections at startup.
            instance.bind("connection", function(connInfo, originalEvent) {
                init(connInfo.connection, connection_label);
            });

            // make all the window divs draggable
            instance.draggable(
                jsPlumb.getSelector(".flowchart-webxmn .window"),
                { grid: [20, 20] });
            // THIS webxmn ONLY USES getSelector FOR CONVENIENCE.
            // Use your library's appropriate selector
            // method, or document.querySelectorAll:
            jsPlumb.draggable(
                document.querySelectorAll(".window"), { grid: [20, 20] });

            // connect a few up
            /*
            instance.connect({uuids:["Window2BottomCenter", "Window3TopCenter"], editable:true});
            instance.connect({uuids:["Window2LeftMiddle", "Window4LeftMiddle"], editable:true});
            instance.connect({uuids:["Window4TopCenter", "Window4RightMiddle"], editable:true});
            instance.connect({uuids:["Window3RightMiddle", "Window2RightMiddle"], editable:true});
            instance.connect({uuids:["Window4BottomCenter", "Window1TopCenter"], editable:true});
            instance.connect({uuids:["Window3BottomCenter", "Window1BottomCenter"], editable:true});
            */

            for(i in _data['connection']) {
                _ = _data['connection'][i];
                _uuids = [_['chain'][0] + _['connector'][0],
                          _['chain'][1] + _['connector'][1]];
                instance.connect(
                    {uuids:_uuids, editable:true}
                );
            }

            //
            // listen for clicks on connections,
            // and offer to delete connections on click.
            //
            instance.bind("dblclick", function(conn, originalEvent) {
                if (confirm(""
                    + "Delete connection from "
                    + conn.sourceId + " to " + conn.targetId + "?")
                ) {
                    jsPlumb.detach(conn);
                }
            });

            instance.bind("connectionDrag", function(connection) {
                console.log(
                    "connection " + connection.id
                    + " is being dragged. suspendedElement is ",
                     connection.suspendedElement, " of type ",
                     connection.suspendedElementType);
            });

            instance.bind("connectionDragStop", function(connection) {
                console.log("connection " + connection.id + " was dragged");
            });

            instance.bind("connectionMoved", function(params) {
                console.log(
                    "connection " + params.connection.id + " was moved"
                );
            });
        };

        // suspend drawing and initialise.
        instance.doWhileSuspended(function() {
           data = [];
           create_node(jsondata);
        });

        $('.flowchart-add').click(function(){
            title = prompt('Set the title of node window:');

            _data = {
                'box': [
                    {'id': title,
                     'label': title,
                     'top': '10px',
                     'left': '10px',
                     'conn_out': conn_out,
                     'conn_in': conn_in
                     }
                ],
                'connection': []
            };

            create_node(_data);
        });
    });
}
