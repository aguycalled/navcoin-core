#ifndef COMMUNITYFUNDDISPLAYPAYMENTREQUESTDETAILED_H
#define COMMUNITYFUNDDISPLAYPAYMENTREQUESTDETAILED_H

#include <QWidget>
#include "consensus/governance.h"
#include "wallet/wallet.h"
#include <QDialog>
#include <QAbstractButton>

namespace Ui {
class CommunityFundDisplayPaymentRequestDetailed;
}

class CommunityFundDisplayPaymentRequestDetailed : public QDialog
{
    Q_OBJECT

public:
    explicit CommunityFundDisplayPaymentRequestDetailed(QWidget *parent = 0, CGovernance::CPaymentRequest prequest = CGovernance::CPaymentRequest());
    ~CommunityFundDisplayPaymentRequestDetailed();

private:
    Ui::CommunityFundDisplayPaymentRequestDetailed *ui;
    CGovernance::CPaymentRequest prequest;
    CWallet *wallet;
    void setPrequestLabels() const;

public Q_SLOTS:
    void click_buttonBoxYesNoVote(QAbstractButton *button);
};

#endif // COMMUNITYFUNDDISPLAYPAYMENTREQUESTDETAILED_H
