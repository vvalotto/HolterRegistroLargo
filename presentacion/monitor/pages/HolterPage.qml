import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "../components"

Item {

    Rectangle {
        id: holterPage
        radius: 10
        Text {
            id: titleHolter
            color: "#518c89"
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

        Rectangle {
            id: goBack
            color: "#00000000"
            anchors.fill: parent
            anchors.topMargin: parent.height*0.9
            Rectangle {
                id: holterToHome
                width: 150
                color: "#00ffffff"
                border.width: 0
                // text: qsTr("<-- Home")
                anchors.left: parent.left
                anchors.top: parent.top
                anchors.bottom: parent.bottom
                anchors.bottomMargin: 0
                anchors.topMargin: 0
                anchors.leftMargin: 30
                BackButton{
                    id: back
                    anchors.left: parent.left
                    anchors.leftMargin: 0
                    onClicked: {
                        home.visible = true
                        configuration.visible = false
                    }
                }

                Text {
                    id: goHome
                    y: 12
                    color: "#518c89"
                    text: qsTr("Home")
                    anchors.left: back.right
                    font.pixelSize: 18
                    verticalAlignment: Text.AlignTop
                    anchors.leftMargin: 10
                    font.italic: true
                    font.bold: true
                }


            }

            Rectangle {
                id: holterToMonitor
                width: 150
                color: "#00ffffff"
                // text: qsTr("Monitoreo")
                anchors.right: parent.right
                anchors.top: parent.top
                anchors.bottom: parent.bottom
                anchors.bottomMargin: 0
                anchors.topMargin: 0
                anchors.rightMargin: 30
                NextButton{
                    id: next
                    anchors.right: parent.right
                    anchors.rightMargin: 0
                    onClicked: {
                        tabBar.currentIndex = 3
                    }
                }

                Text {
                    id: monitorGo
                    x: -493
                    y: 12
                    color: "#518c89"
                    text: qsTr("Monitoreo")
                    anchors.right: next.left
                    font.pixelSize: 18
                    anchors.rightMargin: 10
                    font.italic: true
                    font.bold: true
                }
            }

        }

        Rectangle {
            id: rectConnect
            color: "#00000000"
            anchors.top: descriptionHolter.bottom
            anchors.bottom: parent.bottom
            anchors.right: parent.right
            anchors.left: parent.left
            anchors.bottomMargin: parent.height*0.1
            anchors.rightMargin: parent.width*0.6
            anchors.leftMargin: 30


            Rectangle {
                id: boxConectionType
                color: "#00000000"
                height: parent.height/12
                anchors.top: parent.top
                anchors.topMargin: parent.height/12
                anchors.right: parent.right
                anchors.rightMargin: parent.width*0.2
                anchors.left: parent.left

                ComboBox {
                    id: conectionType
                    anchors.left: boxConectionType.left
                    anchors.right: boxConectionType.right
                    
                    height: 74
                    anchors.verticalCenter: parent.verticalCenter
                    // font.pointSize: 12
                    contentItem: Text {
                        color: "#518c89"
                        text: parent.displayText
                        font.family: "Segoe UI"
                        font.pixelSize: 18
                        font.italic: true
                        verticalAlignment: Text.AlignVCenter
                        horizontalAlignment: Text.AlignHCenter
                        elide: Text.ElideRight
                    }

                    model: ["Conexión Bluetooth", "Conexión USB"]
                }
            }

            Button {
                id: holterDisconnect

                height: parent.height/4
                anchors.top: holterConnect.bottom
                anchors.topMargin: parent.height/12
                anchors.right: parent.right
                anchors.rightMargin: parent.width*0.2
                anchors.left: parent.left

                onClicked: home.connector.holter_connect(false, -1)

                Text {
                    id: textHolterDisconnect
                    color: "#518c89"
                    text: qsTr("Desconectar Holter")
                    anchors.verticalCenter: parent.verticalCenter
                    font.pixelSize: 18
                    font.bold: true
                    anchors.horizontalCenter: parent.horizontalCenter
                }
            }

            Button {
                id: holterConnect
                height: parent.height/4
                anchors.top: boxConectionType.bottom
                anchors.topMargin: parent.height/12
                anchors.right: parent.right
                anchors.rightMargin: parent.width*0.2
                anchors.left: parent.left
                Text{
                    id: textHolterConnect
                    text: qsTr("Conectar Holter")
                    anchors.verticalCenter: parent.verticalCenter
                    color: "#518c89"
                    font.pixelSize: 18
                    font.bold: true
                    anchors.horizontalCenter: parent.horizontalCenter
                }


                onClicked:{ home.connector.holter_connect(true, conectionType.currentIndex)}
            }
            Connections {
                target: connector
                function onHolter_connected(is_connect) {
                    if (is_connect){
                        textHolterConnect.text = qsTr("Holter conectado")
                    }
                    else {
                        textHolterConnect.text = qsTr("Conectar Holter")
                    }
                }
            }
        }

        Rectangle {
            id: rectImage
            color: "#00000000"
            anchors.left: rectConnect.right
            anchors.right: parent.right
            anchors.top: descriptionHolter.bottom
            anchors.bottom: goBack.top
            anchors.topMargin: 0
            anchors.bottomMargin: 0
            anchors.rightMargin: 0
            anchors.leftMargin: 0

            Image {
                id: image
                anchors.fill: parent

                source: "../resources/images/prototipo_holter.png"

                fillMode: Image.PreserveAspectFit
            }
        }

        color: "#f6f6f6"
        anchors.fill: parent
    }


}
/*##^##
Designer {
    D{i:0;autoSize:true;formeditorZoom:0.75;height:480;width:640}D{i:7}
}
##^##*/
