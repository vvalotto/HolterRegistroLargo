import QtQuick
import QtQuick.Controls
import Qt5Compat.GraphicalEffects
import QtCharts 2.3
import "../components"

Item {

    Rectangle {
        id: contentMonitor
        radius: 10
        color: "#f6f6f6"
        anchors.fill: parent
        Text {
            id: titleMonitor
            color: "#518c89"
            text: qsTr("Monitoreo")
            font.bold: true
            font.pixelSize: 30
            horizontalAlignment: Text.AlignLeft
            verticalAlignment: Text.AlignTop
            anchors.left: parent.left
            anchors.top: parent.top
            anchors.topMargin: 10
            anchors.leftMargin: 30
        }
        Text {
            id: descriptionMonitor
            y: 74
            color: "#666666"
            text: "Verifique la adquisición de las señales y luego presione <i>\"Iniciar Estudio\"</i> para comenzar el registro."
            anchors.left: titleMonitor.left
            anchors.bottom: titleMonitor.top
            font.pixelSize: 14
            verticalAlignment: Text.AlignVCenter
            anchors.leftMargin: 0
            anchors.bottomMargin: -80
        }
        FastBlur {
            anchors.fill: signalsPlotArea
            source: signalsPlotArea
            transparentBorder: true
            radius: 10
        }
        Rectangle {
            id: signalsPlotArea
            color: "#f9f9f9"
            radius: 5
            border.color: "#ae930089"
            border.width: 4
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.top: headerPlotArea.bottom
            anchors.rightMargin: 30
            anchors.leftMargin: 30
            anchors.topMargin: 0
            anchors.bottom: parent.bottom
            anchors.bottomMargin: 60
            ////////////////////////
            Rectangle {
                id: recChannel1
                color: "#f9f9f9"
                radius: 5
                border.color: "#00060000"
                border.width: 6
                height: parent.height/3
                anchors.left: parent.left
                anchors.right: parent.right
                anchors.top: parent.top
                // anchors.bottom: parent.bottom
                anchors.rightMargin: 4
                anchors.leftMargin: 30
                anchors.topMargin: 4
                // anchors.bottomMargin: parent.height - parent.height / 3 - 10

                ChartView {
                    id: channel
                    legend.visible: false
                    backgroundColor: "transparent"
                    anchors.fill: parent

                    // anchors.left: parent.left
                    // anchors.right: parent.right
                    // anchors.top: parent.top
                    // anchors.bottom: parent.bottom
                    // anchors.bottomMargin: parent.height - parent.height / 3 - 10

                    ValuesAxis {
                        id: axisX
                        visible: false
                        min: 0.0
                        max: 1600.0
                        // gridLineColor: 'red'
                    }

                    ValuesAxis {
                        id: axisY
                        visible: true
                        min: 3.4
                        max: 4.1
                        // gridLineColor: 'red'
                        // shadesVisible: true
                    }
                }
                Connections {
                    target: plotter
                    function onSend(series) {
                        plotter.get_series(channel.series(0))
                    }
                }

                Component.onCompleted: {
                    var series = channel.createSeries(
                                ChartView.SeriesTypeLine, "Canal 1",
                                axisX, axisY)
                }
                FastBlur {
                    anchors.fill: channel
                    source: channel
                    radius: 20
                }
            }
            ///////////////////////////////////////
            Rectangle {
                id: rectChannel2
                color: "#f9f9f9"
                radius: 5
                height: recChannel1.height
                border.color: "#00060000"
                border.width: 6
                anchors.left: parent.left
                anchors.right: parent.right
                anchors.top: recChannel1.bottom
                anchors.topMargin: -20
                anchors.rightMargin: 4
                anchors.leftMargin: 30
                // anchors.bottomMargin: parent.height / 3

                ChartView {
                    id: channel2
                    legend.visible: false
                    backgroundColor: "transparent"
                    anchors.fill: parent
                    // anchors.left: parent.left
                    // anchors.right: parent.right

                    // anchors.top: parent.top
                    // anchors.bottom: parent.bottom
                    // anchors.bottomMargin: parent.height - (parent.height / 3)*2 - 10
                    ValuesAxis {
                        id: axisX2
                        visible: false
                        min: 0.0
                        max: 1600.0
                        // gridLineColor: 'red'
                    }

                    ValuesAxis {
                        id: axisY2
                        visible: true
                        min: 3
                        max: 4.7
                        // gridLineColor: 'red'
                        // shadesVisible: true
                    }
                }
                Connections {
                    target: plotter2
                    function onSend(series2) {
                        plotter2.get_series(channel2.series(0))
                    }
                }

                Component.onCompleted: {
                    var series2 = channel2.createSeries(
                                ChartView.SeriesTypeLine, "Canal 2",
                                axisX2, axisY2)
                }
                FastBlur {
                    anchors.fill: channel2
                    source: channel2
                    radius: 20
                }
            }
            //////////////////////////////////////
            Rectangle {
                id: rectChannel3
                color: "#f9f9f9"
                radius: 5
                height: recChannel1.height
                border.color: "#00060000"
                border.width: 6
                anchors.left: parent.left
                anchors.right: parent.right
                anchors.top: rectChannel2.bottom
                anchors.topMargin: -20
                anchors.rightMargin: 4
                anchors.leftMargin: 30
                // anchors.bottomMargin: parent.height / 3

                ChartView {
                    id: channel3
                    legend.visible: false
                    backgroundColor: "transparent"
                    anchors.fill: parent
                      ValuesAxis {
                        id: axisX3
                        visible: false
                        min: 0.0
                        max: 1600.0
                        // gridLineColor: 'red'
                    }

                    ValuesAxis {
                        id: axisY3
                        visible: true
                        min: 6.0
                        max: 6.8
                        // gridLineColor: 'red'
                        // shadesVisible: true
                    }
                }
                Connections {
                    target: plotter3
                    function onSend(series3) {
                        plotter3.get_series(channel3.series(0))
                    }
                }

                Component.onCompleted: {
                    var series3 = channel3.createSeries(
                                ChartView.SeriesTypeLine, "Canal 3",
                                axisX3, axisY3)
                }
                FastBlur {
                    anchors.fill: channel3
                    source: channel3
                    radius: 20
                }
            }

            Rectangle {
                id: scaleRect
                color: "#00ffffff"
                border.width: 0
                anchors.left: parent.left
                anchors.right: parent.right
                anchors.top: parent.top
                anchors.bottom: parent.bottom
                anchors.rightMargin: parent.width-30
                anchors.topMargin: 4
                anchors.bottomMargin: 4
                anchors.leftMargin: 4

                Rectangle {
                    id: buttonDownScale
                    height: 30
                    color: "#00ffffff"
                    // text: qsTr("Button")
                    anchors.left: parent.left
                    anchors.right: parent.right
                    anchors.top: parent.top
                    anchors.rightMargin: 0
                    anchors.leftMargin: 0
                    anchors.topMargin: 0
                    UpArrowButton{
                    onClicked: {axisY3.min = axisY3.min+0.5
                        axisY3.max= axisY3.max - 0.5
                        axisY2.min = axisY2.min+0.5
                        axisY2.max= axisY2.max - 0.5
                        axisY.min = axisY.min+0.5
                        axisY.max= axisY.max - 0.5}
                }
                }

                Rectangle {
                    id: decreaseScale
                    height: 30
                    color: "#00ffffff"
                    // text: qsTr("Button")
                    anchors.left: parent.left
                    anchors.right: parent.right
                    anchors.bottom: parent.bottom
                    anchors.bottomMargin: 0
                    anchors.leftMargin: 0
                    anchors.rightMargin: 0
                    DownArrowButton{
                        anchors.fill: pantent.anchors
                    onClicked: {axisY3.min = axisY3.min-0.5
                        axisY3.max= axisY3.max + 0.5
                        axisY2.min = axisY2.min-0.5
                        axisY2.max= axisY2.max + 0.5
                        axisY.min = axisY.min-0.5
                        axisY.max= axisY.max + 0.5}
                }
                }
            }


        }

        Rectangle {
            id: headerPlotArea
            color: "#00000000"
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.top: descriptionMonitor.bottom
            anchors.bottom: parent.bottom
            anchors.rightMargin: 30
            anchors.leftMargin: 30
            anchors.bottomMargin: parent.height*0.75
            anchors.topMargin: 0

            Button {
                id: monitorOn
                width: parent.width*0.4
                height: parent.height*0.8
                anchors.verticalCenter: parent.verticalCenter
                anchors.left: parent.left
                anchors.leftMargin: parent.width*0.05
                onClicked: {
                    connector.monitor_mode(true)
                    // recChannel1.visible = true
                    // rectChannel2.visible = true
                    // rectChannel3.visible = true
                }

                Text {
                    id: textMonitorOn
                    color: "#518c89"
                    text: qsTr("Monitorear")
                    anchors.verticalCenter: parent.verticalCenter
                    font.pixelSize: 18
                    anchors.horizontalCenter: parent.horizontalCenter
                }

            }

            Button {
                id: monitorOff
                width: parent.width*0.4
                height: parent.height*0.8
                anchors.verticalCenter: parent.verticalCenter
                anchors.left: monitorOn.right
                anchors.leftMargin: parent.width*0.1
                Text {
                    id: textMonitorOff
                    color: "#518c89"
                    text: qsTr("Pausa")
                    anchors.verticalCenter: parent.verticalCenter
                    font.pixelSize: 18
                    anchors.horizontalCenter: parent.horizontalCenter
                }
                onClicked: {
                    connector.monitor_mode(false)
                    // recChannel1.visible = false
                    // rectChannel2.visible = false
                    // rectChannel3.visible = false
                }
            }
        }

        Rectangle {
            id: footer
            color: "#00000000"
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.top: signalsPlotArea.bottom
            anchors.bottom: parent.bottom
            anchors.rightMargin: 30
            anchors.leftMargin: 30
            anchors.bottomMargin: 0
            anchors.topMargin: 0

            Text {
                id: plotFeet
                color: "#666666"
                text: qsTr(" Paciente: - ID: - Estudio: - Dispositivo: ")
                anchors.verticalCenter: parent.verticalCenter
                anchors.right: initStudy.left
                font.pixelSize: 14
                anchors.rightMargin: 8
                font.italic: true
                
            }

            Button {
                id: initStudy
                anchors.left: parent.left
                anchors.right: parent.right
                anchors.top: parent.top
                anchors.bottom: parent.bottom
                anchors.leftMargin: parent.width*0.85
                anchors.bottomMargin: parent.height*0.1
                anchors.topMargin: parent.height*0.1
                anchors.rightMargin: 0


                Text {
                    id: textInitStudy
                    text: qsTr("Iniciar Estudio")
                    anchors.fill: parent
                    font.italic: true
                    font.pixelSize: 16
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                    wrapMode: Text.Wrap
                    anchors.topMargin: 3
                    font.bold: true
                    color: "#518c89"
                }
                onClicked: {connector.loggin_init() }
                
            }

            Text {
                id: initRate
                color: "#666666"
                text: qsTr("Ingrese <b>ritmo inicial</b>: ")
                anchors.verticalCenter: parent.verticalCenter
                font.pixelSize: 16
                anchors.leftMargin: 0
                anchors.left: parent.left

            }

            TextInput {
                id: inputInitRate
                x: 161
                y: -326
                anchors.left: initRate.right
                anchors.right: parent.right
                color: "#666666"
                text: qsTr("ej.: Normal")
                anchors.verticalCenter: initRate.verticalCenter
                font.pixelSize: 16
                verticalAlignment: Text.AlignVCenter
                anchors.rightMargin: 326
                font.italic: true
                selectByMouse: true
                cursorVisible: true
                font.wordSpacing: 0.4
                selectionColor: "#b4a6039b"
                anchors.leftMargin: 2
            }
        }
    }
}
/*##^##
Designer {
    D{i:0;autoSize:true;height:480;width:640}D{i:24}
}
##^##*/
