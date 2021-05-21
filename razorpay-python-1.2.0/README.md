# Razorpay Python Client

[![PyPI Version](https://img.shields.io/pypi/v/razorpay.svg)](https://pypi.python.org/pypi/razorpay) [![Build Status](https://travis-ci.org/razorpay/razorpay-python.svg?branch=master)](https://travis-ci.org/razorpay/razorpay-python) [![Coverage Status](https://coveralls.io/repos/github/razorpay/razorpay-python/badge.svg?branch=master)](https://coveralls.io/github/razorpay/razorpay-python?branch=master) [![PyPI](https://img.shields.io/pypi/pyversions/razorpay.svg)]() [![License](https://img.shields.io/:license-mit-blue.svg)](https://opensource.org/licenses/MIT)

Python bindings for interacting with the Razorpay API

This is primarily meant for merchants who wish to perform interactions with the Razorpay API programatically.

## Installation

```sh
$ pip install razorpay
```

## Usage

You need to setup your key and secret using the following:
You can find your API keys at <https://dashboard.razorpay.com/#/app/keys>.

```py
import razorpay
client = razorpay.Client(auth=("<YOUR_API_KEY>", "<YOUR_API_SECRET>"))
```

## App Details

After setting up client, you can set your app details before making any request
to Razorpay using the following:

```py
client.set_app_details({"title" : "<YOUR_APP_TITLE>", "version" : "<YOUR_APP_VERSION>"})
```

For example, you can set the title to `Django` and version to `1.8.17`. Please ensure
that both app title and version are strings.

### Payments

- Fetch all payments

    ```py
    client.payment.all()
    ```

- Fetch a particular payment

    ```py
    client.payment.fetch("<PAYMENT_ID>")
    ```

- Capture a payment

    ```py
    client.payment.capture("<PAYMENT_ID>", "<AMOUNT>")
    Note: <AMOUNT> should be same as the original amount while creating the payment
    ```

- Refund a payment

    ```py
    client.payment.refund("<PAYMENT_ID>", "<AMOUNT>")
    # for full refund

    client.payment.refund("<PAYMENT_ID>", "<AMOUNT_TO_BE_REFUNDED>")
    # for particular amount

    Note: <AMOUNT_TO_BE_REFUNDED> should be equal/less than the original amount
    ```

- Get Bank Transfer Entity for given payment

    ```py
    client.payment.bank_transfer("<PAYMENT_ID>")
    ```

- Create transfer for given payment id

    ```py
    client.payment.transfer("<PAYMENT_ID>")
    ```
    For List of params refer to the API guide :
    https://razorpay.com/docs/route/api-reference/#creating-payments

- Fetch all transfers associated with the payment

    ```py
    client.payment.transfers("<PAYMENT_ID>")
    ```

### Refunds

- Fetch a particular refund

    ```py
    client.refund.fetch("<refund_id>")
    ```

- Fetch all refunds

    ```py
    client.refund.all()
    ```

### Orders

- Create a new order

    ```py
    client.order.create(data=DATA)
    DATA should contain these keys
        amount           : amount of order
        currency         : currency of order
        receipt          : receipt id of order
        payment_capture  : 1 if capture should be done automatically or else 0
        notes(optional)  : optional notes for order
    ```

- fetch a particular order

    ```py
    client.order.fetch("<ORDER_ID>")
    ```

- fetch all orders

    ```py
    client.order.all()
    ```

- fetch Payments of order

    ```py
    client.order.payments("<ORDER_ID>")
    ```


### Payment Link

- Create payment link

    Refer [api docs](https://razorpay.com/docs/payment-links/api/#creating-payment-links) for allowed request parameters.
    ```py
    DATA = {
        "customer": {
            "name": "Test Customer",
            "email": "test@example.com",
            "contact": "+919999888877"
        },
        "type": "link",
        "amount": 100,
        "currency": "INR",
        "description": "Payment link for this purpose - xyz"
    }
    client.invoice.create(data=DATA)
    ```

- Fetch payment link's details by id

    ```py
    client.invoice.fetch("<INVOICE_ID>")
    ```

- Fetch all payment link

    Refer [api docs](https://razorpay.com/docs/payment-links/api/#fetching-get-multiple-payment-links) for allowed query parameters.
    ```py
    client.invoice.all()
    ```

- Cancel a payment link by id

    ```py
    client.invoice.cancel("<INVOICE_ID>")
    ```

- Send/resend notifications for a payment link by id

    ```py
    client.invoice.notify_by("<INVOICE_ID>", "<MEDIUM>")
    # MEDIUM - sms/email
    ```

### Invoices

- Create a new invoice

    Refer [api docs](https://razorpay.com/docs/invoices/api/#creating-an-invoice) for allowed request parameters in detail.
    ```py
    client.invoice.create(data=DATA)
    ```

- Fetch a invoice by id

    ```py
    client.invoice.fetch("<INVOICE_ID>")
    ```

- Fetch all invoices

    Refer [api docs](https://razorpay.com/docs/invoices/api/#fetching-multiple-invoices) for allowed query parameters.
    ```py
    client.invoice.all()
    ```

- Cancel an invoice by id

    ```py
    client.invoice.cancel("<INVOICE_ID>")
    ```

- Send/resend notifications for an invoice by id

    ```py
    client.invoice.notify_by("<INVOICE_ID>", "<MEDIUM>")
    # MEDIUM - sms/email
    ```

- Issue an invoice in draft status by id

    ```py
    client.invoice.issue("<INVOICE_ID>")
    ```

- Delete an invoice by id

    ```py
    client.invoice.delete("<INVOICE_ID>")
    ```

- Edit an invoice by id

    Refer [api docs](https://razorpay.com/docs/invoices/api/#updating-an-invoice) for allowed request parameters in detail.
    ```py
    client.invoice.edit(invoice_id=invoice_id,data=DATA)
    ```


### Settlements

- fetch a particular settlement detail

    ```py
    client.settlement.fetch("<SETTLEMENT_ID>")
    ```

- fetch all settlement detail

    ```py
    client.settlement.all()
    ```

### Card

- fetch a particular card data

    ```py
    client.card.fetch(card_id=card_id)
    ```

### Customer

- fetch a particular customer Info

    ```py
    client.customer.fetch(customer_id=customer_id)
    ```

- Create a customer

    ```py
    client.customer.create(data=data)
    ```

- Edit a customer info

    ```py
    client.customer.edit(customer_id=customer_id, data=data)
    ```

### Token

- fetch a token associated with a customer

    ```py
    client.token.fetch(customer_id=customer_id, token_id=token_id)
    ```

- fetch all tokens associated with customer

    ```py
    client.token.all(customer_id=customer_id)
    ```

- Delete a given token assicated with a customer

    ```py
    client.token.delete(customer_id=customer_id, token_id=token_id)
    ```

### Virtual Account

- fetch all virtual account entities

    ```py
    client.virtual_account.all()
    ```

- fetch single virtual account details

    ```py
    client.virtual_account.fetch(virtual_account_id=virtual_account_id)
    ```

- create virtual account

    ```py
    client.virtual_account.create(data=DATA)
    DATA should contain these keys
        receiver_types        : ['bank_account']
        description           : 'Random Description'
        customer_id(optional) : <CUSTOMER_ID>
    ```

- close virtual account

    ```py
    client.virtual_account.close(virtual_account_id=virtual_account_id)
    ```

- fetch all payments for virtual account id

    ```py
    client.virtual_account.payments(virtual_account_id=virtual_account_id)
    ```

### Utility

- Verify Payment Signature

    `params_dict` should have `razorpay_order_id`, `razorpay_payment_id`, `razorpay_signature` which are received in the callback

    ```py
    client.utility.verify_payment_signature(params_dict)
    ```

- Verify Webhook Signature

    `webhook_signature` is the signature you receive under `X-Razorpay-Signature` in the webhook, while `webhook_secret` is the secret you used when creating the webhook on dashboard.

    ```py
    client.utility.verify_webhook_signature(webhook_body, webhook_signature, webhook_secret)
    ```

### Subscriptions

- Create a new subscription

    ```py
    client.subscription.create(data=DATA)
    DATA should contain these keys
        plan_id           : plan_id of subscription
        customer_id       : id of customer
        total_count       : number of subscriptions
    ```

- Fetch a particular subscription

    ```py
    client.subscription.fetch("<SUBSCRIPTION_ID>")
    ```

- Fetch all subscriptions

    ```py
    client.subscription.all()
    ```

- Cancel subscription

    ```py
    client.subscription.cancel("<SUBSCRIPTION_ID>")
    ```

- Create an addon for subscription
    ```
    client.subscription.createAddon("<SUBSCRIPTION_ID>", data=DATA)
    DATA should have these keys
        item               : dict with keys amount, name and currency
        quantity           : number of items
    ```

- Fetch a particular addon Info

    ```py
    client.addon.fetch(addon_id=addon_id)
    ```

- Delete an addon

    ```py
    client.addon.delete(addon_id=addon_id)
    ```

### Plans

- Create a new plan

    ```py
    client.plan.create(data=DATA)
    DATA should contain these keys
        item_id           : corresponding item_id
    ```

- Fetch a particular plan

    ```py
    client.plan.fetch("<PLAN_ID>")
    ```

- Fetch all plans

    ```py
    client.plan.all()
    ```

### Transfers

- Fetch all Transfers

    ```py
    client.transfer.all()
    ```

- Fetch transfer by ID

    ```py
    client.transfer.fetch("<TRANSFER_ID>")
    ```

- Create Transfer from given data

    ```py
    client.transfer.create(data=DATA)
    DATA should contain these keys
        amount   : 100
        currency : INR
        account  : acc_865rdfghu7632
    ```

- Edit Transfer from given data

    ```py
    client.transfer.edit(transfer_id=transfer_id, data=DATA)
    DATA may contain these keys
        on_hold       : True/False
        on_hold_until : 15678903127
    ```
    For details on Transfer edit, please refer to the API guide:
    https://razorpay.com/docs/route/api-reference/#examples

- Reverse a given Transfer

    ```py
    client.transfer.reverse(transfer_id=transfer_id)
    ```

- Fetch all reversals for a given Transfer

    ```py
    client.transfer.reversals(transfer_id=transfer_id)
    ```

## Bugs? Feature requests? Pull requests?

All of those are welcome. You can [file issues][issues] or [submit pull requests][pulls] in this repository.

[issues]: https://github.com/razorpay/razorpay-python/issues
[pulls]: https://github.com/razorpay/razorpay-python/pulls
