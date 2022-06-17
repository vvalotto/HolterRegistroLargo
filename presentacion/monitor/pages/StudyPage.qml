import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Item {
            
            Rectangle {
                Text {
                    id: titleEstudio
                    color: "#666666"
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
                color: "#f6f6f6"
                anchors.fill: parent
            }
        }