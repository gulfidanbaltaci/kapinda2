from flask import Flask, render_template, request, redirect
import sys, os
sys.path += ['../']
file_dir = os.path.dirname('C:\\Users\\GulfidanBaltaciNephO\\Desktop\\Kapinda-2\\kapinda2\\OdsLib')
sys.path.append(file_dir)
from OdsLib import *

app = Flask(__name__ , template_folder = '../html_src/', static_folder = '../html_src/')
pysql = PySql(app, 'db.yaml')

all_ids = { 'customer_id'           : None,
            'adres_id'            : None,
            'payment_method'        : None }


@app.route('/', methods = ['GET', 'POST'])
def index():
    global all_ids
    all_ids = { 'customer_id'           : None,
                'adres_id'            : None,
                'payment_method'        : None }

    return render_template('index.html')


#########   CUSTOMER RELATED FUNCTIONS ########

@app.route('/CustomerSignIn', methods = ['GET', 'POST'])
def customer_signin_page():

    pysql.init()
    global all_ids

    if request.method == 'POST' :

        # Check if the button is selected
        if 'customer_login' in request.form :
            email = request.form['customer_email']
            Sifre = request.form['customer_Sifre']

            # Check here the email-id and password entered with the sql database
            ans = Customer.check_customer_signin(pysql, email, Sifre)
            all_ids['customer_id'] = ans

            if ans :
                print("Logged In")
                return redirect('/ProductCategory')
            else :
                print("Invalid Email or Sifre")

    return render_template('/CustomerSignIn/customer_signin.html')


@app.route('/CustomerSignUp', methods = ['GET', 'POST'])
def customer_signup_page() :

    pysql.init()
    if request.method == 'POST' :
        if 'customer_signup' in request.form:

            # Get the details
            userDetails = request.form
            Ad = userDetails['customer_Ad']
            Soyad = userDetails['customer_Soyad']
            email = userDetails['customer_email']
            Sifre = userDetails['customer_Sifre']
            Kontrol_Sifre = userDetails['customer_Kontrol_Sifre']
            Telefon_no = userDetails['customer_Telefon_no']
            Telefon_no2 = userDetails['customer_Telefon_no2']

            if Sifre == Kontrol_Sifre :

                # Add the details to the sql database
                customer_id = Customer.customer_signup(pysql, Ad, Soyad, email, Sifre, Telefon_no, Telefon_no2)
                if customer_id != 0 :
                    return render_template('/CustomerSignIn/customer_signup_success.html', customer_id = customer_id)

    return render_template('/CustomerSignIn/customer_signup.html')


@app.route('/ProductCategory', methods = ['GET', 'POST'])
def user_page() :
    return render_template('/Product/product_category.html')


@app.route('/ProductHamburger', methods = ['GET', 'POST'])
def product_hamburger() :
    pysql.init()

    # Get all the mobiles 
    product_details = Product.get_product_by_category(pysql, 'Hamburger')
    global all_ids

    if request.method == 'POST' :

        if 'buy_now' in request.form :
            # get the quantities of product selected by customer
            quantities = request.form.getlist("quantity[]")
            for i in range(len(quantities)) :
                quantities[i] = int(quantities[i])

            # check if the issued quantity is present in product stock
            for i in range(0, len(product_details)) :
                if quantities[i] > 0 :
                    if not(Product.check_if_in_stock(pysql, all_ids['customer_id'], product_details[i][0], quantities[i])) :
                        print("Not enough in stock")
                        return render_template('/Product/product_hamburger.html', product_details = product_details)

            # check if adding the quantities to the cart doesn't exceed cart limit
            if (Cart.get_no_of_products_in_cart(pysql, all_ids['customer_id']) + sum(quantities)) > 5 :
                print("Max cart limit reached")
                return render_template('/Product/product_hamburger.html', product_details = product_details)

            # Add the product to the cart whose quantity value is greater than zero
            for i in range(0, len(product_details)) :
                if quantities[i] > 0 :
                    for j in range(0, quantities[i]) :
                        Cart.add_product_to_cart(pysql, all_ids['customer_id'], product_details[i][0])

            return redirect('/CartInfo')

    return render_template('/Product/product_hamburger.html', product_details = product_details)


