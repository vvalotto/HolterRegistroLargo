import QtQuick
import QtQuick.Controls
import Qt5Compat.GraphicalEffects

Button {
    id: toggleBtn
    property alias toggleBtnIconsource: toggleBtn.icon.source
    property url btnIconSource: "../resources/icons/arrow-right-circle.svg"
    property color btnColorDefault: "#a6039b"
    property color btnColorMouseOver: "#d989cb"
    property color btnColorClicked: "#8c0375"

    QtObject {
        id: internal
        //Mouse over and click change color
        property var dynamicColor: if (toggleBtn.down){
                                   toggleBtn.down ? btnColorClicked : btnColorDefault
                                   } else {
                                   toggleBtn.hovered ? btnColorMouseOver : btnColorDefault
                                   }
    }

    implicitWidth: 50
    implicitHeight: 50

    background: Rectangle {
    id: bgBtn
    color:"#00a6039b" //internal.dynamicColor
    radius: 5

    Image {
    id: iconBtn
    source: btnIconSource
    anchors.verticalCenter: parent.verticalCenter
    anchors.horizontalCenter: parent.horizontalCenter
    height: 40
    width: 35
    fillMode: Image.PreserveAspectFit
    antialiasing: false
    }
    ColorOverlay {
    anchors.fill: iconBtn
    source: iconBtn
    color: internal.dynamicColor
    //color: "#a6039b"
    antialiasing: false
    }
  }
}
