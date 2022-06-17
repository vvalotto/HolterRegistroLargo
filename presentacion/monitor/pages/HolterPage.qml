import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Item {
            
            Rectangle {
                Text {
                    id: titleHolter
                    color: "#666666"
                    text: qsTr("Holter")
                    font.bold: true
                    font.pixelSize: 30
                    verticalAlignment: Text.AlignTop
                    anchors.left: parent.left
                    anchors.top: parent.top
                    anchors.topMargin: 10
                    anchors.leftMargin: 30
                }
                Text {
                    id: descriptionHolter
                    y: 74
                    color: "#666666"
                    text: "Asegurese de realizar el procedimiento de conexión correspondiente. Si tiene dudas, oprima el botón <i>\"Vincular Holter\"</i>."
                    anchors.left: titleHolter.left
                    anchors.bottom: titleHolter.top
                    font.pixelSize: 14
                    verticalAlignment: Text.AlignVCenter
                    anchors.leftMargin: 0
                    anchors.bottomMargin: -80
                }

                Button {
                    id: holterConnect
                    x: 201
                    y: 181
                    width: 156
                    height: 66
                    text: qsTr("Conectar Holter")
                    font.pixelSize: 14
                    highlighted: false
                    flat: false
                    font.bold: false
                    onClicked: connector.holter_connect(true)
                }
                Button {
                    id: holterDisconnect
                    x: 201
                    y: 446
                    width: 211
                    height: 66
                    text: qsTr("Desconectar Holter")
                    font.pixelSize: 14
                    highlighted: false
                    flat: false
                    font.bold: false
                    onClicked: connector.holter_connect(false)
                }

                Image {
                    id: image
                    x: 673
                    y: 181
                    width: 429
                    height: 339
                    source: "Captura.png"
                    
                    // fillMode: Image.PreserveAspectFit
                }
                color: "#f6f6f6"
                anchors.fill: parent
            }

            Image {
                id: captura
                x: 0
                y: 0
                source: "C:/Users/Santiago F/Desktop/Captura.PNG"
                fillMode: Image.PreserveAspectFit
            }
        }
/*##^##
Designer {
    D{i:0;autoSize:true;formeditorZoom:0.75;height:480;width:640}
}
##^##*/
