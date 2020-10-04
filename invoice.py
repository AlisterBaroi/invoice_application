from reportlab.pdfgen import canvas
from datetime import date
import os
import json


print("Welcome to INVOICE SYSTEM \nby Alister Animesh Baroi, alister.baroi@gmail.com \n")


def err():
    print("Invalid input, try again")


def home():
    while True:
        try:
            home = int(input("[1] New Invoice [2] Exit: "))
            if home == 1:
                inputs()
                break
            elif home == 2:
                exit()
            else:
                err()
        except ValueError:
            err()
            continue


def inputs():
    # input validator
    Product = input('Enter Product: ')
    while not Product:
        err()
        Product = input('Enter Product: ')

    # input validator
    while True:
        try:
            PID = int(input('Enter Product ID: '))
            break
        except ValueError:
            err()

    # input validator
    while True:
        try:
            PQnt = int(input('Enter Product Quantity: '))
            break
        except ValueError:
            err()

    # input validator
    while True:
        try:
            PRate = round(float(input('Enter Product Price: ')), 2)
            break
        except ValueError:
            err()

    # input validator
    CName = input('Enter Customer Name: ')
    while not CName:
        err()
        CName = input('Enter Customer Name: ')

    # input validator
    CAddress = input('Enter Customer Address: ')
    while not CAddress:
        err()
        CAddress = input('Enter Customer Address: ')

    # input validator
    CEmail = input('Enter Customer Email: ')
    while not CEmail:
        err()
        CEmail = input('Enter Customer Email: ')

    subTotal = float(round(PQnt * PRate, 2))

    Tax = float(round(subTotal * 0.05, 2))
    PTotal = float(round(subTotal + Tax, 2))

    output(Product, PID, PQnt, PRate, PTotal,
           Tax, subTotal, CName, CAddress, CEmail)
    incoice(Product, PID, PQnt, PRate,
            PTotal, Tax, subTotal, CName, CAddress, CEmail)


def output(Product, PID, PQnt, PRate, PTotal, Tax, subTotal, CName, CAddress, CEmail):
    print("\nCustomer Invoice \n")
    print("Product:", Product)
    print("Product ID:", PID)
    print("Quantity:", PQnt)
    print("Rate: $", PRate)
    print("Tax: $", Tax)
    print("Total Price: $", PTotal)
    print("Billed to:", CName)
    print("Billing Address:", CAddress)
    print("Billing Contact:", CEmail)


def incoice(Product, PID, PQnt, PRate, PTotal,
            Tax, subTotal, CName, CAddress, CEmail):
    # set JSON
    with open('settings/settings.json') as f:
        data = json.load(f)

    # JSON variables
    PDFName = data['Invoice_file_name']
    COMPname = data['Company']
    Cinfo = data['CompanyAddress'] + data['CompanyContact']
    Note = data['TransactionNote']
    Msg = data['Message']
    Footer = data['FooterCredit']
    Footer2 = data['FooterCredit2']

    # pdf name
    pdf = canvas.Canvas(PDFName)
    # pdf title
    pdf.setTitle("Invoice")
    # page title & date
    pdf.setFont("Courier-Bold", 40)
    pdf.drawString(99, 715, "Invoice")
    pdf.setFont("Courier", 12)
    today = "Date: " + str(date.today().strftime("%d %B, %Y"))
    pdf.drawString(100, 690, today)
    # company name, address, contact
    company = pdf.beginText(430, 740)
    company.setFont("Courier-Bold", 20)
    company.textLines(COMPname)
    pdf.drawText(company)
    vadress = pdf.beginText(430, 695)
    vadress.setFont("Courier", 12)
    vadress.textLines(Cinfo)
    pdf.drawText(vadress)

    # customer info
    Cinfo = "BILLED TO:" + "\n" + \
        "Name:     " + CName + "\n" + \
        "Email:    " + CEmail + "\n" + \
        "Adress:   " + CAddress
    # purchase info
    Cinfo2 = "PURCHASE(S):" + "\n" + \
        "Product:                       " + Product + "\n" + \
        "Product ID:                    #" + str(PID) + "\n" + \
        "Quantity:                      " + str(PQnt) + "\n" + \
        "Rate:                          $" + str(PRate) + "\n" + \
        "Subtotal:                      $" + str(subTotal) + "\n\n" + \
        "Tax:                           $" + str(Tax) + "(5%)"

    Cinfo3 = "Total Price:                $" + str(PTotal)
    # rendering infos
    text = pdf.beginText(100, 580)
    text2 = pdf.beginText(100, 450)
    text3 = pdf.beginText(100, 275)
    text.setFont("Courier", 18)
    text3.setFont("Courier-Bold", 20)
    text.textLines(Cinfo)
    text2.textLines(Cinfo2)
    text3.textLines(Cinfo3)
    pdf.drawText(text)
    pdf.drawText(text2)
    pdf.drawText(text3)
    # Note
    pdf.setFont("Courier", 12)
    pdf.drawCentredString(
        290, 230, "NOTE: " + Note)
    pdf.drawCentredString(290, 120, Msg)

    # Footer
    pdf.line(30, 100, 550, 100)
    pdf.setFont("Courier-Bold", 20)
    pdf.drawCentredString(290, 70, Footer)
    pdf.setFont("Courier", 12)
    pdf.drawCentredString(290, 50, Footer2)

    # Close JSON, save, & launch PDF
    f.close()
    pdf.save()
    os.startfile(PDFName)
    print("\n\n")
    home()


home()
