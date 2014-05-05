#include "fileio.h"
#include <QFile>
#include <QTextStream>

FileIO::FileIO(QObject *parent) :
    QObject(parent)
{
    i = 1;
}

void FileIO::read()
{
    if (mSource.isEmpty()){
        emit error("source is empty");
    }

    QFile file(mSource);
    QString fileContent;
    if ( file.open(QIODevice::ReadOnly) ) {
        QString line;
        QTextStream t( &file );
        int y = 0;
        do {
            line = t.readLine();

            if(!line.isNull())
                fileContent = line;
         } while (!line.isNull() && y++ < i);

        i++;
        file.close();
    } else {
        emit error("Unable to open the file");
    }

    lastLine = fileContent.split('\t');
}

QString FileIO::getValue(FlightData parameter)
{
    return lastLine.value(parameter);

//    switch (parameter) {
//    case TIME:
//        return lastLine.value(0);
//        break;

//    case PITCH:
//        return lastLine.value(1);
//        break;

//    case ROLL:
//        return lastLine.value(2);
//        break;

//    case YAW:
//        return lastLine.value(3);
//        break;

//    case SPEED:
//        return lastLine.value(7);
//        break;

//    case TEMPERATURE:
//        return lastLine.value(10);
//        break;

//    case PRESSURE:
//        return lastLine.value(11);
//        break;

//    default:
//        return "Unknown parameter";
//        break;
//    }
}


bool FileIO::write(const QString& data)
{
    emit error("Not implemented");
    return false;
}
