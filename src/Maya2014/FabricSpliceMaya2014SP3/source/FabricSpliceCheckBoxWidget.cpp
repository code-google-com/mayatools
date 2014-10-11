#include "FabricSpliceCheckBoxWidget.h"

FabricSpliceCheckBoxWidget::FabricSpliceCheckBoxWidget(QString label, QWidget * parent)
: QCheckBox(label, parent)
{
  mCallback = NULL;
  mCallbackUD = NULL;
}

void FabricSpliceCheckBoxWidget::checkStateSet()
{
  if(mCallback)
    (*mCallback)(mCallbackUD);
  QCheckBox::checkStateSet();
}

void FabricSpliceCheckBoxWidget::setCallback(FabricSpliceCheckBoxWidget::callback func, void * userData)
{
  mCallback = func;
  mCallbackUD = userData;
}
