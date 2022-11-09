import QtQuick
import QtQuick.Window
import QtQuick.Controls.Material 2.12
import QtQuick.Controls
import QtQuick.Layouts
import Qt5Compat.GraphicalEffects
import QtCharts 2.3
import "pages"
import "components"


Window {
    id: home
    width: 800
    height: 640
    visible: true
    color: "#D989CB"
    property alias holter_logoAnchorsrightMargin: holter_logo.anchors.rightMargin //"#A6038B"
    title: "HOLTER DE LARGO PERIODO"
    //property alias homeColor: home.color
    // color: "#57a20398"
    // visibility: Window.Maximized
    property QtObject connector
    property QtObject plotter
    property QtObject plotter2
    property QtObject plotter3

    Rectangle {
        id: rectangle
        color: "#f2f2f2f2"
        radius: 10
        anchors.fill: parent
        anchors.rightMargin: 10
        anchors.leftMargin: 10
        anchors.bottomMargin: 10
        anchors.topMargin: 10



        Image {
            id: background
            opacity: 0.2
            anchors.fill: parent
            source: "resources/images/fondo_borrar.jpg"
            fillMode: Image.PreserveAspectCrop
        }

        Column {
            id: principal_menu
            property real spacings: (parent.height-4*configuration.height)/5
            anchors.left: parent.left
            anchors.top: parent.top
            anchors.bottom: parent.bottom
            anchors.leftMargin: 0.05*parent.width
            anchors.topMargin: spacings
            anchors.bottomMargin: spacings
            spacing: spacings


            InitButton{
                id: configuration
                opacity: 0.8
                text: "Configuración de estudio"
                font.bold: true
                font.pointSize: 16
                onClicked: {
                    var component = Qt.createComponent("main_configuration.qml")
                    var win = component.createObject(home)
                    win.show()
                    home.visible = false
                }
            }

            InitButton {
                id: download
                opacity: 0.8
                text: "Descarga de datos"
                font.pointSize: 16
                font.bold: true
                onClicked: {
                    var component = Qt.createComponent("main_download.qml")
                    var win = component.createObject(home)
                    win.show()
                    home.visible = false
                }
            }

            InitButton {
                id: analisis
                opacity: 0.8
                text: "Análisis de estudio"
                font.pointSize: 16
                font.bold: true
            }

            InitButton {
                id: reports
                opacity: 0.8
                text: "Reportes"
                font.pointSize: 16
                font.bold: true
            }


        }

        Rectangle {
            id: holter_logo
            color: "#00000000"
            anchors.left: principal_menu.right
            anchors.right: parent.right
            anchors.top: parent.bottom
            anchors.bottom: parent.bottom
            anchors.topMargin: -1*(parent.height*0.1 + 110)
            anchors.bottomMargin: parent.height*0.1
            anchors.rightMargin: 0.05*parent.width
            anchors.leftMargin: 0.05*parent.width


            Image {
                id: image
                anchors.fill: parent
                source: "resources/images/laboratorios_bago_procesada-PhotoRoom.png"
                fillMode: Image.PreserveAspectFit
            }
        }

        Text {
            id: foot_init
            color: "#333333"
            text: qsTr("Holter de largo periodo - Prototipo para monitoreo, registro y descarga")
            anchors.right: parent.right
            anchors.bottom: parent.bottom
            font.pixelSize: 14
            font.italic: true
            anchors.bottomMargin: parent.height*0.01
            anchors.rightMargin: 0.005*parent.width
        }


        

}
}

/*##^##
Designer {
    D{i:0;formeditorZoom:0.5}D{i:2}
}
##^##*/