@app.route('/ProductPizza', methods = ['GET', 'POST'])
def product_pizza() :
    pysql.init()
    product_details = Product.get_product_by_category(pysql, 'Pizza')
    global all_ids

    if request.method == 'POST' :

        if 'buy_now' in request.form :
            # get the quantities of product selected by customer
            quantities = request.form.getlist("quantity[]")
            for i in range(len(quantities)) :
                quantities[i] = int(quantities[i])

            # check if the issued quantity is present in product stock
            for i in range(0, len(product_details)) :
                if quantities[i] > 0 :
                    if not(Product.check_if_in_stock(pysql, all_ids['customer_id'], product_details[i][0], quantities[i])) :
                        print("Not enough in stock")
                        return render_template('/Product/product_hamburger.html', product_details = product_details)

            # check if adding the quantities to the cart doesn't exceed cart limit
            if (Cart.get_no_of_products_in_cart(pysql, all_ids['customer_id']) + sum(quantities)) > 5 :
                print("Max cart limit reached")
                return render_template('/Product/product_pizza.html', product_details = product_details)

            # Add the product to the cart whose quantity value is greater than zero
            for i in range(0, len(product_details)) :
                if quantities[i] > 0 :
                    for j in range(0, quantities[i]) :
                        Cart.add_product_to_cart(pysql, all_ids['customer_id'],
                                product_details[i][0])

            return redirect('/CartInfo')

    return render_template('/Product/product_pizza.html', product_details = product_details)



@app.route('/ProductDoner', methods = ['GET', 'POST'])
def product_doner() :
    pysql.init()
    product_details = Product.get_product_by_category(pysql, 'Doner')
    global all_ids

    if request.method == 'POST' :

        if 'buy_now' in request.form :
            # get the quantities of product selected by customer
            quantities = request.form.getlist("quantity[]")
            for i in range(len(quantities)) :
                quantities[i] = int(quantities[i])

            # check if the issued quantity is present in product stock
            for i in range(0, len(product_details)) :
                if quantities[i] > 0 :
                    if not(Product.check_if_in_stock(pysql, all_ids['customer_id'], product_details[i][0], quantities[i])) :
                        print("Not enough in stock")
                        return render_template('/Product/product_hamburger.html', product_details = product_details)

            # check if adding the quantities to the cart doesn't exceed cart limit
            if (Cart.get_no_of_products_in_cart(pysql, all_ids['customer_id']) + sum(quantities)) > 5 :
                print("Max cart limit reached")
                return render_template('/Product/product_doner.html', product_details = product_details)

            # Add the product to the cart whose quantity value is greater than zero
            for i in range(0, len(product_details)) :
                if quantities[i] > 0 :
                    for j in range(0, quantities[i]) :
                        Cart.add_product_to_cart(pysql, all_ids['customer_id'],
                                product_details[i][0])

            return redirect('/CartInfo')

    return render_template('/Product/product_doner.html', product_details = product_details)


@app.route('/ProductKebap', methods = ['GET', 'POST'])
def product_kebap() :
    pysql.init()
    product_details = Product.get_product_by_category(pysql, 'Kebap')
    global all_ids

    if request.method == 'POST' :

        if 'buy_now' in request.form :
            # get the quantities of product selected by customer
            quantities = request.form.getlist("quantity[]")
            for i in range(len(quantities)) :
                quantities[i] = int(quantities[i])

            # check if the issued quantity is present in product stock
            for i in range(0, len(product_details)) :
                if quantities[i] > 0 :
                    if not(Product.check_if_in_stock(pysql, all_ids['customer_id'], product_details[i][0], quantities[i])) :
                        print("Not enough in stock")
                        return render_template('/Product/product_hamburger.html', product_details = product_details)

            # check if adding the quantities to the cart doesn't exceed cart limit
            if (Cart.get_no_of_products_in_cart(pysql, all_ids['customer_id']) + sum(quantities)) > 5 :
                print("Max cart limit reached")
                return render_template('/Product/product_kebap.html', product_details = product_details)

            # Add the product to the cart whose quantity value is greater than zero
            for i in range(0, len(product_details)) :
                if quantities[i] > 0 :
                    for j in range(0, quantities[i]) :
                        Cart.add_product_to_cart(pysql, all_ids['customer_id'],
                                product_details[i][0])

            return redirect('/CartInfo')

    return render_template('/Product/product_kebap.html', product_details = product_details)


@app.route('/ProductPide', methods = ['GET', 'POST'])
def product_pide() :
    pysql.init()
    product_details = Product.get_product_by_category(pysql, 'Pide')
    global all_ids

    if request.method == 'POST' :

        if 'buy_now' in request.form :
            # get the quantities of product selected by customer
            quantities = request.form.getlist("quantity[]")
            for i in range(len(quantities)) :
                quantities[i] = int(quantities[i])

            # check if the issued quantity is present in product stock
            for i in range(0, len(product_details)) :
                if quantities[i] > 0 :
                    if not(Product.check_if_in_stock(pysql, all_ids['customer_id'], product_details[i][0], quantities[i])) :
                        print("Not enough in stock")
                        return render_template('/Product/product_hamburger.html', product_details = product_details)

            # check if adding the quantities to the cart doesn't exceed cart limit
            if (Cart.get_no_of_products_in_cart(pysql, all_ids['customer_id']) + sum(quantities)) > 5 :
                print("Max cart limit reached")
                return render_template('/Product/product_pide.html', product_details = product_details)

            # Add the product to the cart whose quantity value is greater than zero
            for i in range(0, len(product_details)) :
                if quantities[i] > 0 :
                    for j in range(0, quantities[i]) :
                        Cart.add_product_to_cart(pysql, all_ids['customer_id'],
                                product_details[i][0])

            return redirect('/CartInfo')

    return render_template('/Product/product_pide.html', product_details = product_details)


