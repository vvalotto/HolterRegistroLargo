import QtQuick
import QtQuick.Window
import QtQuick.Controls.Material 2.12
import QtQuick.Controls
import QtQuick.Layouts 6.0
import Qt5Compat.GraphicalEffects
import QtCharts 2.3
import "pages"

Window {
    id: configuration
    width: 800
    height: 640
    visible: true
    //color: "#57a20398"
    //flags: Qt.Sheet
    visibility: Window.Maximized
    title: qsTr("Software en desarrollo - Holter de largo período - Versión para MONITOREO")
    modality: Qt.WindowModal
    property QtObject plotter
    property QtObject plotter2
    property QtObject plotter3
    property QtObject connector

    TabBar {
        id: tabBar
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.top: parent.top
        anchors.bottom: parent.bottom
        anchors.bottomMargin: parent.bottom * 0.15
        spacing: 2
        enabled: true

        currentIndex: 2
        TabButton {
            id: tabPaciente
            text: qsTr("Paciente")
        }
        TabButton {
            id: tabEstudio
            text: qsTr("Estudio")
        }

        TabButton {
            id: tabHolter
            text: qsTr("Holter")
        }
        TabButton {
            id: tabMonitoreo
            text: qsTr("Monitoreo")
        }
    }
    StackLayout {
        id: stackLayout
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.top: tabBar.bottom
        anchors.bottom: parent.bottom
        anchors.topMargin: 15
        anchors.rightMargin: 4
        anchors.leftMargin: 4
        anchors.bottomMargin: 4
        currentIndex: tabBar.currentIndex



        PatientPage{
            id: itemPaciente
        }


        StudyPage{
            id: itemEstudio
        }


        HolterPage{
            id: itemHolter
        }

        MonitorPage {
            id: itemMonitoreo
        }

    }

    FastBlur {
        anchors.left: progressBar.right
        anchors.right: progressBar.left
        anchors.top: progressBar.top
        anchors.bottom: progressBar.bottom
        anchors.rightMargin: -1
        anchors.leftMargin: -1
        anchors.bottomMargin: -4
        anchors.topMargin: -4
        // anchors.fill: progressBar
        source: progressBar
        radius: 32
    }
    ProgressBar {
        id: progressBar
        height: 6
        opacity: 0.80
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.top: tabBar.bottom
        anchors.topMargin: 70
        anchors.rightMargin: 10
        anchors.leftMargin: 10
        //indeterminate: true
        background: Rectangle {
            id: backRect
            implicitWidth: 200
            implicitHeight: 6
            color: "#a6039b"
            radius: 2.5
            border.width: 0
        }

        // contentItem: Item {
        //     implicitWidth: 200
        //     implicitHeight: 4

        //     Rectangle {
        //         id: itemProgressBar
        //         opacity: 0.30
        //         width: progressBar.visualPosition * parent.width
        //         height: parent.height
        //         radius: 2
        //         color: "#a6039b"
        //     }
        // }
    }
    PropertyAnimation {
        target: progressBar
        property: "value"
        easing.type: Easing.OutQuad
        from: 0
        to: 1
        duration: 5000
        running: true

        loops: Animation.Infinite
    }
    Glow {
        id: glow
        anchors.left: progressBar.right
        anchors.right: progressBar.left
        anchors.top: progressBar.top
        anchors.bottom: progressBar.bottom
        anchors.rightMargin: 1
        anchors.leftMargin: 1
        anchors.bottomMargin: 1
        anchors.topMargin: 1
        opacity: 0.65
        radius: 32
        color: "#a6039b"
        source: backRect
    }
}

/*##^##
Designer {
    D{i:0;formeditorZoom:0.66}
}
##^##*/

// Timer {
//     id: miTimer
//     interval: 1 / 24 * 1000 //update every 200ms
//     running: true
//     repeat: true
//     onTriggered: {
//         if (progressBar.value >> 99) {
//             progressBar.value = 0
//         } else {
//             progressBar.value = progressBar.value + 0.08
//         }
//     }
// }
