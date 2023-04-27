#!/bin/bash
URL="chrisdgendev.americaniche.com"
CUSTOMERS="Generate Customers"
ORDERS="Generate Data Orders"
PAYMENTS="Generate Paymentsc"
CUSTOMER_RESULT=$(curl --silent $URL | grep "$CUSTOMERS" | cut -f2 -d ">" | cut -f1 -d "<")
ORDERS_RESULT=$(curl --silent $URL | grep "$ORDERS" | cut -f2 -d ">" | cut -f1 -d "<")
PAYMENTS_RESULT=$(curl --silent $URL | grep "$PAYMENTS" | cut -f2 -d ">" | cut -f1 -d "<")
#if [ "$CUSTOMERS" -eq "$CUSTOMER_RESULT" "$PAYMENTS" -eq "$PAYMENTS_RESULT" && "$ORDERS" -eq "$ORDERS_RESULT" ]
if [ "$CUSTOMERS" = "$CUSTOMER_RESULT" ] &&  [ "$ORDERS" = "$ORDERS_RESULT" ] && [ "$PAYMENTS" = "$PAYMENTS_RESULT" ]
then
    echo "Pass"
    #git checkout qa
    #git merge development qa
    #echo "Merge successful, pushing branch now."
    #git push origin qa
    #echo "Push to QA branch successful."
    
else
    echo "One of the buttons was not found."
fi



