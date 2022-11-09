import QtQuick
import QtQuick.Shapes
import Qt5Compat.GraphicalEffects
import QtQuick.Controls
import QtQuick.Layouts

Item {
    id: progress
        implicitWidth: 250
        implicitHeight: 250

        // Properties
        // General
        property bool roundCap: true
        property int startAngle: -90
        property int maxValue: 0 // debo modificar este valor
        property int value: 0 //debo modificar este valor
        property int samples: 4
        // Drop Shadow
        property bool enableDropShadow: true
        property color dropShadowColor: "#20000000"
        property int dropShadowRadius: 10
        // Bg Circle
        property color bgColor: "transparent"
        property color bgStrokeColor: "#7e7e7e"
        property int strokeBgWidth: 6
        // Progress Circle
        property color progressColor: "#55aaff"
        property int progressWidth: 12
        // Text
        property string text: ""
        property bool textShowValue: true
        property string textFontFamily: "Segoe UI"
        property int textSize: 42
        property color textColor: "#7c7c7c"

        // Internal Properties/Functions
        QtObject{
            id: internal

            property Component dropShadow: DropShadow{
                color: progress.dropShadowColor
                verticalOffset: 3
                horizontalOffset: 3
                radius: progress.dropShadowRadius
            }

        }
        Connections {
                        target: connector
                        function onTotal_files(max_value) {
                            maxValue = max_value
                        }
                        function onDownloaded_files(newValue) {
                            value = newValue
                        }
                    }


        Shape{
            id: shape
            anchors.fill: parent
            smooth: true
            enabled: true
            focus: true
            antialiasing: true
            layer.enabled: true
            layer.samples: progress.samples
            layer.effect: progress.enableDropShadow ? internal.dropShadow : null

            ShapePath{
                id: pathBG
                strokeColor: progress.bgStrokeColor
                fillColor: progress.bgColor
                strokeWidth: progress.strokeBgWidth
                capStyle: progress.roundCap ? ShapePath.RoundCap : ShapePath.FlatCap

                PathAngleArc{
                    radiusX: (progress.width / 2) - (progress.progressWidth / 2)
                    radiusY: (progress.height / 2) - (progress.progressWidth / 2)
                    centerX: progress.width / 2
                    centerY: progress.height / 2
                    startAngle: progress.startAngle
                    sweepAngle: 360
                }
 
}
            ShapePath{
                id: path
                strokeColor: progress.progressColor
                fillColor: "transparent"
                strokeWidth: progress.progressWidth
                capStyle: progress.roundCap ? ShapePath.RoundCap : ShapePath.FlatCap
                PathAngleArc{
                    radiusX: (progress.width / 2) - (progress.progressWidth / 2)
                    radiusY: (progress.height / 2) - (progress.progressWidth / 2)
                    centerX: progress.width / 2
                    centerY: progress.height / 2
                    startAngle: progress.startAngle
                    sweepAngle: (360 / progress.maxValue * progress.value)
                }
            }

            Text {
                id: textProgress
                text: progress.textShowValue ? parseInt(progress.maxValue - progress.value) + progress.text : progress.text
                anchors.verticalCenter: parent.verticalCenter
                anchors.horizontalCenter: parent.horizontalCenter
                color: progress.textColor
                font.pointSize: progress.textSize
                font.family: progress.textFontFamily
            }
        }

}
