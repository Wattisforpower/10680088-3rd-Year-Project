#ifndef ENVIROSENSEMODULE_H
#define ENVIROSENSEMODULE_H

#include <QMainWindow>

QT_BEGIN_NAMESPACE
namespace Ui { class envirosensemodule; }
QT_END_NAMESPACE

class envirosensemodule : public QMainWindow
{
    Q_OBJECT

public:
    envirosensemodule(QWidget *parent = nullptr);
    ~envirosensemodule();

private:
    Ui::envirosensemodule *ui;
};
#endif // ENVIROSENSEMODULE_H
