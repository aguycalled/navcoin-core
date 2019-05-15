#ifndef COMMUNITYFUNDDISPLAYPAYMENTREQUEST_H
#define COMMUNITYFUNDDISPLAYPAYMENTREQUEST_H

#include <QWidget>
#include <QAbstractButton>
#include "consensus/governance.h"
#include "wallet/wallet.h"

namespace Ui {
class CommunityFundDisplayPaymentRequest;
}

class CommunityFundDisplayPaymentRequest : public QWidget
{
    Q_OBJECT

public:
    CommunityFundDisplayPaymentRequest(QWidget *parent = 0, CGovernance::CPaymentRequest prequest = CGovernance::CPaymentRequest());
    void refresh();
    ~CommunityFundDisplayPaymentRequest();

private:
    Ui::CommunityFundDisplayPaymentRequest *ui;
    CGovernance::CPaymentRequest prequest;
    CWallet *wallet;

public Q_SLOTS:
    void click_buttonBoxVote(QAbstractButton *button);
    void click_pushButtonDetails();
};

#endif // COMMUNITYFUNDDISPLAYPAYMENTREQUEST_H
