root = exports ? this

class root.FormSubmitter
    constructor: (@selector, @type, @url, @callback) ->
        @form = $(@selector)
        if @form.length != 1
            console.log("Form not found with selector: "+@selector)
            return
        @disableValidations = true
        @form.form(@validations(), onSuccess: @sendForm)

    validations: () =>
        # validations could by specified with the form
        # for now, we wan't to be each field filled with some value
        fields = @getFields()
        validations = {}

        unless @disableValidations
            for field in fields
                validations[field] =
                    identifier: field
                    rules: [{type: "empty", prompt: "Enter name"}],

        return validations

    setValidations: (validations) =>
        console.log(validations)
        @form.form(validations)

    sendForm: () =>
        # get all input fields? or get all inputs
        fields = @getFields()

        # prepare form data
        formData = @makeFormDataFromFields(fields)

        # send data
        $.ajax
            type: @type
            url: @url
            data: formData
            success: @callback

    makeFormDataFromFields: (fields) =>
        # TODO: could be onliner :)
        data =
            formSelector: @selector

        for field in fields
            value = @getField(field)
            data[field] = value
        return data

    getFields: () =>
        return ($(field).attr("name") for field in @form.find("input"))

    getField: (fieldName) =>
        return @form.form("get field", fieldName).val()
