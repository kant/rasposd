import QtQuick 2.2
import FileIO 1.0

Rectangle {

    /*
     * Some initializations
     */
    property double altitude: 0
    property double speed: 0
    property double temperature: 0

    property double yaw: 0
    property double pitch: 0
    property double roll: 0

    property int saved_angle: 0


    property string date: ""
    property string hour: ""

    property int horizon_voffset: 0

    property double start_longitude: 0
    property double start_latitude: 0

    property double longitude: 0
    property double latitude: 0




    /*
     * Customize text aspect here
     */
    property int font_size: 15

    property string text_color: "white"
    property string text_outline_color: "black"

    property string text_font: "arial"




    /*
     * Customise other components here
     */

    /* Window size */
    width: 720
    height: 576

    color: "transparent"

    /* Max vertical offset of the horizon, when going up or down */
    property int horizon_max_voffset: 200



    /*
     * Change behavior and datas
     */
    property int refresh_interval: 20

    /* Use this to entirely replay a CSV file */
    property bool sim: false

    property string source_file_path: "/home/pi/pilotage-fpv/recorder/records/last/data_pos.csv"

    // arial ne marche pas si je ne la charge pas avant.
    FontLoader {
        id: myfont
        source: "/home/pi/pilotage-fpv/Arial.ttf"
    }

    Rectangle {
        id: hide_bg_left

        width: 130
        height: 960
        anchors.centerIn: parent
        anchors.horizontalCenterOffset: -380
        color: "black"
    }

    Text {
        id: lblTemperature
        text: temperature  + "°C"

        /* Position */
        anchors.right: parent.right
        anchors.top: parent.top
        anchors.margins: 10


        /* Aspect */
        font.pointSize: font_size
        font.family: text_font

        color: text_color
        style: Text.Outline;
        styleColor: text_outline_color

        horizontalAlignment: Text.AlignRight
    }

    Text {
        id: lblLongitude
        text: longitude

        /* Position */
        anchors.left: parent.horizontalCenter
        anchors.top: parent.top
        anchors.margins: 10


        /* Aspect */
        font.pointSize: font_size
        font.family: text_font

        color: text_color
        style: Text.Outline;
        styleColor: text_outline_color
    }

    Text {
        id: lblLatitude
        text: latitude

        /* Position */
        anchors.left: lblLongitude.left
        anchors.top: lblLongitude.bottom


        /* Aspect */
        font.pointSize: font_size
        font.family: text_font

        color: text_color
        style: Text.Outline;
        styleColor: text_outline_color
    }


    Text {
        id: lblStartLongitude
        text: start_longitude

        /* Position */
        anchors.left: parent.left
        anchors.top: parent.top
        anchors.margins: 10


        /* Aspect */
        font.pointSize: font_size
        font.family: text_font

        color: text_color
        style: Text.Outline;
        styleColor: text_outline_color
    }

    Text {
        id: lblStartLatitude
        text: start_latitude

        /* Position */
        anchors.left: lblStartLongitude.left
        anchors.top: lblStartLongitude.bottom


        /* Aspect */
        font.pointSize: font_size
        font.family: text_font

        color: text_color
        style: Text.Outline;
        styleColor: text_outline_color
    }


    Text {
        id: lblDate
        text: date

        /* Position */
        anchors.right: lblDateSep.left
        anchors.bottom: parent.bottom
        anchors.margins: 10


        /* Aspect */
        font.pointSize: font_size
        font.family: text_font

        color: text_color
        style: Text.Outline;
        styleColor: text_outline_color

        horizontalAlignment: Text.AlignRight
    }

    Text {
        id: lblDateSep
        text: "-"

        /* Position */
        anchors.right: lblHeure.left
        anchors.bottom: parent.bottom
        anchors.margins: 10


        /* Aspect */
        font.pointSize: font_size
        font.family: text_font

        color: text_color
        style: Text.Outline;
        styleColor: text_outline_color

        horizontalAlignment: Text.AlignRight
    }

    Text {
        id: lblHeure
        text: hour

        /* Position */
        anchors.right: parent.right
        anchors.bottom: parent.bottom
        anchors.margins: 10


        /* Aspect */
        font.pointSize: font_size
        font.family: text_font

        color: text_color
        style: Text.Outline;
        styleColor: text_outline_color

        horizontalAlignment: Text.AlignRight
    }

    Rectangle  {
        id: centre_cercle

        /* Position */
        width: 50
        height: 50
        radius: 50
        anchors.centerIn: parent

        /* Aspect */
        color: "#00000000"
        border.color: "#A0FF0000"
        border.width: 3
    }

    Rectangle  {
        id: centre_horizontal

        /* Position */
        width: 80
        height: 2
        anchors.centerIn: parent

        /* Aspect */
        color: "#00000000"
        border.color: "#A0FF0000"
        border.width: 3
    }

    Rectangle  {
        id: centre_vertical

        /* Position */
        width: 2
        height: 50 
        anchors.centerIn: parent

        /* Aspect */
        color: "#00000000"
        border.color: "#A0FF0000"
        border.width: 3
    }


    Rectangle {
        id: horizon

        /* Position */
        width: 300
        height:4
        anchors.centerIn: parent
        rotation: roll

        anchors.verticalCenterOffset: -1 * horizon_voffset

        /* Aspect */
        color: "#80008000"
        border.color: "#C0FFFFFF"
        border.width: 1
    }


    Rectangle {
        id: home_indicator

        /* Position */
        width: 20
        height:2
        anchors.centerIn: parent

        /* Aspect */
        color: "#80008000"
        border.color: "#C0FFFFFF"
        border.width: 1
    }

    Ruler {
        id: altitude_ruler

        /* Position */
        width: 10
        height: 300

        anchors.centerIn: parent
        anchors.horizontalCenterOffset: 300

        /* Parameters */
        property double value: altitude
        property int nb_big_slots: 5
        property int nb_small_slots: 5

        property int step: 20

    }


    Ruler {
        id: velocity_ruler

        /* Position */
        width: 10
        height: 300

        anchors.centerIn: parent
        anchors.horizontalCenterOffset: -300

        rotation: 180


        /* Parameters */
        property double value: speed
        property int nb_big_slots: 5
        property int nb_small_slots: 1

        property int step: 5
        property bool reversed: true

    }

    Ruler{
        id: direction_ruler

        /* Position */
        width: 5
        height: 500

        anchors.centerIn: parent
        anchors.verticalCenterOffset: -150

        rotation: -90


        /* Parameters */
        property bool reversed: true

        property double value: -1 * yaw

        property int nb_big_slots: 5
        property int nb_small_slots: 10
        property int step: 15
        property double cycle: 360

        property variant labels
    }

    function refresh() {

        if(sim) {
            data.incrementCurrentSimTime(refresh_interval/1000)
        } else {
            data.readLastLine();
        }

        /* Compute horizon aspect */
        horizon.rotation = parseFloat(data.getValue(FileIO.ROLL))
        horizon_voffset = -(Math.atan(parseFloat(data.getValue(FileIO.PITCH))/40)*horizon_max_voffset)

        /* Rulers values */
        speed = parseFloat(data.getValue(FileIO.SPEED));
        altitude = parseFloat(data.getValue(FileIO.ALTITUDE));
        yaw = parseFloat(data.getValue(FileIO.YAW))


        temperature = parseFloat(data.getValue(FileIO.TEMPERATURE));

        /* Get coordonates */
        longitude = parseFloat(data.getValue(FileIO.LONGITUDE))
        latitude = parseFloat(data.getValue(FileIO.LATITUDE))

        /* Get timestamp and convert to readable format */
        var currentDate = new Date(data.getValue(FileIO.TIME)*1000);
        date = currentDate.getDate() + "." + currentDate.getMonth() + "." + currentDate.getFullYear()
        hour = currentDate.getHours() + ":" + currentDate.getMinutes() + ":" + currentDate.getSeconds()

        /* Compute the home indicator position and aspect */
        var angle = Math.atan((latitude-start_latitude)/(longitude-start_longitude))-yaw/(180/Math.PI);
        home_indicator.rotation = angle*180/Math.PI
        home_indicator.anchors.verticalCenterOffset = 150*Math.sin(angle);
        home_indicator.anchors.horizontalCenterOffset = 150*Math.cos(angle);
    }

    /* Labels for angle with north */
    function directionLabels() {
        var labels = [];
        labels[0] = ' N ';
        labels[45] = 'NE';
        labels[90] = ' E ';
        labels[135] = 'SE';
        labels[180] = ' S ';
        labels[225] = 'SO';
        labels[270] = ' O ';
        labels[315] = 'NO';
        return labels;
    }

    /* Data source */
    FileIO {
        id: data
        source: source_file_path
        onError: console.log(msg)
    }

    /* Init some datas after program is loaded */
    Component.onCompleted: {
        data.open();

        if(sim)
            data.readNextLine()
        else
            data.readLastLine();

        direction_ruler.labels = directionLabels();

        start_longitude = parseFloat(data.getValue(FileIO.LONGITUDE))
        start_latitude = parseFloat(data.getValue(FileIO.LATITUDE))
    }

    /* Refreshes the datas */
    Timer {
        interval: refresh_interval
        onTriggered: refresh()
        repeat: true
        running: true
    }

    /* Makes simulation time pass */
    Timer {
        interval: refresh_interval/2
        onTriggered: data.readNextLine()
        repeat: true
        running: sim
    }
}
