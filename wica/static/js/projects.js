// Generated by CoffeeScript 1.6.3
(function() {
  $(document).ready(function() {
    var submitter;
    submitter = new FormSubmitter(".ui.form", "POST", ".", function(response) {
      return window.location.assign(response);
    });
    return $(".ui.accordion").accordion();
  });

}).call(this);
