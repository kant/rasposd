#include "fileio.h"
#include <QFile>
#include <QTextStream>
#include <QDebug>

FileIO::FileIO(QObject *parent) :
    QObject(parent)
{

}

void FileIO::open()
{
    if (mSource.isEmpty()){
        emit error("source is empty");
    }

    file = new QFile(mSource);

    if (!file->exists())
        emit error("file doesn't exist...");

    file->open(QIODevice::ReadOnly);
}

void FileIO::read()
{

    getLastLinesFromFile();
    return;

//    if (mSource.isEmpty()){
//        emit error("source is empty");
//    }

//    qDebug() << "Trying to open " << mSource;
//    QFile file(mSource);

//    QString lastLine, lastFullLine;
//    if ( file.open(QIODevice::ReadOnly) ) {

//        QString currentLine;
//        QTextStream t( &file );

//        do {
//            currentLine = t.readLine();

//            if(!currentLine.isNull()) {
//                lastFullLine = lastLine;
//                lastLine = currentLine;
//            }
//         } while (!currentLine.isNull());

//        i++;
//    } else {
//        emit error("Unable to open the file");
//    }

//    lastFileLine = lastFullLine.split('\t');
}

void FileIO::getLastLinesFromFile()
{


    file->seek(file->size()-1);

    int count = 0;

    while ( (count < 2) && (file->pos() > 0) )
    {
        char ch;
        file->getChar(&ch);
        file->seek(file->pos()-2); /// minus 2 because getch moves one forward

        if (ch == '\n')
            count++;

    }

    QString r = file->readAll();

    lastFileLine = r.split('\t');


//    file.close();

    return;
}

QString FileIO::getValue(FlightData index)
{
    return lastFileLine.value(index);
}


bool FileIO::write(const QString &data)
{
    emit error("Not implemented");
    return false;
}
