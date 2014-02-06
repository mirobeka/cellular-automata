// Generated by CoffeeScript 1.6.3
(function() {
  var root,
    __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; };

  root = typeof exports !== "undefined" && exports !== null ? exports : this;

  root.FormSubmitter = (function() {
    function FormSubmitter(selector, type, url, callback) {
      this.selector = selector;
      this.type = type;
      this.url = url;
      this.callback = callback;
      this.getField = __bind(this.getField, this);
      this.getFields = __bind(this.getFields, this);
      this.makeFormDataFromFields = __bind(this.makeFormDataFromFields, this);
      this.sendForm = __bind(this.sendForm, this);
      this.setValidations = __bind(this.setValidations, this);
      this.validations = __bind(this.validations, this);
      this.form = $(this.selector);
      if (this.form.length !== 1) {
        console.log("Form not found with selector: " + this.selector);
        return;
      }
      this.form.form(this.validations(), {
        onSuccess: this.sendForm
      });
    }

    FormSubmitter.prototype.validations = function() {
      var field, fields, validations, _i, _len;
      fields = this.getFields();
      validations = {};
      for (_i = 0, _len = fields.length; _i < _len; _i++) {
        field = fields[_i];
        validations[field] = {
          identifier: field,
          rules: [
            {
              type: "empty",
              prompt: "Enter name"
            }
          ]
        };
      }
      return validations;
    };

    FormSubmitter.prototype.setValidations = function(validations) {
      console.log(validations);
      return this.form.form(validations);
    };

    FormSubmitter.prototype.sendForm = function() {
      var fields, formData;
      fields = this.getFields();
      formData = this.makeFormDataFromFields(fields);
      return $.ajax({
        type: this.type,
        url: this.url,
        data: formData,
        success: this.callback
      });
    };

    FormSubmitter.prototype.makeFormDataFromFields = function(fields) {
      var data, field, value, _i, _len;
      data = {
        formSelector: this.selector
      };
      for (_i = 0, _len = fields.length; _i < _len; _i++) {
        field = fields[_i];
        value = this.getField(field);
        data[field] = value;
      }
      return data;
    };

    FormSubmitter.prototype.getFields = function() {
      var field;
      return (function() {
        var _i, _len, _ref, _results;
        _ref = this.form.find("input");
        _results = [];
        for (_i = 0, _len = _ref.length; _i < _len; _i++) {
          field = _ref[_i];
          _results.push($(field).attr("name"));
        }
        return _results;
      }).call(this);
    };

    FormSubmitter.prototype.getField = function(fieldName) {
      return this.form.form("get field", fieldName).val();
    };

    return FormSubmitter;

  })();

}).call(this);
