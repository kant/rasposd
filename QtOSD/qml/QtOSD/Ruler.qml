import QtQuick 2.2


Rectangle {
    id: ruler
    property int line_width: 3

    property int big_slot_height: ruler.height/nb_big_slots
    property int small_slot_height: ruler.height/nb_big_slots/(nb_small_slots+1)

    color: "transparent"
    border.color: "lightblue"
    border.width: 2

    Column {

        Repeater {
            model: nb_big_slots

            Rectangle {

                width: ruler.width
                height: big_slot_height
                color: "transparent"




                Rectangle {
                    id: ruler_line
                    width: ruler.width
                    height: line_width
                    color: "red"
                    anchors.verticalCenter: parent.verticalCenter
                    anchors.verticalCenterOffset: (value%ruler.step)/ruler.step*big_slot_height
                }

                Text {
                    text: (value-value%ruler.step)+(nb_big_slots-index)*ruler.step-(ruler.step*nb_big_slots/2+(ruler.step*nb_big_slots/2%ruler.step))
                    anchors.left: ruler_line.right
                    anchors.verticalCenter: ruler_line.verticalCenter
                    anchors.leftMargin: 5
                    font.pointSize: font_size/2
                    rotation: -ruler.rotation
                }
            }
        }
    }



//    Column {

//        Repeater {
//            model: nb_big_slots*nb_small_slots

//            Rectangle {

//                height: small_slot_height
//                width: ruler.width
//                color: "transparent"


//                Rectangle {
//                    width: ruler.width/2
//                    height: line_width
//                    color: "red"
//                    anchors.verticalCenter: parent.verticalCenter
//                    //anchors.verticalCenterOffset: value%(ruler.step/(nb_big_slots*nb_small_slots))/(ruler.step/nb_small_slots)*big_slot_height
//                    anchors.verticalCenterOffset: (value%(ruler.step/nb_small_slots))/(ruler.step/nb_small_slots)*(small_slot_height)
//                }
//            }
//        }
//    }


    Rectangle {
        id: label
        width: 100
        height: font_size+font_size*0.2
        border.color: "black"
        color: "transparent"
        anchors.verticalCenter: parent.verticalCenter
        anchors.right: parent.left
        anchors.rightMargin: 10

        rotation: -ruler.rotation

        Text {
            text: value
            anchors.verticalCenter: parent.verticalCenter
            anchors.left: parent.left
            anchors.rightMargin: 10
            font.pointSize: font_size

        }

//        Item {
//            id: arrow

//            Rectangle {
//                id: top_arrow
//                rotation: 45
//                width: label.height*0.7
//                height: 2
//                color: "black"
//                anchors.left: label.anchors.right
//            }

//            Rectangle {
//                id: bottom_arrow
//                rotation: -45
//                width: label.height*0.7
//                height: 2
//                color: "black"
//                anchors.top: top_arrow.anchors.bottom
//            }
//        }


    }

}
