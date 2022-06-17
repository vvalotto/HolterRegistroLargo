import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import Qt.labs.qmlmodels 1.0

Item {

    Rectangle {
        id: contentPacient
        property var patientHeader: ["Nombre", "Apellido", "DNI", "Fecha de Nacimiento", "Obra Social", "Número de Afiliado", "Número de Teléfono", "Domicilio", "N Historia Clínica", "Institución", "Médico Solicitante", "Prescripciones", "Enfermedades preexistentes"]

        Text {
            id: titlePaciente
            color: "#666666"
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
            anchors.topMargin: 100
            anchors.bottom: parent.bottom
            anchors.bottomMargin: 60
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.rightMargin: 30
            anchors.leftMargin: 30
            color: "transparent"

            GridLayout {
                id: grid
                anchors.fill: parent
                rows: 13
                rowSpacing: 1
                columnSpacing: 1
                anchors.margins: 4

                // example models
                property var titles: ["Nombre", "Apellido", "DNI", "Fecha de Nacimiento", "Obra Social", "Número de Afiliado", "Número de Teléfono", "Domicilio", "N Historia Clínica", "Institución", "Médico Solicitante", "Prescripciones", "Enfermedades preexistentes"]
                property var values: ["Nombre", "Apellido", "DNI", "Fecha de Nacimiento", "Obra Social", "Número de Afiliado", "Número de Teléfono", "Domicilio", "N Historia Clínica", "Institución", "Médico Solicitante", "Prescripciones", "Enfermedades preexistentes"]

                Repeater {
                    model: grid.titles

                    Rectangle {
                        Layout.row: 0
                        Layout.column: index
                        Layout.fillWidth: false
                        Layout.fillHeight: false
                        // anchors.top: parent.top
                        height: 40
                        Text {
                            text: modelData
                            font.family: "Calibri Light"
                            font.pointSize: 12.5
                            color: "black"
                            font.bold: true
                            // font.italic: true
                            // verticalAlignment: Text.AlignVCenter
                            // wrapMode: Text.Wrap
                            fontSizeMode: Text.VerticalFit
                            horizontalAlignment: Text.AlignHCenter
                            lineHeight: 15
                            wrapMode: Text.WrapAnywhere
                        }
                    }
                }
                Repeater {
                    model: grid.values
                    Rectangle {
                        id: datos
                        Layout.row: 2
                        Layout.column: index
                        height: 40

                        Layout.fillWidth: false
                        Layout.fillHeight: true

                        Text {

                            text: modelData
                            font.family: "Calibri Light"
                            font.pointSize: 12.5
                            color: "black"
                            // font.bold: true
                            font.italic: true
                            // verticalAlignment: Text.AlignVtop
                            wrapMode: Text.Wrap
                            fontSizeMode: Text.HorizontalFit
                            horizontalAlignment: Text.AlignHCenter
                            lineHeight: 15
                        }
                    }
                }
            }
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

