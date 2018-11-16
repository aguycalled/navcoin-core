// Copyright (c) 2018 alex v
// Distributed under the MIT software license, see the accompanying
// file COPYING or http://www.opensource.org/licenses/mit-license.php.

#include "coldstakingwizard.h"

#include <QDebug>

ColdStakingWizard::ColdStakingWizard(QWidget *parent)
    : QWizard(parent)
{
    addPage(new IntroPage);
    addPage(new GetAddressesPage);
    addPage(new ColdStakingAddressPage);

    setWindowTitle(tr("Create a Cold Staking address"));
}

void ColdStakingWizard::accept()
{
    QDialog::accept();
}

IntroPage::IntroPage(QWidget *parent)
    : QWizardPage(parent)
{
    setTitle(tr("Introduction"));

    label = new QLabel(tr("This wizard will help you generate a cold staking<br>"
                          "address where you can safely store coins while<br>"
                          "staking them.<br>"
                          "You will need to provide two addresses from different wallets:<br>"
                          " - a staking address: this address will be authorised to stake the<br>"
                          "      coins sent to the cold staking address.<br>"
                          " - a spending address: this address will authorised to spend the<br>"
                          "      coins sent to the cold staking address.<br>"
                          "These addresses will be used to generate a cold staking address."));
    label->setWordWrap(true);

    QVBoxLayout *layout = new QVBoxLayout;
    layout->addWidget(label);
    setLayout(layout);
}

GetAddressesPage::GetAddressesPage(QWidget *parent)
    : QWizardPage(parent)
{
    setTitle(tr("Specify the addresses"));

    stakingAddressLabel = new QLabel(tr("&Staking Address:"));
    stakingAddressLineEdit = new QLineEdit;
    stakingAddressLabel->setBuddy(stakingAddressLineEdit);

    spendingAddressLabel = new QLabel(tr("S&pending Address:"));
    spendingAddressLineEdit = new QLineEdit;
    spendingAddressLabel->setBuddy(spendingAddressLineEdit);

    descriptionLabel = new QLabel(tr("Your Spending address and Staking address must be different."))

    QGridLayout *layout = new QGridLayout;
    layout->addWidget(stakingAddressLabel, 0, 0);
    layout->addWidget(stakingAddressLineEdit, 0, 1);
    layout->addWidget(spendingAddressLabel, 1, 0);
    layout->addWidget(spendingAddressLineEdit, 1, 1);
    layout->addWidget(descriptionLabel, 2, 0);
    setLayout(layout);

    registerField("stakingAddress", stakingAddressLineEdit);
    registerField("spendingAddress", spendingAddressLineEdit);
}

bool GetAddressesPage::isComplete()
{
    QString stakingAddressStr = field("stakingAddress").toString();
    QString spendingAddressStr = field("spendingAddress").toString();

    CNavCoinAddress stakingAddress(stakingAddressStr.toStdString());
    CNavCoinAddress spendingAddress(spendingAddressStr.toStdString());

    CKeyID stakingKeyID;
    CKeyID spendingKeyID;
    if (field("stakingAddress").toString() == field("spendingAddress").toString()) 
        return false;
    return stakingAddress.IsValid() && stakingAddress.GetKeyID(stakingKeyID) && spendingAddress.IsValid() && spendingAddress.GetKeyID(spendingKeyID);
}

ColdStakingAddressPage::ColdStakingAddressPage(QWidget *parent)
    : QWizardPage(parent)
{

    setTitle(tr("Generated address"));

    image = new QRImageWidget;
    button = new QPushButton("&Copy to Clipboard");

    QVBoxLayout *layout = new QVBoxLayout;
    layout->addWidget(image);
    layout->addWidget(button);
    setLayout(layout);

    connect(button, SIGNAL(released()), this, SLOT(copyToClipboard()));
}

void ColdStakingAddressPage::initializePage()
{
    QString stakingAddressStr = field("stakingAddress").toString();
    QString spendingAddressStr = field("spendingAddress").toString();


    CNavCoinAddress stakingAddress(stakingAddressStr.toStdString());
    CKeyID stakingKeyID;
    stakingAddress.GetKeyID(stakingKeyID);

    CNavCoinAddress spendingAddress(spendingAddressStr.toStdString());
    CKeyID spendingKeyID;
    spendingAddress.GetKeyID(spendingKeyID);

    coldStakingAddress = QString::fromStdString(CNavCoinAddress(stakingKeyID, spendingKeyID).ToString());

#ifdef USE_QRCODE
    QString uri = "navcoin:" + coldStakingAddress;
    image->setText("");
    if(!uri.isEmpty())
    {
        // limit URI length
        if (uri.length() > MAX_URI_LENGTH)
        {
            image->setText(tr("Resulting URI too long, try to reduce the text for label / message."));
        } else {
            QRcode *code = QRcode_encodeString(uri.toUtf8().constData(), 0, QR_ECLEVEL_L, QR_MODE_8, 1);
            if (!code)
            {
                image->setText(tr("Error encoding URI into QR Code."));
                return;
            }
            QImage qrImage = QImage(code->width + 8, code->width + 8, QImage::Format_RGB32);
            qrImage.fill(0xffffff);
            unsigned char *p = code->data;
            for (int y = 0; y < code->width; y++)
            {
                for (int x = 0; x < code->width; x++)
                {
                    qrImage.setPixel(x + 4, y + 4, ((*p & 1) ? 0x0 : 0xffffff));
                    p++;
                }
            }
            QRcode_free(code);

            QImage qrAddrImage = QImage(QR_IMAGE_SIZE*2, QR_IMAGE_SIZE+20, QImage::Format_RGB32);
            qrAddrImage.fill(0xffffff);
            QPainter painter(&qrAddrImage);
            painter.drawImage(QR_IMAGE_SIZE/2, 0, qrImage.scaled(QR_IMAGE_SIZE, QR_IMAGE_SIZE));
            QFont font = GUIUtil::fixedPitchFont();
            font.setPixelSize(12);
            painter.setFont(font);
            QRect paddedRect = qrAddrImage.rect();
            paddedRect.setHeight(QR_IMAGE_SIZE+12);
            painter.drawText(paddedRect, Qt::AlignBottom|Qt::AlignCenter, coldStakingAddress);
            painter.end();

            image->setPixmap(QPixmap::fromImage(qrAddrImage));
        }
    }
#endif
}


void ColdStakingAddressPage::copyToClipboard()
{
    GUIUtil::setClipboard(coldStakingAddress);
}
