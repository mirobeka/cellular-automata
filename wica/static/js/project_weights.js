// Generated by CoffeeScript 1.6.3
(function() {
  var Layer, Layer1, Layer2, addLayer1Neuron, addLayer2Neuron, addNeuron, displayWeightData, getData, getHtml, loadWeight, parseData, replaceHtml,
    __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; },
    __hasProp = {}.hasOwnProperty,
    __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; };

  Layer = (function() {
    function Layer(selector, data, neuron) {
      this.data = data;
      this.neuron = neuron;
      this.mapNetworkToNeigh = __bind(this.mapNetworkToNeigh, this);
      this.normalize = __bind(this.normalize, this);
      this.removeBias = __bind(this.removeBias, this);
      this.draw = __bind(this.draw, this);
      this.canvas = $(selector).get(0);
      this.ctx = this.canvas.getContext("2d");
      this.canvas.width = 99;
      this.canvas.height = 99;
    }

    Layer.prototype.draw = function() {
      var cidx, flatten, max_val, mid_val, min_val, neuron, ridx, row, scale, val, _i, _len, _results;
      neuron = this.getNeuron();
      flatten = [].concat.apply([], neuron);
      min_val = Math.min(0, Math.min.apply(null, flatten));
      max_val = Math.max.apply(null, flatten);
      mid_val = (min_val + max_val) / 2;
      scale = d3.scale.linear().range(["darkturquoise", "white", "orange"]).domain([min_val, 0, max_val]);
      this.ctx.font = "9px curier new";
      _results = [];
      for (ridx = _i = 0, _len = neuron.length; _i < _len; ridx = ++_i) {
        row = neuron[ridx];
        _results.push((function() {
          var _j, _len1, _results1;
          _results1 = [];
          for (cidx = _j = 0, _len1 = row.length; _j < _len1; cidx = ++_j) {
            val = row[cidx];
            this.ctx.fillStyle = scale(val);
            this.ctx.fillRect(33 * cidx, 33 * ridx, 33, 33);
            this.ctx.fillStyle = "#000";
            _results1.push(this.ctx.fillText("" + (Math.round(val * 100) / 100), 33 * cidx + 5, 33 * ridx + 18));
          }
          return _results1;
        }).call(this));
      }
      return _results;
    };

    Layer.prototype.removeBias = function(matrix) {
      var row;
      return (function() {
        var _i, _len, _results;
        _results = [];
        for (_i = 0, _len = matrix.length; _i < _len; _i++) {
          row = matrix[_i];
          _results.push(row.slice(1));
        }
        return _results;
      })();
    };

    Layer.prototype.normalize = function(matrix) {
      var cidx, flatten, max_val, min_val, ridx, row, val, _i, _j, _len, _len1;
      flatten = [].concat.apply([], matrix);
      min_val = Math.min.apply(null, flatten);
      max_val = Math.max.apply(null, flatten);
      for (ridx = _i = 0, _len = matrix.length; _i < _len; ridx = ++_i) {
        row = matrix[ridx];
        for (cidx = _j = 0, _len1 = row.length; _j < _len1; cidx = ++_j) {
          val = row[cidx];
          matrix[ridx][cidx] = (val - min_val) / (max_val - min_val);
        }
      }
      return matrix;
    };

    Layer.prototype.mapNetworkToNeigh = function(neuron, neighType) {
      var e, n, ne, nw, s, se, st, sw, w;
      if (neighType === "vonneumann") {
        st = neuron[0], n = neuron[1], e = neuron[2], s = neuron[3], w = neuron[4];
        return [[0, n, 0], [w, st, e], [0, s, 0]];
      } else if (neighType === "ediemoore") {
        st = neuron[0], n = neuron[1], ne = neuron[2], e = neuron[3], se = neuron[4], s = neuron[5], sw = neuron[6], w = neuron[7], nw = neuron[8];
        return [[nw, n, ne], [w, st, e], [sw, s, se]];
      }
    };

    return Layer;

  })();

  Layer1 = (function(_super) {
    __extends(Layer1, _super);

    function Layer1(data, neuron) {
      this.getNeuron = __bind(this.getNeuron, this);
      Layer1.__super__.constructor.call(this, "#layer1_neuron" + neuron, data, neuron);
      this.layer1 = data["layer1"];
    }

    Layer1.prototype.getNeuron = function() {
      var layer, neuron;
      layer = this.removeBias(this.layer1);
      console.log(layer);
      return neuron = this.mapNetworkToNeigh(layer[this.neuron], this.data["neigh"]);
    };

    return Layer1;

  })(Layer);

  Layer2 = (function(_super) {
    __extends(Layer2, _super);

    function Layer2(data, neuron) {
      this.getNeuron = __bind(this.getNeuron, this);
      Layer2.__super__.constructor.call(this, "#layer2_neuron" + neuron, data, neuron);
      this.layer1 = data["layer1"];
      this.layer2 = data["layer2"];
    }

    Layer2.prototype.multMatrix = function(matrix, y) {
      var row, x;
      return (function() {
        var _i, _len, _results;
        _results = [];
        for (_i = 0, _len = matrix.length; _i < _len; _i++) {
          row = matrix[_i];
          _results.push((function() {
            var _j, _len1, _results1;
            _results1 = [];
            for (_j = 0, _len1 = row.length; _j < _len1; _j++) {
              x = row[_j];
              _results1.push(y * x);
            }
            return _results1;
          })());
        }
        return _results;
      })();
    };

    Layer2.prototype.sumMatrices = function(m1, m2) {
      var c, ci, r, result, ri, _i, _j, _len, _len1;
      result = [];
      for (ri = _i = 0, _len = m1.length; _i < _len; ri = ++_i) {
        r = m1[ri];
        result.push([]);
        for (ci = _j = 0, _len1 = r.length; _j < _len1; ci = ++_j) {
          c = r[ci];
          result[ri].push(m1[ri][ci] + m2[ri][ci]);
        }
      }
      return result;
    };

    Layer2.prototype.getNeuron = function() {
      var idx, layer1, layer2, neuron, sum, x, _i, _len;
      layer2 = this.removeBias(this.layer2)[this.neuron];
      layer1 = this.removeBias(this.layer1);
      sum = [[0, 0, 0], [0, 0, 0], [0, 0, 0]];
      for (idx = _i = 0, _len = layer1.length; _i < _len; idx = ++_i) {
        neuron = layer1[idx];
        x = this.mapNetworkToNeigh(neuron, this.data["neigh"]);
        x = this.multMatrix(x, layer2[idx]);
        sum = this.sumMatrices(sum, x);
      }
      return sum;
    };

    return Layer2;

  })(Layer);

  replaceHtml = function(newHtml) {
    return $("#contentContainer").html(newHtml);
  };

  getHtml = function(weight) {
    var breaklines, html, name, value, x, xx, _i, _len;
    html = "<table class=\"ui table left aligned segment\">\n    <thead>\n        <tr>\n            <th>Property</th>\n            <th>Value</th>\n        </tr>\n    </thead>\n    <tbody>";
    for (name in weight) {
      value = weight[name];
      if (name === "layer1" || name === "layer2") {
        continue;
      }
      if (name === "weights") {
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
    html += "    </tbody>\n</table>\n\n<div class=\"ui middle aligned two column grid\">\n    <div class=\"row\">\n        <div class=\"column\">\n            <div class=\"ui layer1 vertical fluid menu\">\n            </div>\n        </div>\n        <div class=\"column\">\n            <div class=\"ui layer2 vertical fluid menu\">\n            </div>\n        </div>\n    </div>\n</div>\n";
    return html;
  };

  addLayer1Neuron = function(w, idx) {
    return addNeuron(Layer1, ".layer1", "layer1", w, idx);
  };

  addLayer2Neuron = function(w, idx) {
    return addNeuron(Layer2, ".layer2", "layer2", w, idx);
  };

  addNeuron = function(klass, selector, layer, w, idx) {
    var html, l;
    html = "<div class=\"item\">\n    <canvas id=\"" + layer + "_neuron" + idx + "\"></canvas>\n</div>";
    $(selector).append(html);
    l = new klass(w, idx);
    return l.draw();
  };

  displayWeightData = function(weight) {
    var html, idx, _i, _ref;
    html = getHtml(weight);
    replaceHtml(html);
    for (idx = _i = 0, _ref = weight["layer1"].length - 1; 0 <= _ref ? _i <= _ref : _i >= _ref; idx = 0 <= _ref ? ++_i : --_i) {
      addLayer1Neuron(weight, idx);
    }
    return addLayer2Neuron(weight, 0);
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
