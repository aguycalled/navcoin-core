#ifndef SENDCOMMUNITYFUNDDIALOG_H
#define SENDCOMMUNITYFUNDDIALOG_H

#include <QPushButton>
#include <QDialog>
#include <QTimer>

#include "../consensus/governance.h"
#include "wallet/wallet.h"

/* Confirmation dialog for proposals and payment requests. Widgets are hidden according if proposal or payment request*/

namespace Ui {
class SendCommunityFundDialog;
}

class SendCommunityFundDialog : public QDialog
{
    Q_OBJECT

public:
    explicit SendCommunityFundDialog(QWidget *parent = 0, CGovernance::CProposal* proposal = 0, int secDelay = 5);
    explicit SendCommunityFundDialog(QWidget *parent = 0, CGovernance::CPaymentRequest* prequest = 0, int secDelay = 5);
    int exec();
    ~SendCommunityFundDialog();

private Q_SLOTS:
    void countDown();
    void updateYesButton();

private:
    Ui::SendCommunityFundDialog *ui;
    CGovernance::CProposal* proposal;
    CGovernance::CPaymentRequest* prequest;
    QTimer countDownTimer;
    int secDelay;
    CWallet *wallet;
};

#endif // SENDCOMMUNITYFUNDDIALOG_H
