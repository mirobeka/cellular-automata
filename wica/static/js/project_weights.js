// Generated by CoffeeScript 1.6.3
(function() {
  var displayWeightData, getData, getHtml, loadWeight, parseData, replaceHtml;

  replaceHtml = function(newHtml) {
    return $("#contentContainer").html(newHtml);
  };

  getHtml = function(weight) {
    var breaklines, html, name, value, x, xx, _i, _len;
    html = "<table class=\"ui table left aligned segment\">\n    <thead>\n        <tr>\n            <th>Property</th>\n            <th>Value</th>\n        </tr>\n    </thead>\n    <tbody>";
    for (name in weight) {
      value = weight[name];
      if (name === "weights") {
        console.log(value);
        xx = 0;
        breaklines = "[";
        for (_i = 0, _len = value.length; _i < _len; _i++) {
          x = value[_i];
          if (xx === 4) {
            xx = 0;
            breaklines += "\n";
          }
          breaklines += " " + x + ",";
          xx += 1;
        }
        value = breaklines.substring(0, breaklines.length - 1);
        value += " ]";
      }
      html += "<tr>\n    <td>" + name + "</td>\n    <td>" + value + "</td>\n</tr>";
    }
    html += "    </tbody>\n</table>";
    console.log(html);
    return html;
  };

  displayWeightData = function(weight) {
    var html;
    html = getHtml(weight);
    return replaceHtml(html);
  };

  getData = function(weightName, callback) {
    return $.ajax({
      type: "GET",
      url: "../weight/" + weightName + "/",
      success: callback
    });
  };

  parseData = function(data) {
    data = JSON.parse(data);
    displayWeightData(data);
    return $(".ui.dimmable").dimmer("hide");
  };

  loadWeight = function(event) {
    var replayName;
    $(".ui.dimmable").dimmer("show");
    replayName = $(this).attr("data-name");
    return getData(replayName, parseData);
  };

  $(document).ready(function() {
    $(".ui.dimmable").dimmer({
      duration: {
        show: 300,
        hide: 700
      }
    });
    return $('.load.weight').bind('click', loadWeight);
  });

}).call(this);