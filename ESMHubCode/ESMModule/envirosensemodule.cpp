#include "envirosensemodule.h"
#include "./ui_envirosensemodule.h"

envirosensemodule::envirosensemodule(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::envirosensemodule)
{
    ui->setupUi(this);
}

envirosensemodule::~envirosensemodule()
{
    delete ui;
}