@app.route('/CartInfo', methods = ['GET', 'POST'])
def view_cart() :

    pysql.init()
    global all_ids
    product_details = []
    total = 0


    if request.method == 'POST' :
        # Clear Shopping Cart
        if 'clear_cart' in request.form :
            Cart.clear_cart(pysql, all_ids['customer_id'])

        # If place_order button is pressed
        elif 'place_order' in request.form :
            selected_adres_id = request.form['adres_radio']
            all_ids['adres_id'] = selected_adres_id

            selected_payment_method = request.form['payment_method']
            all_ids['payment_method'] = selected_payment_method
            return redirect('/PlaceOrder')

    # Show current products in cart
    else :
        # Get ids of the product currently present in cart
        prodids_incart = Cart.get_prod_in_cart(pysql, all_ids['customer_id'])
        prodids_incart = prodids_incart[0]

        # Get the total price of products in the cart
        total = Cart.get_total(pysql, all_ids['customer_id'])

        # for each product id, get the product details
        for i in prodids_incart :
            if i is not None :
                ans = Product.get_product_details(pysql, i)
                ans = ans[0]
                product_details.append(ans)

    # Choose Adres

    adres_details = Adres.view_all_adres_of_customer(pysql, all_ids['customer_id'])
    return render_template('/Cart/cart_info.html', product_details = product_details, total = total, adres_details = adres_details)


@app.route('/PlaceOrder', methods = ['GET', 'POST'])
def order_success() :

    pysql.init()
    global all_ids

    # If cart is empty, order not to be placed
    if Cart.get_no_of_products_in_cart(pysql, all_ids['customer_id']) == 0 :
        adres_details = Adres.view_all_adres_of_customer(pysql, all_ids['customer_id'])
        return render_template('/Cart/cart_info.html', adres_details = adres_details, total = 0)

    # Place the order
    order_id = Orders.place_order(pysql, all_ids['customer_id'], all_ids['adres_id'], all_ids['payment_method'])
    if order_id != 0 :
        return render_template('/Cart/order_placed.html', order_id = order_id)

    return render_template('/Cart/cart_info.html')


@app.route('/YourAccount', methods = ['GET', 'POST'])
def profile_view_and_updation() :

    pysql.init()
    global all_ids

    # get the user account details (name, email, etc)
    profile = Customer.get_customer_profile(pysql, all_ids['customer_id'])

    Ad = profile[0][0]
    Soyad = profile[0][1]
    email = profile[0][2]
    Telefon_no = profile[0][3]
    Telefon_no2 = profile[0][4]

    # get all the adres that are linked with customer account
    adres_details = Adres.view_all_adres_of_customer(pysql, all_ids['customer_id'])

    if request.method == 'POST' :
        if 'update' in request.form :
            profile_details = request.form
            Ad = profile_details['Ad']
            Soyad = profile_details['Soyad']
            email = profile_details['email']
            Telefon_no = profile_details['Telefon_no']
            Telefon_no2 = profile_details['Telefon_no2']


        # Update the profile 
        ans = Customer.update_customer_profile(pysql, all_ids['customer_id'], Ad, Soyad, email, Telefon_no, Telefon_no2)
        if ans :
            print("Profile Updated Successfully!")
        else :
            print("Profile Updation Failed")

    return render_template('/CustomerSignIn/your_account.html', customer_id = all_ids['customer_id'], Ad = Ad, Soyad = Soyad, email = email, Telefon_no = Telefon_no, Telefon_no2 = Telefon_no2, adres_details = adres_details)


@app.route('/YourOrders', methods = ['GET', 'POST'])
def show_orders() :
    pysql.init()
    global all_ids

    # Display all the order history of the customer 
    order_details = Orders.get_order_details(pysql, all_ids['customer_id'])
    return render_template('/CustomerSignIn/your_orders.html', order_details = order_details)


@app.route('/AddAdres', methods = ['GET', 'POST'])
def add_adres() :

    pysql.init()
    global all_ids

    if request.method == 'POST' :
        if 'add_adres' in request.form :

            addr_details = request.form
            street = addr_details['street']
            landmark = addr_details['landmark']
            city = addr_details['city']
            state = addr_details['state']
            pincode = addr_details['pincode']
            adres_type = addr_details['adres_type']

            # Add the adres to the customer account
            ans = Adres.add_customer_adres(pysql, all_ids['customer_id'], pincode, street, landmark, city, state, adres_type)
            print(ans)

            if ans :
                print("Adres Added")
                return redirect('/ProductCategory')
            else :
                print("Adding Adres Failed")

    return render_template('/CustomerSignIn/add_adres.html')


if __name__ == "__main__" :
    app.run(debug = True)
