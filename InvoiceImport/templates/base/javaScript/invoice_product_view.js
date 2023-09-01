$(document).ready(function () {
    // pulling form in
    var invoiceForm = $('.invoices-products-form')



    invoiceForm.submit(function (event) {

        // grabbing data related to this form
        var thisForm = $(this)
        // the url
        var actionEndpoint = thisForm.attr("data-endpoint")
        // actual method - GET
        var httpMethod = thisForm.attr("method")
        // the form data
        var formData = thisForm.serialize();

        console.log({formData})

        $.ajax({
            type: "GET",
            url: actionEndpoint,
            method: httpMethod,
            data: formData,

            success: function (data) {
                console.log({data});
            }
        })
    })
});