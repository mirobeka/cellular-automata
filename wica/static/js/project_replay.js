// Generated by CoffeeScript 1.6.3
(function() {
  var Cell, ReplayPlayer, root,
    __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; };

  root = typeof exports !== "undefined" && exports !== null ? exports : this;

  ReplayPlayer = (function() {
    function ReplayPlayer(replay) {
      var c, _i, _len, _ref;
      this.replay = replay;
      this.setState = __bind(this.setState, this);
      this.loop = __bind(this.loop, this);
      this.clearCanvas = __bind(this.clearCanvas, this);
      this.stop = __bind(this.stop, this);
      this.pause = __bind(this.pause, this);
      this.start = __bind(this.start, this);
      this.removeCell = __bind(this.removeCell, this);
      this.addCell = __bind(this.addCell, this);
      this.initCells = __bind(this.initCells, this);
      this.initControls = __bind(this.initControls, this);
      _ref = oCanvas.canvasList;
      for (_i = 0, _len = _ref.length; _i < _len; _i++) {
        c = _ref[_i];
        if (c !== null) {
          c.destroy();
        }
        oCanvas.canvasList = [];
      }
      this.canvas = oCanvas.create({
        canvas: "#replayCanvas",
        background: "#eee"
      });
      this.cells = [];
      this.stepIndex = 0;
    }

    ReplayPlayer.prototype.initControls = function() {
      $(".play.icon").parent().bind("click", this.start);
      $(".pause.icon").parent().bind("click", this.pause);
      return $(".stop.icon").parent().bind("click", this.stop);
    };

    ReplayPlayer.prototype.initCells = function() {
      var idx, _i, _ref, _results;
      _results = [];
      for (idx = _i = 0, _ref = (this.replay.width * this.replay.height) - 1; 0 <= _ref ? _i <= _ref : _i >= _ref; idx = 0 <= _ref ? ++_i : --_i) {
        _results.push(this.addCell(idx));
      }
      return _results;
    };

    ReplayPlayer.prototype.addCell = function(idx) {
      var cell, x, y;
      x = idx % this.replay.width;
      y = idx / this.replay.height;
      cell = new Cell(this.canvas, idx, this.replay.resolution, x, y);
      return this.cells.push(cell);
    };

    ReplayPlayer.prototype.removeCell = function(cell) {
      return this.canvas.removeChild(cell.rectangle);
    };

    ReplayPlayer.prototype.start = function(speed) {
      if (speed == null) {
        speed = 1;
      }
      this.canvas.settings.fps = speed;
      return this.canvas.setLoop(this.loop).start();
    };

    ReplayPlayer.prototype.pause = function() {
      return this.canvas.timeline.stop();
    };

    ReplayPlayer.prototype.stop = function() {
      this.canvas.timeline.stop();
      this.stepIndex = 0;
      this.clearCanvas();
      return this.initCells();
    };

    ReplayPlayer.prototype.clearCanvas = function() {
      var cell, _i, _len, _ref;
      _ref = this.cells;
      for (_i = 0, _len = _ref.length; _i < _len; _i++) {
        cell = _ref[_i];
        this.removeCell(cell);
      }
      return this.cells = [];
    };

    ReplayPlayer.prototype.loop = function() {
      var cell, _i, _len, _ref, _results;
      this.stepIndex++;
      if (!(this.stepIndex < this.replay.length)) {
        return false;
      }
      _ref = this.cells;
      _results = [];
      for (_i = 0, _len = _ref.length; _i < _len; _i++) {
        cell = _ref[_i];
        this.setState(this.stepIndex, cell);
        _results.push(this.canvas.draw.redraw());
      }
      return _results;
    };

    ReplayPlayer.prototype.setState = function(stepIndex, cell) {
      var gray, rgb;
      gray = Math.round(255 * this.replay.data[stepIndex][cell.idx]);
      rgb = "rgb(" + gray + "," + gray + "," + gray + ")";
      return cell.rectangle.fill = rgb;
    };

    return ReplayPlayer;

  })();

  Cell = (function() {
    function Cell(canvas, idx, size, x, y) {
      this.canvas = canvas;
      this.idx = idx;
      this.size = size;
      this.x = x;
      this.y = y;
      this.rectangle = this.canvas.display.rectangle({
        x: Math.floor(this.x) * this.size,
        y: Math.floor(this.y) * this.size,
        origin: {
          x: "left",
          y: "top"
        },
        width: this.size,
        height: this.size,
        stroke: "#999",
        fill: "#aaa"
      }).add();
    }

    return Cell;

  })();

  $(document).ready(function() {
    var foo, hmm, loadReplayData, otherFoo;
    new FormSubmitter(".ui.update.form", "PUT", ".", function(response) {
      return window.location.assign(response);
    });
    new FormSubmitter(".ui.delete.form", "DELETE", ".", function(response) {
      return window.location.assign(response);
    });
    loadReplayData = function(replayName, callback) {
      return $.ajax({
        type: "GET",
        url: "../replay/" + replayName + "/",
        success: callback
      });
    };
    otherFoo = function(replayData) {
      var player;
      replayData = JSON.parse(replayData);
      player = new ReplayPlayer(replayData);
      player.initControls();
      return player.initCells();
    };
    foo = function(event) {
      var jsonData, replayName;
      replayName = $(this).attr("data-name");
      return jsonData = loadReplayData(replayName, otherFoo);
    };
    return hmm = $('a.load.replay').bind('click', foo);
  });

}).call(this);
