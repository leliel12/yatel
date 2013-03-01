/*
 * "THE WISKEY-WARE LICENSE":
 * <utn_kdd@googlegroups.com> wrote this file. As long as you retain this notice
 * you can do whatever you want with this stuff. If we meet some day, and you
 * think this stuff is worth it, you can buy me a WISKEY us return.
 *
 */


/*==============================================================================
 CONSTANTS
==============================================================================*/

var COLOR_FROM = {r: 32, g: 79, b: 25};
var COLOR_TO = {r: 180, g: 255, b: 158};


/*==============================================================================
 UTILS
==============================================================================*/

var utils = {
    choice: function(arr){
        var rand = Math.random();
        rand *= arr.length;
        rand = Math.floor(rand);
        return arr[rand];
    },
    getRandomColor: function(){
        var a = COLOR_FROM;
        var b = COLOR_TO;
        var r = Math.random();
            return 'rgb('+
            ((a.r+(b.r-a.r)*r)|0).toString() + ','+
            ((a.g+(b.g-a.g)*r)|0).toString() + ','+
            ((a.b+(b.b-a.b)*r)|0).toString() + ')';
    }
}


/*==============================================================================
 MAIN  CLASS
==============================================================================*/

var YatelNetwork = function(rootid){

    this.sigRoot = document.getElementById(rootid);
    this.sigInst = sigma.init(this.sigRoot);;
    this._nodes = {};
    this._edges = {};


    // style the canvas
    this.sigRoot.style.marginLeft = "auto";
    this.sigRoot.style.marginRight = "auto";
    this.sigRoot.style.position = "relative";
    this.sigRoot.style.borderRadius = "10px";
    this.sigRoot.style.background = "#222";
    this.sigRoot.style.width = "100%";
    this.sigRoot.style.height = "100%";
    this.sigRoot.style.top = 0;
    this.sigRoot.style.left = 0;

    // style the network
    this.sigInst.drawingProperties({defaultLabelColor: '#ccc',
                               font: 'Arial',
                               edgeColor: 'source',
                               defaultEdgeType: 'curve'});
    this.sigInst.graphProperties({minNodeSize: 1, maxNodeSize: 10});
    this.sigInst.draw();

}


/*========
 FUNCTIONS
========*/

YatelNetwork.prototype.addNode = function(id, label, x, y){
    var node = this.sigInst.addNode(id, {label: label,
                                    color: utils.getRandomColor(),
                                    x: x, y: y});
    this._nodes[id] = node;
}

YatelNetwork.prototype.addEdge = function(idf, idt, label){
    var edge = this.sigInst.addEdge(label, idf, idt);
}


/*==============================================================================
 INITS
==============================================================================*/

function init(rootid){
    network = new YatelNetwork(rootid);
}
