import QtQuick
import QtQuick.Controls
import Qt5Compat.GraphicalEffects
import QtCharts 2.3



Item {
          
            Rectangle {
                id: contentMonitor
                Text {
                    id: titleMonitor
                    color: "#666666"
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
                Text {
                    id: initRate
                    x: 30
                    color: "#666666"
                    text: qsTr("Ingrese <b>ritmo inicial</b>: ")
                    font.pixelSize: 16
                    anchors.top: descriptionMonitor.bottom
                    anchors.topMargin: 30
                    anchors.left: descriptionMonitor.left
                    
                }
                TextInput {
                    id: inputInitRate
                    anchors.left: initRate.right
                    width: 2 * initRate.width
                    //height: 2 * initRate.height
                    color: "#666666"
                    text: qsTr("ej.: Normal")
                    anchors.verticalCenter: initRate.verticalCenter
                    font.pixelSize: 16
                    verticalAlignment: Text.AlignVCenter
                    font.italic: true
                    selectByMouse: true
                    cursorVisible: true
                    font.wordSpacing: 0.4
                    selectionColor: "#b4a6039b"
                    anchors.leftMargin: 10

                    Button {
                        id: monitorOn
                        x: 397
                        y: -9
                        width: 166
                        height: 39
                        text: qsTr("Monitorear")
                        font.pixelSize: 12
                        onClicked: {
                            connector.monitor_mode(true)
                            // recChannel1.visible = true
                            // rectChannel2.visible = true
                            // rectChannel3.visible = true
                            }

                    }
                    Button {
                        id: monitorOff
                        x: 619
                        y: -9
                        width: 166
                        height: 39
                        text: qsTr("Stop")
                        font.pixelSize: 12
                        onClicked: {
                            connector.monitor_mode(false)
                            // recChannel1.visible = false
                            // rectChannel2.visible = false
                            // rectChannel3.visible = false
                                    }
                    }
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
                    anchors.top: initRate.bottom
                    anchors.rightMargin: 30
                    anchors.leftMargin: 30
                    anchors.topMargin: 32
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
                        anchors.leftMargin: 4
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
                        anchors.leftMargin: 4
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
                        anchors.leftMargin: 4
                        // anchors.bottomMargin: parent.height / 3

                    ChartView {
                        id: channel3
                        legend.visible: false
                        backgroundColor: "transparent"
                        anchors.fill: parent
                        // anchors.left: parent.left
                        // anchors.right: parent.right
                        
                        // anchors.top: parent.top
                        // anchors.bottom: parent.bottom
                        // anchors.bottomMargin: parent.height - (parent.height / 3)*2 - 10
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


                }
                Button {
                    id: initStudio
                    text: qsTr("Iniciar Estudio")
                    height: 45
                    font.pixelSize: 14
                    font.italic: true
                    anchors.right: signalsPlotArea.right
                    anchors.top: signalsPlotArea.bottom
                    anchors.topMargin: 2
                }
                Text {
                    id: plotFeet
                    color: "#666666"
                    text: qsTr(" Paciente: - ID: - Estudio: - Dispositivo: ")
                    anchors.verticalCenter: initStudio.verticalCenter
                    font.pixelSize: 14
                    font.italic: true
                    anchors.rightMargin: 10

                    anchors.right: initStudio.left
                }

                color: "#f6f6f6"
                anchors.fill: parent
            }
        }
/*##^##
Designer {
    D{i:0;autoSize:true;height:480;width:640}
}
##^##*/
