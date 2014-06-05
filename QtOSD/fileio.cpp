#include "fileio.h"
#include <QFile>
#include <QTextStream>
#include <QDebug>

#include <limits>

FileIO::FileIO(QObject *parent) :
    QObject(parent)
{
    reuse = false;
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

    file->readLine(); // Skip header


    currentSimTime = std::numeric_limits<double>::max();

    readNextLine(); // First datas
    currentSimTime = currentLine.value(TIME).toDouble();
}

void FileIO::readLastLine()
{
    /* Go to the end of the file */
    file->seek(file->size()-1);

    int count = 0;

    /* Go two lines back */
    while ( (count < 2) && (file->pos() > 0) )
    {
        char ch;
        file->getChar(&ch);
        file->seek(file->pos()-2); /// minus 2 because getch moves one forward

        if (ch == '\n')
            count++;
    }

    /* Get the line where the pointer is, the second to last line 
     * We don't want the last, it could be uncomplete
     */
    QString r = file->readAll();

    /* Split the columns */
    currentLine = r.split('\t');

    return;

}

void FileIO::readNextLine()
{
    /* If the last data was consumed, read a new one */
    if(!reuse) {
        QString nextLineRaw = file->readLine();
        nextLine = nextLineRaw.split('\t');
    }

    /* If the next line is in the "past or present" of the simulation, use it */
    if( nextLine.value(TIME).toDouble() <= currentSimTime )
        reuse = false;
        currentLine = nextLine;
    else
        reuse = true;
}


QString FileIO::getValue(FlightData index)
{
    /* Getting the value at the given index. Index depend on FlightData enum type */
    return currentLine.value(index);
}

void FileIO::incrementCurrentSimTime(double step)
{
    currentSimTime += step;
}


bool FileIO::write(const QString &data)
{
    emit error("Not implemented");
    return false;
}
