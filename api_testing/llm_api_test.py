from dotenv import load_dotenv
import requests, os
from urllib.parse import quote

load_dotenv()

text = "TTM Technologies INVOICE Global Headquarters200East Sandpointe,Suite 400 Santa Aa, CA 92707 76-1000109008 TTM Technologies, Inc. BUILD SITE: DENVER, COLORADO 10570 Bradford Road, Littleton, CO 80127 Email P: (303) 972-4105 /F: (303) 904-6191 BILL TO: 4526 SHIP TO: PLEXUS MANUFACTURING SDN BHD(3 ATTN: ACCOUNTS PAYABLE PLEXUS MANUFACTURING (399136-M)(RIVERSIDE EAST) (399136-M)(RIVERSIDE) PLOT 88 &89 LEBUHRAYAKAMPUNG PLOT 87 LEBUHRAYA KAMPUNG JAWA BAYANLEPAS,PEN11900 BAYAN LEPAS, PEN 11900 MALAYSIA DATE OF INVOICE SHIP VIA COL / PPD BUYER TERMS 08/26/2020 DHL INTL #967435853 2.50% /65NET 65 SALES REP(S) CUSTOMER PO NUMBER PROD. ORDER NUMBER KW POH 677-8165985-OP 44689-2 QUANTITY SHIPPED PART NUMBER UNIT PRICE AMOUNT 3 3K1507RevF/B 300.00 900.00 COMMENTS: Please Remit To: TTM Technologies, Inc. NET INVOICE: 900.00 ACH/ Wire Transfer: Mailed Checks: DISCOUNT: 0.00 TTM Technologies, Inc. TTM Technologies, Inc. FREIGHT: 0.00 JP Morgan Chase Bank, N.A. P.O.Box 731840 SALES TAX: 0.00 1 Chase Manhattan Plaza, New York, NY 10005 Dallas, TX 75373 Routing (ABA) Number: 021000021 Swift Code: CHASUS33 Overnight Mail: Account Number: 449117634 Lockbox Address: INVOICE TOTAL: 900.00 JP Morgan Chase (TX1-0029) USD ATTN: TTM Technologies, Inc. USA Lockbox 731840 14800 Frye Road, 2nd Floor Ft Worth, TX 76155 All Remittance To: ARRemit@ttmtech.com QuestionsTo:ARTeam@ttmtech.com INTEREST SHALL BE CHARGED AT THE MAXIMUM AMOUNT ALL SALES ARE EXPRESSLY CONDITIONED UPON TTM's (INCLUDING ANY TTM TECHNOLOGIES GROUP PERMITTED BY LAW ON ALLAMOUNTS PAST DUE. PAYMENT DOES COMPANY) TERMS AND CONDITIONS: http:/www.tmtech.com/tc.pdf NOT CONVEY ANY TITLE OR INTEREST IN TOOLING."
questions = "Part number, Unit price, Amount"

api_url = str(os.getenv('LAMBDA_URL_LLM'))

# Properly encode parameters
encoded_text = quote(text)
encoded_questions = quote(questions)

api_url += f"?text={encoded_text}&questions={encoded_questions}"

response = requests.post(api_url)

# If success, print out the mapped questions and answers
if response.status_code == 200:
    # API returns JSON, parse the response
    data = response.json()

    print(data)

    for q, a in zip(questions.split(", "), data.get("result")):
        print(f"{q}: {a}")
else:
    print('message', 'Error occurred')