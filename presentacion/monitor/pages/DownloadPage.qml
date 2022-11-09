import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "../components"

Item {

    Rectangle {
        id: downloadPage
        radius: 10
        Text {
            id: titleHolter
            color: "#518c89"
            text: qsTr("Descarga de datos")
            font.bold: true
            font.pixelSize: 30
            verticalAlignment: Text.AlignTop
            anchors.left: parent.left
            anchors.top: parent.top
            anchors.topMargin: 10
            anchors.leftMargin: 30
        }

        Rectangle {
            id: contentDownload
            radius: 6
            border.color: "#930089"
            border.width: 5
            anchors.top: titleHolter.bottom
            anchors.topMargin: 40
            anchors.bottom: parent.bottom
            anchors.bottomMargin: parent.height*0.66
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.rightMargin: 30
            anchors.leftMargin: 30
            color: "transparent"

            Column {
                id: column
                anchors.left: parent.left
                anchors.right: parent.right
                anchors.top: parent.top
                anchors.bottom: parent.bottom
                anchors.leftMargin: parent.width*0.05
                anchors.rightMargin: parent.width*0.6
                anchors.bottomMargin: 8
                anchors.topMargin: 8

                RadioButton {
                    id: completeDownload
                    text: qsTr("Descarga completa")

                    anchors.left: parent.left
                    anchors.right: parent.right
                    anchors.top: parent.top
                    anchors.bottom: parent.verticalCenter
                    checked: true
                    anchors.bottomMargin: 0
                    
                    contentItem: Text {
                        text: completeDownload.text
                        color: "#518c89"
                        leftPadding: completeDownload.indicator.width + completeDownload.spacing
                        verticalAlignment: Text.AlignVCenter
                        font.pointSize: 14
                    }
                    onClicked: {description.text = "Descarga completa: se descargarán las señales completas de las derivaciones, los eventos detectados y las marcas. "
                    }
                }

                RadioButton {
                    id: eventDownload
                    text: qsTr("Descarga de eventos")
                    anchors.left: parent.left
                    anchors.right: parent.right
                    anchors.top: parent.verticalCenter
                    anchors.bottom: parent.bottom
                    anchors.topMargin: 0
                    contentItem: Text {
                        text: eventDownload.text
                        color: "#518c89"
                        leftPadding: eventDownload.indicator.width + eventDownload.spacing
                        verticalAlignment: Text.AlignVCenter
                        font.pointSize: 14
                    }
                    onClicked: {
                        description.text = "Descarga de eventos: este tipo de descarga se encuentra en desarrollo. Seleccione 'Descarga completa'."
                    }
                }
            }

            Text {
                id: descriptionTypeDownload
                color: "#518c89"
                text: qsTr("Descripción de tipo de descarga")
                anchors.left: column.right
                anchors.right: parent.right
                anchors.top: parent.top
                font.pixelSize: 16
                horizontalAlignment: Text.AlignLeft
                anchors.topMargin: 8
                anchors.rightMargin: 0
                anchors.leftMargin: parent.width*0.15
                font.bold: true
            }

            Text {
                id: description
                color: "#518c89"
                text: qsTr("Descarga completa: se descargarán las señales completas de las derivaciones, los eventos detectados y las marcas. ")
                anchors.left: column.right
                anchors.right: parent.right
                anchors.top: descriptionTypeDownload.bottom
                anchors.bottom: parent.bottom
                font.pixelSize: 16
                verticalAlignment: Text.AlignVCenter
                wrapMode: Text.Wrap
                anchors.bottomMargin: 4
                anchors.rightMargin: 0
                anchors.topMargin: 2
                anchors.leftMargin: parent.width*0.15
            }
        }

        Rectangle {
            id: downloadPregress
            radius: 6
            border.color: "#930089"
            border.width: 5
            anchors.top: contentDownload.bottom
            anchors.topMargin: 10
            anchors.bottom: goBack.top
            anchors.bottomMargin: 10
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.rightMargin: 30
            anchors.leftMargin: 30
            color: "transparent"
            CircularProgressBar{ id: progressDownload; width: 175; height: 175; anchors.verticalCenter: parent.verticalCenter
                anchors.right: parent.right
                progressColor: "#73d9d3"
                bgStrokeColor: "#66666666"
                anchors.rightMargin: 30
            }

            Rectangle {
                id: contentImgDownload
                color: "#00ffffff"
                border.width: 0
                anchors.left: parent.left
                anchors.right: progressDownload.left
                anchors.top: parent.top
                anchors.bottom: parent.bottom
                anchors.bottomMargin: 20
                anchors.topMargin: 20
                anchors.rightMargin: 10
                anchors.leftMargin: 20

                Image {
                    id: imgHolter
                    anchors.left: parent.left
                    anchors.right: parent.right
                    anchors.top: parent.top
                    anchors.bottom: parent.bottom
                    source: "../resources/images/prototipo_holter.png"
                    anchors.bottomMargin: 0
                    anchors.topMargin: 0
                    anchors.rightMargin: (parent.width/3)*2
                    anchors.leftMargin: 0
                    fillMode: Image.PreserveAspectFit
                }

                Rectangle {
                    id: rectangle
                    y: 29
                    opacity: 0.8
                    color: "#00ffffff"
                    radius: 10
                    border.color: "#86f0e7"
                    border.width: 2
                    anchors.left: parent.left
                    anchors.right: parent.right
                    anchors.top: parent.top
                    anchors.bottom: parent.bottom
                    anchors.bottomMargin: 40
                    anchors.topMargin: 40
                    anchors.rightMargin: 0
                    anchors.leftMargin: parent.width/3+10

                    AnimatedImage {
                        id: animatedImage
                        opacity: 0.7
                        anchors.fill: parent
                        source: "../resources/images/GargantuanDiscreteAmethystsunbird-max-1mb.gif"
                        playing: false
                        speed: 0.5
                        fillMode: Image.Stretch
                    }
                }

            }

        }


        Rectangle {
            id: goBack
            color: "#00000000"
            anchors.fill: parent
            anchors.topMargin: parent.height*0.9

            Button {
                id: initDownload
                anchors.left: parent.left
                anchors.right: parent.right
                anchors.top: parent.top
                anchors.bottom: parent.bottom
                anchors.bottomMargin: 3
                anchors.topMargin: 3
                anchors.rightMargin: parent.width*0.35

                Text {
                    id: textInitDownload
                    color: "#518c89"
                    text: qsTr("Iniciar Descarga")
                    anchors.fill: parent
                    font.pixelSize: 16
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                    wrapMode: Text.Wrap
                    anchors.rightMargin: 5
                    anchors.leftMargin: 5
                    anchors.bottomMargin: 5
                    font.bold: true
                    anchors.topMargin: 5
                    font.italic: true
                }
                anchors.leftMargin: parent.width*0.35
                onClicked: {connector.download_init()
                animatedImage.playing = true}
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
