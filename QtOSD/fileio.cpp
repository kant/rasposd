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
    QString lastLine, lastFullLine;
    if ( file.open(QIODevice::ReadOnly) ) {
        QString currentLine;
        QTextStream t( &file );

        //content = t.readAll();

        //int y = 0;
        do {
            currentLine = t.readLine();

            if(!currentLine.isNull()) {
                lastFullLine = lastLine;
                lastLine = currentLine;
            }
         } while (!currentLine.isNull());

        i++;
        file.close();
    } else {
        emit error("Unable to open the file");
    }

    lastFileLine = lastFullLine.split('\t');
}

QString FileIO::getValue(FlightData index)
{
    return lastFileLine.value(index);
}


bool FileIO::write(const QString& data)
{
    emit error("Not implemented");
    return false;
}
