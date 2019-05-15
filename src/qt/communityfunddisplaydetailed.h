#ifndef COMMUNITYFUNDDISPLAYDETAILED_H
#define COMMUNITYFUNDDISPLAYDETAILED_H

#include "consensus/governance.h"
#include "wallet/wallet.h"
#include <QDialog>
#include <QAbstractButton>

namespace Ui {
class CommunityFundDisplayDetailed;
}

class CommunityFundDisplayDetailed : public QDialog
{
    Q_OBJECT

public:
    explicit CommunityFundDisplayDetailed(QWidget *parent = 0, CGovernance::CProposal proposal = CGovernance::CProposal());
    ~CommunityFundDisplayDetailed();

private:
    Ui::CommunityFundDisplayDetailed *ui;
    CGovernance::CProposal proposal;
    CWallet *wallet;
    void setProposalLabels() const;

public Q_SLOTS:
    void click_buttonBoxYesNoVote(QAbstractButton *button);
};

#endif // COMMUNITYFUNDDISPLAYDETAILED_H
