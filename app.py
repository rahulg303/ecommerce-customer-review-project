from flask import Flask, request, render_template
from flask_cors import cross_origin
from sklearn.ensemble import RandomForestClassifier 
import pickle
import pandas as pd

app = Flask(__name__)

model = pickle.load(open('ecom_rf.pkl', 'rb'))
df = pd.read_csv("final.csv")


@app.route("/")
@cross_origin()
def home():
    return render_template("ecom.html")




@app.route("/", methods = ["GET", "POST"])
@cross_origin()
def predict():
    if request.method == "POST":

         # Price
        price = request.form.get("Price", False)

        # Freight Value
        freight_value= request.form.get("Freight Value", False)


        # Order Status
        order_status = request.form["Order Status"]
        if (order_status == 'Delivered'):
            order_status_delivered = 1
            order_status_shipped = 0
            order_status_canceled = 0
            order_status_processing = 0
            order_status_invoiced = 0
            order_status_unavailable = 0
            order_status_approved = 0

        elif (order_status == 'Shipped'):
            order_status_delivered = 0
            order_status_shipped = 1
            order_status_canceled = 0
            order_status_processing = 0
            order_status_invoiced = 0
            order_status_unavailable = 0
            order_status_approved = 0

        elif (order_status == 'Canceled'):
            order_status_delivered = 0
            order_status_shipped = 0
            order_status_canceled = 1
            order_status_processing = 0
            order_status_invoiced = 0
            order_status_unavailable = 0
            order_status_approved = 0

        elif (order_status == 'Processing'):
            order_status_delivered = 0
            order_status_shipped = 0
            order_status_canceled = 0
            order_status_processing = 1
            order_status_invoiced = 0
            order_status_unavailable = 0
            order_status_approved = 0

        elif (order_status == 'Invoiced'):
            order_status_delivered = 0
            order_status_shipped = 0
            order_status_canceled = 0
            order_status_processing = 0
            order_status_invoiced = 1
            order_status_unavailable = 0
            order_status_approved = 0

        elif (order_status == 'Unavailable'):
            order_status_delivered = 0
            order_status_shipped = 0
            order_status_canceled = 0
            order_status_processing = 0
            order_status_invoiced = 0
            order_status_unavailable = 1
            order_status_approved = 0

        elif (order_status == 'Approved'):
            order_status_delivered = 0
            order_status_shipped = 0
            order_status_canceled = 0
            order_status_processing = 0
            order_status_invoiced = 0
            order_status_unavailable = 0
            order_status_approved = 1

        else:
            order_status_delivered = 0
            order_status_shipped = 0
            order_status_canceled = 0
            order_status_processing = 0
            order_status_invoiced = 0
            order_status_unavailable = 0
            order_status_approved = 0
            
       
        # Payment type
        payment_type = request.form["Payment Type"]
        if (payment_type == 'Credit Card'):
            payment_type_credit_card = 1
            payment_type_debit_card = 0
            payment_type_voucher = 0
            payment_type_boleto = 0

        elif (payment_type == 'Debit Card'):
            payment_type_credit_card = 0
            payment_type_debit_card = 1
            payment_type_voucher = 0
            payment_type_boleto = 0

        elif (payment_type == 'Voucher'):
            payment_type_credit_card = 0
            payment_type_debit_card = 0
            payment_type_voucher = 1
            payment_type_boleto = 0

        elif (payment_type == 'Boleto'):
            payment_type_credit_card = 0
            payment_type_debit_card = 0
            payment_type_voucher = 0
            payment_type_boleto = 1

        else:
            payment_type_credit_card = 0
            payment_type_debit_card = 0
            payment_type_voucher = 0
            payment_type_boleto = 0

       
        prediction=model.predict([[
            price,
            freight_value,
            order_status_delivered,
            order_status_shipped,
            order_status_canceled,
            order_status_processing,
            order_status_invoiced,
            order_status_unavailable,
            order_status_approved,
            payment_type_credit_card,
            payment_type_debit_card,
            payment_type_voucher,
            payment_type_boleto
        ]])

        if prediction == 1:
            output = ("This customer is not happy, suggest better offer: {}".format(prediction))

        elif prediction == 2:
            output = ("This customer is not happy, suggest better offer: {}".format(prediction))

        elif prediction == 3:
            output = ("This customer is satisfied: {}".format(prediction))

        elif prediction == 4:
            output = ("This customer is happy: {}".format(prediction))
      
        else:
            output = ("This customer is happy: {}".format(prediction))


        return render_template('ecom.html', output = output)


    return render_template("ecom.html")


if __name__ == "__main__":
    app.run(debug=True)