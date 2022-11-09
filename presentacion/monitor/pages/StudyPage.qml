import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Item {
            
            Rectangle {
                radius: 10
                Text {
                    id: titleEstudio
                    color: "#518c89"
                    text: qsTr("Estudio")
                    font.bold: true
                    font.pixelSize: 30
                    verticalAlignment: Text.AlignTop
                    anchors.left: parent.left
                    anchors.top: parent.top
                    anchors.topMargin: 10
                    anchors.leftMargin: 30
                }
                Text {
                    id: descriptionStudy
                    y: 74
                    color: "#666666"
                    text: "Ingrese los datos solicitados para registrar un nuevo estudio y luego presione el botón de <i>\"Avanzar\"</i>."
                    anchors.left: titleEstudio.left
                    anchors.bottom: titleEstudio.top
                    font.pixelSize: 14
                    verticalAlignment: Text.AlignVCenter
                    anchors.leftMargin: 0
                    anchors.bottomMargin: -80
                }

            Rectangle {
            id: tablePatient
            radius: 6
            border.color: "#930089"
            border.width: 5
            anchors.top: descriptionStudy.bottom
            anchors.topMargin: 60
            anchors.bottom: parent.bottom
            anchors.bottomMargin: 60
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.rightMargin: 30
            anchors.leftMargin: 30
            color: "transparent"

        }
                color: "#f6f6f6"
                anchors.fill: parent
            }
        }
