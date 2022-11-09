import QtQuick
import QtQuick.Controls
import Qt5Compat.GraphicalEffects

Button {
    id: btnTopBar
    property alias toggleBtnIconsource: btnTopBar.icon.source
    property url btnIconSource: "../resources/icons/minimize-2.svg"
    property color btnColorDefault: "#1c1d20"

    property color btnColorMouseOver: "#23272E"
    property color btnColorClicked: "#00a1f1"

    QtObject {
        id: internal
        //Mouse over and click change color
        property var dynamicColor: if (btnTopBar.down){
                                   btnTopBar.down ? btnColorClicked : btnColorDefault
                                   } else {
                                   btnTopBar.hovered ? btnColorMouseOver : btnColorDefault
                                   }
    }

    //implicitWidth: 35
    //implicitHeight: 35
    width: 35
    height: 35

    background: Rectangle {
    id: bgBtn
    color: internal.dynamicColor

    Image {
    id: iconBtn
    source: btnIconSource
    anchors.verticalCenter: parent.verticalCenter
    anchors.horizontalCenter: parent.horizontalCenter
    height: 16
    width: 16

    fillMode: Image.PreserveAspectFit
    antialiasing: false
    }
    ColorOverlay {
    anchors.fill: iconBtn
    source: iconBtn
    color: "#ffffff"
    antialiasing: false
    }


  }
}
