import QtQuick
import QtQuick.Controls

Button  {
        id: modernButton

        property color colorDefault: "#A6039B"
        property color colorMouseOver: "#D989CB"
        property color colorPressed: "#8C0375"

        QtObject {
        id: internal

        property var dynamicColor: if(modernButton.down){
                                   modernButton.down ? colorPressed: colorDefault

                                 } else {
                                   modernButton.hovered? colorMouseOver : colorDefault
                                   }
        }

        text: qsTr("Init Btn")
        implicitWidth: 200
        implicitHeight: 100

        background: Rectangle {
            color: internal.dynamicColor
            radius: 10
            border.width: 2
            border.color: "#8C5D7C"

                }
 
contentItem: Item {
    id: contentItm
    Text {
        id: textBtn
        text: modernButton.text
        anchors.fill: parent
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
        wrapMode: Text.WordWrap
        anchors.rightMargin: 4
        anchors.leftMargin: 4
        anchors.bottomMargin: 4
        anchors.topMargin: 4
        font.pointSize: modernButton.font.pointSize
        color: "#ffffff"
        font.bold: modernButton.font.bold
        font.hintingPreference : modernButton.font.hintingPreference


    }
}
}


