import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import Qt.labs.qmlmodels 1.0

Item {

    Rectangle {
        id: contentPacient
        radius: 10
        Text {
            id: titlePaciente
            color: "#518c89"
            text: qsTr("Paciente")
            anchors.left: parent.left
            anchors.top: parent.top
            anchors.topMargin: 10
            anchors.leftMargin: 30
            font.bold: true
            font.pixelSize: 30
            verticalAlignment: Text.AlignTop
        }
        Text {
            id: descriptionPatient
            y: 74
            color: "#666666"
            text: "Indique qué paciente se realizará el estudio. De no encontrarse registrado, oprima el botón <i>\"Agregar Nuevo Paciente\"</i>."
            anchors.left: titlePaciente.left
            anchors.bottom: titlePaciente.top
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
            anchors.top: descriptionPatient.bottom
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

/*##^##
Designer {
    D{i:0;autoSize:true;formeditorZoom:0.75;height:480;width:640}
}
##^##*/

