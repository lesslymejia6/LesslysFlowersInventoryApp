$(document).ready(function () {
    // pulling form in
    var invoiceForm = $('.invoice-form')
    console.log('inside .ready')

    invoiceForm.submit(function (event) {
        console.log('inside submit function')
        // grabbing data related to this form
        var thisForm = $(this)
        // the url
        var actionEndpoint = thisForm.attr("data-endpoint")
        // actual method - GET
        var httpMethod = thisForm.attr("method")
        // the form data
        var formData = thisForm.serialize();

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