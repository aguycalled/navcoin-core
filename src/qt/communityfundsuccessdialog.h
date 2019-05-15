#ifndef COMMUNITYFUNDSUCCESSDIALOG_H
#define COMMUNITYFUNDSUCCESSDIALOG_H

#include <QWidget>
#include <QPushButton>
#include <QDialog>
#include "../consensus/governance.h"

namespace Ui {
class CommunityFundSuccessDialog;
}

class CommunityFundSuccessDialog : public QDialog
{
    Q_OBJECT

public:
    explicit CommunityFundSuccessDialog(uint256 hash, QWidget *parent = 0, CGovernance::CPaymentRequest* prequest = 0);
    explicit CommunityFundSuccessDialog(uint256 hash, QWidget *parent = 0, CGovernance::CProposal* proposal = 0);
    ~CommunityFundSuccessDialog();

private:
    Ui::CommunityFundSuccessDialog *ui;
    CGovernance::CProposal* proposal;
    CGovernance::CPaymentRequest* prequest;
};

#endif // COMMUNITYFUNDSUCCESSDIALOG_H
