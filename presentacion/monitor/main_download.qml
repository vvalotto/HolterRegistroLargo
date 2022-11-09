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
    id: download
    width: 800
    height: 640
    visible: true
    color: "#73d9d3"

    title: qsTr("Software en desarrollo - Holter de largo período - Versión para monitoreo, registro y descarga")
    modality: Qt.WindowModal


    TabBar {
        id: tabBar
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.top: parent.top
        anchors.bottom: parent.bottom
        anchors.bottomMargin: parent.bottom * 0.15
        spacing: 2
        enabled: true
        currentIndex: 1
        TabButton {
            id: tabSelection
            text: qsTr("Selección de estudio")
        }
        TabButton {
            id: tabDownload
            text: qsTr("Tipo de descarga")
        }
    }

    StackLayout {
        id: stackLayout
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.top: tabBar.bottom
        anchors.bottom: parent.bottom
        anchors.topMargin: 8
        anchors.rightMargin: 4
        anchors.leftMargin: 4
        anchors.bottomMargin: 4
        currentIndex: tabBar.currentIndex

        StudySelectionPage{
            id: itemSelection
        }

        DownloadPage{
            id: itemDownload
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

    }

    HomeButton{ anchors.right: progressBar.right
                anchors.top: stackLayout.top
                anchors.topMargin: 10
                anchors.rightMargin: 0
                onClicked: {
                    home.visible = true
                    download.visible = false
                }
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
