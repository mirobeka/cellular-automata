// Generated by CoffeeScript 1.6.3
(function() {
  var Useless,
    __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; };

  Useless = (function() {
    function Useless() {
      this.do_stuff = __bind(this.do_stuff, this);
      $('#content').bind('click', this.do_stuff);
    }

    Useless.prototype.do_stuff = function() {
      return alert("stuff");
    };

    return Useless;

  })();

  $(document).ready(function() {
    return new Useless;
  });

}).call(this);